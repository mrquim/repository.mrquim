# -*- coding: utf-8 -*-
#------------------------------------------------------------
# jami
#------------------------------------------------------------
# Licença: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Baseado no código do addon youtube
#------------------------------------------------------------

import xbmc, xbmcaddon, xbmcplugin, os, sys, plugintools
from addon.common.addon import Addon

addonID = 'plugin.video.jami'
addon   = Addon(addonID, sys.argv)
local   = xbmcaddon.Addon(id=addonID)
icon    = local.getAddonInfo('icon')
base    = 'plugin://plugin.video.youtube/'

fan01 = 'special://home/addons/plugin.video.jami/resources/fan01.jpg'
icon01 = 'special://home/addons/plugin.video.jami/resources/icon01.png'
icon02 = 'special://home/addons/plugin.video.jami/resources/icon02.png'
icon03 = 'special://home/addons/plugin.video.jami/resources/icon03.png'
icon04 = 'special://home/addons/plugin.video.jami/resources/icon04.png'
icon05 = 'special://home/addons/plugin.video.jami/resources/icon05.png'
icon06 = 'special://home/addons/plugin.video.jami/resources/icon06.png'
icon07 = 'special://home/addons/plugin.video.jami/resources/icon07.png'
icon08 = 'special://home/addons/plugin.video.jami/resources/icon08.png'
icon09 = 'special://home/addons/plugin.video.jami/resources/icon09.png'
icon10 = 'special://home/addons/plugin.video.jami/resources/icon10.png'
icon11 = 'special://home/addons/plugin.video.jami/resources/icon11.png'
icon12 = 'special://home/addons/plugin.video.jami/resources/icon12.png'
icon13 = 'special://home/addons/plugin.video.jami/resources/icon13.png'
icon14 = 'special://home/addons/plugin.video.jami/resources/icon14.png'
icon15 = 'special://home/addons/plugin.video.jami/resources/icon15.png'
icon16 = 'special://home/addons/plugin.video.jami/resources/icon16.png'
icon17 = 'special://home/addons/plugin.video.jami/resources/icon17.png'
icon18 = 'special://home/addons/plugin.video.jami/resources/icon18.png'
icon19 = 'special://home/addons/plugin.video.jami/resources/icon19.png'
icon20 = 'special://home/addons/plugin.video.jami/resources/icon20.png'
icon21 = 'special://home/addons/plugin.video.jami/resources/icon21.png'
icon22 = 'special://home/addons/plugin.video.jami/resources/icon22.png'
icon23 = 'special://home/addons/plugin.video.jami/resources/icon23.png'
icon24 = 'special://home/addons/plugin.video.jami/resources/icon24.png'
icon25 = 'special://home/addons/plugin.video.jami/resources/icon25.png'
icon26 = 'special://home/addons/plugin.video.jami/resources/icon26.png'


def run():
    plugintools.log("jami.run")
    params = plugintools.get_params()
    if params.get("action") is None: main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    plugintools.close_item_list()

