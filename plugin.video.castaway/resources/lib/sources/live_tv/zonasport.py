from resources.lib.modules import client,webutils
import re,sys,xbmcgui,os
from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
        self.mode = 'zonasport'
        self.name = 'Zonasports.in'
        self.icon = 'zonasport.png'
        self.categorized = False
        self.paginated = False
        self.multilink = True

class main():
    def __init__(self, url='http://zonasports.in'):
        self.base = 'http://zonasports.in'
        self.url = url   

    def links(self,url):
        links = url.split(',')
        links = self.__prepare_links(links)
        return links

    def channels(self):
        result = client.request(self.base)
        reg = re.compile('<td><span class="t">(.+?)</span></td>\s*<td align="center">\s*<img src=".+?"/></td>\s*<td align="left">(.+?):\s*<b>(.+?)\s*\(([^\)]+)',re.DOTALL)
        events = re.findall(reg,result)
        events = self.__prepare_events(events)
        return events
    

    @staticmethod
    def convert_time(time):
        li = time.split(':')
        hour,minute=li[0],li[1]
        import datetime
        from resources.lib.modules import pytzimp
        d = pytzimp.timezone(str(pytzimp.timezone('Europe/Ljubljana'))).localize(datetime.datetime(2000 , 1, 1, hour=int(hour), minute=int(minute)))
        timezona= addon.get_setting('timezone_new')
        my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
        convertido=d.astimezone(my_location)
        fmt = "%H:%M"
        time=convertido.strftime(fmt)
        return time

    

    def __prepare_events(self,events):
        new = []
        for event in events:
            try:
                url = event[3].replace('\n','').strip()
                title = event[2]
                sport = event[1]
                time = self.convert_time(event[0])
                title = '[COLOR orange](%s)[/COLOR] (%s) [B]%s[/B] - %s'%(time,sport,title,url)
                title = title.encode('utf-8').replace('\n','')
                new.append((url,title, icon_path(info().icon)))
            except:
                pass
        for i in range(14):
            url = 'CH%s'%(i+1)
            title = 'Zonasport %s'%(i+1)
            new.append((url,title, icon_path(info().icon)))

        return new

    def __prepare_links(self,links):
        new=[]
        
        for link in links:
            id = link.replace('CH','').strip()
            url = 'http://zonasports.in/ch.php?id=%s'%id
            title = 'Zonasport ' + id
            new.append((url,title))
            
        return new