from resources.lib.modules import client,webutils
import re,sys,xbmcgui
from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

class info():
    def __init__(self):
        self.mode = 'rojadirecta'
        self.name = 'Rojadirecta.me'
        self.icon = 'roja.jpg'
        self.categorized = False
        self.paginated = False
        self.multilink = True

class main():
    def __init__(self):
        self.base = addon.get_setting('roja_base')       

    def links(self,url):
        result = client.request(self.base)
        soup = webutils.bs(result)
        table = soup.find('span',{'class': url})
        links = table.findAll('tr')
        links.pop(0)
        links = self.__prepare_links(links)
        return links

    def events(self):
        import requests
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        result = requests.get(self.base, headers=headers).text
        reg = re.compile('<span class="(.+?)".+\s*.+<div class="menutitle".+?<span class="t">(.+?)</span>(.+?)</div>')
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
                url = event[0]
                title = event[2]
                title = re.sub('<span class="es">.*?</span>','',title).replace('<span class="en">','').replace('</span>','').replace('()','').replace('</time>','').replace('<span itemprop="name">','')
                sport,title = re.findall('(.*)<b>\s*(.*?)\s*</b>',title)[0]
                sport = sport.replace(':','')
                time = self.convert_time(event[1])
                title = '[COLOR orange](%s)[/COLOR] (%s) [B]%s[/B]'%(time,sport,title)
                title = title.encode('utf-8')
                new.append((url,title))
            except:
                pass
        
        return new

    def __prepare_links(self,links):
        new=[]
        precheck = addon.get_setting('link_precheck')
        if precheck=='true':
            pDialog = xbmcgui.DialogProgress()
            pDialog.create('Checking links', 'Checking links...')
        i=1
        items = len(links)
        for link in links:
            info = link.findAll('td')
            name = info[1].getText()
            lang = info[2].getText()
            service = info[3].getText()
            kbps = info[4].getText()
            url = self.base + '/' + info[5].find('a')['href']
            title = "%s (%s, %skbps) - %s"%(name, lang, kbps, service)
            found = True
            perc = 100*i/items
            if precheck=='true':
                import liveresolver
                if 'Acestream' not in service and 'Sopcast' not in service:
                    found = liveresolver.find_link(url)
                pDialog.update(perc, 'Checking:',name)
            if found:
                new.append((url,title))
            i+=1
            if (precheck=='true' and pDialog.iscanceled()): return new
        return new