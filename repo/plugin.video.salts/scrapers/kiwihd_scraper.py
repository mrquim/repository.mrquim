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
import re
import urllib
import urlparse
import kodi
import log_utils
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper

BASE_URL = 'http://www.kiwihd.com'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.base_url2 = 'http://watch.kiwihd.com'

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'KiwiHD'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            if video.video_type == VIDEO_TYPES.MOVIE:
                url = urlparse.urljoin(self.base_url, source_url)
                html = self._http_get(url, cache_limit=8)
                html = self.__get_watch_now(html, url)
            else:
                url = urlparse.urljoin(self.base_url2, source_url)
                html = self._http_get(url, cache_limit=8)

            source = dom_parser.parse_dom(html, 'source', {'type': 'video/mp4'}, ret='src')
            if source:
                source = source[0].replace(' ', '')
                host = self._get_direct_hostname(source)
                stream_url = source + '|User-Agent=%s' % (scraper_utils.get_ua())
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': QUALITIES.HD720, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                hosters.append(hoster)

        return hosters

    def __get_watch_now(self, html, page_url):
        link = dom_parser.parse_dom(html, 'a', {'class': 'adf'}, ret='href')
        if link:
            headers = {'Referer': page_url}
            html = self._http_get(link[0], headers=headers, cache_limit=.5)
        
        return html
    
    def _get_episode_url(self, season_url, video):
        episode_pattern = 'href="([^"]*-ep-0*%s[._][^"]*)' % (video.episode)
        return self._default_get_episode_url(season_url, video, episode_pattern)
    
    def search(self, video_type, title, year, season=''):
        results = []
        if not year: return results
        search_url = urlparse.urljoin(self.base_url, '/search/label/%s&max-results=50')
        search_url = search_url % (year)
        html = self._http_get(search_url, cache_limit=8)
        norm_title = scraper_utils.normalize_title(title)
        for item in dom_parser.parse_dom(html, 'div', {'class': "[^']*hentry[^']*"}):
            tags = dom_parser.parse_dom(item, 'a', {'rel': 'tag'})
            post_title = dom_parser.parse_dom(item, 'h\d+', {'class': "[^']*post-title[^']*"})
            match_url = ''
            match_title_year = ''
            if post_title:
                match = re.search("href='([^']+)[^>]+>([^<]+)", post_title[0])
                if match:
                    match_url, match_title_year = match.groups()

            if match_url and match_title_year:
                is_season = re.search('season\s+(\d+)', match_title_year, re.I)
                has_episodes = dom_parser.parse_dom(item, 'a', {'class': 'adf'})
                has_episodes = True if has_episodes and '01' in has_episodes[0] else False
                if (not is_season and video_type == VIDEO_TYPES.MOVIE) or ((has_episodes or is_season) and video_type == VIDEO_TYPES.SEASON):
                    if video_type == VIDEO_TYPES.MOVIE:
                        match = re.search('(.*?)\s*-\s*(\d{4})$', match_title_year)
                        if match:
                            match_title, match_year = match.groups()
                        else:
                            match_title = match_title_year
                            match_year = self.__year_from_tags(tags)
                    else:
                        if (season and not is_season) or (season and is_season and int(is_season.group(1)) != int(season)):
                            continue
                        
                        match_title = match_title_year
                        match_year = ''
                
                    if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                        result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                        results.append(result)
        return results
    
    def __year_from_tags(self, tags):
        for tag in tags:
            if re.match('\d{4}', tag): return tag
        return ''
