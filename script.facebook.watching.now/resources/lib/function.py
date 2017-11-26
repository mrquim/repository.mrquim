# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcvfs
import urllib
import urllib2
import os
import json

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__datapath__            = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/') + '/'

import debug

DATA_FILE = 'data.json'

def sendRequest(url, method, get={}, post={}):
    if len(get) > 0:
        get = '?' + urllib.urlencode(get)
    else:
        get = ''
    
    if len(post) > 0:
        post = urllib.urlencode(post)
    else:
        post = None
    
    try:
        req = urllib2.Request(url + method + get, post)
        response = urllib2.urlopen(req)
        data = response.read()
        return json.loads(data)
    except Exception as error:
        debug.debug(str(error))
        return False
        
def readAccounts():
    if not xbmcvfs.exists(__datapath__) or not xbmcvfs.exists(__datapath__ + DATA_FILE):
        return {}
        
    f = xbmcvfs.File(__datapath__ + DATA_FILE)
    data = f.read()
    f.close()
    
    try:
        json_data = json.loads(data)
    except:
        return {}
    return json_data
    
def saveAccounts(data):
    if not xbmcvfs.exists(__datapath__):
        xbmcvfs.mkdirs(__datapath__)
        
    f = xbmcvfs.File(__datapath__ + DATA_FILE, 'w')
    result = f.write(json.dumps(data))
    f.close()
    