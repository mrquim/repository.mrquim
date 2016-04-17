from _csv import Error
import select

__author__ = 'mark'

import xbmc
import xbmcaddon
import urllib
import time
import json



def callunblockr(key):
    try:

        response = urllib.urlopen(
            'http://manage.unblockr.net/api/unblockr-ip?_key=UnblockrIPResetUserKey&key=%s' % (key))
        if 200 != response.code:
            xbmc.executebuiltin( 'Notification(%s, %s, %d, %s)' % (__addonname__, "Failed (code:%d) to call Unblockr URL" % response.code, dialogtime, __icon__) )
        else:
            unblockrJSON = response.read();
            resp = json.loads(unblockrJSON)
            if resp['code']  < 0:
                raise Error(resp['msg'])

    except (IOError, Error) as E:
        errmsg = 'Unblockr IP Reset (%s)' % (E)
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, errmsg, dialogtime, __icon__))

__addon__ = xbmcaddon.Addon(id='script.service.unblockr')
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')

key = __addon__.getSetting('unblockr_key')
loop = __addon__.getSetting('sleep')
sleeptime = int(float(loop))

if (sleeptime < 60):
    sleeptime = 60
    __addon__.setSetting('sleep',str(60))

dialogtime = 2000
messageshown = 0
count = 0

while (not xbmc.abortRequested):
    loop = __addon__.getSetting('sleep')
    sleeptime = int(float(loop))
    key = __addon__.getSetting('unblockr_key')

    if (sleeptime < 60):
        sleeptime = 60
        __addon__.setSetting('sleep',str(60))

    if (key != "xyxyxy"):
        if count == 0 :
            if (messageshown == 0):
                line1 = "Unblockr IP reset IP every %d seconds" % sleeptime
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, line1, dialogtime, __icon__))
                messageshown = 1

            callunblockr(key)
        count = count + 1
        if count == sleeptime :
            count = 0

    time.sleep(1)
