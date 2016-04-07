#!/usr/bin/env python
# -- coding: utf-8 --
import base64
import binascii
import cookielib
import json
import re
import traceback
import urllib
import urllib2
import urlparse


base_url = "http://ratotv.top"

class LoginError(Exception):
    pass


def json_get(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    data = json.load(urllib2.urlopen(req))
    return data


def post_page(url, user, password):
    mydata = [('login_name', user), ('login_password', password), ('login', 'submit')]
    mydata = urllib.urlencode(mydata)
    req = urllib2.Request(url, mydata)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    page = urllib2.urlopen(req).read()
    return page


def post_page_free(url, mydata, headers=None):
    mydata = urllib.urlencode(mydata)
    req = urllib2.Request(url, mydata)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    if headers:
        for header in headers:
            req.add_header(header[0],header[1])
    page = urllib2.urlopen(req).read()
    return page


def abrir_url(url, encoding='utf-8'):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    if encoding != 'utf-8': link = link.decode(encoding).encode('utf-8')
    return link


def xmlhttp_request(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Accept', 'text/html, */*')
    req.add_header('X-Requested-With', '    XMLHttpRequest')
    response = urllib2.urlopen(req)
    data = response.read()
    response.close()
    return data


def resolve_vmail(url):
    # http://my.mail.ru/mail/rishuam/video/_myvideo/5404.html
    base_profile_url = url.split("/video/")[0]
    video_id = url.split("/")[-1][:-5]
    ajax_url = base_profile_url + "/ajax?ajax_call=1&func_name=video.get_item&mna=&mnb=&arg_id=" + video_id
    print "[vmail] ajax_url:", ajax_url
    ajax_resp = urllib2.urlopen(ajax_url)
    api_url = re.compile(r'\\"signVideoUrl\\"\:\ \\"(.+?)\\"', re.DOTALL).findall(ajax_resp.read())[0]
    print "[vmail] api_url:", api_url
    api_resp = urllib2.urlopen(api_url)
    video_key = re.compile('(video_key=[^\;]+)').findall(api_resp.headers.get('Set-Cookie', ''))[0]
    print "[vmail] Cookie:", video_key
    video_json = json.load(api_resp)
    result = []
    for v in video_json["videos"]:
        headers = {"Cookie":video_key}
        result.append({"provider":"videomail.ru", "quality":v['key'], "url": v['url'], "headers":headers})
    return result


def resolve_vkcom(url):
    rato_vk_url = "http://ratotv.top/zencrypt/pluginsw/plugins_vk.php"
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"
    post_data1 = [
        ("iagent", user_agent),
        ("url", url),
        ("ihttpheader", "true"),
        ("icookie", ""),
        ("iheader", "true")
    ]
    print "[vk.com] post_data:", post_data1
    data1 = post_page_free(rato_vk_url, post_data1)
    print "[vk.com] data1 line1:", data1.split("\n")[0]
    data2 = post_page_free(rato_vk_url, [("checkcookie", "true")])
    # print "[vk] data2:", data2
    cookie = data2.replace("&cookie=", "")
    print "[vk,com] cookie:", cookie
    oid_part, vid = url.split("/")[-1].split("_")
    oid = oid_part.replace("video", "")
    print "[vk.com] oid:", oid
    print "[vk.com] vid:", vid
    post_data3 = [
        ("iheader", "true"),
        ("url", "https://vk.com/al_video.php"),
        ("ipost", "true"),
        ("iagent", user_agent),
        ("ipostfield", "oid=" + oid + "&act=video_embed_box&al=1&vid=" + vid),
        ("ihttpheader", "true"),
        ("icookie", "remixlang=3; remixsid=" + cookie),
        ("isslverify", "true")
    ]
    data3 = post_page_free(rato_vk_url, post_data3)
    print "[vk.com] data3 line1", data3.split("\n")[0]
    # print "[vk] data3", data3
    embed_hash = re.search(r"vk\.com/video_ext\.php\?oid=%s\&id=%s\&hash=([^\"\']+)" % (oid, vid), data3, re.DOTALL).group(1)
    # print "[vk] embed_hash:", embed_hash
    api_url = "http://api.vk.com/method/video.getEmbed?oid=%s&video_id=%s&embed_hash=%s" % (oid, vid, embed_hash)
    print "[vk.com] api_url:", api_url
    video_json = json_get(api_url)["response"]
    result = []
    url240 = video_json.get("url240")
    url360 = video_json.get("url360")
    url480 = video_json.get("url480")
    url720 = video_json.get("url720")
    url1080 = video_json.get("url1080")
    if url240:
        result.append({"provider":"vk.com", "quality":"240p", "url":url240})
    if url360:
        result.append({"provider":"vk.com", "quality":"360p", "url":url360})
    if url480:
        result.append({"provider":"vk.com", "quality":"480p", "url":url480})
    if url720:
        result.append({"provider":"vk.com", "quality":"720p", "url":url720})
    if url1080:
        result.append({"provider":"vk.com", "quality":"1080p", "url":url1080})
    return result


def resolve_ok(url):
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"
    vid = url
    vid = url.split("/")[-1]
    print "[ok.ru] vid:", vid
    api_url = 'http://ok.ru/dk?cmd=videoPlayerMetadata&mid=' + vid
    api_req = urllib2.Request(api_url)
    api_req.add_header('User-Agent', user_agent)
    api_req.add_header('Accept', accept)
    api_req.add_header('Cache-Control', 'no-transform')
    video_json = json.load(urllib2.urlopen(api_req))
    result = []
    for v in video_json["videos"]:
        if v['name'] == "lowest":
            quality = "240p"
        elif v['name'] == "low":
            quality = "360p"
        elif v['name'] == "sd":
            quality = "480p"
        elif v['name'] == "hd":
            quality = "720p"
        elif v['name'] == "full":
            quality = "1080p"
        else:
            continue
        vurl = v['url'].decode("unicode-escape")
        headers = {
            "User-Agent":user_agent,
            "Accept":accept,
            "Referer":"http://ratotv.top"
        }
        result.append({"provider":"ok.ru", "quality":quality, "url":vurl, "headers":headers})
    return result


def resolve_upstream(url):
    video_req = urllib2.Request(url)
    video_req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
    video_page = urllib2.urlopen(video_req).read()
    #print "[upstream] html = ", video_page
    video_data = re.search(r"(<video).+?(</video>)", video_page, re.DOTALL).group()
    result = []
    for source in re.finditer("<source src=\'(.+?)\'.+?data-res=\'(.+?)\'", video_data, re.DOTALL):
        url = source.group(1)
        if url.startswith("//"):
            url = "http:" + url
        result.append({"provider":"upstream.com", "url":url, "quality":source.group(2)})
    return result


def resolve_gdrive(url):
    # https://drive.google.com/file/d/0B8kCEtrnzKhDLTNmYzZBSnpPeEE/edit?pli=1
    vid = urlparse.urlparse(url).path.split("/")[-2]
    print "[gdrive] vid = %s" % vid
    # direct link for uploaded video, non-seekable..
    # return [{"provider":"gdrive", "url":"https://googledrive.com/host/%s"% vid, "quality":"???"}]

    # ydl gdrive, seekable urls..
    video_req = urllib2.Request(url)
    video_req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
    video_data = urllib2.urlopen(video_req).read().decode('unicode_escape')
    # print "[gdrive]", video_data
    formats = {
        '5': {'ext': 'flv'},
        '6': {'ext': 'flv'},
        '13': {'ext': '3gp'},
        '17': {'ext': '3gp'},
        '18': {'ext': 'mp4'},
        '22': {'ext': 'mp4'},
        '34': {'ext': 'flv'},
        '35': {'ext': 'flv'},
        '36': {'ext': '3gp'},
        '37': {'ext': 'mp4'},
        '38': {'ext': 'mp4'},
        '43': {'ext': 'webm'},
        '44': {'ext': 'webm'},
        '45': {'ext': 'webm'},
        '46': {'ext': 'webm'},
        '59': {'ext': 'mp4'}
    }
    fmt_list = re.search(r'"fmt_list"\s*,\s*"([^"]+)', video_data).group(1)
    fmt_list = fmt_list.split(',')
    print "[gdrive] fmt_list = %r" % fmt_list
    fmt_stream_map = re.search(r'"fmt_stream_map"\s*,\s*"([^"]+)', video_data).group(1)
    fmt_stream_map = fmt_stream_map.split(',')
    #print "[gdrive] fmt_stream_map = %r, len=%d" % (fmt_stream_map, len(fmt_stream_map))
    result = []
    for i in range(len(fmt_stream_map)):
        fmt_id, fmt_url = fmt_stream_map[i].split('|')
        fmt = formats.get(fmt_id)
        extension = fmt and fmt['ext']
        resolution = fmt_list[i].split('/')[1]
        width, height = resolution.split('x')
        result.append({"provider":"gdrive", "url":fmt_url, "quality": height+"p", "ext":extension})
    return result

def resolver_externos(link_data):
    videos = []
    decoded_url = link_data['link']
    #print link_data
    try:
        request = link_data['request']
        if request['method'] == 'POST':
            headers = []
            if 'referer' in request:
                headers.append(('Referer', request['referer']))
            if 'cookie' in request:
                headers.append(('Cookie', request['cookie']))
            data = json.loads(post_page_free(link_data['request']['url'], request['data'], headers))
            #print '[resolve_externos] data = ', data
            request_data = {}
            request_data['link'] = link_data['link']
            request_data['poscom'] = link_data['poscom']
            request_data['response'] = data
            post_data = [('data', base64.encodestring(json.dumps(request_data)))]
            data2 = json.loads(post_page_free('http://ratotv.top/newplay/gkpluginsphp.php', post_data))
            #print '[resolve_externos] data2 = ', data2
            decoded_url = data2['link']
    except:
        traceback.print_exc()
    #print "decoded url = ", decoded_url

    if "my.mail.ru/mail/" in decoded_url:
        print "___resolving videomail.ru url___"
        try:
            videos = resolve_vmail(decoded_url)
        except:
            traceback.print_exc()
    elif "vk.com/video" in  decoded_url:
        print "___resolving vk.com url___"
        try:
            videos = resolve_vkcom(decoded_url)
        except:
            traceback.print_exc()
    elif "odnoklassniki.ru/video/" in decoded_url or "ok.ru" in decoded_url:
        print "___resolving ok.ru url___"
        try:
            videos = resolve_ok(decoded_url)
        except:
            traceback.print_exc()
    elif "uptostream.com/" in decoded_url:
        print "___resolving uptostream.com url___"
        try:
            videos = resolve_upstream(decoded_url)
        except:
            traceback.print_exc()
    elif "drive.google.com/file/d/" in decoded_url:
        print "___resolving drive.google.com url___"
        try:
            videos = resolve_gdrive(decoded_url)
        except:
            traceback.print_exc()
    else:
        print "not supported host!"
    return videos

def rm(m, u, p):
    #if m in [1,2,3,4,5,6,8,10,16,26,36,39,40,42,45,59]:
        #data = post_page(base_url+"/user/"+u, u, p)
        #groupo_li = re.search("Tehcb:(.+?)</yv>".decode("rot13"), data).group(1)
        #if not ("Nqzvavfgenqbe".decode("rot13") in groupo_li or
            #"Zbqrenqbe".decode("rot13") in groupo_li or
            #"Hcybnqref".decode("rot13") in groupo_li or
            #"Qbangbe".decode("rot13") in groupo_li): dw().doModal()
    return m



def _get_gks_data(html_source):
    #print html_source
    mstr_match = re.compile('var a = \d+').findall(html_source)
    mstr_match = mstr_match[0].replace('var a = ','')
    print "mstr_match:", mstr_match
    if len(mstr_match) == 0:
        print "mstr_match vazio!"
        return
    gks_match = re.compile('"(/gks2.php\?id=.+?\&a=)"').findall(html_source)
    print "gks_match:", gks_match
    if len(gks_match) == 0:
        print "gks_match vazio!!"
        return
    gks_url = base_url + gks_match[0] + urllib.quote_plus(mstr_match)
    print "gks_url:", gks_url
    gks_data = xmlhttp_request(gks_url)
    #print "gks_data:", gks_data
    return gks_data


def list_tvshow(url, username, password):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
    urllib2.install_opener(opener)
    print "Lista: %s" % (url)
    try:
        html_source = post_page(url, username, password)
    except:
        raise LoginError()
    gks_data = _get_gks_data(html_source)
    if gks_data is None:
        print "Nenhuma série encontrada!"
        return result
    #print gks_data
    dp_data = json.loads(re.search(r'var display_data = (\[.+?\])</script>', gks_data).group(1))[0]
    dp_link = json.loads(re.search(r'var display_links = (\[.+?\])</script>', gks_data).group(1))[0]
    #print "dp_data =", dp_data
    #print "dp_link =", dp_link
    result = {}
    for season in dp_data.keys():
        result[season] = {}
        if isinstance(dp_data[season], list):
            season_episodes_list = True
            episodes_list = (str(i) for i in range(1, len(dp_data[season])))
        else:
            season_episodes_list = False
            episodes_list = dp_data[season].keys()

        for episode in episodes_list:
            if season_episodes_list:
                result[season][episode] = dp_data[season][int(episode)-1]
            else:
                result[season][episode] = dp_data[season][episode]
            result[season][episode]['options'] = []
            for option in sorted(dp_link.keys()):
                if season not in dp_link[option]:
                    print '[list_tv_show] missing links for season %s!' % season
                    continue
                if isinstance(dp_link[option][season], list):
                    try:
                        result[season][episode]['options'].append({'subtitle':result[season][episode].get('subtitle'), 'link': dp_link[option][season][int(episode)-1]})
                    except IndexError:
                        print '[list_tv_show] missing links for season %s episode %s!' % (season, episode)
                        continue
                else:
                    if episode not in dp_link[option][season]:
                        print '[list_tv_show] missing links for season %s episode %s!' % (season, episode)
                        continue
                    result[season][episode]['options'].append({'subtitle':result[season][episode].get('subtitle'),'link':dp_link[option][season][episode]})
    return result

def list_episodes(url, username, password, season, tvshow_dict, progress_hook=None):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
    urllib2.install_opener(opener)
    try:
        html_source = post_page(url, username, password)
    except:
        raise LoginError()
    result = tvshow_dict[season]
    for episode in result.keys():
        result[episode]['watched'] = False
    for m in re.finditer(r'<div data-sid="(?P<sid>\d+)" data-eid="(?P<eid>\d+)" data-watch="(?P<watch>\d+)"', html_source):
        if m.group('sid') == season:
            if m.group('eid') not in result:
                continue
            result[m.group('eid')]['watched'] = bool(int(m.group('watch')))
    return result

def get_quality_key(video_item):
    try:
        return int(video_item['quality'][:-1])
    except:
        pass
    return video_item['quality']

def get_options(url, username, password, flashvar_list=None, progress_hook=None):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
    urllib2.install_opener(opener)
    options = []
    progress_type = 0
    if flashvar_list is None:
        flashvar_list = []
        progress_type = 1
        try: 
            html_source = post_page(url, username, password)
        except:
            raise LoginError()
        gks_data = _get_gks_data(html_source)
        dp_data = json.loads(re.search(r'var dp_data = (\[[^\]]+\]);', gks_data).group(1))[0]
        dp_link = json.loads(re.search(r'var dp_link = (\[[^\]]+\]);', gks_data).group(1))[0]
        #print "dp_data = ", dp_data
        #print "dp_link = ", dp_link
        for idx, key in enumerate(sorted(dp_data)):
            dp_data[key]['link'] = dp_link[key]
            flashvar_list.append(dp_data[key])
            if progress_hook:
                progress_hook(int((idx + 1) / float(len(dp_data.keys())) * 50))
        print "flashvar_list = ", flashvar_list

    print "__found %d options__\n\n" % len(flashvar_list)
    for idx, f in enumerate(flashvar_list):
        print "__processing %d option__\n" % idx
        f['link_data'] = json.loads(post_page_free(base_url + "/newplay/gkpluginsphp.php", [("link", f["link"])]))
        #print f['link_data']
        videos = resolver_externos(f['link_data'])
        if len(videos) == 0:
            print "no videos resolved!"
            continue
        else:
            print "%d videos resolved" % len(videos)
            for v in videos:
                print "video_url[%s] : %s" % (v['quality'], v['url'])
        if f.get('subtitle'):
            subs = []
            for sub_path in f['subtitle'].split(','):
                subs.append(base_url + sub_path)
            print 'subs:', subs
            for v in videos:
                v['subs'] = subs
        videos.sort(key=get_quality_key, reverse=True)
        options.append(videos)
        if progress_hook:
            if progress_type == 0:
                progress_hook(int((idx + 1) / float(len(flashvar_list)) * 100))
            else:
                progress_hook(50 + int((idx + 1) / float(len(flashvar_list)) * 50))
        print '\n'
    return options