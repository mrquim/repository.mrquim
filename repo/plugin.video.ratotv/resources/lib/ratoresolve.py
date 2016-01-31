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


base_url = "http://ratotv.xyz"

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


def post_page_free(url, mydata):
    mydata = urllib.urlencode(mydata)
    req = urllib2.Request(url, mydata)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
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
    rato_vk_url = "http://ratotv.xyz/zencrypt/pluginsw/plugins_vk.php"
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
            "Referer":"http://ratotv.xyz"
        }
        result.append({"provider":"ok.ru", "quality":quality, "url":vurl, "headers":headers})
    return result


def resolve_upstream(url):
    video_req = urllib2.Request(url)
    video_req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
    video_data = re.search("<video id.+?</video>", urllib2.urlopen(video_req).read(), re.DOTALL).group(0)
    result = []
    for source in re.finditer("<source src=\'(.+?)\'.+?data-res=\'(.+?)\'", video_data, re.DOTALL):
        result.append({"provider":"upstream.com", "url":source.group(1), "quality":source.group(2)})
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

def resolver_externos(hashstring):
    videos = []
    try:
        decoded_str = base64.decodestring(re.search("<div.+?>(.+?)</div>", abrir_url("http://ratotv.xyz/xbmc/xbmc2.php?hash=" + hashstring), re.DOTALL).group(1))
        #print "decoded_str",decoded_str
    except:
        print "cannot decode rato*hash :("
        raise
    match1 = re.search(binascii.unhexlify(''.join('68 74 74 70 3a 2f 2f 76 6b 2e 63 6f 6d 2f'.split())), decoded_str) #vk
    match2 = re.search(binascii.unhexlify(''.join('68 74 74 70 3a 2f 2f 6d 79 2e 6d 61 69 6c 2e 72 75 2f'.split())), decoded_str)  #mail
    match3 = re.search(binascii.unhexlify(''.join('68 74 74 70 73 3a 2f 2f 75 70 74 6f 73 74 72 65 61 6d 2e 63 6f 6d 2f'.split())), decoded_str) #up
    match4 = re.search(binascii.unhexlify(''.join('68 74 74 70 3a 2f 2f 77 77 77 2e 6f 64 6e 6f 6b 6c 61 73 73 6e 69 6b 69 2e 72 75 2f'.split())), decoded_str) #ok
    match5 = re.search(binascii.unhexlify(''.join('68 74 74 70 73 3a 2f 2f 64 72 69 76 65 2e 67 6f 6f 67 6c 65 2e 63 6f 6d 2f'.split())), decoded_str) #gdrive
    if match1:
        #decoded_url = binascii.unhexlify(''.join('68 74 74 70 3a 2f 2f 76 6b 2e 63 6f 6d 2f'.split())) + (decoded_str)
        decoded_url = decoded_str
        #print "decoded_url_vk", decoded_url
    elif match2:
        decoded_url = decoded_str
        #print "decoded_url_mail", decoded_url
    elif match3:
        decoded_url = decoded_str
        #print "decoded_url_up", decoded_url
    elif match4:
        decoded_url = decoded_str
        #print "decoded_url_ok", decoded_url
    elif match5:
        decoded_url = decoded_str
        #print "decoded_url_gdrive", decoded_url
    else:
        print "cannot decode rato*string :("

    #print "decoded url:", decoded_url
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
    elif "odnoklassniki.ru/video/" in decoded_url:
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
    mstr_match = re.compile('var a = \d+').findall(html_source)
    mstr_match = mstr_match[0].replace('var a = ','')
    print "mstr_match:", mstr_match
    if len(mstr_match) == 0:
        print "mstr_match vazio!"
        return
    gks_match = re.compile('"(/gks.php\?id=.+?\&a=)"').findall(html_source)
    print "gks_match:", gks_match
    if len(gks_match) == 0:
        print "gks_match vazio!!"
        return
    gks_url = base_url + gks_match[0] + urllib.quote_plus(mstr_match)
    print "gks_url:", gks_url
    gks_data = xmlhttp_request(gks_url)
    print "gks_data:", gks_data
    return gks_data


def list_seasons(url, username, password):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
    urllib2.install_opener(opener)
    print "Lista: %s" % (url)
    result = {}
    try:
        html_source = post_page(url, username, password)
    except:
        raise LoginError()
    gks_data = _get_gks_data(html_source)
    if gks_data is None:
        print "Nenhuma série encontrada!"
        return result
    gks2_match = re.compile('data-html="(.+?)"').findall(gks_data)
    for idx, gks2 in enumerate(gks2_match):
        gks2_parsed = urlparse.urlparse(base_url + gks2)
        gks2_query = dict((q.split('=')[0], q.split('=')[1]) for q in gks2_parsed.query.split('&'))
        if gks2_query['t'] == 1:
            print "Isto é um filme, não uma temporada!"
            return result
        season_num = gks2_query['s']
        print "...processando %s temporada" % (season_num)
        if not season_num in result:
            result[season_num] = []
        result[season_num].append(gks2)
    return result


