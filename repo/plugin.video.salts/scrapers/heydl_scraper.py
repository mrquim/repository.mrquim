# -*- coding: utf-8 -*-
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
import kodi
import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://dl2.heydl.com/film'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.row_pattern = '<td>\s*<a\s+href="(?P<link>[^"]+)">(?P<title>[^<]+)</a></td>\s*<td>\s*(?P<size>.*?)</td><td>(?P<date>.*?)</td>'

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'HeyDL'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if source_url and source_url != FORCE_NO_MATCH:
            meta = scraper_utils.parse_movie_link(source_url)
            stream_url = source_url + '|User-Agent=%s' % (scraper_utils.get_ua())
            quality = scraper_utils.height_get_quality(meta['height'])
            hoster = {'multi-part': False, 'host': self._get_direct_hostname(stream_url), 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
            if 'format' in meta: hoster['format'] = meta['format']
            hosters.append(hoster)
        return hosters

    def search(self, video_type, title, year, season=''):
        results = []
        norm_title = scraper_utils.normalize_title(title)
        for item in self._get_files(self.base_url, cache_limit=48):
            if not item['directory']:
                meta = scraper_utils.parse_movie_link(item['title'])
                if meta['dubbed']: continue
                if (norm_title in scraper_utils.normalize_title(meta['title'])) and (not year or not meta['year'] or year == meta['year']):
                    match_title = meta['title'].replace('.', ' ')
                    match_title += ' [%sp.%s]' % (meta['height'], meta['extra'])
                    match_url = item['url'].replace(self.base_url, '')
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': meta['year']}
                    results.append(result)
        return results
