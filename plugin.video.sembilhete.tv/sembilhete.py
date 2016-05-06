# -*- coding: utf-8 -*-
import sys
l1l1111_SBK_ = sys.version_info [0] == 2
l1ll11_SBK_ = 2048
l11lll1_SBK_ = 7
def l1l111_SBK_ (l11lll_SBK_):
	global l1l1l1l_SBK_
	l1ll1l11_SBK_ = ord (l11lll_SBK_ [-1])
	l11lllll_SBK_ = l11lll_SBK_ [:-1]
	l11l1l1_SBK_ = l1ll1l11_SBK_ % len (l11lllll_SBK_)
	l111ll_SBK_ = l11lllll_SBK_ [:l11l1l1_SBK_] + l11lllll_SBK_ [l11l1l1_SBK_:]
	if l1l1111_SBK_:
		l1llll_SBK_ = unicode () .join ([unichr (ord (char) - l1ll11_SBK_ - (l1l1l_SBK_ + l1ll1l11_SBK_) % l11lll1_SBK_) for l1l1l_SBK_, char in enumerate (l111ll_SBK_)])
	else:
		l1llll_SBK_ = str () .join ([chr (ord (char) - l1ll11_SBK_ - (l1l1l_SBK_ + l1ll1l11_SBK_) % l11lll1_SBK_) for l1l1l_SBK_, char in enumerate (l111ll_SBK_)])
	return eval (l1llll_SBK_)
import sys
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,json,threading,xbmcvfs
from resources.lib import Player
from resources.lib import requests
import HTMLParser
import datetime
import base64
import re
__ADDON_ID__   = xbmcaddon.Addon().getAddonInfo(l1l111_SBK_ (u"ࠣ࡫ࡧࠦ࡟"))
__ADDON__   = xbmcaddon.Addon(__ADDON_ID__)
__ADDON_FOLDER__    = __ADDON__.getAddonInfo(l1l111_SBK_ (u"ࠩࡳࡥࡹ࡮ࠧࡠ"))
__SETTING__ = xbmcaddon.Addon().getSetting
__ART_FOLDER__  = os.path.join(__ADDON_FOLDER__,l1l111_SBK_ (u"ࠪࡶࡪࡹ࡯ࡶࡴࡦࡩࡸ࠭ࡡ"),l1l111_SBK_ (u"ࠫ࡮ࡳࡧࠨࡢ"))
__FANART__      = os.path.join(__ADDON_FOLDER__,l1l111_SBK_ (u"ࠬ࡬ࡡ࡯ࡣࡵࡸ࠳ࡰࡰࡨࠩࡣ"))
__PASTA_FILMES__ = xbmc.translatePath(__ADDON__.getSetting(l1l111_SBK_ (u"࠭ࡢࡪࡤ࡯࡭ࡴࡺࡥࡤࡣࡉ࡭ࡱࡳࡥࡴࠩࡤ")))
__PASTA_SERIES__ = xbmc.translatePath(__ADDON__.getSetting(l1l111_SBK_ (u"ࠧࡣ࡫ࡥࡰ࡮ࡵࡴࡦࡥࡤࡗࡪࡸࡩࡦࡵࠪࡥ")))
__SKIN__ = l1l111_SBK_ (u"ࠨࡸ࠴ࠫࡦ")
__SITE__ = l1l111_SBK_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡶࡩࡲࡨࡩ࡭ࡪࡨࡸࡪ࠴ࡴࡷࠩࡧ")
__ALERTA__ = xbmcgui.Dialog().ok
def l1111l1l_SBK_():
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠪࡊ࡮ࡲ࡭ࡦࡵࠪࡨ"), __SITE__+l1l111_SBK_ (u"ࠫ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡳ࡯ࡷ࡫ࡨ࠳ࡄࡲࡩ࡮࡫ࡷࡁ࠶࠹ࠧࡩ"), 1, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠬࡳ࡯ࡷ࡫ࡨࡷ࠳ࡶ࡮ࡨࠩࡪ")))
        l1lll1l11_SBK_(l1l111_SBK_ (u"࠭ࡓ࣪ࡴ࡬ࡩࡸ࠭࡫"), __SITE__+l1l111_SBK_ (u"ࠧ࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡨࡶ࡮࡫࠯ࡀ࡮࡬ࡱ࡮ࡺ࠽࠲࠵ࠪ࡬"), 12, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠨࡵࡨࡶ࡮࡫ࡳ࠯ࡲࡱ࡫ࠬ࡭")))
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠩࠪ࡮"), l1l111_SBK_ (u"ࠪࠫ࡯"), l1l111_SBK_ (u"ࠫࠬࡰ"), os.path.join(__ADDON_FOLDER__,l1l111_SBK_ (u"ࠬ࡯ࡣࡰࡰ࠱࡮ࡵ࡭ࠧࡱ")), 0)
        l1lll1l11_SBK_(l1l111_SBK_ (u"࠭ࡌࡪࡵࡷࡥࡷࠦࡆࡪ࡮ࡰࡩࡸ࠭ࡲ"), __SITE__+l1l111_SBK_ (u"ࠧ࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡩࡨࡲࡷ࡫࠯ࠨࡳ"), 9, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠨ࡯ࡲࡺ࡮࡫ࡳ࠯ࡲࡱ࡫ࠬࡴ")))
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠩࡓࡩࡸࡷࡵࡪࡵࡤࠫࡵ"), __SITE__, 6, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠪࡷࡪࡧࡲࡤࡪ࠱ࡴࡳ࡭ࠧࡶ")))
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠫࠬࡷ"), l1l111_SBK_ (u"ࠬ࠭ࡸ"), l1l111_SBK_ (u"࠭ࠧࡹ"), os.path.join(__ADDON_FOLDER__,l1l111_SBK_ (u"ࠧࡪࡥࡲࡲ࠳ࡰࡰࡨࠩࡺ")), 0)
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠨࡈࡤࡺࡴࡸࡩࡵࡱࡶࠫࡻ"), __SITE__+l1l111_SBK_ (u"ࠩ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡹࡸ࡫ࡲ࠰ࠩࡼ")+__ADDON__.getSetting(l1l111_SBK_ (u"ࠥࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠧࡽ"))+l1l111_SBK_ (u"ࠫ࠴࡬ࡡࡷࡱࡵ࡭ࡹ࡫ࡳ࠰ࠩࡾ"), 8, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠬࡹࡴࡢࡴ࠱ࡴࡳ࡭ࠧࡿ")))
        l1lll1l11_SBK_(l1l111_SBK_ (u"࠭ࡌࡪࡵࡷࡥࠥࡏ࡮ࡵࡧࡵࡩࡸࡹࡥࡴࠩࢀ"), __SITE__+l1l111_SBK_ (u"ࠧ࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡷࡶࡩࡷ࠵ࠧࢁ")+__ADDON__.getSetting(l1l111_SBK_ (u"ࠣࡷࡶࡩࡷࡴࡡ࡮ࡧࠥࢂ"))+l1l111_SBK_ (u"ࠩ࠲ࡻࡦࡺࡣࡩ࡮࡬ࡷࡹ࠵ࠧࢃ"), 8, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠪࡰ࡮ࡹࡴࡴ࠰ࡳࡲ࡬࠭ࢄ")))
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠫࡑ࡯ࡳࡵࡣࠣࡨࡪࠦࡃࡰࡰࡷࡩࣿࡪ࡯ࡴࠩࢅ"), __SITE__+l1l111_SBK_ (u"ࠬ࠵ࡡࡱ࡫࠲ࡺ࠶࠵࡬ࡪࡵࡷࡷ࠴࠭ࢆ"), 7, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"࠭࡬ࡪࡵࡷࡷ࠳ࡶ࡮ࡨࠩࢇ")))
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠧࡏࡱࡷ࡭࡫࡯ࡣࡢࣩࣸࡩࡸࠦࠨࠦࡵࠬࠫ࢈") % l1l11ll11_SBK_(), __SITE__+l1l111_SBK_ (u"ࠨ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡱࡳࡹ࡯ࡦࡪࡥࡤࡸ࡮ࡵ࡮ࡴ࠱ࡸࡲࡷ࡫ࡡࡥ࠱ࠪࢉ"), 10, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠩࡥࡩࡱࡲ࠮ࡱࡰࡪࠫࢊ")))
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠪࠫࢋ"), l1l111_SBK_ (u"ࠫࠬࢌ"), l1l111_SBK_ (u"ࠬ࠭ࢍ"), os.path.join(__ADDON_FOLDER__,l1l111_SBK_ (u"࠭ࡩࡤࡱࡱ࠲࡯ࡶࡧࠨࢎ")), 0)
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠧࡅࡧࡩ࡭ࡳ࡯ࣶࣧࡧࡶࠫ࢏"), l1l111_SBK_ (u"ࠨࡷࡵࡰࠬ࢐"), 1000, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶ࠲ࡵࡴࡧࠨ࢑")))
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠪࡗࡦ࡯ࡲࠨ࢒"), l1l111_SBK_ (u"ࠫࡺࡸ࡬ࠨ࢓"), 99, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹ࠮ࡱࡰࡪࠫ࢔")))
        l1l1l1l1l_SBK_(l1l111_SBK_ (u"࠭࡭ࡦࡰࡸࠫ࢕"))
l1l111_SBK_ (u"ࠧࠨࠩࠍࡨࡪ࡬ࠠ࡮࡫ࡱ࡬ࡦࡉ࡯࡯ࡶࡤࠬ࠮ࡀࠊࠡࠢࠣࠤࡦࡪࡤࡅ࡫ࡵࠬࠬࡌࡡࡷࡱࡵ࡭ࡹࡵࡳࠨ࠮ࠣࡣࡤ࡙ࡉࡕࡇࡢࡣ࠰࠭ࠧ࠭ࠢ࠴࠵࠱ࠦ࡯ࡴ࠰ࡳࡥࡹ࡮࠮࡫ࡱ࡬ࡲ࠭ࡥ࡟ࡂࡔࡗࡣࡋࡕࡌࡅࡇࡕࡣࡤ࠲ࠠࡠࡡࡖࡏࡎࡔ࡟ࡠ࠮ࠣࠫ࡫ࡧࡶࡰࡴ࡬ࡸࡴࡹ࠮ࡱࡰࡪࠫ࠮࠯ࠊࠡࠢࠣࠤࡦࡪࡤࡅ࡫ࡵࠬࠬࡇࡧࡦࡰࡧࡥࡩࡵࡳࠨ࠮ࠣࡣࡤ࡙ࡉࡕࡇࡢࡣ࠰࠭ࠧ࠭ࠢ࠴࠵࠱ࠦ࡯ࡴ࠰ࡳࡥࡹ࡮࠮࡫ࡱ࡬ࡲ࠭ࡥ࡟ࡂࡔࡗࡣࡋࡕࡌࡅࡇࡕࡣࡤ࠲ࠠࡠࡡࡖࡏࡎࡔ࡟ࡠ࠮ࠣࠫࡦ࡭ࡥ࡯ࡦࡤࡨࡴࡹ࠮ࡱࡰࡪࠫ࠮࠯ࠊࠡࠢࠣࠤࡦࡪࡤࡅ࡫ࡵࠬࠬ࣠࡬ࡵ࡫ࡰࡳࡸࠦࡆࡪ࡮ࡰࡩࡸࠦࡖࡪࡵࡷࡳࡸ࠭ࠬࠡࡡࡢࡗࡎ࡚ࡅࡠࡡ࠮ࠫࠬ࠲ࠠ࠲࠳࠯ࠤࡴࡹ࠮ࡱࡣࡷ࡬࠳ࡰ࡯ࡪࡰࠫࡣࡤࡇࡒࡕࡡࡉࡓࡑࡊࡅࡓࡡࡢ࠰ࠥࡥ࡟ࡔࡍࡌࡒࡤࡥࠬࠡࠩࡸࡰࡹ࡯࡭ࡰࡵ࠱ࡴࡳ࡭ࠧࠪࠫࠍࠤࠥࠦࠠࡷ࡫ࡨࡻࡤࡶࡡࡨࡧࠫࠫࡲ࡫࡮ࡶࠩࠬࠎࠬ࠭ࠧ࢖")
def l1111ll1_SBK_():
    l1ll1l11l_SBK_ = l11ll1l11_SBK_()
    if l1ll1l11l_SBK_:
        l1111l1l_SBK_()
    else:
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠨࡃ࡯ࡸࡪࡸࡡࡳࠢࡇࡩ࡫࡯࡮ࡪࣩࣸࡩࡸ࠭ࢗ"), l1l111_SBK_ (u"ࠩࡸࡶࡱ࠭࢘"), 1000, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷ࠳ࡶ࡮ࡨ࢙ࠩ")))
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠫࡊࡴࡴࡳࡣࡵࠤࡳࡵࡶࡢ࡯ࡨࡲࡹ࡫࢚ࠧ"), l1l111_SBK_ (u"ࠬࡻࡲ࡭࢛ࠩ"), None, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"࠭ࡰࡳࡧࡹ࡭ࡴࡻࡳ࠯ࡲࡱ࡫ࠬ࢜")))
        l1l1l1l1l_SBK_(l1l111_SBK_ (u"ࠧ࡮ࡧࡱࡹࠬ࢝"))
    return
