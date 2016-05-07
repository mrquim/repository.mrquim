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

icon01 = 'http://img.fnac.com.br/Imagens/Produtos/354-647221-0-5-belos-contos-de-fada-para-meninos.jpg'
icon02 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/7/9/8/9789892309897.jpg'
icon03 = 'http://2.bp.blogspot.com/_7WgaK1xWlsc/SONRoeLP68I/AAAAAAAAARc/0nBqB050ugQ/s400/DARTACAOO.JPG'
icon04 = 'http://vignette3.wikia.nocookie.net/pocoyoworld/images/2/2f/Pocoyo-Image-300x300_Pato_Elly_Loula_Sleepy_Bird.jpg'
icon05 = 'http://www.leyaonline.com/fotos/produtos/500_9789892308722_noddy_joga_as_escondidas.jpg'
icon06 = 'https://s-media-cache-ak0.pinimg.com/236x/9e/54/6f/9e546fcdcf39b9c77d4f059ee300a0eb.jpg'
icon07 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/1/4/0/9789892315041.jpg'
icon08 = 'http://lh6.ggpht.com/U2HRHrr3p0Y0s-2L0rOtDArAOMs3IDm0P1DWRD19DWPjsCZoRQFFhxdmPIUK07v6mVee=w300'
icon09 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/5/5/1/9789892702155.jpg'
icon10 = 'http://www.childrens-rooms.co.uk/childrensrooms-web/v2/images/products/viewproduct_popup/5281.jpg'
icon11 = 'http://pumpkin.pt/article/12249/featured_large.png'
icon12 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/1/6/8/0602537176861.jpg'
icon13 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/6/8/6/0602527851686.jpg'
icon14 = 'http://img.lum.dolimg.com/v1/images/open-uri20150422-20810-1hyxdss_2afe84d9.jpeg'
icon15 = 'https://s-media-cache-ak0.pinimg.com/favicons/70f47683076ee0670a2e4b51ba9eea443f005a3cccde9f2ab04da67b.png?027f4656c074a031ee558ec7f584d80b'
icon16 = 'http://img.submarino.com.br/produtos/01/00/item/7043/2/7043215g1.jpg'
icon17 = 'http://img.elo7.com.br/product/zoom/10A1C0E/capa-almofada-snoopy-charlie-brown-presentes.jpg'
icon18 = 'http://vignette4.wikia.nocookie.net/doblaje/images/a/aa/Jelly_Jamm.jpg'
icon19 = 'https://sdsouthard.files.wordpress.com/2013/08/daniel-tigers-neighborhood.jpg'

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
	plugintools.add_item(title = "Contos Infantis [PT]", url = base + "channel/UCOre4lsfRMaC62bOHUjPp2Q/", thumbnail = icon01, folder = True)
	plugintools.add_item(title = "Ruca [PT]", url = base + "playlist/PLQOUgVTEqh7mNhuwQpSEEqoarMbA74B9o/", thumbnail = icon02, folder = True)
	plugintools.add_item(title = "Dartacão [PT]", url = base + "playlist/PLrH5HKiu5jUe8ZF8jwdtprpucMVEjRON5/", thumbnail = icon03, folder = True)	
	plugintools.add_item(title = "Pocoyo [PT]", url = base + "user/childrenvideos/", thumbnail = icon04, folder = True)	
	plugintools.add_item(title = "Noddy [PT]", url = base + "channel/UCbJ3FpU6NZ4T4Ca_BxXtaGA/" , thumbnail = icon05, folder = True)	
	plugintools.add_item(title = "Ovelha Choné [PT]", url = base + "playlist/PLYbNlr-XymEXbsyrLjyqoZRRFtGiFrGyf/"           , thumbnail = icon06, folder = True)	
	plugintools.add_item(title = "Vila Moleza [PT]", url = base + "playlist/PLrH5HKiu5jUeWGDGh3EYBvMQ-eU1CSy4J/", thumbnail = icon07, folder = True)
	plugintools.add_item(title = "Herois da Cidade [PT]", url = base + "channel/UCnfjtca0KeZND5e27IO4INg/", thumbnail = icon08, folder = True)
	plugintools.add_item(title = "Bob o Construtor [PT]", url = base + "playlist/PLrH5HKiu5jUd7KNHHylSmu_WvFZ1pyURq/", thumbnail = icon09, folder = True)
	plugintools.add_item(title = "Thomas e Amigos [PT]", url = base + "playlist/PLZ-7k3FZDGmm5XODLaqSXX98OME6gk6Um/", thumbnail = icon10, folder = True)
	plugintools.add_item(title = "Abelha Maia [PT]", url = base + "playlist/PLkodmAlL47W0kgZKcX7XJKd0CC6qknZVV/", thumbnail = icon11, folder = True)
	plugintools.add_item(title = "Panda e os Caricas [PT]", url = base + "channel/UCvw-R-r3p6Hc-yj1qyoPslQ/", thumbnail = icon12, folder = True)
	plugintools.add_item(title = "Xana Toc Toc [PT]", url = base + "user/XanaTocTocVEVO/", thumbnail = icon13, folder = True)
	plugintools.add_item(title = "Disney [BR]", url = base + "user/DisneyDesenhos/", thumbnail = icon14, folder = True)
	plugintools.add_item(title = "Looney Tunes [BR]", url = base + "playlist/PLpWx6MEwzdl43CvZffNXnYbcUFyB2ZPlz/", thumbnail = icon15, folder = True)
	plugintools.add_item(title = "Turma da Mónica [BR]", url = base + "channel/UCV4XcEqBswMCryorV_gNENw/", thumbnail = icon16, folder = True)
	plugintools.add_item(title = "Snoopy [BR]", url = base + "playlist/PLolevrZYo2eGlwPrvK1Nr_rwUGSpbJMYK/", thumbnail = icon17, folder = True)
	plugintools.add_item(title = "Jelly Jamm [BR]"  , url = base + "user/JellyJammPortugues/", thumbnail = icon18, folder = True)
	plugintools.add_item(title = "Daniel Tigre [BR]", url = base + "channel/UC0uzSknyMFmFV6YrKyglYfQ/", thumbnail = icon19, folder = True)
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode()')
	
run()
