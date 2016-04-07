# -*- coding: utf-8 -*-
import datetime,xbmc,xbmcplugin,xbmcgui,xbmcaddon

class service:
	def __init__(self):
		while (not xbmc.abortRequested):
			if xbmcaddon.Addon().getSetting("series-library") == 'true':
				try:
					t1 = datetime.datetime.strptime(xbmcaddon.Addon().getSetting("series-last-update"), "%Y-%m-%d %H:%M:%S.%f")
					t2 = datetime.datetime.now()
					hoursList = [2, 5, 10, 15, 24]
					interval = int(xbmcaddon.Addon().getSetting("series-library-interval"))
					update = abs(t2 - t1) > datetime.timedelta(hours=hoursList[interval])
					if update is False: raise Exception()
					if not (xbmc.Player().isPlaying() or xbmc.getCondVisibility('Library.IsScanningVideo')):
						if xbmcaddon.Addon().getSetting("series-watchlist") == 'true': xbmc.executebuiltin('RunPlugin(plugin://plugin.video.ratotv/?mode=54&name=actualizarlib&url=ratotv.top)')
						xbmc.sleep(200)
						xbmc.executebuiltin('RunPlugin(plugin://plugin.video.ratotv/?mode=48&name=service&url=ratotv.top)')
						xbmcaddon.Addon().setSetting("series-last-update", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
				except:
					pass
			if xbmcaddon.Addon().getSetting("filmes-library") == 'true':
				try:
					t1 = datetime.datetime.strptime(xbmcaddon.Addon().getSetting("movies-last-update"), "%Y-%m-%d %H:%M:%S.%f")
					t2 = datetime.datetime.now()
					hoursList = [2, 5, 10, 15, 24]
					interval = int(xbmcaddon.Addon().getSetting("filmes-library-interval"))
					update = abs(t2 - t1) > datetime.timedelta(hours=hoursList[interval])
					if update is False: raise Exception()
					if not (xbmc.Player().isPlaying() or xbmc.getCondVisibility('Library.IsScanningVideo')):
						if xbmcaddon.Addon().getSetting("filmes-watchlist") == 'true': 
							xbmc.executebuiltin('RunPlugin(plugin://plugin.video.ratotv/?mode=53&name=ratotv&url=ratotv.top)')
							xbmc.sleep(200)
							xbmc.executebuiltin("XBMC.UpdateLibrary(video,"+os.path.join(selfAddon.getSetting('libraryfolder'),'movies')+")")
						xbmc.sleep(200)
						if xbmcaddon.Addon().getSetting("filmes-service") == '0' or xbmcaddon.Addon().getSetting("filmes-service") == '1':
							xbmc.executebuiltin('RunPlugin(plugin://plugin.video.ratotv/?mode=47&name=novos&url=ratotv.top)')
						xbmcaddon.Addon().setSetting('movies-last-update', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
				except:
					pass
			xbmc.sleep(1000)

service()