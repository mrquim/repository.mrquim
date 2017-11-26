# -*- coding: utf-8 -*-

from common import *

class Upcoming:

    def __init__(self, i):
        self.item = {}
        unixtime = re.search('data-unix="(.+?)"', i).group(1)[:10]
        self.date = date(unixtime)
        self.teams = re.findall('<div class="team">(.+?)</div>', i, re.DOTALL)
        self.name = re.search('<td class="placeholder-text-cell">(.+?)</td>', i, re.DOTALL)
        self.url = re.search('<a href="(.+?)"', i, re.DOTALL).group(1)
        self.info = re.search('<span class="event-name">(.+?)<', i, re.DOTALL)
        
        self.title = self.get_title()
        
        if self.title:
            self.update_item()
        
    def get_title(self):
        if self.teams:
            return utfenc('%s %s vs %s' % (self.date, self.teams[0].strip(), self.teams[1].strip()))
        elif self.name:
            return utfenc('{0} {1}'.format(self.date, self.name.group(1)))
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