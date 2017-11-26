# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import os
import json

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path'))
__lang__                = __addon__.getLocalizedString
__path__                = os.path.join(__addonpath__, 'resources', 'lib' )
__path_img__            = os.path.join(__addonpath__, 'resources', 'media' )

sys.path.append(__path__)

import debug
import function

API_URL = 'https://graph.facebook.com'
USER = 'me'
METHOD = 'kodiactions:watching_now'
PRIVACY = ['SELF', 'ALL_FRIENDS', 'FRIENDS_OF_FRIENDS', 'EVERYONE']

class WATCHING_NOW:
    def __init__(self):
        self.start()
        
    def start(self):
        # clear property for auto close menu
        xbmcgui.Window(10000).clearProperty(__addon_id__ + '_autoclose')
        
        # open sync dialog if no parameter
        if (len(sys.argv) == 0 or len(sys.argv[0]) == 0):
            import menu
            menu.MENU().start()
            return
        
        # get id and type from service
        try:
            id = sys.argv[1]
            type = sys.argv[2]
        except:
            return
            
        # get movie link
        import searchLink
        link = searchLink.LINK().start(id, type)
        debug.debug(str(link))
        if link is None:
            debug.notify(__lang__(32110))
            return
        
        # prepare users
        import dialog
        accounts = function.readAccounts()
        xbmcgui.Window(10000).setProperty(__addon_id__ + '_autoclose', '1' if 'true' in __addon__.getSetting('autoclose') else '0')
        for user in accounts.values():
            ret = dialog.DIALOG().start('script-facebook-watching-now-menu.xml', labels={10030: user['name']}, buttons=[__lang__(32100)], list=10040)
            if ret is not None:
                self.prepare(user, link)
        
    def prepare(self, user, link):
        token = user['token']
        # check token
        ret = function.sendRequest(API_URL, '/me', get={'access_token': token})
        if ret is False:
            debug.notify(__lang__(32111), True)
            import auth
            token = auth.AUTH().start()
            if token is None:
                debug.notify(__lang__(32112), True)
                return
        
        ret = self.sendAction(token, link)
        if ret is False:
            debug.notify(__lang__(32113), True)
        else:
            debug.notify(__lang__(32114))
        
    def sendAction(self, token, link):
        url = link[0]
        runtime = link[1]
        action = {
            'movie': url,
            'fb:explicitly_shared': 'true',
            'privacy': json.dumps({'value': PRIVACY[int(__addon__.getSetting('privacy'))]}),
            'expires_in': runtime
        }
        ret = function.sendRequest(API_URL, '/' + USER + '/' + METHOD, get={'access_token': token}, post=action)
        if ret is False:
            return False

# lock script to prevent duplicates
if (xbmcgui.Window(10000).getProperty(__addon_id__ + '_running') != 'True'):
    WATCHING_NOW()
    xbmcgui.Window(10000).clearProperty(__addon_id__ + '_running')
