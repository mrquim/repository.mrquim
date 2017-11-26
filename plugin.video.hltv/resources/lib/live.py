# -*- coding: utf-8 -*-

from common import *

class Live:

    def __init__(self, i):
        self.item = {}
        self.teams = re.findall('<span class="team-name">(.+?)</span>', i, re.DOTALL)
        self.name = re.search('<td class="placeholder-text-cell">(.+?)</td>', i, re.DOTALL)
        self.url = re.search('<a href="(.+?)"', i, re.DOTALL).group(1)
        self.info = re.search('<div class="event-name">(.+?)<', i, re.DOTALL)
        
        self.title = self.get_title()
        
        if self.title:
            self.update_item()
        
    def get_title(self):
        if self.teams:
            return utfenc('[COLOR red]LIVE[/COLOR] %s vs %s' % (self.teams[0].strip(), self.teams[1].strip()))
        elif self.name:
            return utfenc('[COLOR red]LIVE[/COLOR] {1}'.format(self.name.group(1)))
        else:
            return None
        
    def get_plot(self):
        if self.info:
            info = self.info.group(1).strip()
        else:
            info = ''
        return utfenc('%s\n%s' % (self.title, info))
        
    def update_item(self):
        self.item['mode'] = 'details'
        self.item['title'] = self.title
        self.item['id'] = self.url
        self.item['plot'] = self.get_plot()