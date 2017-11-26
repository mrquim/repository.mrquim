# -*- coding: utf-8 -*-

from common import *
from items import Items

items = Items()
        
def home_items(data):
    from live import Live
    from upcoming import Upcoming
    home = [
        {
            'mode':'archive',
            'title':'Archive',
            'plot':'CS:GO match archive, complete with all CS:GO pro matches.'
        },
    ]
    for i in home:
        items.add_item(i)
    live = re.findall('<div class="live-matches">(.*?)<div class="section-spacer">', data, re.DOTALL)
    if live:
        for l in re.findall('<div class="live-match">(.*?)</table>', live[0], re.DOTALL):
            items.add_item(Live(html_unescape(l)).item)
    upcoming = re.findall('<div class="upcoming-matches">(.*?)<div class="results">', data, re.DOTALL)
    if upcoming:
        for u in re.findall('(<a href=".*?)</table>', upcoming[0], re.DOTALL):
            items.add_item(Upcoming(html_unescape(u)).item)
    items.list_items()
    
def archive_items(data):
    from archive import Archive
    results = re.findall('<div class="results-all"(.*?)<div class="results">', data, re.DOTALL)
    if results:
        for r in re.findall('<div class="result-con"(.*?)</table>', results[0], re.DOTALL):
            items.add_item(Archive(html_unescape(r)).item)
    items.list_items()
    
def details_items(data):
    from details import Details
    for each_stream in re.findall('<div class="stream-box\s*"(.*?)</div>', data, re.DOTALL):
        items.add_item(Details(html_unescape(each_stream)).item)
    for each_highlight in re.findall('<div class="highlight\s*(.*?)</div>', data, re.DOTALL):
        items.add_item(Details(html_unescape(each_highlight)).item)
    items.list_items()

def play(url):
    from resolver import Resolver
    r = Resolver(url)
    items.play_item(r.resolved_url)
    if r.seektime:
        items.seek_item(r.seektime)