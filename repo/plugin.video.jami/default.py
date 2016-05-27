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
icon01 = 'special://home/addons/plugin.video.jami/resources/icon01.jpg'
icon02 = 'special://home/addons/plugin.video.jami/resources/icon02.jpg'
icon03 = 'special://home/addons/plugin.video.jami/resources/icon03.jpg'
icon04 = 'special://home/addons/plugin.video.jami/resources/icon04.jpg'
icon05 = 'special://home/addons/plugin.video.jami/resources/icon05.jpg'
icon06 = 'special://home/addons/plugin.video.jami/resources/icon06.jpg'
icon07 = 'special://home/addons/plugin.video.jami/resources/icon07.jpg'
icon08 = 'special://home/addons/plugin.video.jami/resources/icon08.jpg'
icon09 = 'special://home/addons/plugin.video.jami/resources/icon09.jpg'
icon10 = 'special://home/addons/plugin.video.jami/resources/icon10.jpg'
icon11 = 'special://home/addons/plugin.video.jami/resources/icon11.jpg'
icon12 = 'special://home/addons/plugin.video.jami/resources/icon12.jpg'
icon13 = 'special://home/addons/plugin.video.jami/resources/icon13.jpg'
icon14 = 'special://home/addons/plugin.video.jami/resources/icon14.jpg'
icon15 = 'special://home/addons/plugin.video.jami/resources/icon15.jpg'
icon16 = 'special://home/addons/plugin.video.jami/resources/icon16.jpg'
icon17 = 'special://home/addons/plugin.video.jami/resources/icon17.jpg'
icon17a = 'special://home/addons/plugin.video.jami/resources/icon17a.jpg'
icon18 = 'special://home/addons/plugin.video.jami/resources/icon18.jpg'
icon19 = 'special://home/addons/plugin.video.jami/resources/icon19.jpg'
icon20 = 'special://home/addons/plugin.video.jami/resources/icon20.jpg'
icon21 = 'special://home/addons/plugin.video.jami/resources/icon21.jpg'
icon22 = 'special://home/addons/plugin.video.jami/resources/icon22.jpg'
icon23 = 'special://home/addons/plugin.video.jami/resources/icon23.jpg'
icon24 = 'special://home/addons/plugin.video.jami/resources/icon24.jpg'
icon25 = 'special://home/addons/plugin.video.jami/resources/icon25.jpg'
icon26 = 'special://home/addons/plugin.video.jami/resources/icon26.jpg'
icon27 = 'special://home/addons/plugin.video.jami/resources/icon27.jpg'
icon28 = 'special://home/addons/plugin.video.jami/resources/icon28.jpg'
icon29 = 'special://home/addons/plugin.video.jami/resources/icon29.jpg'
icon30 = 'special://home/addons/plugin.video.jami/resources/icon30.jpg'


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
	plugintools.add_item(title = "Octonautas [PT]", url = base + "playlist/PLjRUOcyjSeAxv2ITxi2CVbNKUz-cK9YfA/", thumbnail = icon04, fanart = fan01, folder = True)
	plugintools.add_item(title = "Noddy [PT]", url = base + "playlist/PLrH5HKiu5jUeEVAVEctaHl1qud4zbYg5O/" , thumbnail = icon05, fanart = fan01, folder = True)	
	plugintools.add_item(title = "Pocoyo [PT]", url = base + "user/childrenvideos/", thumbnail = icon06, fanart = fan01, folder = True)
	plugintools.add_item(title = "Heidi 3D [PT]", url = base + "playlist/PLnp6B7ujCv2A8aaaa-6niKGW-SoChr88d/", thumbnail = icon07, fanart = fan01, folder = True)	
	plugintools.add_item(title = "Abelha Maia 3D [PT]", url = base + "playlist/PLTf5zA07OijMLjuAJGYQ_dT7s8fgo7kpN/", thumbnail = icon08, fanart = fan01, folder = True)
	plugintools.add_item(title = "Herois da Cidade [PT]", url = base + "playlist/PLFepGKlvmn74D95OwZkSSQR3uk4T2ReHD/", thumbnail = icon09, fanart = fan01, folder = True)
	plugintools.add_item(title = "Bob o Construtor [PT]", url = base + "playlist/PLrH5HKiu5jUd7KNHHylSmu_WvFZ1pyURq/", thumbnail = icon10, fanart = fan01, folder = True)
	plugintools.add_item(title = "Thomas e Amigos [PT]", url = base + "playlist/PLZ-7k3FZDGmm5XODLaqSXX98OME6gk6Um/", thumbnail = icon11, fanart = fan01, folder = True)
	plugintools.add_item(title = "Ovelha Choné [PT]", url = base + "playlist/PLsWbExGo1KParAPrKtn8aQfLnEFepaajb/", thumbnail = icon12, fanart = fan01, folder = True)
	plugintools.add_item(title = "Vila Moleza [PT]", url = base + "playlist/PLrH5HKiu5jUeWGDGh3EYBvMQ-eU1CSy4J/", thumbnail = icon13, fanart = fan01, folder = True)
	plugintools.add_item(title = "Panda e os Caricas [PT]", url = base + "channel/UCvw-R-r3p6Hc-yj1qyoPslQ/", thumbnail = icon14, fanart = fan01, folder = True)
	plugintools.add_item(title = "Hello Kitty [PT]", url = base + "playlist/PLsWbExGo1KPZxKeoOmZQNe-UpKotBwcbt/", thumbnail = icon15, fanart = fan01, folder = True)
	plugintools.add_item(title = "Xana Toc Toc [PT]", url = base + "user/XanaTocTocVEVO/", thumbnail = icon16, fanart = fan01, folder = True)
	plugintools.add_item(title = "Violetta [Musicais]", url = base + "playlist/PLE308E8FD36F34EAC/", thumbnail = icon17, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Bernard Bear ]", url = base + "playlist/PLsWbExGo1KPaloN_t_O2t1yHz_8uCBTVj/", thumbnail = icon17a, fanart = fan01, folder = True)
	plugintools.add_item(title = "Chaves - T01 a T05 [BR]", url = base + "playlist/PLsWbExGo1KPYzBmOG6XPDby_xI3hVbXxm/", thumbnail = icon18, fanart = fan01, folder = True)
	plugintools.add_item(title = "Charlie Brown [BR]", url = base + "playlist/PLolevrZYo2eGlwPrvK1Nr_rwUGSpbJMYK/", thumbnail = icon19, fanart = fan01, folder = True)
	plugintools.add_item(title = "Daniel Tigre [BR]", url = base + "playlist/PLoaBAxtZve6nmFuNHCmIRLz_bo2aCD4wX/", thumbnail = icon20, fanart = fan01, folder = True)
	plugintools.add_item(title = "Masha e o Urso [BR]", url = base + "playlist/PLsWbExGo1KPYsGKNTnOemWCEdxRNHJyRm/", thumbnail = icon21, fanart = fan01, folder = True)
	plugintools.add_item(title = "Jelly Jamm [BR]"  , url = base + "playlist/PL-CfLd2XMlrw7Cq-LT4UMNJrzLr9OjMpk/", thumbnail = icon22, fanart = fan01, folder = True)
	plugintools.add_item(title = "Turma da Mónica [BR]", url = base + "playlist/PLWduEF1R_tVZYNTH8ajFOEDkDT_hfIQL9/", thumbnail = icon23, fanart = fan01, folder = True)
	plugintools.add_item(title = "Sonic X [BR]", url = base + "playlist/PLj0Fsa9q1GRCKN_i_-1zRTM0m9m-GW6E1/", thumbnail = icon24, fanart = fan01, folder = True)
	plugintools.add_item(title = "Team Hot Wheels [BR]", url = base + "playlist/PLsWbExGo1KPb-TTwpvyEDIZa51JUYLr9l/", thumbnail = icon25, fanart = fan01, folder = True)
	plugintools.add_item(title = "Tartarugas Ninja [PT]", url = base + "playlist/PL12TUMahWFQR6XqoHTKm5-RvCSYy1EPg1/", thumbnail = icon26, fanart = fan01, folder = True)
	plugintools.add_item(title = "Irmãos Grimm [PT]", url = base + "playlist/PLaerdHbAdrDIIi3LuIIdCRGdFoHe3lS_D/", thumbnail = icon27, fanart = fan01, folder = True)
	plugintools.add_item(title = "Dartacão [PT]", url = base + "playlist/PLrH5HKiu5jUe8ZF8jwdtprpucMVEjRON5/", thumbnail = icon28, fanart = fan01, folder = True)
	plugintools.add_item(title = "Era uma vez - 4 Temporadas [PT]", url = base + "playlist/PLsWbExGo1KPZRlqvLY2Ja_SAJZMgBcdxD/", thumbnail = icon29, fanart = fan01, folder = True)
	plugintools.add_item(title = "Contos Infantis [PT]", url = base + "channel/UCOre4lsfRMaC62bOHUjPp2Q/", thumbnail = icon30, fanart = fan01, folder = True)
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
run()