def l11ll1l11_SBK_():
    if __ADDON__.getSetting(l1l111_SBK_ (u"ࠣࡲࡤࡷࡸࡽ࡯ࡳࡦࠥ࢞")) == l1l111_SBK_ (u"ࠩࠪ࢟") or __ADDON__.getSetting(l1l111_SBK_ (u"ࠪࡩࡲࡧࡩ࡭ࠩࢠ")) == l1l111_SBK_ (u"ࠫࠬࢡ"):
        __ALERTA__(l1l111_SBK_ (u"࡙ࠬࡥ࡮ࡄ࡬ࡰ࡭࡫ࡴࡦ࠰ࡷࡺࠬࢢ"), l1l111_SBK_ (u"࠭ࡐࡳࡧࡦ࡭ࡸࡧࠠࡥࡧࠣࡨࡪ࡬ࡩ࡯࡫ࡵࠤࡺࡳࡡࠡࡥࡲࡲࡹࡧ࠮ࠨࢣ"))
        return False
    else:
        try:
            l1l11lll1_SBK_ = l1ll11ll1_SBK_(__SITE__+l1l111_SBK_ (u"ࠧ࠰ࡣࡳ࡭࠴ࡼ࠱࠰࡮ࡲ࡫࡮ࡴ࠯ࠨࢤ"), True)
        except:
            __ALERTA__(l1l111_SBK_ (u"ࠨࡕࡨࡱࡇ࡯࡬ࡩࡧࡷࡩ࠳ࡺࡶࠨࢥ"), l1l111_SBK_ (u"ࠩࡑࣧࡴࠦࡦࡰ࡫ࠣࡴࡴࡹࡳ࣮ࡸࡨࡰࠥࡧࡢࡳ࡫ࡵࠤࡦࠦࡰ࣢ࡩ࡬ࡲࡦ࠴ࠠࡑࡱࡵࠤ࡫ࡧࡶࡰࡴࠣࡸࡪࡴࡴࡦࠢࡱࡳࡻࡧ࡭ࡦࡰࡷࡩࠬࢦ"))
            return False
        else:
            try:
                l1l11lll1_SBK_[l1l111_SBK_ (u"ࠪࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬࢧ")]
            except:
                __ALERTA__(l1l111_SBK_ (u"ࠫࡘ࡫࡭ࡃ࡫࡯࡬ࡪࡺࡥ࠯ࡶࡹࠫࢨ"), l1l111_SBK_ (u"ࠬࡋ࡭ࡢ࡫࡯ࠤࡪ࠵࡯ࡶࠢࡓࡥࡸࡹࡷࡰࡴࡧࠤ࡮ࡴࡣࡰࡴࡵࡩࡹࡵࡳࠨࢩ"))
                return False
            else:
                __ADDON__.setSetting(l1l111_SBK_ (u"࠭ࡡࡱ࡫࡮ࡩࡾ࠭ࢪ"), l1l11lll1_SBK_[l1l111_SBK_ (u"ࠧࡢࡲ࡬ࡣࡰ࡫ࡹࠨࢫ")])
                __ADDON__.setSetting(l1l111_SBK_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧࠪࢬ"), l1l11lll1_SBK_[l1l111_SBK_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫࢭ")].encode(l1l111_SBK_ (u"ࠪࡹࡹ࡬࠭࠹ࠩࢮ")))
                xbmc.executebuiltin(l1l111_SBK_ (u"ࠦ࡝ࡈࡍࡄ࠰ࡑࡳࡹ࡯ࡦࡪࡥࡤࡸ࡮ࡵ࡮ࠩࡕࡨࡱࡇ࡯࡬ࡩࡧࡷࡩ࠳ࡺࡶ࠭ࠢࡖࡩࡸࡹࡡࡰࠢ࡬ࡲ࡮ࡩࡩࡢࡦࡤࠤࡨࡵ࡭ࡰ࠼ࠣࠦࢯ")+l1l11lll1_SBK_[l1l111_SBK_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧࢰ")].encode(l1l111_SBK_ (u"࠭ࡵࡵࡨ࠰࠼ࠬࢱ"))+l1l111_SBK_ (u"ࠢ࠭ࠢࠪ࠵࠵࠶࠰࠱ࠩ࠯ࠤࠧࢲ")+__ADDON_FOLDER__+l1l111_SBK_ (u"ࠣ࠱࡬ࡧࡴࡴ࠮ࡱࡰࡪ࠭ࠧࢳ"))
                return True
def l1l11ll11_SBK_():
    l11llllll_SBK_ = 0
    l11llll11_SBK_ = l1ll11ll1_SBK_(__SITE__+l1l111_SBK_ (u"ࠩ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡲࡴࡺࡩࡧ࡫ࡦࡥࡹ࡯࡯࡯ࡵ࠲ࠫࢴ"))
    for l1lll1ll1_SBK_ in l11llll11_SBK_[l1l111_SBK_ (u"ࠪࡲࡴࡺࡩࡧ࡫ࡦࡥࡹ࡯࡯࡯ࡵࠪࢵ")]:
        if l1lll1ll1_SBK_[l1l111_SBK_ (u"ࠫࡺࡴࡲࡦࡣࡧࠫࢶ")]:
            l11llllll_SBK_ += 1
    if l11llllll_SBK_ > 0:
        return l1l111_SBK_ (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡿࡥ࡭࡮ࡲࡻࡢ࠭ࢷ")+str(l11llllll_SBK_)+l1l111_SBK_ (u"࡛࠭࠰ࡅࡒࡐࡔࡘ࡝ࠨࢸ")
    else:
        return str(l11llllll_SBK_)
def l111l1l1_SBK_(url):
    l1llll1l1_SBK_ = l1l111_SBK_ (u"ࠧࠨࢹ")
    l11llll11_SBK_ = l1ll11ll1_SBK_(url)
    for l1lll1ll1_SBK_ in l11llll11_SBK_[l1l111_SBK_ (u"ࠨࡰࡲࡸ࡮࡬ࡩࡤࡣࡷ࡭ࡴࡴࡳࠨࢺ")]:
        l1llll1l1_SBK_ +=  l1lll1ll1_SBK_[l1l111_SBK_ (u"ࠩࡱࡥࡲ࡫ࠧࢻ")] + l1l111_SBK_ (u"ࠥࡠࡳࠨࢼ")
    l1ll111l1_SBK_ = xbmcgui.Dialog()
    l1ll111l1_SBK_.ok(l1l111_SBK_ (u"ࠦࡆࡪࡩࡤ࡫ࡲࡲࡦࡪ࡯ࠡࡔࡨࡧࡪࡴࡴࡦ࡯ࡨࡲࡹ࡫ࠢࢽ"), l1llll1l1_SBK_)
    try:
        l1ll11ll1_SBK_(__SITE__+l1l111_SBK_ (u"ࠬ࠵ࡡࡱ࡫࠲ࡺ࠶࠵࡮ࡰࡶ࡬ࡪ࡮ࡩࡡࡵ࡫ࡲࡲࡸ࠵࡭ࡢࡴ࡮࠱ࡦࡲ࡬࠮ࡣࡶ࠱ࡷ࡫ࡡࡥ࠱ࠪࢾ"))
    except:
        pass
    l1111l1l_SBK_()
    return
def l11111l1_SBK_(url):
    l1l11l1ll_SBK_ = l1ll11ll1_SBK_(url)
    l1lllll1l_SBK_ = l1l11l1ll_SBK_[l1l111_SBK_ (u"࠭࡭ࡦࡶࡤࠫࢿ")][l1l111_SBK_ (u"ࠧ࡯ࡧࡻࡸࠬࣀ")]
    l1l1l11ll_SBK_ = l1l11l1ll_SBK_[l1l111_SBK_ (u"ࠨ࡯ࡨࡸࡦ࠭ࣁ")][l1l111_SBK_ (u"ࠩࡳࡶࡪࡼࡩࡰࡷࡶࠫࣂ")]
    for l11l1lll1_SBK_ in l1l11l1ll_SBK_[l1l111_SBK_ (u"ࠪࡳࡧࡰࡥࡤࡶࡶࠫࣃ")]:
            try:
                l1l1ll1l1_SBK_ = l1ll11ll1_SBK_(__SITE__+l1l111_SBK_ (u"ࠫ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡳ࡯ࡷ࡫ࡨ࠳ࠬࣄ")+l11l1lll1_SBK_[l1l111_SBK_ (u"ࠬ࡯࡭ࡥࡤࡢ࡭ࡩ࠭ࣅ")])
            except:
                pass
            try:
                title = l1l1ll1l1_SBK_[l1l111_SBK_ (u"࠭ࡴࡪࡶ࡯ࡩࠬࣆ")]
                year = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠧࡺࡧࡤࡶࠬࣇ")]
                l11ll1111_SBK_ = __SITE__+l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠨࡥࡲࡺࡪࡸࠧࣈ")]
                l1l1l111l_SBK_ = __SITE__+l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠩࡳࡳࡸࡺࡥࡳࠩࣉ")]
                l1l1ll111_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠪࡳࡻ࡫ࡲࡷ࡫ࡨࡻࠬ࣊")]
                l1ll1l111_SBK_ = l1l11l111_SBK_(l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠫ࡬࡫࡮ࡳࡧࠪ࣋")])
                l111llll_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠬ࡯࡭ࡥࡤࡢࡶࡦࡺࡩ࡯ࡩࠪ࣌")]
                l11lll11l_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"࠭ࡤࡪࡴࡨࡧࡹࡵࡲࠨ࣍")]
                l1111111_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠧࡪ࡯ࡧࡦࡤ࡯ࡤࠨ࣎")]
                l1lll11ll_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠨ࡫ࡰࡨࡧࡥࡶࡰࡶࡨࡷ࣏ࠬ")]
                infoLabels = {l1l111_SBK_ (u"ࠩࡗ࡭ࡹࡲࡥࠨ࣐"): title, l1l111_SBK_ (u"ࠪ࡝ࡪࡧࡲࠨ࣑"): year, l1l111_SBK_ (u"ࠫࡌ࡫࡮ࡳࡧ࣒ࠪ"): l1ll1l111_SBK_, l1l111_SBK_ (u"ࠬࡖ࡬ࡰࡶ࣓ࠪ"): l1l1ll111_SBK_, l1l111_SBK_ (u"࠭ࡉࡎࡆࡅࡒࡺࡳࡢࡦࡴࠪࣔ"): l1111111_SBK_, l1l111_SBK_ (u"ࠧࡓࡣࡷ࡭ࡳ࡭ࠧࣕ"): l111llll_SBK_, l1l111_SBK_ (u"ࠨࡘࡲࡸࡪࡹࠧࣖ"): l1lll11ll_SBK_, l1l111_SBK_ (u"ࠩࡇ࡭ࡷ࡫ࡣࡵࡱࡵࠫࣗ"): l11lll11l_SBK_}
                l11lll111_SBK_(title+l1l111_SBK_ (u"ࠪࠤ࠭࠭ࣘ")+year+l1l111_SBK_ (u"ࠫ࠮࠭ࣙ"), l1111111_SBK_, 3, l1l1l111l_SBK_, l1l111_SBK_ (u"ࠬ࡬ࡩ࡭࡯ࡨࠫࣚ"), 0, 0, infoLabels, l11ll1111_SBK_)
            except:
                pass
    l1lll1l11_SBK_(l1l111_SBK_ (u"࠭ࡐࡳࣵࡻ࡭ࡲࡵࠠ࠿ࠩࣛ"), __SITE__+l1lllll1l_SBK_, 1, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠧ࡯ࡧࡻࡸ࠳ࡶ࡮ࡨࠩࣜ")))
    l1l1l1l1l_SBK_(l1l111_SBK_ (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࡠࡵࡨࡶ࡮࡫ࡳࠨࣝ"))
def l1l1ll1ll_SBK_(url):
    l1l111l1l_SBK_ = l1ll11ll1_SBK_(url)
    l1lllll1l_SBK_ = l1l111l1l_SBK_[l1l111_SBK_ (u"ࠩࡰࡩࡹࡧࠧࣞ")][l1l111_SBK_ (u"ࠪࡲࡪࡾࡴࠨࣟ")]
    l1l1l11ll_SBK_ = l1l111l1l_SBK_[l1l111_SBK_ (u"ࠫࡲ࡫ࡴࡢࠩ࣠")][l1l111_SBK_ (u"ࠬࡶࡲࡦࡸ࡬ࡳࡺࡹࠧ࣡")]
    for l111l111_SBK_ in l1l111l1l_SBK_[l1l111_SBK_ (u"࠭࡯ࡣ࡬ࡨࡧࡹࡹࠧ࣢")]:
        try:
            title = l111l111_SBK_[l1l111_SBK_ (u"ࠧࡵ࡫ࡷࡰࡪࣣ࠭")]
            l1ll1ll1l_SBK_ = l111l111_SBK_[l1l111_SBK_ (u"ࠨࡵࡷࡥࡷࡺ࡟ࡺࡧࡤࡶࠬࣤ")]
            l1l1l111l_SBK_ = __SITE__+l111l111_SBK_[l1l111_SBK_ (u"ࠩࡳࡳࡸࡺࡥࡳࠩࣥ")]
            l1llll1ll_SBK_ = l111l111_SBK_[l1l111_SBK_ (u"ࠪࡶࡪࡹ࡯ࡶࡴࡦࡩࡤࡻࡲࡪࣦࠩ")]
            infoLabels = {l1l111_SBK_ (u"࡙ࠫ࡯ࡴ࡭ࡧࠪࣧ"):title, l1l111_SBK_ (u"ࠬ࡟ࡥࡢࡴࠪࣨ"):l1ll1ll1l_SBK_}
            l1lll1l11_SBK_(title+ l1l111_SBK_ (u"ࣩ࠭ࠠࠩࠩ")+l1ll1ll1l_SBK_+l1l111_SBK_ (u"ࠧࠪࠩ࣪"), __SITE__+l1llll1ll_SBK_, 4, l1l1l111l_SBK_, l1l111_SBK_ (u"ࠨࡵࡨࡶ࡮࡫ࠧ࣫"), infoLabels, l1l1l111l_SBK_)
        except:
            pass
    l1lll1l11_SBK_(l1l111_SBK_ (u"ࠩࡓࡶࣸࡾࡩ࡮ࡱࠣࡂࠬ࣬"), __SITE__+l1lllll1l_SBK_, 12, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠪࡲࡪࡾࡴ࠯ࡲࡱ࡫࣭ࠬ")))
    l1l1l1l1l_SBK_(l1l111_SBK_ (u"ࠫࡲࡵࡶࡪࡧࡶࡣࡸ࡫ࡲࡪࡧࡶ࣮ࠫ"))
def l1ll11111_SBK_(url):
    l1l111ll1_SBK_ = l1ll11ll1_SBK_(url)
    l1l1l111l_SBK_ = __SITE__+l1l111ll1_SBK_[l1l111_SBK_ (u"ࠬࡶ࡯ࡴࡶࡨࡶ࣯ࠬ")]
    for season in l1l111ll1_SBK_[l1l111_SBK_ (u"࠭ࡳࡦࡣࡶࡳࡳࡹࣰࠧ")]:
        l11llll1l_SBK_ = str(season[l1l111_SBK_ (u"ࠧࡴࡧࡤࡷࡴࡴ࡟࡯ࡷࡰࡦࡪࡸࣱࠧ")])
        l1lll11l1_SBK_ = season[l1l111_SBK_ (u"ࠨࡴࡨࡷࡴࡻࡲࡤࡧࡢࡹࡷ࡯ࣲࠧ")]
        l111111l_SBK_(l1l111_SBK_ (u"ࠤ࡞ࡆࡢ࡚ࡥ࡮ࡲࡲࡶࡦࡪࡡ࡜࠱ࡅࡡࠥࠨࣳ")+l11llll1l_SBK_, __SITE__+l1lll11l1_SBK_, 5, l1l1l111l_SBK_, l11llll1l_SBK_)
    l1l1l1l1l_SBK_(l1l111_SBK_ (u"ࠪࡷࡪࡧࡳࡰࡰࡶࠫࣴ"))
def l111l1ll_SBK_(url):
    l11ll11l1_SBK_ = l1ll11ll1_SBK_(url)
    l11llll1l_SBK_ = l11ll11l1_SBK_[l1l111_SBK_ (u"ࠫࡸ࡫ࡡࡴࡱࡱࡣࡳࡻ࡭ࡣࡧࡵࠫࣵ")]
    for episode in l11ll11l1_SBK_[l1l111_SBK_ (u"ࠬ࡫ࡰࡪࡵࡲࡨࡪࡹࣶࠧ")]:
        title = episode[l1l111_SBK_ (u"࠭࡮ࡢ࡯ࡨࠫࣷ")]
        l1lll1l1l_SBK_ = episode[l1l111_SBK_ (u"ࠧࡦࡲ࡬ࡷࡴࡪࡥࡠࡰࡸࡱࡧ࡫ࡲࠨࣸ")]
        l1111111_SBK_ = episode[l1l111_SBK_ (u"ࠨ࡫ࡰࡨࡧࡥࡩࡥࣹࠩ")]
        try:
            l111l11l_SBK_ = __SITE__+episode[l1l111_SBK_ (u"ࠩࡶࡸ࡮ࡲ࡬ࠨࣺ")]
        except:
            l111l11l_SBK_ = __SITE__+l1l111_SBK_ (u"ࠪ࠳ࡸࡺࡡࡵ࡫ࡦ࠳࡮ࡳࡧ࠰ࡦࡨࡪࡦࡻ࡬ࡵࡡࡶࡸ࡮ࡲ࡬࠯ࡲࡱ࡫ࠬࣻ")
        l1l1ll111_SBK_ = episode[l1l111_SBK_ (u"ࠫࡴࡼࡥࡳࡸ࡬ࡩࡼ࠭ࣼ")]
        l11lll1l1_SBK_ = episode[l1l111_SBK_ (u"ࠬࡧࡩࡳࡡࡧࡥࡹ࡫ࠧࣽ")]
        infoLabels = {l1l111_SBK_ (u"࠭ࡔࡪࡶ࡯ࡩࠬࣾ"):title, l1l111_SBK_ (u"ࠧࡑ࡮ࡲࡸࠬࣿ"):l1l1ll111_SBK_, l1l111_SBK_ (u"ࠨࡕࡨࡥࡸࡵ࡮ࠨऀ"):l11llll1l_SBK_, l1l111_SBK_ (u"ࠩࡈࡴ࡮ࡹ࡯ࡥࡧࠪँ"):l1lll1l1l_SBK_, l1l111_SBK_ (u"ࠪࡅ࡮ࡸࡥࡥࠩं"):l11lll1l1_SBK_}
        l11lll111_SBK_(l1l111_SBK_ (u"ࠫࡠࡈ࡝ࡆࡲ࡬ࡷࡴࡪࡩࡰࠢࠪः")+str(l1lll1l1l_SBK_)+l1l111_SBK_ (u"ࠬࡡ࠯ࡃ࡟ࠣࢀࠥ࠭ऄ")+title, l1111111_SBK_, 3, l111l11l_SBK_, l1l111_SBK_ (u"࠭ࡥࡱ࡫ࡶࡳࡩ࡫ࠧअ"), l11llll1l_SBK_, l1lll1l1l_SBK_, infoLabels, l111l11l_SBK_)
    l1l1l1l1l_SBK_(l1l111_SBK_ (u"ࠧࡦࡲ࡬ࡷࡴࡪࡥࡴࠩआ"))
def l1ll111ll_SBK_(url):
    l1l1l11l1_SBK_ = [(l1l111_SBK_ (u"ࠨࡰࡨࡻࡪࡹࡴ࠮ࡣࡧࡨࡪࡪࠧइ"),l1l111_SBK_ (u"ࠩ࡞ࡒࡔ࡜ࡏࡔ࡟ࠣࡖࡪࡩࡥ࡯ࡶࡨࡷࠬई")),
                (l1l111_SBK_ (u"ࠪࡳࡱࡪࡥࡴࡶ࠰ࡥࡩࡪࡥࡥࠩउ"), l1l111_SBK_ (u"ࠫࡠࡔࡏࡗࡑࡖࡡࠥࡇ࡮ࡵ࡫ࡪࡳࡸ࠭ऊ")),
                (l1l111_SBK_ (u"ࠬࡴࡥࡸࡧࡶࡸ࠲ࡿࡥࡢࡴࠪऋ"),l1l111_SBK_ (u"࡛࠭ࡂࡐࡒࡡࠥࡘࡥࡤࡧࡱࡸࡪࡹࠧऌ")),
                (l1l111_SBK_ (u"ࠧࡰ࡮ࡧࡩࡸࡺ࠭ࡺࡧࡤࡶࠬऍ"),l1l111_SBK_ (u"ࠨ࡝ࡄࡒࡔࡣࠠࡂࡰࡷ࡭࡬ࡵࡳࠨऎ")),
                (l1l111_SBK_ (u"ࠩࡥࡩࡸࡺ࠭ࡳࡣࡷ࡭ࡳ࡭ࠧए"),l1l111_SBK_ (u"ࠪ࡟ࡈࡒࡁࡔࡕࡌࡊࡎࡉࡁࣈࣅࡒࡡࠥࡓࡥ࡭ࡪࡲࡶࠬऐ")),
                (l1l111_SBK_ (u"ࠫࡼࡵࡲࡴࡧ࠰ࡶࡦࡺࡩ࡯ࡩࠪऑ"),l1l111_SBK_ (u"ࠬࡡࡃࡍࡃࡖࡗࡎࡌࡉࡄࡃ࣊ࣇࡔࡣࠠࡑ࡫ࡲࡶࠬऒ")),
                (l1l111_SBK_ (u"࠭࡭ࡰࡵࡷ࠱ࡻ࡯ࡥࡸࡧࡧࠫओ"),l1l111_SBK_ (u"ࠧ࡜ࡘࡌ࡞࡚ࡇࡌࡊ࡜ࡄ࣋ࣚࡋࡓ࡞ࠢࡐࡥ࡮ࡹࠠࡗ࡫ࡶࡸࡴࡹࠧऔ")),
                (l1l111_SBK_ (u"ࠨ࡮ࡨࡷࡸ࠳ࡶࡪࡧࡺࡩࡩ࠭क"),l1l111_SBK_ (u"ࠩ࡞࡚ࡎࡠࡕࡂࡎࡌ࡞ࡆ࣍ࣕࡆࡕࡠࠤࡒ࡫࡮ࡰࡵ࡚ࠣ࡮ࡹࡴࡰࡵࠪख"))]
    for l1111l1l_SBK_ in l1l1l11l1_SBK_:
        l1lll1l11_SBK_(l1111l1l_SBK_[1], __SITE__+l1l111_SBK_ (u"ࠪ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࡲࡵࡶࡪࡧ࠲ࡃࡱ࡯࡭ࡪࡶࡀ࠵࠸ࠬ࡯ࡳࡦࡨࡶࡤࡨࡹ࠾ࠩग")+l1111l1l_SBK_[0], 1, l1l111_SBK_ (u"ࠫࠬघ"), l1l111_SBK_ (u"ࠬ࠭ङ"))
    l1ll1l1l1_SBK_ = l1ll11ll1_SBK_(url)
    l1l1111ll_SBK_ = l1ll1l1l1_SBK_[l1l111_SBK_ (u"࠭࡯ࡣ࡬ࡨࡧࡹࡹࠧच")]
    l111111l_SBK_(l1l111_SBK_ (u"ࠧ࡜ࡄࡠࡋ࣮ࡴࡥࡳࡱ࡞࠳ࡇࡣࠧछ"), l1l111_SBK_ (u"ࠨࠩज"), 1, l1l111_SBK_ (u"ࠩࠪझ"), l1l111_SBK_ (u"ࠪࠫञ"))
    for l1111l1l_SBK_ in l1l1111ll_SBK_:
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠫࠥࠦ࠭ࠡࠩट")+l1111l1l_SBK_[l1l111_SBK_ (u"ࠬࡴࡡ࡮ࡧࠪठ")].encode(l1l111_SBK_ (u"࠭ࡵࡵࡨ࠰࠼ࠬड")), __SITE__+l1l111_SBK_ (u"ࠧ࠰ࡣࡳ࡭࠴ࡼ࠱࠰࡯ࡲࡺ࡮࡫࠯ࡀ࡮࡬ࡱ࡮ࡺ࠽࠲࠵ࠩ࡫ࡪࡴࡲࡦ࠿ࠪढ")+l1111l1l_SBK_[l1l111_SBK_ (u"ࠨࡵ࡯ࡹ࡬࠭ण")], 1, l1l111_SBK_ (u"ࠩࠪत"), l1l111_SBK_ (u"ࠪࠫथ"))
    l1l1l1l1l_SBK_(l1l111_SBK_ (u"ࠫࡲ࡫࡮ࡶࠩद"))
def l1ll1lll1_SBK_(url):
    l1l111111_SBK_ = l1ll11ll1_SBK_(url)
    for list in l1l111111_SBK_[l1l111_SBK_ (u"ࠬࡲࡩࡴࡶࡶࠫध")]:
        try:
            name = list[l1l111_SBK_ (u"࠭࡮ࡢ࡯ࡨࠫन")].encode(l1l111_SBK_ (u"ࠧࡶࡶࡩ࠱࠽࠭ऩ"))
            l1lll1l11_SBK_(name, __SITE__+l1l111_SBK_ (u"ࠨ࠱ࡤࡴ࡮࠵ࡶ࠲࠱࡯࡭ࡸࡺ࠯ࠨप")+list[l1l111_SBK_ (u"ࠩࡶࡰࡺ࡭ࠧफ")], 71, l1l111_SBK_ (u"ࠪࠫब"), l1l111_SBK_ (u"ࠫࠬभ"), l1l111_SBK_ (u"ࠬ࠭म"), l1l111_SBK_ (u"࠭ࠧय"))
        except:
                pass
    l1l1l1l1l_SBK_(l1l111_SBK_ (u"ࠧࡴࡧࡤࡷࡴࡴࡳࠨर"))
def l1lllllll_SBK_(url):
    l1l11l1ll_SBK_ = l1ll11ll1_SBK_(url)
    for l11l1lll1_SBK_ in l1l11l1ll_SBK_[l1l111_SBK_ (u"ࠨ࡫ࡷࡩࡲࡹࠧऱ")]:
        l1llll1ll_SBK_ = l11l1lll1_SBK_[l1l111_SBK_ (u"ࠩࡵࡩࡸࡵࡵࡳࡥࡨࡣࡺࡸࡩࠨल")]
        l11llll1l_SBK_ = None
        l11ll1ll1_SBK_ = None
        try:
            l11ll1l1l_SBK_ = re.search(l1l111_SBK_ (u"ࡵࠫࡡ࠵ࡳࡦࡣࡶࡳࡳࡢ࠯ࠩ࡞ࡧ࠯࠮ࡢ࠯ࠨळ"), l1llll1ll_SBK_)
            l11llll1l_SBK_ = l11ll1l1l_SBK_.group(1)
        except:
            pass
        try:
            l11ll1ll1_SBK_ = l11l1lll1_SBK_[l1l111_SBK_ (u"ࠫࡸ࡫ࡡࡴࡱࡱࡷࠬऴ")]
        except:
            pass
        if l11ll1ll1_SBK_:
            try:
                title = l11l1lll1_SBK_[l1l111_SBK_ (u"ࠬࡺࡩࡵ࡮ࡨࠫव")]
                l1ll1ll1l_SBK_ = l11l1lll1_SBK_[l1l111_SBK_ (u"࠭ࡳࡵࡣࡵࡸࡤࡿࡥࡢࡴࠪश")]
                l1l1l111l_SBK_ = __SITE__+l11l1lll1_SBK_[l1l111_SBK_ (u"ࠧࡱࡱࡶࡸࡪࡸࠧष")]
                infoLabels = {l1l111_SBK_ (u"ࠨࡖ࡬ࡸࡱ࡫ࠧस"):title, l1l111_SBK_ (u"ࠩ࡜ࡩࡦࡸࠧह"):l1ll1ll1l_SBK_}
                l1lll1l11_SBK_(title+ l1l111_SBK_ (u"ࠪࠤ࠭࠭ऺ")+l1ll1ll1l_SBK_+l1l111_SBK_ (u"ࠫ࠮࠭ऻ"), __SITE__+l1llll1ll_SBK_, 4, l1l1l111l_SBK_, l1l111_SBK_ (u"ࠬࡹࡥࡳ࡫ࡨ़ࠫ"), infoLabels, l1l1l111l_SBK_)
            except:
                pass
        elif l11llll1l_SBK_:
            l1lll1l1l_SBK_ = l11l1lll1_SBK_[l1l111_SBK_ (u"࠭ࡥࡱ࡫ࡶࡳࡩ࡫࡟࡯ࡷࡰࡦࡪࡸࠧऽ")]
            title = l11l1lll1_SBK_[l1l111_SBK_ (u"ࠧ࡯ࡣࡰࡩࠬा")]
            l1111111_SBK_ = l11l1lll1_SBK_[l1l111_SBK_ (u"ࠨ࡫ࡰࡨࡧࡥࡩࡥࠩि")]
            l1l1ll111_SBK_ = l11l1lll1_SBK_[l1l111_SBK_ (u"ࠩࡲࡺࡪࡸࡶࡪࡧࡺࠫी")]
            l11lll1l1_SBK_ = l11l1lll1_SBK_[l1l111_SBK_ (u"ࠪࡥ࡮ࡸ࡟ࡥࡣࡷࡩࠬु")]
            try:
                l111l11l_SBK_ = __SITE__+l11l1lll1_SBK_[l1l111_SBK_ (u"ࠫࡸࡺࡩ࡭࡮ࠪू")]
            except:
                l111l11l_SBK_ = __SITE__+l1l111_SBK_ (u"ࠬ࠵ࡳࡵࡣࡷ࡭ࡨ࠵ࡩ࡮ࡩ࠲ࡨࡪ࡬ࡡࡶ࡮ࡷࡣࡸࡺࡩ࡭࡮࠱ࡴࡳ࡭ࠧृ")
            infoLabels = {l1l111_SBK_ (u"࠭ࡔࡪࡶ࡯ࡩࠬॄ"):title, l1l111_SBK_ (u"ࠧࡑ࡮ࡲࡸࠬॅ"):l1l1ll111_SBK_, l1l111_SBK_ (u"ࠨࡕࡨࡥࡸࡵ࡮ࠨॆ"):l11llll1l_SBK_, l1l111_SBK_ (u"ࠩࡈࡴ࡮ࡹ࡯ࡥࡧࠪे"):l1lll1l1l_SBK_, l1l111_SBK_ (u"ࠪࡅ࡮ࡸࡥࡥࠩै"):l11lll1l1_SBK_}
            l11lll111_SBK_(l1l111_SBK_ (u"ࠫࡠࡈ࡝ࡆࡲ࡬ࡷࡴࡪࡩࡰࠢࠪॉ")+str(l1lll1l1l_SBK_)+l1l111_SBK_ (u"ࠬࡡ࠯ࡃ࡟ࠣࢀࠥ࠭ॊ")+title, l1111111_SBK_, 3, l111l11l_SBK_, l1l111_SBK_ (u"࠭ࡥࡱ࡫ࡶࡳࡩ࡫ࠧो"), l11llll1l_SBK_, l1lll1l1l_SBK_, infoLabels, l111l11l_SBK_)
        else:
            try:
                l1l1ll1l1_SBK_ = l1ll11ll1_SBK_(__SITE__+l1l111_SBK_ (u"ࠧ࠰ࡣࡳ࡭࠴ࡼ࠱࠰࡯ࡲࡺ࡮࡫࠯ࠨौ")+l11l1lll1_SBK_[l1l111_SBK_ (u"ࠨ࡫ࡰࡨࡧࡥࡩࡥ्ࠩ")])
            except:
                pass
            try:
                title = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠩࡷ࡭ࡹࡲࡥࠨॎ")]
                year = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠪࡽࡪࡧࡲࠨॏ")]
                l11ll1111_SBK_ = __SITE__+l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠫࡨࡵࡶࡦࡴࠪॐ")]
                l1l1l111l_SBK_ = __SITE__+l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠬࡶ࡯ࡴࡶࡨࡶࠬ॑")]
                l1l1ll111_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"࠭࡯ࡷࡧࡵࡺ࡮࡫ࡷࠨ॒")]
                l1ll1l111_SBK_ = l1l11l111_SBK_(l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠧࡨࡧࡱࡶࡪ࠭॓")])
                l111llll_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠨ࡫ࡰࡨࡧࡥࡲࡢࡶ࡬ࡲ࡬࠭॔")]
                l11lll11l_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠩࡧ࡭ࡷ࡫ࡣࡵࡱࡵࠫॕ")]
                l1111111_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠪ࡭ࡲࡪࡢࡠ࡫ࡧࠫॖ")]
                l1lll11ll_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠫ࡮ࡳࡤࡣࡡࡹࡳࡹ࡫ࡳࠨॗ")]
                infoLabels = {l1l111_SBK_ (u"࡚ࠬࡩࡵ࡮ࡨࠫक़"): title, l1l111_SBK_ (u"࡙࠭ࡦࡣࡵࠫख़"): year, l1l111_SBK_ (u"ࠧࡈࡧࡱࡶࡪ࠭ग़"): l1ll1l111_SBK_, l1l111_SBK_ (u"ࠨࡒ࡯ࡳࡹ࠭ज़"): l1l1ll111_SBK_, l1l111_SBK_ (u"ࠩࡌࡑࡉࡈࡎࡶ࡯ࡥࡩࡷ࠭ड़"): l1111111_SBK_, l1l111_SBK_ (u"ࠪࡖࡦࡺࡩ࡯ࡩࠪढ़"): l111llll_SBK_, l1l111_SBK_ (u"࡛ࠫࡵࡴࡦࡵࠪफ़"): l1lll11ll_SBK_, l1l111_SBK_ (u"ࠬࡊࡩࡳࡧࡦࡸࡴࡸࠧय़"): l11lll11l_SBK_}
                l11lll111_SBK_(title+l1l111_SBK_ (u"࠭ࠠࠩࠩॠ")+year+l1l111_SBK_ (u"ࠧࠪࠩॡ"), l1111111_SBK_, 3, l1l1l111l_SBK_, l1l111_SBK_ (u"ࠨࡨ࡬ࡰࡲ࡫ࠧॢ"), 0, 0, infoLabels, l11ll1111_SBK_)
            except:
                pass
    l1l1l1l1l_SBK_(l1l111_SBK_ (u"ࠩࡰࡳࡻ࡯ࡥࡴࡡࡶࡩࡷ࡯ࡥࡴࠩॣ"))
def search():
    l11ll11ll_SBK_ = xbmc.Keyboard(l1l111_SBK_ (u"ࠪࠫ।"), l1l111_SBK_ (u"ࠫࡔࠦࡱࡶࡧࠣࡵࡺ࡫ࡲࠡࡲࡨࡷࡶࡻࡩࡴࡣࡵࡃࠬ॥"))
    l11ll11ll_SBK_.doModal()
    if l11ll11ll_SBK_.isConfirmed():
        l1ll11lll_SBK_ = l11ll11ll_SBK_.getText()
        l111ll11_SBK_ = l1ll11ll1_SBK_(__SITE__+l1l111_SBK_ (u"ࠬ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡦࡣࡵࡧ࡭࠵࠿ࡲࡷࡨࡶࡾࡃࠧ०")+l1ll11lll_SBK_+l1l111_SBK_ (u"࠭ࠦ࡭࡫ࡰ࡭ࡹࡃ࠱࠱ࠩ१"))
        for l1ll11l11_SBK_ in l111ll11_SBK_[l1l111_SBK_ (u"ࠧࡰࡤ࡭ࡩࡨࡺࡳࠨ२")]:
            try:
                title = l1ll11l11_SBK_[l1l111_SBK_ (u"ࠨࡶ࡬ࡸࡱ࡫ࠧ३")]
                year = l1ll11l11_SBK_[l1l111_SBK_ (u"ࠩࡧࡥࡹ࡫ࠧ४")]
                type = l1ll11l11_SBK_[l1l111_SBK_ (u"ࠪࡸࡾࡶࡥࠨ५")]
                l1l1l111l_SBK_ = __SITE__+l1ll11l11_SBK_[l1l111_SBK_ (u"ࠫࡵࡵࡳࡵࡧࡵࠫ६")]
                l1111111_SBK_ = l1ll11l11_SBK_[l1l111_SBK_ (u"ࠬ࡯࡭ࡥࡤࡢ࡭ࡩ࠭७")]
                l1llll1ll_SBK_ = l1ll11l11_SBK_[l1l111_SBK_ (u"࠭ࡲࡦࡵࡲࡹࡷࡩࡥࡠࡷࡵ࡭ࠬ८")]
            except:
                pass
            if type == l1l111_SBK_ (u"ࠧ࡮ࡱࡹ࡭ࡪ࠭९"):
                try:
                    l1l1ll1l1_SBK_ = l1ll11ll1_SBK_(__SITE__+l1l111_SBK_ (u"ࠨ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡰࡳࡻ࡯ࡥ࠰ࠩ॰")+l1111111_SBK_)
                except:
                    pass
                try:
                    title = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠩࡷ࡭ࡹࡲࡥࠨॱ")]
                    year = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠪࡽࡪࡧࡲࠨॲ")]
                    l11ll1111_SBK_ = __SITE__+l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠫࡨࡵࡶࡦࡴࠪॳ")]
                    l1l1l111l_SBK_ = __SITE__+l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠬࡶ࡯ࡴࡶࡨࡶࠬॴ")]
                    l1l1ll111_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"࠭࡯ࡷࡧࡵࡺ࡮࡫ࡷࠨॵ")]
                    l1ll1l111_SBK_ = l1l11l111_SBK_(l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠧࡨࡧࡱࡶࡪ࠭ॶ")])
                    l111llll_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠨ࡫ࡰࡨࡧࡥࡲࡢࡶ࡬ࡲ࡬࠭ॷ")]
                    l11lll11l_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠩࡧ࡭ࡷ࡫ࡣࡵࡱࡵࠫॸ")]
                    l1111111_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠪ࡭ࡲࡪࡢࡠ࡫ࡧࠫॹ")]
                except:
                    pass
                infoLabels = {l1l111_SBK_ (u"࡙ࠫ࡯ࡴ࡭ࡧࠪॺ"): title, l1l111_SBK_ (u"ࠬ࡟ࡥࡢࡴࠪॻ"): year, l1l111_SBK_ (u"࠭ࡇࡦࡰࡵࡩࠬॼ"): l1ll1l111_SBK_, l1l111_SBK_ (u"ࠧࡑ࡮ࡲࡸࠬॽ"): l1l1ll111_SBK_, l1l111_SBK_ (u"ࠨࡔࡤࡸ࡮ࡴࡧࠨॾ"): l111llll_SBK_, l1l111_SBK_ (u"ࠩࡇ࡭ࡷ࡫ࡣࡵࡱࡵࠫॿ"): l11lll11l_SBK_ }
                l11lll111_SBK_(l1l111_SBK_ (u"ࠪ࡟ࡋࡏࡌࡎࡇࡠࠤࠥ࠭ঀ")+title+l1l111_SBK_ (u"ࠫࠥ࠮ࠧঁ")+year+l1l111_SBK_ (u"ࠬ࠯ࠧং"), l1111111_SBK_, 3, l1l1l111l_SBK_, l1l111_SBK_ (u"࠭ࡦࡪ࡮ࡰࡩࠬঃ"), 0, 0, infoLabels, l1l1l111l_SBK_)
            if type == l1l111_SBK_ (u"ࠧࡴࡧࡵ࡭ࡪ࠭঄"):
                infoLabels = {l1l111_SBK_ (u"ࠨࡖ࡬ࡸࡱ࡫ࠧঅ"): title, l1l111_SBK_ (u"ࠩ࡜ࡩࡦࡸࠧআ"): year}
                l1lll1l11_SBK_(l1l111_SBK_ (u"ࠪ࡟ࡘࡋࡒࡊࡇࡠࠤࠥ࠭ই")+title+ l1l111_SBK_ (u"ࠫࠥ࠮ࠧঈ")+year+l1l111_SBK_ (u"ࠬ࠯ࠧউ"), __SITE__+l1llll1ll_SBK_, 4, l1l1l111l_SBK_, l1l111_SBK_ (u"࠭ࡳࡦࡴ࡬ࡩࠬঊ"), infoLabels, l1l1l111l_SBK_)
        else:
            l1lll1l11_SBK_(l1l111_SBK_ (u"ࠧ࠽࡙ࠢࡳࡱࡺࡡࡳࠩঋ"), l1l111_SBK_ (u"ࠨࡷࡵࡰࠬঌ"), None, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠩࡳࡶࡪࡼࡩࡰࡷࡶ࠲ࡵࡴࡧࠨ঍")))
    l1l1l1l1l_SBK_(l1l111_SBK_ (u"ࠪࡱࡴࡼࡩࡦࡵࡢࡷࡪࡸࡩࡦࡵࠪ঎"))
def l1llll111_SBK_(url):
    l11ll1lll_SBK_ = l1ll11ll1_SBK_(url)
    for l11l1llll_SBK_ in l11ll1lll_SBK_[l1l111_SBK_ (u"ࠫࡲࡵࡶࡪࡧࡶࠫএ")]:
        try:
            title = l11l1llll_SBK_[l1l111_SBK_ (u"ࠬࡺࡩࡵ࡮ࡨࠫঐ")]
            year = l11l1llll_SBK_[l1l111_SBK_ (u"࠭ࡹࡦࡣࡵࠫ঑")]
            l1l1l111l_SBK_ = __SITE__+l11l1llll_SBK_[l1l111_SBK_ (u"ࠧࡱࡱࡶࡸࡪࡸࠧ঒")]
            l1111111_SBK_ = l11l1llll_SBK_[l1l111_SBK_ (u"ࠨ࡫ࡰࡨࡧࡥࡩࡥࠩও")]
            l1llll1ll_SBK_ = l11l1llll_SBK_[l1l111_SBK_ (u"ࠩࡵࡩࡸࡵࡵࡳࡥࡨࡣࡺࡸࡩࠨঔ")]
        except:
            pass
        try:
            l1l1ll1l1_SBK_ = l1ll11ll1_SBK_(__SITE__+l1l111_SBK_ (u"ࠪ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࡲࡵࡶࡪࡧ࠲ࠫক")+l1111111_SBK_)
        except:
            pass
        try:
            title = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠫࡹ࡯ࡴ࡭ࡧࠪখ")]
            year = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠬࡿࡥࡢࡴࠪগ")]
            l11ll1111_SBK_ = __SITE__+l1l1ll1l1_SBK_[l1l111_SBK_ (u"࠭ࡣࡰࡸࡨࡶࠬঘ")]
            l1l1l111l_SBK_ = __SITE__+l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠧࡱࡱࡶࡸࡪࡸࠧঙ")]
            l1l1ll111_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠨࡱࡹࡩࡷࡼࡩࡦࡹࠪচ")]
            l1ll1l111_SBK_ = l1l11l111_SBK_(l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠩࡪࡩࡳࡸࡥࠨছ")])
            l111llll_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠪ࡭ࡲࡪࡢࡠࡴࡤࡸ࡮ࡴࡧࠨজ")]
            l11lll11l_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࡳࡷ࠭ঝ")]
            l1111111_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠬ࡯࡭ࡥࡤࡢ࡭ࡩ࠭ঞ")]
        except:
            pass
        infoLabels = {l1l111_SBK_ (u"࠭ࡔࡪࡶ࡯ࡩࠬট"): title, l1l111_SBK_ (u"࡚ࠧࡧࡤࡶࠬঠ"): year, l1l111_SBK_ (u"ࠨࡉࡨࡲࡷ࡫ࠧড"): l1ll1l111_SBK_, l1l111_SBK_ (u"ࠩࡓࡰࡴࡺࠧঢ"): l1l1ll111_SBK_, l1l111_SBK_ (u"ࠪࡖࡦࡺࡩ࡯ࡩࠪণ"): l111llll_SBK_, l1l111_SBK_ (u"ࠫࡉ࡯ࡲࡦࡥࡷࡳࡷ࠭ত"): l11lll11l_SBK_ }
        l11lll111_SBK_(l1l111_SBK_ (u"ࠬࡡࡆࡊࡎࡐࡉࡢࠦࠠࠨথ")+title+l1l111_SBK_ (u"࠭ࠠࠩࠩদ")+year+l1l111_SBK_ (u"ࠧࠪࠩধ"), l1111111_SBK_, 3, l1l1l111l_SBK_, l1l111_SBK_ (u"ࠨࡨ࡬ࡰࡲ࡫ࠧন"), 0, 0, infoLabels, l1l1l111l_SBK_)
    for l1l1l1111_SBK_ in l11ll1lll_SBK_[l1l111_SBK_ (u"ࠩࡶࡩࡷ࡯ࡥࡴࠩ঩")]:
        try:
            title = l1l1l1111_SBK_[l1l111_SBK_ (u"ࠪࡸ࡮ࡺ࡬ࡦࠩপ")]
            year = l1l1l1111_SBK_[l1l111_SBK_ (u"ࠫࡸࡺࡡࡳࡶࡢࡽࡪࡧࡲࠨফ")]
            l1l1l111l_SBK_ = __SITE__+l1l1l1111_SBK_[l1l111_SBK_ (u"ࠬࡶ࡯ࡴࡶࡨࡶࠬব")]
            l1111111_SBK_ = l1l1l1111_SBK_[l1l111_SBK_ (u"࠭ࡩ࡮ࡦࡥࡣ࡮ࡪࠧভ")]
            l1llll1ll_SBK_ = l1l1l1111_SBK_[l1l111_SBK_ (u"ࠧࡳࡧࡶࡳࡺࡸࡣࡦࡡࡸࡶ࡮࠭ম")]
        except:
            pass
        infoLabels = {l1l111_SBK_ (u"ࠨࡖ࡬ࡸࡱ࡫ࠧয"): title, l1l111_SBK_ (u"ࠩ࡜ࡩࡦࡸࠧর"): year}
        l1lll1l11_SBK_(l1l111_SBK_ (u"ࠪ࡟ࡘࡋࡒࡊࡇࡠࠤࠥ࠭঱")+title+ l1l111_SBK_ (u"ࠫࠥ࠮ࠧল")+year+l1l111_SBK_ (u"ࠬ࠯ࠧ঳"), __SITE__+l1llll1ll_SBK_, 4, l1l1l111l_SBK_, l1l111_SBK_ (u"࠭ࡳࡦࡴ࡬ࡩࠬ঴"), infoLabels, l1l1l111l_SBK_)
    l1lll1l11_SBK_(l1l111_SBK_ (u"ࠧ࠽࡙ࠢࡳࡱࡺࡡࡳࠩ঵"), l1l111_SBK_ (u"ࠨࡷࡵࡰࠬশ"), None, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠩࡳࡶࡪࡼࡩࡰࡷࡶ࠲ࡵࡴࡧࠨষ")))
    l1l1l1l1l_SBK_(l1l111_SBK_ (u"ࠪࡱࡴࡼࡩࡦࡵࡢࡷࡪࡸࡩࡦࡵࠪস"))
def l1ll1111l_SBK_():
    __ADDON__.openSettings()
    l1lll1l11_SBK_(l1l111_SBK_ (u"ࠫࡊࡴࡴࡳࡣࡵࠤࡳࡵࡶࡢ࡯ࡨࡲࡹ࡫ࠧহ"),l1l111_SBK_ (u"ࠬࡻࡲ࡭ࠩ঺"),None,os.path.join(__ART_FOLDER__, __SKIN__,l1l111_SBK_ (u"࠭ࡰࡳࡧࡹ࡭ࡴࡻࡳ࠯ࡲࡱ࡫ࠬ঻")))
    l1l1l1l1l_SBK_(l1l111_SBK_ (u"ࠧ࡮ࡧࡱࡹ়ࠬ"))
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
def l1l1l1l1l_SBK_(option):
    if option == l1l111_SBK_ (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࡠࡵࡨࡶ࡮࡫ࡳࠨঽ"):
        l1ll1l1ll_SBK_ = __ADDON__.getSetting(l1l111_SBK_ (u"ࠩࡩ࡭ࡱࡳࡥࡴࡕࡨࡶ࡮࡫ࡳࡗ࡫ࡨࡻࠬা"))
    elif option == l1l111_SBK_ (u"ࠪࡱࡪࡴࡵࠨি"):
        l1ll1l1ll_SBK_ = __ADDON__.getSetting(l1l111_SBK_ (u"ࠫࡲ࡫࡮ࡶࡘ࡬ࡩࡼ࠭ী"))
    elif option == l1l111_SBK_ (u"ࠬࡹࡥࡢࡵࡲࡲࡸ࠭ু"):
        l1ll1l1ll_SBK_ = __ADDON__.getSetting(l1l111_SBK_ (u"࠭ࡳࡦࡣࡶࡳࡳࡹࡖࡪࡧࡺࠫূ"))
    elif option == l1l111_SBK_ (u"ࠧࡦࡲ࡬ࡷࡴࡪࡥࡴࠩৃ"):
        l1ll1l1ll_SBK_ = __ADDON__.getSetting(l1l111_SBK_ (u"ࠨࡧࡳ࡭ࡸࡵࡤࡪࡱࡶ࡚࡮࡫ࡷࠨৄ"))
    else:
        l1ll1l1ll_SBK_ = l1l111_SBK_ (u"ࠩ࠳ࠫ৅")
    if l1ll1l1ll_SBK_:
        if l1ll1l1ll_SBK_ == l1l111_SBK_ (u"ࠪ࠴ࠬ৆"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠦࡈࡵ࡮ࡵࡣ࡬ࡲࡪࡸ࠮ࡔࡧࡷ࡚࡮࡫ࡷࡎࡱࡧࡩ࠭࠻࠰ࠪࠤে"))
        elif l1ll1l1ll_SBK_ == l1l111_SBK_ (u"ࠬ࠷ࠧৈ"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠨࡃࡰࡰࡷࡥ࡮ࡴࡥࡳ࠰ࡖࡩࡹ࡜ࡩࡦࡹࡐࡳࡩ࡫ࠨ࠶࠳ࠬࠦ৉"))
        elif l1ll1l1ll_SBK_ == l1l111_SBK_ (u"ࠧ࠳ࠩ৊"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠣࡅࡲࡲࡹࡧࡩ࡯ࡧࡵ࠲ࡘ࡫ࡴࡗ࡫ࡨࡻࡒࡵࡤࡦࠪ࠸࠴࠵࠯ࠢো"))
        elif l1ll1l1ll_SBK_ == l1l111_SBK_ (u"ࠩ࠶ࠫৌ"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠥࡇࡴࡴࡴࡢ࡫ࡱࡩࡷ࠴ࡓࡦࡶ࡙࡭ࡪࡽࡍࡰࡦࡨࠬ࠺࠶࠱ࠪࠤ্"))
        elif l1ll1l1ll_SBK_ == l1l111_SBK_ (u"ࠫ࠹࠭ৎ"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠧࡉ࡯࡯ࡶࡤ࡭ࡳ࡫ࡲ࠯ࡕࡨࡸ࡛࡯ࡥࡸࡏࡲࡨࡪ࠮࠵࠱࠺ࠬࠦ৏"))
        elif l1ll1l1ll_SBK_ == l1l111_SBK_ (u"࠭࠵ࠨ৐"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠢࡄࡱࡱࡸࡦ࡯࡮ࡦࡴ࠱ࡗࡪࡺࡖࡪࡧࡺࡑࡴࡪࡥࠩ࠷࠳࠸࠮ࠨ৑"))
        elif l1ll1l1ll_SBK_ == l1l111_SBK_ (u"ࠨ࠸ࠪ৒"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠤࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡙ࡥࡵࡘ࡬ࡩࡼࡓ࡯ࡥࡧࠫ࠹࠵࠹ࠩࠣ৓"))
        elif l1ll1l1ll_SBK_ == l1l111_SBK_ (u"ࠪ࠻ࠬ৔"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠦࡈࡵ࡮ࡵࡣ࡬ࡲࡪࡸ࠮ࡔࡧࡷ࡚࡮࡫ࡷࡎࡱࡧࡩ࠭࠻࠱࠶ࠫࠥ৕"))
def l1l11l111_SBK_(list):
    l11l1ll1l_SBK_ = []
    for l1ll1l111_SBK_ in list:
        l11l1ll1l_SBK_.append(l1ll1l111_SBK_[l1l111_SBK_ (u"ࠬࡴࡡ࡮ࡧࠪ৖")])
    return l1l111_SBK_ (u"࠭ࠬࠡࠩৗ").join(l11l1ll1l_SBK_)
def l1ll11ll1_SBK_(url, l11ll1l11_SBK_=l1l111_SBK_ (u"ࠧࠨ৘"), l1l11l11l_SBK_=l1l111_SBK_ (u"ࠨࠩ৙")):
    l11111ll_SBK_ = l1l111_SBK_ (u"ࠩࠪ৚")
    l1llll11l_SBK_ = HTMLParser.HTMLParser()
    if l11ll1l11_SBK_:
        email = urllib.quote(l1llll11l_SBK_.unescape(__ADDON__.getSetting(l1l111_SBK_ (u"ࠪࡩࡲࡧࡩ࡭ࠩ৛"))))
        password = urllib.quote(l1llll11l_SBK_.unescape(__ADDON__.getSetting(l1l111_SBK_ (u"ࠦࡵࡧࡳࡴࡹࡲࡶࡩࠨড়"))))
        l11111ll_SBK_ = requests.get(url, params=l1l111_SBK_ (u"ࠬࡲ࡯ࡨ࡫ࡱࡁࠬঢ়")+email+l1l111_SBK_ (u"࠭ࠦࡱࡣࡶࡷࡼࡵࡲࡥ࠿ࠪ৞")+password).json()
    else:
        username = urllib.quote(l1llll11l_SBK_.unescape(__ADDON__.getSetting(l1l111_SBK_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩয়"))))
        l11111ll_SBK_ = requests.get(url, params=l1l111_SBK_ (u"ࠨࡣࡳ࡭ࡤࡱࡥࡺ࠿ࠪৠ")+__ADDON__.getSetting(l1l111_SBK_ (u"ࠩࡤࡴ࡮ࡱࡥࡺࠩৡ"))+l1l111_SBK_ (u"ࠪࠪࡺࡹࡥࡳࡰࡤࡱࡪࡃࠧৢ")+username).json()
    if l1l11l11l_SBK_:
        username = urllib.quote(l1llll11l_SBK_.unescape(__ADDON__.getSetting(l1l111_SBK_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭ৣ"))))
        l11111ll_SBK_ = requests.post(url, data=l1l11l11l_SBK_, params=l1l111_SBK_ (u"ࠬࡧࡰࡪࡡ࡮ࡩࡾࡃࠧ৤")+__ADDON__.getSetting(l1l111_SBK_ (u"࠭ࡡࡱ࡫࡮ࡩࡾ࠭৥"))+l1l111_SBK_ (u"ࠧࠧࡷࡶࡩࡷࡴࡡ࡮ࡧࡀࠫ০")+username).json()
    return l11111ll_SBK_
def l1l1lllll_SBK_(name,url,iconimage):
    l11lll1ll_SBK_=xbmcgui.ListItem(name, iconImage=l1l111_SBK_ (u"ࠣࡆࡨࡪࡦࡻ࡬ࡵࡘ࡬ࡨࡪࡵ࠮ࡱࡰࡪࠦ১"), thumbnailImage=iconimage)
    l11lll1ll_SBK_.setProperty(l1l111_SBK_ (u"ࠩࡩࡥࡳࡧࡲࡵࡡ࡬ࡱࡦ࡭ࡥࠨ২"), iconimage)
    l11lll1ll_SBK_.setInfo( type=l1l111_SBK_ (u"࡚ࠥ࡮ࡪࡥࡰࠤ৩"), infoLabels={ l1l111_SBK_ (u"࡙ࠦ࡯ࡴ࡭ࡧࠥ৪"): name } )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=l11lll1ll_SBK_)
    return True
def l1lll1l11_SBK_(name,url,mode,iconimage,l11ll111l_SBK_=False,infoLabels=False,l1l1l111l_SBK_=False):
    if infoLabels: infoLabelsAux = infoLabels
    else: infoLabelsAux = {l1l111_SBK_ (u"࡚ࠬࡩࡵ࡮ࡨࠫ৫"): name}
    if l1l1l111l_SBK_: l1111lll_SBK_ = l1l1l111l_SBK_
    else: l1111lll_SBK_ = iconimage
    u=sys.argv[0]+l1l111_SBK_ (u"ࠨ࠿ࡶࡴ࡯ࡁࠧ৬")+urllib.quote_plus(url)+l1l111_SBK_ (u"ࠢࠧ࡯ࡲࡨࡪࡃࠢ৭")+str(mode)+l1l111_SBK_ (u"ࠣࠨࡱࡥࡲ࡫࠽ࠣ৮")+urllib.quote_plus(name)
    l1l1l1ll1_SBK_ = __FANART__
    if l11ll111l_SBK_ == l1l111_SBK_ (u"ࠩࡩ࡭ࡱࡳࡥࠨ৯"):
        l1l1l1ll1_SBK_ = l1111lll_SBK_
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠪࡑࡴࡼࡩࡦࡵࠪৰ"))
    elif l11ll111l_SBK_ == l1l111_SBK_ (u"ࠫࡸ࡫ࡲࡪࡧࠪৱ"):
        l1l1l1ll1_SBK_ = l1111lll_SBK_
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭৲"))
    elif l11ll111l_SBK_ == l1l111_SBK_ (u"࠭ࡥࡱ࡫ࡶࡳࡩ࡫ࠧ৳"):
        l1l1l1ll1_SBK_ = l1111lll_SBK_
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠧࡦࡲ࡬ࡷࡴࡪࡥࡴࠩ৴"))
    else:
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠨࡏࡲࡺ࡮࡫ࡳࠨ৵"))
    l11lll1ll_SBK_=xbmcgui.ListItem(name, iconImage=l1111lll_SBK_, thumbnailImage=l1111lll_SBK_)
    l11lll1ll_SBK_.setProperty(l1l111_SBK_ (u"ࠩࡩࡥࡳࡧࡲࡵࡡ࡬ࡱࡦ࡭ࡥࠨ৶"), l1l1l1ll1_SBK_)
    l11lll1ll_SBK_.setInfo( type=l1l111_SBK_ (u"࡚ࠥ࡮ࡪࡥࡰࠤ৷"), infoLabels=infoLabelsAux )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l11lll1ll_SBK_,isFolder=True)
    return True
def l1l1l1lll_SBK_(name,url,mode,iconimage,l1111l11_SBK_):
    u=sys.argv[0]+l1l111_SBK_ (u"ࠦࡄࡻࡲ࡭࠿ࠥ৸")+urllib.quote_plus(url)+l1l111_SBK_ (u"ࠧࠬ࡭ࡰࡦࡨࡁࠧ৹")+str(mode)+l1l111_SBK_ (u"ࠨࠦ࡯ࡣࡰࡩࡂࠨ৺")+urllib.quote_plus(name)
    l11lll1ll_SBK_=xbmcgui.ListItem(name, iconImage=l1l111_SBK_ (u"ࠢࡧࡣࡱࡥࡷࡺ࠮࡫ࡲࡪࠦ৻"), thumbnailImage=iconimage)
    l11lll1ll_SBK_.setProperty(l1l111_SBK_ (u"ࠨࡨࡤࡲࡦࡸࡴࡠ࡫ࡰࡥ࡬࡫ࠧৼ"), iconimage)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l11lll1ll_SBK_,isFolder=l1111l11_SBK_)
    return True
def l111111l_SBK_(name,url,mode,iconimage,season):
    u=sys.argv[0]+l1l111_SBK_ (u"ࠤࡂࡹࡷࡲ࠽ࠣ৽")+urllib.quote_plus(url)+l1l111_SBK_ (u"ࠥࠪࡲࡵࡤࡦ࠿ࠥ৾")+str(mode)+l1l111_SBK_ (u"ࠦࠫࡴࡡ࡮ࡧࡀࠦ৿")+urllib.quote_plus(name)+l1l111_SBK_ (u"ࠧࠬࡳࡦࡣࡶࡳࡳࡃࠢ਀")+str(season)
    xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"࠭ࡍࡰࡸ࡬ࡩࡸ࠭ਁ"))
    l11lll1ll_SBK_=xbmcgui.ListItem(name, iconImage=l1l111_SBK_ (u"ࠢࡧࡣࡱࡥࡷࡺ࠮࡫ࡲࡪࠦਂ"), thumbnailImage=iconimage)
    l11lll1ll_SBK_.setProperty(l1l111_SBK_ (u"ࠨࡨࡤࡲࡦࡸࡴࡠ࡫ࡰࡥ࡬࡫ࠧਃ"), __FANART__)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l11lll1ll_SBK_,isFolder=True)
    return True
def l11lll111_SBK_(name,url,mode,iconimage,l11ll111l_SBK_,season,episode,infoLabels,l1l1l111l_SBK_):
    if l11ll111l_SBK_ == l1l111_SBK_ (u"ࠩࡩ࡭ࡱࡳࡥࠨ਄"):
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠪࡑࡴࡼࡩࡦࡵࠪਅ"))
    elif l11ll111l_SBK_ == l1l111_SBK_ (u"ࠫࡸ࡫ࡲࡪࡧࠪਆ"):
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ਇ"))
    elif l11ll111l_SBK_ == l1l111_SBK_ (u"࠭ࡥࡱ࡫ࡶࡳࡩ࡫ࠧਈ"):
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠧࡦࡲ࡬ࡷࡴࡪࡥࡴࠩਉ"))
    u=sys.argv[0]+l1l111_SBK_ (u"ࠣࡁࡸࡶࡱࡃࠢਊ")+urllib.quote_plus(url.encode(l1l111_SBK_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ਋")))+l1l111_SBK_ (u"ࠥࠪࡲࡵࡤࡦ࠿ࠥ਌")+str(mode)+l1l111_SBK_ (u"ࠦࠫࡹࡥࡢࡵࡲࡲࡂࠨ਍")+str(season)+l1l111_SBK_ (u"ࠧࠬࡥࡱ࡫ࡶࡳࡩ࡫࠽ࠣ਎")+str(episode)+l1l111_SBK_ (u"ࠨࠦ࡯ࡣࡰࡩࡂࠨਏ")+urllib.quote_plus(name.encode(l1l111_SBK_ (u"ࠧࡶࡶࡩ࠱࠽࠭ਐ")))+l1l111_SBK_ (u"ࠣࠨ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࡂࠨ਑")+urllib.quote_plus(iconimage)
    l11lll1ll_SBK_=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    l11lll1ll_SBK_.setProperty(l1l111_SBK_ (u"ࠩࡩࡥࡳࡧࡲࡵࡡ࡬ࡱࡦ࡭ࡥࠨ਒"), l1l1l111l_SBK_)
    l11lll1ll_SBK_.setInfo( type=l1l111_SBK_ (u"࡚ࠥ࡮ࡪࡥࡰࠤਓ"), infoLabels=infoLabels )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l11lll1ll_SBK_,isFolder=False)
    return True
def l1lll111l_SBK_():
    xbmc.executebuiltin(l1l111_SBK_ (u"ࠦ࡝ࡈࡍࡄ࠰ࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡛ࡰࡥࡣࡷࡩ࠭ࡶࡡࡵࡪ࠯ࡶࡪࡶ࡬ࡢࡥࡨ࠭ࠧਔ"))
    xbmc.executebuiltin(l1l111_SBK_ (u"ࠧ࡞ࡂࡎࡅ࠱ࡅࡨࡺࡩࡷࡣࡷࡩ࡜࡯࡮ࡥࡱࡺࠬࡍࡵ࡭ࡦࠫࠥਕ"))
def l1l11111l_SBK_(url,path):
    l1l1111l1_SBK_ = requests.get(url.encode(l1l111_SBK_ (u"࠭ࡵࡵࡨ࠰࠼ࠬਖ"))).content
    if l1l1111l1_SBK_:
        with open(path, l1l111_SBK_ (u"ࠧࡸࠩਗ")) as fh:
            fh.write(l1l1111l1_SBK_)
            fh.close()
    return url
def l11l1ll11_SBK_(lang):
    if lang == l1l111_SBK_ (u"ࠨࡲࡷ࠱ࡕ࡚ࠧਘ"):
        return l1l111_SBK_ (u"ࠩࡳࡸ࠲ࡖࡔࠨਙ")
    elif lang == l1l111_SBK_ (u"ࠪࡴࡹ࠳ࡂࡓࠩਚ"):
        return l1l111_SBK_ (u"ࠫࡵࡺ࠭ࡃࡔࠪਛ")
    elif lang == l1l111_SBK_ (u"ࠬ࡫࡮ࠨਜ"):
        return l1l111_SBK_ (u"࠭ࡅ࡯ࡩ࡯࡭ࡸ࡮ࠧਝ")
    else:
        return None
def l1ll1ll11_SBK_(lang):
    l1l1lll11_SBK_ = l1l111_SBK_ (u"ࠧࡪࡥࡲࡲ࠳ࡶ࡮ࡨࠩਞ")
    language = l1l111_SBK_ (u"ࠨࠩਟ")
    if lang == l1l111_SBK_ (u"ࠩࡳࡸ࠲ࡖࡔࠨਠ"):
        language = l1l111_SBK_ (u"ࠪࡔࡴࡸࡴࡶࡩࡸࡩࡸࠦࠨࡑࡖࠬࠫਡ")
        l1l1lll11_SBK_ = l1l111_SBK_ (u"ࠫࡵࡵࡲࡵࡷࡪࡹࡪࡹࡥ࠯ࡲࡱ࡫ࠬਢ")
    elif lang == l1l111_SBK_ (u"ࠬࡶࡴ࠮ࡄࡕࠫਣ"):
        language = l1l111_SBK_ (u"࠭ࡐࡰࡴࡷࡹ࡬ࡻࡥࡴࠢࠫࡆࡗ࠯ࠧਤ")
        l1l1lll11_SBK_ = l1l111_SBK_ (u"ࠧࡣࡴࡤࡾ࡮ࡲ࠮ࡱࡰࡪࠫਥ")
    elif lang == l1l111_SBK_ (u"ࠨࡧࡱࠫਦ"):
        language = l1l111_SBK_ (u"ࠩࡈࡲ࡬ࡲࡩࡴࡪࠪਧ")
        l1l1lll11_SBK_ = l1l111_SBK_ (u"ࠪࡩࡳ࡭࡬ࡪࡵ࡫࠲ࡵࡴࡧࠨਨ")
    else:
        return None
    return xbmc.executebuiltin(l1l111_SBK_ (u"ࠦ࡝ࡈࡍࡄ࠰ࡑࡳࡹ࡯ࡦࡪࡥࡤࡸ࡮ࡵ࡮ࠩࡕࡨࡱࡇ࡯࡬ࡩࡧࡷࡩ࠳ࡺࡶ࠭ࠢࡏࡩ࡬࡫࡮ࡥࡣࠣࡧࡦࡸࡲࡦࡩࡤࡨࡦࡀࠠࠣ਩")+language+l1l111_SBK_ (u"ࠧ࠲ࠠࠨ࠳࠳࠴࠵࠶ࠧ࠭ࠢࠥਪ")+os.path.join(__ART_FOLDER__, __SKIN__,l1l1lll11_SBK_)+l1l111_SBK_ (u"ࠨࠩࠣਫ"))
def l11l1l1ll_SBK_(imdb):
    l1l111lll_SBK_ = l1ll11ll1_SBK_(__SITE__+l1l111_SBK_ (u"ࠧ࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡥࡲࡲࡹ࡫࡮ࡵ࠱ࡵࡩࡶࡻࡥࡴࡶ࠲ࠫਬ")+imdb+l1l111_SBK_ (u"ࠨ࠱ࠪਭ"))
    l1lll1lll_SBK_ = l1l111lll_SBK_
    l1lll1111_SBK_ = None
    if l1l111_SBK_ (u"ࠩࡳࡶࡴࡼࡩࡥࡧࡵࠫਮ") in l1lll1lll_SBK_:
        try:
            headers = json.loads(urllib.unquote(base64.standard_b64decode(urllib.unquote(l1lll1lll_SBK_[l1l111_SBK_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫਯ")]).encode(l1l111_SBK_ (u"ࠫࡺࡺࡦ࠮࠺ࠪਰ")))))
        except:
            headers = l1l111_SBK_ (u"ࠬ࠭਱")
        l1l11ll1l_SBK_ = requests.request(l1lll1lll_SBK_[l1l111_SBK_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ਲ")], l1lll1lll_SBK_[l1l111_SBK_ (u"ࠧࡶࡴ࡯ࠫਲ਼")], data=l1lll1lll_SBK_[l1l111_SBK_ (u"ࠨࡦࡤࡸࡦ࠭਴")], headers=headers)
        l1llllll1_SBK_ = urllib.quote(base64.standard_b64encode(urllib.quote(bytes(l1l11ll1l_SBK_.text.encode(l1l111_SBK_ (u"ࠩࡤࡷࡨ࡯ࡩࠨਵ"), l1l111_SBK_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࠪਸ਼"))))))
        l1llll11l_SBK_ = HTMLParser.HTMLParser()
        username = urllib.quote(l1llll11l_SBK_.unescape(__ADDON__.getSetting(l1l111_SBK_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭਷"))))
        content = requests.post(__SITE__+l1l111_SBK_ (u"ࠬ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡣࡰࡰࡷࡩࡳࡺ࠯ࠨਸ")+imdb+l1l111_SBK_ (u"࠭࠯ࠨਹ"), data={l1l111_SBK_ (u"ࠧࡱࡴࡲࡺ࡮ࡪࡥࡳࠩ਺"): l1lll1lll_SBK_[l1l111_SBK_ (u"ࠨࡲࡵࡳࡻ࡯ࡤࡦࡴࠪ਻")], l1l111_SBK_ (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶ਼ࠪ"): l1llllll1_SBK_}, params=l1l111_SBK_ (u"ࠪࡥࡵ࡯࡟࡬ࡧࡼࡁࠬ਽")+__ADDON__.getSetting(l1l111_SBK_ (u"ࠫࡦࡶࡩ࡬ࡧࡼࠫਾ"))+l1l111_SBK_ (u"ࠬࠬࡵࡴࡧࡵࡲࡦࡳࡥ࠾ࠩਿ")+username).json()
        url = content[l1l111_SBK_ (u"࠭ࡵࡳ࡮ࡶࠫੀ")][0][l1l111_SBK_ (u"ࠧࡶࡴ࡯ࠫੁ")]
        l1lll1111_SBK_ = { l1l111_SBK_ (u"ࠨࡵࡸࡦࡹ࡯ࡴ࡭ࡧࡶࠫੂ") : content[l1l111_SBK_ (u"ࠩࡶࡹࡧࡺࡩࡵ࡮ࡨࡷࠬ੃")], l1l111_SBK_ (u"ࠪࡹࡷࡲࠧ੄") : url }
        return l1lll1111_SBK_
    else:
        content = l1l111lll_SBK_
        l1lll1111_SBK_ = { l1l111_SBK_ (u"ࠫࡸࡻࡢࡵ࡫ࡷࡰࡪࡹࠧ੅") : content[l1l111_SBK_ (u"ࠬࡹࡵࡣࡶ࡬ࡸࡱ࡫ࡳࠨ੆")], l1l111_SBK_ (u"࠭ࡵࡳ࡮ࠪੇ") : content[l1l111_SBK_ (u"ࠧࡶࡴ࡯ࡷࠬੈ")][0][l1l111_SBK_ (u"ࠨࡷࡵࡰࠬ੉")] }
        return l1lll1111_SBK_
def l1l11llll_SBK_(name,imdb,iconimage,season,episode,serieNome=l1l111_SBK_ (u"ࠩࠪ੊")):
    l11l1lll1_SBK_ = l11l1l1ll_SBK_(imdb)
    url = l11l1lll1_SBK_[l1l111_SBK_ (u"ࠪࡹࡷࡲࠧੋ")]
    l11lllll1_SBK_ = []
    if len(l11l1lll1_SBK_[l1l111_SBK_ (u"ࠫࡸࡻࡢࡵ࡫ࡷࡰࡪࡹࠧੌ")]) > 0:
        for l1l1llll1_SBK_ in l11l1lll1_SBK_[l1l111_SBK_ (u"ࠬࡹࡵࡣࡶ࡬ࡸࡱ࡫ࡳࠨ੍")]:
            language = l11l1ll11_SBK_(l1l1llll1_SBK_[l1l111_SBK_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ੎")])
            l1l111l11_SBK_ = os.path.join(xbmc.translatePath(l1l111_SBK_ (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲ࡸࡪࡳࡰࠨ੏")).encode(l1l111_SBK_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ੐")), imdb+l1l111_SBK_ (u"ࠩ࠱ࠫੑ")+language+l1l111_SBK_ (u"ࠪ࠲ࡸࡸࡴࠨ੒"))
            l1l11111l_SBK_(__SITE__+l1l1llll1_SBK_[l1l111_SBK_ (u"ࠫࡺࡸ࡬ࠨ੓")],l1l111l11_SBK_)
            l1ll1ll11_SBK_(l1l1llll1_SBK_[l1l111_SBK_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧ੔")])
            l11lllll1_SBK_.append(l1l111l11_SBK_)
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(name, iconImage=l1l111_SBK_ (u"ࠨࡄࡦࡨࡤࡹࡱࡺࡖࡪࡦࡨࡳ࠳ࡶ࡮ࡨࠤ੕"), thumbnailImage=iconimage)
    listitem.setInfo(l1l111_SBK_ (u"ࠢࡗ࡫ࡧࡩࡴࠨ੖"), {l1l111_SBK_ (u"ࠣࡶ࡬ࡸࡱ࡫ࠢ੗"):name})
    listitem.setProperty(l1l111_SBK_ (u"ࠩࡰ࡭ࡲ࡫ࡴࡺࡲࡨࠫ੘"), l1l111_SBK_ (u"ࠪࡺ࡮ࡪࡥࡰ࠱ࡻ࠱ࡲࡹࡶࡪࡦࡨࡳࠬਖ਼"))
    listitem.setProperty(l1l111_SBK_ (u"ࠫࡎࡹࡐ࡭ࡣࡼࡥࡧࡲࡥࠨਗ਼"), l1l111_SBK_ (u"ࠬࡺࡲࡶࡧࠪਜ਼"))
    playlist.add(url, listitem)
    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
    l1l11llll_SBK_ = Player.Player(url=url, idFilme=imdb, pastaData=l1l111_SBK_ (u"࠭ࠧੜ"), season=season, episode=episode, nome=name, ano=l1l111_SBK_ (u"ࠧ࠳࠲࠴࠹ࠬ੝"), logo=os.path.join(__ADDON_FOLDER__,l1l111_SBK_ (u"ࠨ࡫ࡦࡳࡳ࠴ࡰ࡯ࡩࠪਫ਼")), serieNome=l1l111_SBK_ (u"ࠩࠪ੟"))
    l1l11llll_SBK_.play(playlist)
    if len(l11lllll1_SBK_) > 0:
        for l1l1lll1l_SBK_ in l11lllll1_SBK_:
            l1l11llll_SBK_.setSubtitles(l1l1lll1l_SBK_)
def get_params():
    param=[]
    l1l1ll11l_SBK_=sys.argv[2]
    if len(l1l1ll11l_SBK_)>=2:
        params=sys.argv[2]
        l1ll11l1l_SBK_=params.replace(l1l111_SBK_ (u"ࠪࡃࠬ੠"),l1l111_SBK_ (u"ࠫࠬ੡"))
        if (params[len(params)-1]==l1l111_SBK_ (u"ࠬ࠵ࠧ੢")): params=params[0:len(params)-2]
        l111lll1_SBK_=l1ll11l1l_SBK_.split(l1l111_SBK_ (u"࠭ࠦࠨ੣"))
        param={}
        for i in range(len(l111lll1_SBK_)):
            l111ll1l_SBK_={}
            l111ll1l_SBK_=l111lll1_SBK_[i].split(l1l111_SBK_ (u"ࠧ࠾ࠩ੤"))
            if (len(l111ll1l_SBK_))==2: param[l111ll1l_SBK_[0]]=l111ll1l_SBK_[1]
    return param
def main():
    params=get_params()
    url=None
    name=None
    mode=None
    iconimage=None
    link=None
    l1l1l1l11_SBK_=None
    l1l11l1l1_SBK_=None
    season=None
    episode=None
    try: url=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠣࡷࡵࡰࠧ੥")])
    except: pass
    try: link=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠤ࡯࡭ࡳࡱࠢ੦")])
    except: pass
    try: l1l1l1l11_SBK_=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠥࡰࡪ࡭ࡥ࡯ࡦࡤࠦ੧")])
    except: pass
    try: name=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠦࡳࡧ࡭ࡦࠤ੨")])
    except: pass
    try: season=int(params[l1l111_SBK_ (u"ࠧࡹࡥࡢࡵࡲࡲࠧ੩")])
    except: pass
    try: episode=int(params[l1l111_SBK_ (u"ࠨࡥࡱ࡫ࡶࡳࡩ࡫ࠢ੪")])
    except: pass
    try: mode=int(params[l1l111_SBK_ (u"ࠢ࡮ࡱࡧࡩࠧ੫")])
    except: pass
    try: l1l11l1l1_SBK_=int(params[l1l111_SBK_ (u"ࠣࡲࡤ࡫࡮ࡴࡡࠣ੬")])
    except: pass
    try: iconimage=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠤ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࠧ੭")])
    except: pass
    try : serieNome=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠥࡷࡪࡸࡩࡦࡐࡲࡱࡪࠨ੮")])
    except: pass
    if mode==None or url==None or len(url)<1: l1111ll1_SBK_()
    elif mode==1: l11111l1_SBK_(url)
    elif mode==12: l1l1ll1ll_SBK_(url)
    elif mode==2: l1lllll11_SBK_(url, l1l11l1l1_SBK_)
    elif mode==3: l1l11llll_SBK_(name, url, iconimage, season, episode, serieNome=l1l111_SBK_ (u"ࠫࠬ੯"))
    elif mode==4: l1ll11111_SBK_(url)
    elif mode==5: l111l1ll_SBK_(url)
    elif mode==6: search()
    elif mode==7: l1ll1lll1_SBK_(url)
    elif mode==71: l1lllllll_SBK_(url)
    elif mode==8: l1llll111_SBK_(url)
    elif mode==9: l1ll111ll_SBK_(url)
    elif mode==10: l111l1l1_SBK_(url)
    elif mode==99: l1lll111l_SBK_()
    elif mode==1000: l1ll1111l_SBK_()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
if __name__ == l1l111_SBK_ (u"ࠧࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠢੰ"):
    main()