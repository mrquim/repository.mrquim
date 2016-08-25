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
import urllib
import urlparse
import kodi
import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://movieflix.to'
TYPES = {VIDEO_TYPES.MOVIE: 'movie', VIDEO_TYPES.TVSHOW: 'tvshow'}
BASE_QUERY = {'add_mroot': 1, 'cast': 0, 'crew': 0, 'description': 1, 'postersize': 'poster',
              'previewsizes': '{"preview_grid":"video-block","preview_list":"big3-index"}', 'slug': 1}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'MovieFlix'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            query = {'episodes_list': 1, 'season_list': 0, 'sub': 1}
            query.update(BASE_QUERY)
            js_data = self.__get_json(source_url, query, self.base_url, cache_limit=2)
            media = js_data.get('item', {}).get('media', {})
            for key in media:
                stream_url = media[key]
                host = self._get_direct_hostname(stream_url)
                if host == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                else:
                    quality = scraper_utils.height_get_quality(key)
                stream_url += '|User-Agent=%s' % (scraper_utils.get_ua())
                views = js_data.get('views', 0)
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': views, 'rating': None, 'url': stream_url, 'direct': True}
                hosters.append(hoster)
                
        return hosters

    def _get_episode_url(self, show_url, video):
        season_url = urlparse.urljoin(self.base_url, show_url)
        season_url += '/season-%s' % (video.season)
        query = {'episodes_list': 1, 'season_list': 0}
        query.update(BASE_QUERY)
        js_data = self.__get_json(season_url, query, self.base_url, cache_limit=8)
        force_title = scraper_utils.force_title(video)
        if not force_title:
            for episode in js_data.get('episodes', {}):
                if episode.get('seq') == video.episode:
                    return scraper_utils.pathify_url(episode['url'])
        
        if (force_title or kodi.get_setting('title-fallback') == 'true') and video.ep_title:
            norm_title = scraper_utils.normalize_title(video.ep_title)
            for episode in js_data.get('episodes', {}):
                if norm_title == scraper_utils.normalize_title(episode.get('title', '')):
                    return scraper_utils.pathify_url(episode['url'])
    
    def search(self, video_type, title, year, season=''):
        results = []
        query = {'p': 1, 'postersizes': '{"poster_search":"poster-search-square"}', 'q': title}
        referer = urlparse.urljoin(self.base_url, '/search?q=%s' % (urllib.quote(title)))
        js_data = self.__get_json('/search', query, referer, cache_limit=24)
        for item in js_data.get('items', []):
            if item.get('type') != TYPES[video_type]: continue
            if 'title' in item and 'url' in item:
                match_year = str(item.get('year', ''))
                match_title = item['title']
                match_url = item['url']
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)
        return results

    def __get_json(self, url, query, referer, cache_limit=8):
        search_url = urlparse.urljoin(self.base_url, url)
        search_url = search_url + '?' + urllib.urlencode(query)
        headers = {'Referer': referer, 'Accept': 'application/json'}
        html = self._http_get(search_url, headers=headers, cache_limit=cache_limit)
        return scraper_utils.parse_json(html, search_url)
