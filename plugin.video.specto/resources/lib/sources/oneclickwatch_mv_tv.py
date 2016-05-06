# -*- coding: utf-8 -*-

'''
    Specto Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urlparse,time, urllib

from resources.lib.libraries import client
from resources.lib.libraries import cloudflare
from resources.lib.libraries import cleantitle

from resources.lib.libraries import workers
from resources.lib.libraries import control
from resources.lib.resolvers import cloudzilla
from resources.lib.resolvers import openload
from resources.lib.resolvers import uptobox
from resources.lib.resolvers import zstream
from resources.lib.resolvers import vidspot


from resources.lib import resolvers
from resources.lib import sources


class source:
    def __init__(self):
        self.base_link = 'http://oneclickwatch.ws'
        self.search_link = '/search/%s/feed/rss2/'
        self.title = ''
        #view-source:http://oneclickwatch.ws/search/game+of+thrones+s06e01/feed/rss2/

    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % urllib.quote_plus(title +' '+year)
            #control.log("##OneClickWatch movie  - res00 %s" % query)
            self.title = title +' '+year
            return query
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = tvshowtitle
            url = client.cleanHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            url = '%s S%02dE%02d' % (url, int(season), int(episode))
            self.title = url
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            url = self.search_link % urllib.quote_plus(url)
            #control.log("##OneClickWatch movie  - Sess0 %s" % url)


            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            self.sources =[]
            mylinks = []
            control.log("##OneClickWatch movie  - res00 %s" % self.title)


            query = urlparse.urljoin(self.base_link, url)

            result = client.source(query)
            result = re.compile('<item>(.*?)</item>', re.DOTALL).findall(result)

            for y in result:
                mytitle = re.compile('<title>(.*?)</title>', re.DOTALL).findall(y)[0]
                if cleantitle.movie(self.title) in cleantitle.movie(mytitle):
                    if any(word in mytitle for word in
                           ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'ts']):
                        quality = 'CAM'
                    elif '1080p' in mytitle:
                        quality = '1080p'
                    elif '720p' in mytitle:
                        quality = 'HD'
                    else:
                        quality = 'MQ'
                    links = client.parseDOM(y, 'a', attrs={'rel': 'nofollow'})
                    links = [i for i in links if i.startswith('http')]
                    for a in links:
                        mylinks.append([a,quality])


            threads = []
            for i in mylinks: threads.append(workers.Thread(self.check, i))
            [i.start() for i in threads]
            for i in range(0, 10 * 2):
                is_alive = [x.is_alive() for x in threads]
                if all(x == False for x in is_alive): break
                time.sleep(1)
            return self.sources
        except:
            return self.sources


    def check(self, i):
        try:
            url = client.replaceHTMLCodes(i[0])
            url = url.encode('utf-8')

            host = urlparse.urlparse(url).netloc
            host = host.replace('www.', '').replace('embed.', '')
            host = host.rsplit('.', 1)[0]
            host = host.lower()
            host = client.replaceHTMLCodes(host)
            host = host.encode('utf-8')
            #control.log("##OneClickWatch %s - url %s" % (host, i[0]))

            if host == 'openload': check = openload.check(url)
            elif host == 'uptobox': check = uptobox.check(url)
            elif host == 'cloudzilla': check = cloudzilla.check(url)
            elif host == 'zstream': check = zstream.check(url)
            elif host == 'vidspot': check = vidspot.check(url)

            else: raise Exception()

            if check == None or check == False: raise Exception()

            self.sources.append({'source': host, 'quality': i[1], 'provider': 'Oneclickwatch', 'url': url})
        except:
            pass


    def resolve(self, url):
        try:
            url = resolvers.request(url)
            return url
        except:
            return


