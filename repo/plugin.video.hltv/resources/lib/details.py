# -*- coding: utf-8 -*-

from common import *

class Details:

    def __init__(self, i):
        self.item = {}
        self.language = re.search('title="(.+?)"', i, re.DOTALL)
        self.name = re.search('title=".+?">(.+?)<', i, re.DOTALL)
        self.highlight = re.search('highlight.+?>(.+?)$', i, re.DOTALL)
        self.stream = re.search('data-.+?-embed="(.+?)"', i, re.DOTALL)
        self.viewers = re.search('class="viewers.+?">(\d+)<', i, re.DOTALL)
        
        if self.stream and (self.name or self.highlight):
            self.update_item()
            
    def get_title(self):
        if self.highlight:
            return utfenc(self.highlight.group(1))
        else:
            views = ''
            if self.viewers:
                views = self.viewers.group(1)
            name = re.sub('<.+?>', '', self.name.group(1))
            return utfenc('%s (%s) %s' % (name, self.language.group(1), views))
        
    def update_item(self):
        self.item['mode'] = 'play'
        self.item['title'] = self.get_title()
        self.item['id'] = self.stream.group(1)
        self.item['plot'] = self.get_title()