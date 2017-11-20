import re
import requests
import xbmc
from ..scraper import Scraper
from ..common import clean_title

class enet24doc(Scraper):
    domains = ['http://enet24-045.enet24.eu']
    name = "E24Docs"
    sources = []

    def __init__(self):
        self.base_link = 'http://enet24-045.enet24.eu/Documentary/'
                          

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url= self.base_link
            html = requests.get(start_url,timeout=5).content 
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
            for url,name in match:
                new_title = name.split('20')[0]
                if clean_title(title).lower() in clean_title(new_title).lower():
                    if year in url:
                        url = self.base_link+url
                        if '1080p' in url:                                          
                            qual = '1080p'
                        elif '720p' in url: 
                            qual = '720p'
                        elif '480p' in url:
                            qual = '480p'
                        else:
                            qual = 'SD'
                        self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': url,'direct': True})
            return self.sources
        except Exception as e:
            print repr(e)
            pass
            return []

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url = self.base_link
            html = requests.get(start_url,timeout=5).content                    
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)      
            for media_url,name in match:
                if clean_title(title.lower()) in clean_title(name.lower()):     
                    season_info = "0%s"%season if len(season)<2 else season
                    episode_info = "0%s"%episode if len(episode)<2 else episode   
                    episode_chk = 's%se%s' %(season_info,episode_info)         
                    
                    if media_url.endswith('/'):                                    
                        new_url = self.base_link + media_url                        
                        folder = requests.get(new_url,timeout=5).content           
                        match2 = re.compile('<a href="(.+?)"').findall(folder)      
                        for media_url in match2:
                            if episode_chk.lower() in media_url.lower():            
                                if '1080p' in media_url:
                                    qual = '1080p'
                                elif '720p' in media_url:
                                    qual = '720p'
                                elif '560p' in media_url:
                                    qual = '560p'
                                elif '480p' in media_url:
                                    qual = '480p'
                                else:
                                    qual = 'SD'
                                final = new_url + media_url   
                                self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': final,'direct': True})                    
                    
                    else:
                        if episode_chk.lower() in media_url.lower(): 
                            if '1080p' in media_url:
                                qual = '1080p'
                            elif '720p' in media_url:
                                qual = '720p'
                            elif '560p' in media_url:
                                qual = '560p'
                            elif '480p' in media_url:
                                qual = '480p'
                            else:
                                qual = 'SD'
                            final = self.base_link + media_url
                            self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': final,'direct': True})
            return self.sources
        except Exception as e:
            print repr(e)
            pass
            return []      