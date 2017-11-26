# -*- coding: utf-8 -*-

import xbmcaddon
import xbmcgui
import os

__addon__               = xbmcaddon.Addon()
__lang__                = __addon__.getLocalizedString

import debug
import function
import dialog

API_URL = 'https://graph.facebook.com'

class MENU:
    def start(self):
        
        ret = dialog.DIALOG().start('script-facebook-watching-now-menu.xml', labels={10030: __lang__(32115)}, buttons=[__lang__(32116), __lang__(32117), __lang__(32118)], list=10040)
        # add account
        if ret == 0:
            self.addAccount()
        
        # delete account
        if ret == 1:
            self.deleteAccount()
            
        # re auth account
        if ret == 2:
            self.reauthAccount()
            
    def addAccount(self):
        import auth
        token = auth.AUTH().start()
        if token is None:
            return
        
        data = function.readAccounts()
        
        # get user name and id
        ret = function.sendRequest(API_URL, '/me', get={'access_token': token})
        if ret is False or 'name' not in ret or 'id' not in ret:
            return
        
        if ret['id'] in data:
            debug.notify(__lang__(32119))
            return
            
        data[ret['id']] = { 'name': ret['name'], 'token': token }
        
        function.saveAccounts(data)
        debug.notify(__lang__(32120) + ' ' + ret['name'])
    
    
    def deleteAccount(self):
        data = function.readAccounts()
        
        if len(data) == 0:
            debug.notify(__lang__(32121))
            return
        
        id = []
        name = []
        for d in data:
            id.append(d)
            name.append(data[d]['name'])
        ret = dialog.DIALOG().start('script-facebook-watching-now-menu.xml', labels={10030: __lang__(32122)}, buttons=name, list=10040)
        if ret is None:
            return
        dial = xbmcgui.Dialog().yesno(__lang__(32123), __lang__(32124) + ' - ' + name[ret])
        if dial:
            del data[id[ret]]
            function.saveAccounts(data)
            debug.notify(__lang__(32125) + ' ' + name[ret] + ' ' + __lang__(32126))
        
    def reauthAccount(self):
        data = function.readAccounts()
        
        if len(data) == 0:
            debug.notify(__lang__(32127))
            return
        
        import auth
        token = auth.AUTH().start()
        if token is None:
            return
        
        # get user name and id
        ret = function.sendRequest(API_URL, '/me', get={'access_token': token})
        if ret is False or 'name' not in ret or 'id' not in ret:
            return
        
        if ret['id'] not in data:
            debug.notify(__lang__(32125) + ' ' + ret['name'] + ' ' + __lang__(32128))
            return
            
        data[ret['id']] = { 'name': ret['name'], 'token': token }
        
        function.saveAccounts(data)
        debug.notify(__lang__(32125) + ' ' + ret['name'] + ' ' + __lang__(32129))
            