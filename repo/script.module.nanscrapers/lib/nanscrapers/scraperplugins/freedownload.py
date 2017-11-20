import requests
import re
import xbmc
from ..scraper import Scraper
from ..common import clean_title,clean_search
            

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                                           
class freedownload(Scraper):
    domains = ['http://freemoviedownloads6.com']
    name = "FreeDownload"
    sources = []

    def __init__(self):
        self.base_link = 'http://freemoviedownloads6.com'
                       

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = self.base_link + '/?s=' + search_id.replace(' ','+')
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            links = html.split('<h2 class="title"')[1]
            match = re.compile('href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(links)
            for url,name in match:
                if clean_title(title).lower() in clean_title(name).lower():
                    if year in name:
                        self.get_source(url)

            return self.sources
        except:
            pass
            return[]

    def get_source(self,url):
        try:
            headers={'User-Agent':User_Agent}
            OPEN = requests.get(url,headers=headers,timeout=10).content
            OPEN = OPEN.split("type='video/mp4'")[1]
            Regex = re.compile('href="(.+?)"',re.DOTALL).findall(OPEN)
            for link in Regex:
                if '1080' in link:
                    res = '1080p'
                elif '720' in link:
                    res = '720p'
                elif '480' in link:
                    res = '480p'
                else:
                    res = 'SD'                
                if '.mkv' in link:
                    self.sources.append({'source': 'DirectLink', 'quality': res, 'scraper': self.name, 'url': link,'direct': True})
                if '.mp4' in link:
                    self.sources.append({'source': 'DirectLink', 'quality': res, 'scraper': self.name, 'url': link,'direct': True})                    
        except:
            pass

