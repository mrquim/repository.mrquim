from resources.lib.modules import client,webutils,cloudflare
import re,sys,xbmcgui,os
from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
        self.mode = 'tugoleada'
        self.name = 'tugoleada.com'
        self.icon = 'tugoleada.png'
        self.categorized = False
        self.paginated = False
        self.multilink = False

class main():
    def __init__(self, url='http://tugoleada.com'):
        self.base = 'http://tugoleada.com'
        self.url = url   


    def channels(self):
        result = client.request(self.base)
        events = re.findall('<th>(.+?)</th>\s*<th style=.+?>(.+?)</th>\s*<th><img src="http://tugoleada.com/img/(.+?).png" /></th>\s*<th><a href="(.+?)">',result, flags=re.UNICODE)
        events = self.__prepare_events(events)
        return events
    

    @staticmethod
    def convert_time(time):
        li = time.split('.')
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
                url = event[3].replace('\n','').strip()
                title = event[1]
                lang = event[2]
                time = self.convert_time(event[0])
                title = '[COLOR orange](%s)[/COLOR] [B]%s[/B] (%s)'%(time,title,lang.upper())
                new.append((url,title, icon_path(info().icon)))
        for i in range(11):
            url = 'http://tugoleada.com/canal%s.php'%(i+1)
            title = 'CANAL %s'%(i+1)
            new.append((url,title, icon_path(info().icon)))

        return new
