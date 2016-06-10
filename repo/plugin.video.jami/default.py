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

fan01 = 'special://home/addons/plugin.video.jami/resources/fan01.png'
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
icon27 = 'special://home/addons/plugin.video.jami/resources/icon27.png'
icon28 = 'special://home/addons/plugin.video.jami/resources/icon28.png'
icon29 = 'special://home/addons/plugin.video.jami/resources/icon29.png'
icon30 = 'special://home/addons/plugin.video.jami/resources/icon30.png'
icon31 = 'special://home/addons/plugin.video.jami/resources/icon31.png'
icon32 = 'special://home/addons/plugin.video.jami/resources/icon32.png'
icon33 = 'special://home/addons/plugin.video.jami/resources/icon33.png'
icon34 = 'special://home/addons/plugin.video.jami/resources/icon34.png'
icon35 = 'special://home/addons/plugin.video.jami/resources/icon35.png'

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
	plugintools.add_item(title = "O mundo maravilhoso dos Animais", url = base + "playlist/PLsWbExGo1KPappAs8nPxrqDgrntNy9Sto/", thumbnail = icon01, fanart = fan01, folder = True)
	plugintools.add_item(title = "Banana Cartoon [PT]", url = base + "channel/UCPeLZYqHrQdV4xdZ2Lj3Reg/", thumbnail = icon02, fanart = fan01, folder = True)
	plugintools.add_item(title = "Angry Birds [PT]", url = base + "playlist/PLsWbExGo1KPbiUa9ZPIy1q7oUhsJq6uPT/", thumbnail = icon03, fanart = fan01, folder = True)
	plugintools.add_item(title = "Ruca - T01 a T24 [PT]", url = base + "playlist/PLsWbExGo1KPaYUuRSfzyF1X11Czip4259/", thumbnail = icon04, fanart = fan01, folder = True)
	plugintools.add_item(title = "Max - T01 a T05 [PT]", url = base + "playlist/PLsWbExGo1KPbil5fBWgJlv2gQPTcABI7x/", thumbnail = icon05, fanart = fan01, folder = True)
	plugintools.add_item(title = "Octonautas [PT]", url = base + "playlist/PLsWbExGo1KPazbyjJE2UwlXn5rYZMDVoh/", thumbnail = icon06, fanart = fan01, folder = True)
	plugintools.add_item(title = "Noddy [PT]", url = base + "playlist/PLsWbExGo1KPZTiUyNEHtkbN2atTuAoQHL/", thumbnail = icon07, fanart = fan01, folder = True)	
	plugintools.add_item(title = "Pocoyo [PT]", url = base + "user/childrenvideos/", thumbnail = icon08, fanart = fan01, folder = True)
	plugintools.add_item(title = "Heidi 3D [PT]", url = base + "playlist/PLsWbExGo1KPZKVQoMG3-ikbIIyU5_AsvY/", thumbnail = icon09, fanart = fan01, folder = True)	
	plugintools.add_item(title = "Abelha Maia 3D [PT]", url = base + "playlist/PLsWbExGo1KPaQx2dXjba2q29_teZBeEfm/", thumbnail = icon10, fanart = fan01, folder = True)
	plugintools.add_item(title = "Herois da Cidade [PT]", url = base + "playlist/PLFepGKlvmn74D95OwZkSSQR3uk4T2ReHD/", thumbnail = icon11, fanart = fan01, folder = True)
	plugintools.add_item(title = "Bob o Construtor [PT]", url = base + "playlist/PLsWbExGo1KPZITh_DyO7ye-UVdMfAQXfh/", thumbnail = icon12, fanart = fan01, folder = True)
	plugintools.add_item(title = "Thomas e Amigos [PT]", url = base + "playlist/PLsWbExGo1KPb3PoKuk3chB4460GEKgqjP/", thumbnail = icon13, fanart = fan01, folder = True)
	plugintools.add_item(title = "Ovelha Choné [PT]", url = base + "playlist/PLsWbExGo1KParAPrKtn8aQfLnEFepaajb/", thumbnail = icon14, fanart = fan01, folder = True)
	plugintools.add_item(title = "Vila Moleza [PT]", url = base + "playlist/PLsWbExGo1KPaYskF8yclTCPUNCvvNP35E/", thumbnail = icon15, fanart = fan01, folder = True)
	plugintools.add_item(title = "Panda [PT]", url = base + "playlist/PLsWbExGo1KPaOQDuO_oLgY-ar_AzpF3c5/", thumbnail = icon16, fanart = fan01, folder = True)
	plugintools.add_item(title = "Hello Kitty [PT]", url = base + "playlist/PLsWbExGo1KPZxKeoOmZQNe-UpKotBwcbt/", thumbnail = icon17, fanart = fan01, folder = True)
	plugintools.add_item(title = "Xana Toc Toc [PT]", url = base + "playlist/PLsWbExGo1KPYu3w9mnbqvlPQMaTVEixF7/", thumbnail = icon18, fanart = fan01, folder = True)
	plugintools.add_item(title = "Violetta [Musicais]", url = base + "playlist/PLsWbExGo1KPZW1aCXP-Z5FZW9ZfTOfeTY/", thumbnail = icon19, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Bernard Bear ]", url = base + "playlist/PLsWbExGo1KPaloN_t_O2t1yHz_8uCBTVj/", thumbnail = icon20, fanart = fan01, folder = True)
	plugintools.add_item(title = "Chaves - T01 a T05 [BR]", url = base + "playlist/PLsWbExGo1KPYzBmOG6XPDby_xI3hVbXxm/", thumbnail = icon21, fanart = fan01, folder = True)
	plugintools.add_item(title = "Charlie Brown [BR]", url = base + "playlist/PLsWbExGo1KPYzN1D-Dce-zBTH8GzS2QAl/", thumbnail = icon22, fanart = fan01, folder = True)
	plugintools.add_item(title = "Daniel Tigre [BR]", url = base + "playlist/PLoaBAxtZve6nmFuNHCmIRLz_bo2aCD4wX/", thumbnail = icon23, fanart = fan01, folder = True)
	plugintools.add_item(title = "Masha e o Urso [BR]", url = base + "playlist/PLsWbExGo1KPYsGKNTnOemWCEdxRNHJyRm/", thumbnail = icon24, fanart = fan01, folder = True)
	plugintools.add_item(title = "Jelly Jamm [BR]", url = base + "playlist/PLsWbExGo1KPbgMZ7xHfz22oOLjT7TisY0/", thumbnail = icon25, fanart = fan01, folder = True)
	plugintools.add_item(title = "Turma da Mónica [BR]", url = base + "playlist/PLsWbExGo1KPb3_KkJ3ekYws_Rivr-4x93/", thumbnail = icon26, fanart = fan01, folder = True)
	plugintools.add_item(title = "Sonic X [BR]", url = base + "playlist/PLsWbExGo1KPY408CLKjPa1hko7rtTovFw/", thumbnail = icon27, fanart = fan01, folder = True)
	plugintools.add_item(title = "Sonic Boom [BR]", url = base + "playlist/PLsWbExGo1KPbeaWxsnpmRJOKABA6-DyN9/", thumbnail = icon28, fanart = fan01, folder = True)
	plugintools.add_item(title = "Team Hot Wheels [BR]", url = base + "playlist/PLsWbExGo1KPb-TTwpvyEDIZa51JUYLr9l/", thumbnail = icon29, fanart = fan01, folder = True)
	plugintools.add_item(title = "Tartarugas Ninja [PT]", url = base + "playlist/PLsWbExGo1KPZpo076XQwp5nzVco5ZRUcN/", thumbnail = icon30, fanart = fan01, folder = True)
	plugintools.add_item(title = "Irmãos Grimm [PT]", url = base + "playlist/PLaerdHbAdrDIIi3LuIIdCRGdFoHe3lS_D/", thumbnail = icon31, fanart = fan01, folder = True)
	plugintools.add_item(title = "Dartacão [PT]", url = base + "playlist/PLsWbExGo1KPb3QuNAHUoBDBGdA981SDjP/", thumbnail = icon32, fanart = fan01, folder = True)
	plugintools.add_item(title = "Tom Sawyer [PT]", url = base + "playlist/PLsWbExGo1KPbgxDBmh-wn0zIzJY8kiqSY/", thumbnail = icon33, fanart = fan01, folder = True)
	plugintools.add_item(title = "Rua Sésamo [PT]", url = base + "playlist/PLsWbExGo1KPZMSjszQz49Let2KEsNptif/", thumbnail = icon34, fanart = fan01, folder = True)
	plugintools.add_item(title = "Era uma vez - 4 Temporadas [PT]", url = base + "playlist/PLsWbExGo1KPZRlqvLY2Ja_SAJZMgBcdxD/", thumbnail = icon35, fanart = fan01, folder = True)
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
run()
