# -*- coding: utf-8 -*-

'''



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



import re,urllib,urlparse,random
from BeautifulSoup import BeautifulSoup
from ..common import clean_title, random_agent, clean_search, replaceHTMLCodes, filter_host, get_rd_domains
from ..scraper import Scraper
import requests
import xbmc


class Wzrcraft(Scraper):
    domains = ['wzrcraft.net']
    name = "wzrcraft"

    def __init__(self):
        self.domains = ['wrzcraft.net']
        self.base_link = 'http://wrzcraft.net'
        self.search_link = '/search/%s+%s/feed/rss2/'

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            if not debrid:
                return []
            url = self.movie(imdb, title, year)
            sources = self.sources(url, [], [])
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return []

    def scrape_episode(self, title, show_year, year, season, episode,
                       imdb, tvdb, debrid=False):
        try:
            if not debrid:
                return []
            show_url = self.tvshow(imdb, tvdb, title, show_year)
            url = self.episode(show_url, imdb, tvdb, title,
                               year, season, episode)
            sources = self.sources(url, [], [])
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return []

    def movie(self, imdb, title, year):
        self.elysium_url = []
        try:
            title = clean_search(title)
            cleanmovie = clean_title(title)
            titlecheck = cleanmovie+year
            query = self.search_link % (
                urllib.quote_plus(title.replace("'", "")), year)
            query = urlparse.urljoin(self.base_link, query)
            print ("WRZCRAFT QUERY", query)
            r = requests.get(query).content
            posts = parse_dom(r, 'item')
            for post in posts:
                try:
                    t = parse_dom(post, 'title')[0]
                    t = t.encode('utf-8')
                    check = clean_title(t)
                    if titlecheck not in check:
                        continue
                    c = parse_dom(post, 'content.+?')[0]
                    u = parse_dom(c, 'p')
                    u = [parse_dom(i, 'a', ret='href') for i in u]
                    u = [i[0] for i in u if len(i) == 1]
                    if not u:
                        raise Exception()

                    u = [(t, i) for i in u]

                    self.elysium_url += u
                    # self.elysium_url.append([links,t])

                except:
                    pass
                print ("WRZCRAFT PASSED", self.elysium_url)
                return self.elysium_url

        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        self.elysium_url = []
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = clean_search(title)
            cleanmovie = clean_title(title)
            data['season'], data['episode'] = season, episode
            episodecheck = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            episodecheck = episodecheck.lower()
            titlecheck = cleanmovie+episodecheck
            query = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            query = self.search_link % (
                urllib.quote_plus(title.replace("'", "")), query)
            query = urlparse.urljoin(self.base_link, query)
            print ("WRZCRAFT SHOW", query)

            r = requests.get(query).content
            posts = parse_dom(r, 'item')
            for post in posts:
                try:
                    t = parse_dom(post, 'title')[0]
                    t = t.encode('utf-8')
                    check = clean_title(t)
                    if titlecheck not in check:
                        continue
                    c = parse_dom(post, 'content.+?')[0]
                    u = parse_dom(c, 'p')
                    u = [parse_dom(i, 'a', ret='href') for i in u]
                    u = [i[0] for i in u if len(i) == 1]
                    if not u:
                        raise Exception()
                    u = [(t, i) for i in u]
                    self.elysium_url += u

                except:
                    pass
                print ("WRZCRAFT PASSED", self.elysium_url)
            return self.elysium_url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            for title, url in self.elysium_url:
                quality = "SD"
                quality = quality_tag(title)
                if "1080p" in url.lower():
                    quality = "1080p"
                elif "720p" in url.lower():
                    quality = "HD"

                info = ''
                if "hevc" in title.lower():
                    info = "HEVC"
                loc = urlparse.urlparse(url).netloc
                if not filter_host(loc):
                    rd_domains = get_rd_domains()
                    if loc not in rd_domains:
                        continue
                try:
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                except:
                    host = 'Videomega'
                url = replaceHTMLCodes(url)
                url = url.encode('utf-8')
                sources.append({'source': host, 'quality': quality,
                                'provider': 'Wrzcraft', 'url': url,
                                'info': info, 'direct': False,
                                'debridonly': True})
            return sources
        except:
            return sources

    def resolve(self, url):

            return url


def _getDOMContent(html, name, match, ret):
    end_str = "</%s" % (name)
    start_str = '<%s' % (name)

    start = html.find(match)
    end = html.find(end_str, start)
    pos = html.find(start_str, start + 1)

    while pos < end and pos != -1:  # Ignore too early </endstr> return
        tend = html.find(end_str, end + len(end_str))
        if tend != -1:
            end = tend
        pos = html.find(start_str, pos + 1)

    if start == -1 and end == -1:
        result = ''
    elif start > -1 and end > -1:
        result = html[start + len(match):end]
    elif end > -1:
        result = html[:end]
    elif start > -1:
        result = html[start + len(match):]
    else:
        result = ''

    if ret:
        endstr = html[end:html.find(">", html.find(end_str)) + 1]
        result = match + result + endstr

    return result


def _getDOMAttributes(match, name, ret):
    pattern = '''<%s[^>]* %s\s*=\s*(?:(['"])(.*?)\\1|([^'"].*?)(?:>|\s))''' % (name, ret)
    results = re.findall(pattern, match, re.I | re.M | re.S)
    return [result[1] if result[1] else result[2] for result in results]


def _getDOMElements(item, name, attrs):
    if not attrs:
        pattern = '(<%s(?: [^>]*>|/?>))' % (name)
        this_list = re.findall(pattern, item, re.M | re.S | re.I)
    else:
        last_list = None
        for key in attrs:
            pattern = '''(<%s [^>]*%s=['"]%s['"][^>]*>)''' % (name, key, attrs[key])
            this_list = re.findall(pattern, item, re.M | re. S | re.I)
            if not this_list and ' ' not in attrs[key]:
                pattern = '''(<%s [^>]*%s=%s[^>]*>)''' % (name, key, attrs[key])
                this_list = re.findall(pattern, item, re.M | re. S | re.I)

            if last_list is None:
                last_list = this_list
            else:
                last_list = [item for item in this_list if item in last_list]
        this_list = last_list

    return this_list


def parse_dom(html, name='', attrs=None, ret=False):
    if attrs is None:
        attrs = {}
    if isinstance(html, str):
        try:
            html = [html.decode("utf-8")]  # Replace with chardet thingy
        except:
            print "none"
            try:
                html = [html.decode("utf-8", "replace")]
            except:

                html = [html]
    elif isinstance(html, unicode):
        html = [html]
    elif not isinstance(html, list):

        return ''

    if not name.strip():

        return ''

    if not isinstance(attrs, dict):

        return ''

    ret_lst = []
    for item in html:
        for match in re.findall('(<[^>]*\n[^>]*>)', item):
            item = item.replace(match, match.replace('\n', ' ').replace('\r', ' '))

        lst = _getDOMElements(item, name, attrs)

        if isinstance(ret, str):
            lst2 = []
            for match in lst:
                lst2 += _getDOMAttributes(match, name, ret)
            lst = lst2
        else:
            lst2 = []
            for match in lst:
                temp = _getDOMContent(item, name, match, ret).strip()
                item = item[item.find(temp, item.find(match)):]
                lst2.append(temp)
            lst = lst2
        ret_lst += lst

    # log_utils.log("Done: " + repr(ret_lst), xbmc.LOGDEBUG)
    return ret_lst

def quality_tag(txt):
    if any(value in txt for value in ['1080', '1080p','1080P']):
        quality = "1080p"
    elif any(value in txt for value in ['720', '720p','720P']):
        quality = "HD"
    else:
        quality = "SD"
    return quality
