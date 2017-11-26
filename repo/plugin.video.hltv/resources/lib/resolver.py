# -*- coding: utf-8 -*-

import simple_requests as requests
from common import *

class Resolver:

    def __init__(self, url):
        
        self.resolved_url = ''
        self.seektime = False
        
        if 'twitch' in url:
            self.twitch(url)
            
        elif 'stream.me' in url:
            self.stream_me(url)
            
        elif 'oddshot' in url:
            self.oddshot(url)
            
        elif 'hitbox' in url:
            self.hitbox(url)
            
        elif 'youtube' in url:
            self.youtube(url)
            
    def twitch(self, url):
        
        def time_to_sec(t):
            seconds = 0
            h = re.search('(\d+)h', t)
            m = re.search('(\d+)m', t)
            s = re.search('(\d+)s', t)
            if h:
                seconds += int(h.group(1))*60*60
            if m:
                seconds += int(m.group(1))*60
            if s:
                seconds += int(s.group(1))
            return seconds
        
        headers={'Client-ID': 'jzkbprff40iqj646a697cyrvl0zt2m6'}
        
        if 'channel=' in url:
            _id_ = url.split('channel=')[1].lower()
            access = 'https://api.twitch.tv/api/channels/%s/access_token' % _id_
            hls = 'http://usher.ttvnw.net/api/channel/hls/%s.m3u8?%s'
        elif 'video=' in url:
            _id_ = re.sub('http.*?video=v|&.*?$', '', url)
            start_point = time_to_sec(re.sub('http.*?&t=', '', url))
            info = requests.get('https://api.twitch.tv/api/videos/v%s' % _id_, headers=headers).json()
            self.seektime = start_point
            access = 'https://api.twitch.tv/api/vods/%s/access_token' % _id_
            hls = 'https://usher.ttvnw.net/vod/%s.m3u8?%s'
        elif 'clips' in url:
            data = requests.get(url).text
            quality_options = re.search('quality_options\s*:\s*\[(.*?)\]', data, re.DOTALL).group(1)
            self.resolved_url = re.search('"source"\s*:\s*"(.+?)"', quality_options).group(1)
            return
        data = requests.get(access, headers=headers).json()
        params  = {'allow_source':'true'}
        params['sig']   = data['sig']
        params['token'] = data['token']
        self.resolved_url = hls % (_id_, urllib.urlencode(params))
        
    def stream_me(self, url):
        data = requests.get(url).text
        self.resolved_url = re.search('"hlsmp4":\{"href":"(.+?)"', data).group(1)
        
    def oddshot(self, url):
        data = requests.get(url).text
        self.resolved_url = re.search('"url":"(.+?)"', data).group(1)
        
    def hitbox(self, url):
        channel = re.sub('\?.+?$', '', url.split('embed/')[1])
        api = 'http://www.hitbox.tv/api/player/config/live/%s'
        data = requests.get(api % channel, headers={'Accept': 'application/json, text/plain, */*'}).json()
        bitrate = 0
        bitrates = data['playlist'][0]['bitrates']
        for i in bitrates:
            if bitrate < int(i['bitrate']):
                url = i['url']
                bitrate = int(i['bitrate'])
        self.resolved_url = url
        
    def youtube(self, url):
        
        start_point = re.search('start=(\d+)', url)
        if start_point:
            self.seektime = int(start_point.group(1))
        _id_ = re.search('http.*?/embed/(.+?)(\?|$)', url)
        if _id_:
            _id_ = _id_.group(1)
            params = {
                'video_id': _id_,
                'eurl': 'https://youtube.googleapis.com/v/' + _id_,
                'ssl_stream': '1',
                'ps': 'default',
                'el': 'default'
            }
            url = 'https://www.youtube.com/get_video_info'
            data = requests.get(url, params=params).text
            params = dict(urlparse.parse_qsl(data))
            dash = params.get('dashmpd', '')
            hls = params.get('hlsvp', '')
            if dash:
                self.resolved_url = dash
            if hls and not self.resolved_url:
                self.resolved_url =  hls
                
        if not self.resolved_url and _id_:
            from .signature.cipher import Cipher
            url = 'https://www.youtube.com/watch?v=%s' % (_id_)
            html = requests.get(url).text
            pos = html.find('<script>var ytplayer')
            if pos >= 0:
                html2 = html[pos:]
                pos = html2.find('</script>')
                if pos:
                    html = html2[:pos]

            re_match_js = re.search(r'\"js\"[^:]*:[^"]*\"(?P<js>.+?)\"', html)
            js = ''
            cipher = None
            if re_match_js:
                js = re_match_js.group('js').replace('\\', '').strip('//')
                cipher = Cipher(java_script_url=js)

            re_match = re.search(r'\"url_encoded_fmt_stream_map\"\s*:\s*\"(?P<url_encoded_fmt_stream_map>[^"]*)\"', html)
            if re_match:
                url_encoded_fmt_stream_map = re_match.group('url_encoded_fmt_stream_map')
                url_encoded_fmt_stream_map = url_encoded_fmt_stream_map.split(',')
                for value in url_encoded_fmt_stream_map:
                    value = value.replace('\\u0026', '&')
                    attr = dict(urlparse.parse_qsl(value))
                    url = attr.get('url', None)
                    if url:
                        url = urllib.unquote(attr['url'])
                        if 'signature' in url:
                            self.resolved_url = url
                            break
                        signature = ''
                        if attr.get('s', ''):
                            signature = cipher.get_signature(attr['s'])
                        elif attr.get('sig', ''):
                            signature = attr.get('sig', '')
                        if signature:
                            url += '&signature=%s' % signature
                            self.resolved_url = url
                            break