def list_episodes(url, username, password, season, gks2_list, progress_hook=None):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
    urllib2.install_opener(opener)
    try:
        html_source = post_page(url, username, password)
    except:
        raise LoginError()
    result = {}
    for idx, gks2 in enumerate(gks2_list):
        print "html_sourcehtml_source", html_source
        print base_url + gks2
        gks2_source = xmlhttp_request(base_url + gks2)
        if gks2_source == "<script>parent.window.location.reload(true);</script>":
            _get_gks_data(html_source)
            gks2_source = xmlhttp_request(base_url + gks2)
        season_data = json.loads(re.compile('\&proxy.list=(.+?)\&').findall(gks2_source)[0]) 
        print "season_dataaa", season_data
        for episode in season_data:
            episode_key = re.search(".*?(\d+)", episode['title']).group(1)
            if episode_key not in result:
                result[episode_key] = {"options":[], "watched":None}
            result[episode_key]["options"].append(episode)
            if progress_hook:
                progress_hook(int((idx+1)/float(len(gks2_list)) * 100))
    for m  in re.finditer(r'<div data-sid="(\d+)" data-eid="(\d+)" data-watch=\"(\d+)">.+?</div>', html_source):
        if m.group(1) == season:
            if m.group(2) not in result:
                continue
            result[m.group(2)]["watched"] = bool(int(m.group(3)))
    return result

def list_page(url, username, password):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
    urllib2.install_opener(opener)
    print "Lista: %s" % (url)
    result = {}
    try:
        html_source = post_page(url, username, password)
    except:
        raise LoginError()
    gks_data = _get_gks_data(html_source)
    if gks_data is None:
        print "Nenhum filme/série encontrado :("
        return
    gks2_match = re.compile('data-html="(.+?)"').findall(gks_data)
    for idx, gks2 in enumerate(gks2_match):
        gks2_parsed = urlparse.urlparse(base_url + gks2)
        gks2_query = dict((q.split('=')[0], q.split('=')[1]) for q in gks2_parsed.query.split('&'))
        if gks2_query['t'] == 1:
            print "filme detetado..."
            result['type'] = 'movie'
        else:
            print "serie detetado..."
            result['type'] = 'series'
        break
    if result['type'] == 'movie':
        print "extracting filme metadata..."
        gks2_source = xmlhttp_request(base_url + gks2_match[0])
        options = re.compile('\&proxy.list=(.+?)\&').findall(gks2_source)
        print "...encontrado %d options" % (len(options))
        for o in options:
            result['options'].append(json.loads(o))
    elif result['type'] == 'series':
        print "extracting series metadata..."
        title = re.compile('<strong>Título Original: </strong>(.+?)</li>').findall(html_source)
        if title:
            print "...titulo detetado = %s" % (title[0])
            result['title'] = title[0]
        year = re.compile('<strong>Ano: </strong><a href=".+?">(.+?)</a>').findall(html_source)
        if year:
            print "...titulo detetado = %s" % (year[0])
            result["year"] = year[0]
        result['seasons'] = {}
        for idx, gks2 in enumerate(gks2_match):
            gks2_parsed = urlparse.urlparse(base_url + gks2)
            gks2_query = dict((q.split('=')[0], q.split('=')[1]) for q in gks2_parsed.query.split('&'))
            season_num = gks2_query['s']
            print "...extracting %s temporadas" % (season_num)
            if not season_num in result['seasons']:
                result['seasons'][season_num] = {}
            season_dict = result['seasons'][season_num]
            gks2_source = xmlhttp_request(base_url + gks2)
            season_data = json.loads(re.compile('\&proxy.list=(.+?)\&').findall(gks2_source)[0]) 
            for episode in season_data:
                episode_key = re.search(".*?(\d+)", episode['title']).group(1)
                if episode_key not in season_dict:
                    season_dict[episode_key] = []
                season_dict[episode_key].append(episode)
            print "....option[%d] - %d episodes" % (len(season_dict[episode_key]), len(season_dict.keys()))
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
        gks2_match = re.compile('data-html="(.+?)"').findall(gks_data)
        print "\n\ngks2_match:", gks2_match
        for idx, gks2 in enumerate(gks2_match):
            gks2_url = base_url + gks2
            print "gks2_url:", gks2_url
            html_source = xmlhttp_request(gks2_url)
            flashvar_list.append(json.loads(re.compile('\&proxy.list=(.+?)\&').findall(html_source)[0])[0])
            if progress_hook:
                progress_hook(int((idx + 1) / float(len(gks2_match)) * 50))
    print "__found %d options__\n\n" % len(flashvar_list)
    for idx, f in enumerate(flashvar_list):
        print "__processing %d option__\n" % idx
        print "ratohash:", f['file']
        videos = resolver_externos(f['file'])
        if len(videos) == 0:
            print "no videos resolved!"
            continue
        else:
            print "%d videos resolved" % len(videos)
            for v in videos:
                print "video_url[%s] : %s" % (v['quality'], v['url'])
        if 'captions.files' in f:
            subs = []
            for sub_path in f['captions.files'].split(','):
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