def main_list(params):
	plugintools.log("jami ===> " + repr(params))
	plugintools.add_item(title = "[ Angry Birds ]", url = base + "playlist/PLVZggjiHl7zWTZDWcXNok7JFZUlb8vdHZ/", thumbnail = icon01, fanart = fan01, folder = True)
	plugintools.add_item(title = "Ruca - T01 a T24 [PT]", url = base + "playlist/PLsWbExGo1KPaYUuRSfzyF1X11Czip4259/", thumbnail = icon02, fanart = fan01, folder = True)
	plugintools.add_item(title = "Max - T01 a T05 [PT]", url = base + "playlist/PLsWbExGo1KPbil5fBWgJlv2gQPTcABI7x/", thumbnail = icon03, fanart = fan01, folder = True)
	plugintools.add_item(title = "PJ Masks [PT]", url = base + "playlist/PLsWbExGo1KPZM5dSa6L2uwYTbjpgjwNnf/", thumbnail = icon04, fanart = fan01, folder = True)
	plugintools.add_item(title = "Octonautas [PT]", url = base + "playlist/PLjRUOcyjSeAxv2ITxi2CVbNKUz-cK9YfA/", thumbnail = icon05, fanart = fan01, folder = True)
	plugintools.add_item(title = "Noddy [PT]", url = base + "playlist/PLrH5HKiu5jUeEVAVEctaHl1qud4zbYg5O/" , thumbnail = icon06, fanart = fan01, folder = True)	
	plugintools.add_item(title = "Pocoyo [PT]", url = base + "user/childrenvideos/", thumbnail = icon07, fanart = fan01, folder = True)
	plugintools.add_item(title = "Heidi 3D [PT]", url = base + "playlist/PLnp6B7ujCv2A8aaaa-6niKGW-SoChr88d/", thumbnail = icon08, fanart = fan01, folder = True)	
	plugintools.add_item(title = "Abelha Maia 3D [PT]", url = base + "playlist/PLTf5zA07OijMLjuAJGYQ_dT7s8fgo7kpN/", thumbnail = icon09, fanart = fan01, folder = True)
	plugintools.add_item(title = "Herois da Cidade [PT]", url = base + "playlist/PLFepGKlvmn74D95OwZkSSQR3uk4T2ReHD/", thumbnail = icon10, fanart = fan01, folder = True)
	plugintools.add_item(title = "Bob o Construtor [PT]", url = base + "playlist/PLrH5HKiu5jUd7KNHHylSmu_WvFZ1pyURq/", thumbnail = icon11, fanart = fan01, folder = True)
	plugintools.add_item(title = "Thomas e Amigos [PT]", url = base + "playlist/PLZ-7k3FZDGmm5XODLaqSXX98OME6gk6Um/", thumbnail = icon12, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Ovelha Choné - T01/T02 ]", url = base + "playlist/PLsWbExGo1KParAPrKtn8aQfLnEFepaajb/", thumbnail = icon13, fanart = fan01, folder = True)
	plugintools.add_item(title = "Vila Moleza [PT]", url = base + "playlist/PLrH5HKiu5jUeWGDGh3EYBvMQ-eU1CSy4J/", thumbnail = icon14, fanart = fan01, folder = True)
	plugintools.add_item(title = "Panda e os Caricas [PT]", url = base + "channel/UCvw-R-r3p6Hc-yj1qyoPslQ/", thumbnail = icon15, fanart = fan01, folder = True)
	plugintools.add_item(title = "Xana Toc Toc [PT]", url = base + "user/XanaTocTocVEVO/", thumbnail = icon16, fanart = fan01, folder = True)
	plugintools.add_item(title = "Violeta [Musicais]", url = base + "playlist/PLE308E8FD36F34EAC/", thumbnail = icon17, fanart = fan01, folder = True)
	plugintools.add_item(title = "Turma da Mónica [BR]", url = base + "playlist/PLWduEF1R_tVZYNTH8ajFOEDkDT_hfIQL9/", thumbnail = icon18, fanart = fan01, folder = True)
	plugintools.add_item(title = "Charlie Brown [BR]", url = base + "playlist/PLolevrZYo2eGlwPrvK1Nr_rwUGSpbJMYK/", thumbnail = icon19, fanart = fan01, folder = True)
	plugintools.add_item(title = "Masha e o Urso [BR]", url = base + "playlist/PLsWbExGo1KPYsGKNTnOemWCEdxRNHJyRm/", thumbnail = icon20, fanart = fan01, folder = True)
	plugintools.add_item(title = "Jelly Jamm [BR]"  , url = base + "playlist/PL-CfLd2XMlrw7Cq-LT4UMNJrzLr9OjMpk/", thumbnail = icon21, fanart = fan01, folder = True)
	plugintools.add_item(title = "Sonic X [BR]", url = base + "playlist/PLj0Fsa9q1GRCKN_i_-1zRTM0m9m-GW6E1/", thumbnail = icon22, fanart = fan01, folder = True)
	plugintools.add_item(title = "Tartarugas Ninja [PT]", url = base + "playlist/PL12TUMahWFQR6XqoHTKm5-RvCSYy1EPg1/", thumbnail = icon23, fanart = fan01, folder = True)
	plugintools.add_item(title = "Dartacão [PT]", url = base + "playlist/PLrH5HKiu5jUe8ZF8jwdtprpucMVEjRON5/", thumbnail = icon24, fanart = fan01, folder = True)
	plugintools.add_item(title = "Era uma vez o Homem [ 4 Temporadas ]", url = base + "playlist/PLsWbExGo1KPZRlqvLY2Ja_SAJZMgBcdxD/", thumbnail = icon25, fanart = fan01, folder = True)
	plugintools.add_item(title = "Contos Infantis [PT]", url = base + "channel/UCOre4lsfRMaC62bOHUjPp2Q/", thumbnail = icon26, fanart = fan01, folder = True)
	plugintools.add_item(title = "Fim da Lista", thumbnail = icon, fanart = fan01, folder = True)
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
run()
