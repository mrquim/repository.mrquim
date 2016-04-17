__author__ = 'mark'

import xbmcaddon
import xbmcgui
import urllib
import time
import json

import socket;

# USeful resources
# Look up
# http://kodi.wiki/view/InfoLabels

# {
#     "YourFuckingIPAddress": "109.151.51.156",
#     "YourFuckingLocation": "Cambridge, C3, United Kingdom",
#     "YourFuckingHostname": "host109-151-51-156.range109-151.btcentralplus.com",
#     "YourFuckingISP": "BT"
# }


# def getExternalIPInfo():
#     try:
#         response = urllib.urlopen(
#             'http://wtfismyip.com/json')
#         # 'http://manage.unblockr.net/api/unblockr-ip?_key=UnblockrIPResetUserKey&key=%s' % (key))
#         if 200 != response.code:
#             xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (
#             __addonname__, "Failed (code:%d) to call wtfismyip.com" % response.code, dialogtime, __icon__))
#         else:
#             unblockrJSON = response.read();
#             resp = json.loads(unblockrJSON)
#             ipAddress = resp['YourFuckingIPAddress']
#
#     except (IOError, Error) as E:
#         errmsg = 'Calling wtfismyip.com (%s)' % (E)
#         xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, errmsg, dialogtime, __icon__))
#
#     return ipAddress;


def getInternalIP():
    return xbmc.getInfoLabel('Network.IPAddress')


def getGatewayIP():
    return xbmc.getInfoLabel('Network.GatewayAddress');


def getDNS1IP():
    return xbmc.getInfoLabel('Network.DNS1Address');


def getDNS2IP():
    return xbmc.getInfoLabel('Network.DNS2Address');


__addon__ = xbmcaddon.Addon(id='script.service.unblockr')
__addonname__ = __addon__.getAddonInfo('name')
line1 = "Welcome to Unblockr";
line2 = "Internal IP:%s   GatewayIP:%s" % (getInternalIP(), getGatewayIP());
line3 = "Current DNS: %s,  %s" % (getDNS1IP(), getDNS2IP());

xbmcgui.Dialog().ok(__addonname__, line1, line2, line3);

__addon__.openSettings();
