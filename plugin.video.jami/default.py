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

icon01 = 'https://scontent.cdninstagram.com/t51.2885-19/s150x150/12965714_546124852233591_2033050455_a.jpg'
icon02 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/1/6/8/0602537176861.jpg'
icon03 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/6/8/6/0602527851686.jpg'
icon04 = 'http://vignette3.wikia.nocookie.net/pocoyoworld/images/2/2f/Pocoyo-Image-300x300_Pato_Elly_Loula_Sleepy_Bird.jpg/revision/latest?cb=20140101011604'
icon05 = 'http://www.leyaonline.com/fotos/produtos/500_9789892308722_noddy_joga_as_escondidas.jpg'
icon06 = 'http://lh6.ggpht.com/U2HRHrr3p0Y0s-2L0rOtDArAOMs3IDm0P1DWRD19DWPjsCZoRQFFhxdmPIUK07v6mVee=w300'
icon07 = 'https://pbs.twimg.com/profile_images/608590304514441216/BS7MfUjz_400x400.jpg'
icon08 = 'https://patrick44.files.wordpress.com/2012/01/patrickschultzcollage21.jpg'
icon09 = 'http://videosinfantis.pt/wp-content/uploads/2013/09/Ruca_5.jpg'
icon10 = 'http://vignette4.wikia.nocookie.net/doblaje/images/a/aa/Jelly_Jamm.jpg/revision/latest?cb=20120728140403&path-prefix=es'
icon11 = 'http://www.difundir.com.br/fotos/01942_49240p3.jpg'
icon12 = 'http://www.childrens-rooms.co.uk/childrensrooms-web/v2/images/products/viewproduct_popup/5281.jpg'

def run():
    plugintools.log("jami.run")
    
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

def main_list(params):
		plugintools.log("jami ===> " + repr(params))

		plugintools.add_item(title = "Mundo Animado [PT]"            , url = base + "channel/UCOre4lsfRMaC62bOHUjPp2Q/"                   , thumbnail = icon01, folder = True)
		plugintools.add_item(title = "Canal Panda [PT]"                   , url = base + "channel/UCvw-R-r3p6Hc-yj1qyoPslQ/", thumbnail = icon02, folder = True)
		plugintools.add_item(title = "Xana Toc Toc [PT]"                          , url = base + "user/XanaTocTocVEVO/"                , thumbnail = icon03, folder = True)	

		plugintools.add_item(title = "Pocoyo [PT]"                       , url = base + "user/childrenvideos/", thumbnail = icon04, folder = True)	

                plugintools.add_item(title = "Noddy [PT]"                    , url = base + "channel/UCbJ3FpU6NZ4T4Ca_BxXtaGA/"               , thumbnail = icon05, folder = True)	
              
		plugintools.add_item(title = "Herois da Cidade [PT]"                    , url = base + "channel/UCnfjtca0KeZND5e27IO4INg/"           , thumbnail = icon06, folder = True)	

		plugintools.add_item(title = "Disney [PT]"                            , url = base + "channel/UCF41Om13uiorwWbD-BZivEw/", thumbnail = icon07, folder = True)
		plugintools.add_item(title = "Perna Longa [BR]"                                , url = base + "channel/UCItsJgbVelzGpw4JyFRiA8w/", thumbnail = icon08, folder = True)
		plugintools.add_item(title = "Ruca [BR]"                            , url = base + "channel/UCxc9Eq3hOuhAbovmyTqBIig/", thumbnail = icon09, folder = True)
		plugintools.add_item(title = "Jelly Jamm [BR]"                            , url = base + "user/JellyJammPortugues/", thumbnail = icon10, folder = True)
		plugintools.add_item(title = "Turma da Mónica [BR]"                            , url = base + "channel/UCV4XcEqBswMCryorV_gNENw/", thumbnail = icon11, folder = True)
		plugintools.add_item(title = "Thomas e amigos [BR]"                            , url = base + "user/ThomaseSeusAmigos/", thumbnail = icon12, folder = True)
		
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin('Container.SetViewMode()')
		
run()
