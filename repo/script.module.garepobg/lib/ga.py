#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import requests
import string
import random

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

class ga():
  def __init__ (self, tid = 'UA-61449088-3'):
    self.__addon = xbmcaddon.Addon('script.module.garepobg')
    self.__payload = {
        'v': '1',
        'tid': tid,
      }
    self.__url = 'http://www.google-analytics.com/collect?payload_data'
    if self.__addon.getSetting("firstrun") == "true":
      self.__addon.setSetting("firstrun", "false")
      self.__addon.setSetting("uid", self.__rnd_gen(size=32))

  def __get_platform(self):
    platforms = {
      "Linux": "X11; Linux",
      "Windows": "Windows NT %d.%d",
      "OSX": "Macintosh; Intel Mac OS X",
      "IOS": "iPad; CPU OS 6_1 like Mac OS X",
      "android": "Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K"
      }

    for platform, ua_platform_name in platforms.items():
      if xbmc.getCondVisibility("System.Platform.%s" % platform):
        if platform == "Windows":
          import sys
          version = sys.getwindowsversion()
          ua_platform_name %= (version[0], version[1])
        return ua_platform_name

  def __mkua(self):
     return "KODI/%s (%s)" % (xbmc.getInfoLabel("System.BuildVersion").split(" ")[0], self.__get_platform())

  def __rnd_gen(self, size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

  def __except_report(self, e):
    import traceback
    l = '%s-' % e[0]
    for file, line, func, text in traceback.extract_tb(e[2]):
      l += '%d %s:' % (line, os.path.split(file)[1])
    return l[:150]

  def update(self, data, crash):
    ret = None
    data.update(self.__payload)
    data['z'] = self.__rnd_gen()
    data['t'] = 'event'
    data['ua'] = self.__mkua()
    data['cid'] = self.__addon.getSetting('uid')
    data['uid'] = self.__addon.getSetting('uid')
    data['aiid'] = u'-'.join([xbmc.getInfoLabel('System.FriendlyName').split()[0], xbmc.getInfoLabel('System.BuildVersion')])

    if crash is not None:
      data['t'] = 'exception'
      data['exd'] = self.__except_report(crash)
      data['exf'] = '1'

    if self.__addon.getSetting('dbg') == 'true':
      xbmc.log((u">>> %s -> %s <<<" % (self.__addon.getAddonInfo('name'), data,)).encode('utf-8'),level=xbmc.LOGNOTICE)

    if self.__addon.getSetting('ga') != 'true':
      return ret

    try:
      ret = requests.post(self.__url, data=data)
    except:
      pass

    return ret
