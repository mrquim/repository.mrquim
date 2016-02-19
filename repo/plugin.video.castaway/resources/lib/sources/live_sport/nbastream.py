from resources.lib.modules import client,webutils
import re,sys
from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

class info():
    def __init__(self):
        self.mode = 'nbastream'
        self.name = 'nbastream.net'
        self.icon = 'nbastream.png'
        self.categorized = False
        self.paginated = False
        self.multilink = False

class main():
    def __init__(self):
        self.base = 'http://nbastream.net'
        self.html = client.request(self.base)


    def events(self):
        events = re.findall('<h3.+?>(.+?)</h3>(.*?)(?:<h3|<!-- Start Day|$)',self.html,re.DOTALL)
        events = self.__prepare_events(events)
        return events

    @staticmethod
    def convert_time(time):
        time = time.replace('<hr>','').replace('<br>','')
        try:
            li = time.split(':')
            hour,minute=li[0],li[1]
        except: return time.replace('PMET','').replace('AMET','')
        
        if 'PM' in minute:
            hour = int(hour) + 12
        if hour == 24:
            hour = 0

        minute = minute.replace('PMET','').replace('AMET','')
        import datetime
        from resources.lib.modules import pytzimp
        d = pytzimp.timezone(str(pytzimp.timezone('America/New_York'))).localize(datetime.datetime(2000 , 1, 1, hour=int(hour), minute=int(minute)))
        timezona= addon.get_setting('timezone_new')
        my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
        convertido=d.astimezone(my_location)
        fmt = "%H:%M"
        time=convertido.strftime(fmt)
        return time

    def __prepare_events(self,events):
        new = []
        for event in events:
            new.append(('x','[COLOR yellow]%s[/COLOR]'%event[0]))
            soup = webutils.bs(event[1])
            evs = soup.findAll('div',{'class':'custom-box'})
            hrefs = soup.findAll('a')
            i=0
            for ev in evs:
                time = self.convert_time(ev.find('div',{'class':'time'}).getText())
                url = 'http://nbastream.net/' + hrefs[i]['href']
                title = hrefs[i]['title'].replace('Live Stream','').strip()

                title = '[COLOR orange](%s)[/COLOR] [B]%s[/B]'%(time,title)
                new.append((url,title))
                i+=2

        return new

