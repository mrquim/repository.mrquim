# -*- coding: utf-8 -*-

import os,sys,urllib,urlparse
import time,datetime,random,re
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import HTMLParser

addon_handle = int(sys.argv[1])
addon = xbmcaddon.Addon()
dialog = xbmcgui.Dialog()
addon_id = addon.getAddonInfo('id')
addon_name  = addon.getAddonInfo('name')
version = addon.getAddonInfo('version')
icon = addon.getAddonInfo('icon')
fanart = addon.getAddonInfo('fanart')
content = addon.getSetting('content')
view_id = addon.getSetting('view_id')
force_view = addon.getSetting('force_view') == 'true'
language = addon.getSetting('language')

base_hltv = 'http://hltv.org'

def log(msg):
    xbmc.log(str(msg), xbmc.LOGNOTICE)
    
def getString(_id):
    return addon.getLocalizedString(_id)

def build_url(query):
    return sys.argv[0] + '?' + urllib.urlencode(query)
    
def utfenc(string):
    try:
        string = string.encode('utf-8')
    except:
        pass
    return string

def html_unescape(html):
    try:
        html = HTMLParser.HTMLParser().unescape(html)
    except:
        pass
    return html

def timedelta_total_seconds(timedelta):
    return (
        timedelta.microseconds + 0.0 +
        (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6

def date(timestamp):
    value = datetime.datetime.fromtimestamp(int(timestamp))
    return value.strftime('%Y-%m-%d %H:%M')