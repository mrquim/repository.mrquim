# -*- coding: utf-8 -*-

import xbmcaddon
import xbmcgui
import os
import urllib
import urllib2
import json
import random
import string
import time

__addon__               = xbmcaddon.Addon()
__lang__                = __addon__.getLocalizedString

import debug
import function

RETRY_TIME = 5
COUNT_RETRY = 50
AUTH_URL = 'http://auth-kodi.tk'

class AUTH:
    def start(self):
        self.bar = xbmcgui.DialogProgress()
        self.bar.create(__lang__(32130), __lang__(32131) + '...')
        
        # generate random key
        key = self.generateKEY()
        
        # init auth with random key
        ret = function.sendRequest(AUTH_URL, '', get={'option': 'init', 'key': key})
        if ret is False or 'init' not in ret or 'ok' not in ret['init']:
            self.bar.close()
            debug.notify(__lang__(32132), True)
            return None
            
        # wait for authenticate
        self.bar.update(25, __lang__(32133), __lang__(32134) + ' ' + AUTH_URL + ' ' + __lang__(32135) + ' ' + key, __lang__(32136) + '...')
        token = self.checkForResponse(key)
        if token is None:
            debug.notify(__lang__(32137), True)
        self.bar.close()
        return token
    
    def generateKEY(self):
        key = ''
        for i in range(8):
            key = key + random.SystemRandom().choice(string.ascii_uppercase + string.digits)
            if i == 3:
                key = key + '-'
        return key
    
    def checkForResponse(self, key):
        for i in range(COUNT_RETRY):
            if (self.bar.iscanceled()):
                return None
            
            ret = function.sendRequest(AUTH_URL, '', get={'option': 'auth', 'key': key})
            if ret is not False and key in ret and len(ret[key]) > 0:
                return ret[key]
            time.sleep(RETRY_TIME)
        return None
    