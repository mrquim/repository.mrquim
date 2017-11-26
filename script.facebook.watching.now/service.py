# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import json


__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')

class Monitor(xbmc.Monitor):
    
    def __init__(self):
        xbmc.Monitor.__init__(self)
        self.nowPlaying = 0
        
    def onNotification(self, sender, method, data):
        data = json.loads(data)
        
        # reset nowPlaying item
        if 'Player.OnStop' in method:
            self.nowPlaying = 0
        
        # run script
        if (
            'true' in __addon__.getSetting('autoshow') and
            'Player.OnPlay' in method and
            data is not None and
            'item' in data and
            'id' in data['item'] and
            'type' in data['item'] and
            'movie' in data['item']['type'] and
            data['item']['id'] != self.nowPlaying
        ):
            
            id = data['item']['id']
            type = data['item']['type']
            self.nowPlaying = id
            xbmc.executebuiltin('XBMC.RunScript(' + __addon_id__ + ', ' + str(id) + ', ' + type + ')')
    
monitor = Monitor()

while(not xbmc.abortRequested):
    xbmc.sleep(100)