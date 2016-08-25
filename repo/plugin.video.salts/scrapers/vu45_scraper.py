"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

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
"""
import scraper
import urlparse
import urllib
import re
import kodi
import log_utils
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://vu45.com'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'vu45'

    def resolve_link(self, link):
        if 'watch.php' in link:
            _direct, sources = self.__get_links(link)
            if sources:
                return sources[0]
        else:
            return link

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=2)
            fragment = dom_parser.parse_dom(html, 'div', {'id': 'player-container'})
            if fragment:
                iframe_urls = dom_parser.parse_dom(fragment[0], 'iframe', ret='src')
                labels = dom_parser.parse_dom(fragment[0], 'a', {'href': '#play-\d+'})
                
                for iframe_url, label in zip(iframe_urls, labels):
                    if re.search('\(Part?\s+\d+\)', label):
                        multipart = True
                        continue  # skip multipart
                    else:
                        multipart = False
                    
                    direct, streams = self.__get_links(iframe_url, url)
                    for stream_url in streams:
                        if stream_url:
                            if direct:
                                host = self._get_direct_hostname(stream_url)
                                if host == 'gvideo':
                                    quality = scraper_utils.gv_get_quality(stream_url)
                                else:
                                    quality = QUALITIES.HD720
                            else:
                                host = urlparse.urlparse(stream_url).hostname
                                quality = QUALITIES.HIGH
                                
                            stream_url += '|User-Agent=%s' % (scraper_utils.get_ua())
                            source = {'multi-part': multipart, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': direct}
                            sources.append(source)

        return sources

    def __get_links(self, iframe_url, page_url):
        sources = []
        direct = True
        headers = {'Referer': page_url}
        html = self._http_get(iframe_url, headers=headers, cache_limit=2)
        iframe_url2 = dom_parser.parse_dom(html, 'iframe', ret='src')
        if iframe_url2 and 'token=&' not in iframe_url2[0]:
            headers = {'Referer': iframe_url}
            html = self._http_get(iframe_url2[0], headers=headers, cache_limit=2)
            if 'fmt_stream_map' in html:
                sources = self._parse_gdocs(iframe_url2[0])
                direct = True
            else:
                sources = dom_parser.parse_dom(html, 'source', {'type': 'video[^"]*'}, ret='src')
                direct = True
            
            if not sources:
                match = re.search('proxy\.link=([^&"]+)', html)
                if match:
                    sources = [match.group(1)]
                    direct = False
                    
        return direct, sources
        
    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/?s=%s' % (urllib.quote_plus(title)))
        html = self._http_get(search_url, cache_limit=8)
        fragment = dom_parser.parse_dom(html, 'div', {'id': 'box_movies'})
        if fragment:
            for movie in dom_parser.parse_dom(fragment[0], 'div', {'class': 'movie'}):
                match = re.search('href="([^"]+)', movie)
                if match:
                    match_url = match.group(1)
                    match_title_year = dom_parser.parse_dom(movie, 'img', ret='alt')
                    if match_title_year:
                        match_title_year = match_title_year[0]
                        match = re.search('(.*?)\s+\((\d{4})\)', match_title_year)
                        if match:
                            match_title, match_year = match.groups()
                        else:
                            match_title = match_title_year
                            match_year = dom_parser.parse_dom(movie, 'div', {'class': 'year'})
                            try: match_year = match_year[0]
                            except: match_year = ''
                            
                        if not year or not match_year or year == match_year:
                            result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                            results.append(result)

        return results
