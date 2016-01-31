# coding: UTF-8
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
__ADDON_ID__   = xbmcaddon.Addon().getAddonInfo(l1l111_SBK_ (u"ࠣ࡫ࡧࠦ࡟"))
__ADDON__   = xbmcaddon.Addon(__ADDON_ID__)
__ADDON_FOLDER__    = __ADDON__.getAddonInfo(l1l111_SBK_ (u"ࠩࡳࡥࡹ࡮ࠧࡠ"))
__SETTING__ = xbmcaddon.Addon().getSetting
__ART_FOLDER__  = os.path.join(__ADDON_FOLDER__,l1l111_SBK_ (u"ࠪࡶࡪࡹ࡯ࡶࡴࡦࡩࡸ࠭ࡡ"),l1l111_SBK_ (u"ࠫ࡮ࡳࡧࠨࡢ"))
__FANART__      = os.path.join(__ADDON_FOLDER__,l1l111_SBK_ (u"ࠬ࡬ࡡ࡯ࡣࡵࡸ࠳ࡰࡰࡨࠩࡣ"))
__PASTA_FILMES__ = xbmc.translatePath(__ADDON__.getSetting(l1l111_SBK_ (u"࠭ࡢࡪࡤ࡯࡭ࡴࡺࡥࡤࡣࡉ࡭ࡱࡳࡥࡴࠩࡤ")))
__PASTA_SERIES__ = xbmc.translatePath(__ADDON__.getSetting(l1l111_SBK_ (u"ࠧࡣ࡫ࡥࡰ࡮ࡵࡴࡦࡥࡤࡗࡪࡸࡩࡦࡵࠪࡥ")))
__SKIN__ = l1l111_SBK_ (u"ࠨࡸ࠴ࠫࡦ")
__SITE__ = l1l111_SBK_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡶࡩࡲࡨࡩ࡭ࡪࡨࡸࡪ࠴ࡴࡷ࠱ࠪࡧ")
__ALERTA__ = xbmcgui.Dialog().ok
def l1lll1l1l_SBK_():
    l1ll111l1_SBK_ = l1l1lll11_SBK_()
    if l1ll111l1_SBK_:
        l1lll111l_SBK_(l1l111_SBK_ (u"ࠪࡊ࡮ࡲ࡭ࡦࡵࠪࡨ"), __SITE__+l1l111_SBK_ (u"ࠫ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡳ࡯ࡷ࡫ࡨ࠳ࡄࡲࡩ࡮࡫ࡷࡁ࠶࠹ࠧࡩ"), 1, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠬࡳ࡯ࡷ࡫ࡨࡷ࠳ࡶ࡮ࡨࠩࡪ")))
        l1lll111l_SBK_(l1l111_SBK_ (u"࠭ࡓ࣪ࡴ࡬ࡩࡸ࠭࡫"), __SITE__+l1l111_SBK_ (u"ࠧ࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡨࡶ࡮࡫࠯ࡀ࡮࡬ࡱ࡮ࡺ࠽࠲࠵ࠪ࡬"), 12, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠨࡵࡨࡶ࡮࡫ࡳ࠯ࡲࡱ࡫ࠬ࡭")))
        l1lll111l_SBK_(l1l111_SBK_ (u"ࠩࠪ࡮"), l1l111_SBK_ (u"ࠪࠫ࡯"), l1l111_SBK_ (u"ࠫࠬࡰ"), os.path.join(__ADDON_FOLDER__,l1l111_SBK_ (u"ࠬ࡯ࡣࡰࡰ࠱࡮ࡵ࡭ࠧࡱ")), 0)
        l1lll111l_SBK_(l1l111_SBK_ (u"࠭ࡌࡪࡵࡷࡥࡷࠦࡆࡪ࡮ࡰࡩࡸ࠭ࡲ"), l1l111_SBK_ (u"ࠧࡶࡴ࡯ࠫࡳ"), 9, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠨ࡯ࡲࡺ࡮࡫ࡳ࠯ࡲࡱ࡫ࠬࡴ")))
        l1lll111l_SBK_(l1l111_SBK_ (u"ࠩࡓࡩࡸࡷࡵࡪࡵࡤࠫࡵ"), __SITE__, 6, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠪࡷࡪࡧࡲࡤࡪ࠱ࡴࡳ࡭ࠧࡶ")))
        l1lll111l_SBK_(l1l111_SBK_ (u"ࠫࠬࡷ"), l1l111_SBK_ (u"ࠬ࠭ࡸ"), l1l111_SBK_ (u"࠭ࠧࡹ"), os.path.join(__ADDON_FOLDER__,l1l111_SBK_ (u"ࠧࡪࡥࡲࡲ࠳ࡰࡰࡨࠩࡺ")), 0)
        l1lll111l_SBK_(l1l111_SBK_ (u"ࠨࡆࡨࡪ࡮ࡴࡩࣨࣷࡨࡷࠬࡻ"), l1l111_SBK_ (u"ࠩࡸࡶࡱ࠭ࡼ"), 1000, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷ࠳ࡶ࡮ࡨࠩࡽ")))
        l1lll1111_SBK_(l1l111_SBK_ (u"ࠫࡲ࡫࡮ࡶࠩࡾ"))
    else:
        l1lll111l_SBK_(l1l111_SBK_ (u"ࠬࡇ࡬ࡵࡧࡵࡥࡷࠦࡄࡦࡨ࡬ࡲ࡮࣭ࣵࡦࡵࠪࡿ"), l1l111_SBK_ (u"࠭ࡵࡳ࡮ࠪࢀ"), 1000, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴ࠰ࡳࡲ࡬࠭ࢁ")))
        l1lll111l_SBK_(l1l111_SBK_ (u"ࠨࡇࡱࡸࡷࡧࡲࠡࡰࡲࡺࡦࡳࡥ࡯ࡶࡨࠫࢂ"), l1l111_SBK_ (u"ࠩࡸࡶࡱ࠭ࢃ"), None, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠪࡴࡷ࡫ࡶࡪࡱࡸࡷ࠳ࡶ࡮ࡨࠩࢄ")))
        l1lll1111_SBK_(l1l111_SBK_ (u"ࠫࡲ࡫࡮ࡶࠩࢅ"))
l1l111_SBK_ (u"ࠬ࠭ࠧࠋࡦࡨࡪࠥࡳࡩ࡯ࡪࡤࡇࡴࡴࡴࡢࠪࠬ࠾ࠏࠦࠠࠡࠢࡤࡨࡩࡊࡩࡳࠪࠪࡊࡦࡼ࡯ࡳ࡫ࡷࡳࡸ࠭ࠬࠡࡡࡢࡗࡎ࡚ࡅࡠࡡ࠮ࠫࠬ࠲ࠠ࠲࠳࠯ࠤࡴࡹ࠮ࡱࡣࡷ࡬࠳ࡰ࡯ࡪࡰࠫࡣࡤࡇࡒࡕࡡࡉࡓࡑࡊࡅࡓࡡࡢ࠰ࠥࡥ࡟ࡔࡍࡌࡒࡤࡥࠬࠡࠩࡩࡥࡻࡵࡲࡪࡶࡲࡷ࠳ࡶ࡮ࡨࠩࠬ࠭ࠏࠦࠠࠡࠢࡤࡨࡩࡊࡩࡳࠪࠪࡅ࡬࡫࡮ࡥࡣࡧࡳࡸ࠭ࠬࠡࡡࡢࡗࡎ࡚ࡅࡠࡡ࠮ࠫࠬ࠲ࠠ࠲࠳࠯ࠤࡴࡹ࠮ࡱࡣࡷ࡬࠳ࡰ࡯ࡪࡰࠫࡣࡤࡇࡒࡕࡡࡉࡓࡑࡊࡅࡓࡡࡢ࠰ࠥࡥ࡟ࡔࡍࡌࡒࡤࡥࠬࠡࠩࡤ࡫ࡪࡴࡤࡢࡦࡲࡷ࠳ࡶ࡮ࡨࠩࠬ࠭ࠏࠦࠠࠡࠢࡤࡨࡩࡊࡩࡳࠪࠪࣞࡱࡺࡩ࡮ࡱࡶࠤࡋ࡯࡬࡮ࡧࡶࠤ࡛࡯ࡳࡵࡱࡶࠫ࠱ࠦ࡟ࡠࡕࡌࡘࡊࡥ࡟ࠬࠩࠪ࠰ࠥ࠷࠱࠭ࠢࡲࡷ࠳ࡶࡡࡵࡪ࠱࡮ࡴ࡯࡮ࠩࡡࡢࡅࡗ࡚࡟ࡇࡑࡏࡈࡊࡘ࡟ࡠ࠮ࠣࡣࡤ࡙ࡋࡊࡐࡢࡣ࠱ࠦࠧࡶ࡮ࡷ࡭ࡲࡵࡳ࠯ࡲࡱ࡫ࠬ࠯ࠩࠋࠢࠣࠤࠥࡼࡩࡦࡹࡢࡴࡦ࡭ࡥࠩࠩࡰࡩࡳࡻࠧࠪࠌࠪࠫࠬࢆ")
def l1l1lll11_SBK_():
    if __ADDON__.getSetting(l1l111_SBK_ (u"ࠨࡰࡢࡵࡶࡻࡴࡸࡤࠣࢇ")) == l1l111_SBK_ (u"ࠧࠨ࢈") or __ADDON__.getSetting(l1l111_SBK_ (u"ࠨࡧࡰࡥ࡮ࡲࠧࢉ")) == l1l111_SBK_ (u"ࠩࠪࢊ"):
        __ALERTA__(l1l111_SBK_ (u"ࠪࡗࡪࡳࡂࡪ࡮࡫ࡩࡹ࡫࠮ࡵࡸࠪࢋ"), l1l111_SBK_ (u"ࠫࡕࡸࡥࡤ࡫ࡶࡥࠥࡪࡥࠡࡦࡨࡪ࡮ࡴࡩࡳࠢࡸࡱࡦࠦࡣࡰࡰࡷࡥ࠳࠭ࢌ"))
        return False
    else:
        try:
            l1l1l1ll1_SBK_ = l1l1ll1ll_SBK_(__SITE__+l1l111_SBK_ (u"ࠬ࠵ࡡࡱ࡫࠲ࡺ࠶࠵࡬ࡰࡩ࡬ࡲ࠴࠭ࢍ"), True)
        except:
            __ALERTA__(l1l111_SBK_ (u"࠭ࡓࡦ࡯ࡅ࡭ࡱ࡮ࡥࡵࡧ࠱ࡸࡻ࠭ࢎ"), l1l111_SBK_ (u"ࠧࡏࣥࡲࠤ࡫ࡵࡩࠡࡲࡲࡷࡸࣳࡶࡦ࡮ࠣࡥࡧࡸࡩࡳࠢࡤࠤࡵࣧࡧࡪࡰࡤ࠲ࠥࡖ࡯ࡳࠢࡩࡥࡻࡵࡲࠡࡶࡨࡲࡹ࡫ࠠ࡯ࡱࡹࡥࡲ࡫࡮ࡵࡧࠪ࢏"))
            return False
        else:
            try:
                l1l1l1ll1_SBK_[l1l111_SBK_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧࠪ࢐")]
            except:
                __ALERTA__(l1l111_SBK_ (u"ࠩࡖࡩࡲࡈࡩ࡭ࡪࡨࡸࡪ࠴ࡴࡷࠩ࢑"), l1l111_SBK_ (u"ࠪࡉࡲࡧࡩ࡭ࠢࡨ࠳ࡴࡻࠠࡑࡣࡶࡷࡼࡵࡲࡥࠢ࡬ࡲࡨࡵࡲࡳࡧࡷࡳࡸ࠭࢒"))
                return False
            else:
                __ADDON__.setSetting(l1l111_SBK_ (u"ࠫࡦࡶࡩ࡬ࡧࡼࠫ࢓"), l1l1l1ll1_SBK_[l1l111_SBK_ (u"ࠬࡧࡰࡪࡡ࡮ࡩࡾ࠭࢔")])
                __ADDON__.setSetting(l1l111_SBK_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨ࢕"), l1l1l1ll1_SBK_[l1l111_SBK_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ࢖")].encode(l1l111_SBK_ (u"ࠨࡷࡷࡪ࠲࠾ࠧࢗ")))
                xbmc.executebuiltin(l1l111_SBK_ (u"ࠤ࡛ࡆࡒࡉ࠮ࡏࡱࡷ࡭࡫࡯ࡣࡢࡶ࡬ࡳࡳ࠮ࡓࡦ࡯ࡅ࡭ࡱ࡮ࡥࡵࡧ࠱ࡸࡻ࠲ࠠࡔࡧࡶࡷࡦࡵࠠࡪࡰ࡬ࡧ࡮ࡧࡤࡢࠢࡦࡳࡲࡵ࠺ࠡࠤ࢘")+l1l1l1ll1_SBK_[l1l111_SBK_ (u"ࠪࡹࡸ࡫ࡲ࡯ࡣࡰࡩ࢙ࠬ")].encode(l1l111_SBK_ (u"ࠫࡺࡺࡦ࠮࠺࢚ࠪ"))+l1l111_SBK_ (u"ࠧ࠲ࠠࠨ࠳࠳࠴࠵࠶࢛ࠧ࠭ࠢࠥ")+__ADDON_FOLDER__+l1l111_SBK_ (u"ࠨ࠯ࡪࡥࡲࡲ࠳ࡶ࡮ࡨࠫࠥ࢜"))
                return True
def l1l1lllll_SBK_(url):
    l1l11llll_SBK_ = l1l1ll1ll_SBK_(url)
    l111lll1_SBK_ = l1l11llll_SBK_[l1l111_SBK_ (u"ࠧ࡮ࡧࡷࡥࠬ࢝")][l1l111_SBK_ (u"ࠨࡰࡨࡼࡹ࠭࢞")]
    l1lll1lll_SBK_ = l1l11llll_SBK_[l1l111_SBK_ (u"ࠩࡰࡩࡹࡧࠧ࢟")][l1l111_SBK_ (u"ࠪࡴࡷ࡫ࡶࡪࡱࡸࡷࠬࢠ")]
    for l1l11l11l_SBK_ in l1l11llll_SBK_[l1l111_SBK_ (u"ࠫࡴࡨࡪࡦࡥࡷࡷࠬࢡ")]:
            l1llll11l_SBK_ = l1l1ll1ll_SBK_(__SITE__+l1l111_SBK_ (u"ࠬ࠵ࡡࡱ࡫࠲ࡺ࠶࠵࡭ࡰࡸ࡬ࡩ࠴࠭ࢢ")+l1l11l11l_SBK_[l1l111_SBK_ (u"࠭ࡩ࡮ࡦࡥࡣ࡮ࡪࠧࢣ")])
            try:
                title = l1llll11l_SBK_[l1l111_SBK_ (u"ࠧࡵ࡫ࡷࡰࡪ࠭ࢤ")]
                year = l1llll11l_SBK_[l1l111_SBK_ (u"ࠨࡻࡨࡥࡷ࠭ࢥ")]
                l1l1l11ll_SBK_ = __SITE__+l1llll11l_SBK_[l1l111_SBK_ (u"ࠩࡦࡳࡻ࡫ࡲࠨࢦ")]
                l1ll1111l_SBK_ = __SITE__+l1llll11l_SBK_[l1l111_SBK_ (u"ࠪࡴࡴࡹࡴࡦࡴࠪࢧ")]
                l1ll11l1l_SBK_ = l1llll11l_SBK_[l1l111_SBK_ (u"ࠫࡴࡼࡥࡳࡸ࡬ࡩࡼ࠭ࢨ")]
                l1l1llll1_SBK_ = l1111lll_SBK_(l1llll11l_SBK_[l1l111_SBK_ (u"ࠬ࡭ࡥ࡯ࡴࡨࠫࢩ")])
                l111llll_SBK_ = l1llll11l_SBK_[l1l111_SBK_ (u"࠭ࡩ࡮ࡦࡥࡣࡷࡧࡴࡪࡰࡪࠫࢪ")]
                l1ll11111_SBK_ = l1llll11l_SBK_[l1l111_SBK_ (u"ࠧࡥ࡫ࡵࡩࡨࡺ࡯ࡳࠩࢫ")]
                l1l1l1l1l_SBK_ = l1llll11l_SBK_[l1l111_SBK_ (u"ࠨ࡫ࡰࡨࡧࡥࡩࡥࠩࢬ")]
                infoLabels = {l1l111_SBK_ (u"ࠩࡗ࡭ࡹࡲࡥࠨࢭ"): title, l1l111_SBK_ (u"ࠪ࡝ࡪࡧࡲࠨࢮ"): year, l1l111_SBK_ (u"ࠫࡌ࡫࡮ࡳࡧࠪࢯ"): l1l1llll1_SBK_, l1l111_SBK_ (u"ࠬࡖ࡬ࡰࡶࠪࢰ"): l1ll11l1l_SBK_, l1l111_SBK_ (u"࠭ࡒࡢࡶ࡬ࡲ࡬࠭ࢱ"): l111llll_SBK_, l1l111_SBK_ (u"ࠧࡅ࡫ࡵࡩࡨࡺ࡯ࡳࠩࢲ"): l1ll11111_SBK_}
                l1l1l11l1_SBK_(title+l1l111_SBK_ (u"ࠨࠢࠫࠫࢳ")+year+l1l111_SBK_ (u"ࠩࠬࠫࢴ"), l1l1l1l1l_SBK_, 3, l1ll1111l_SBK_, l1l111_SBK_ (u"ࠪࡪ࡮ࡲ࡭ࡦࠩࢵ"), 0, 0, infoLabels, l1l1l11ll_SBK_)
            except:
                pass
    l1lll111l_SBK_(l1l111_SBK_ (u"ࠫࡕࡸ࡯ࡹ࡫ࡰࡳࠥࡄࠧࢶ"), __SITE__+l111lll1_SBK_, 1, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠬࡴࡥࡹࡶ࠱ࡴࡳ࡭ࠧࢷ")))
    l1lll1111_SBK_(l1l111_SBK_ (u"࠭࡭ࡰࡸ࡬ࡩࡸࡥࡳࡦࡴ࡬ࡩࡸ࠭ࢸ"))
def l1111l11_SBK_(url):
    l111111l_SBK_ = l1l1ll1ll_SBK_(url)
    l111lll1_SBK_ = l111111l_SBK_[l1l111_SBK_ (u"ࠧ࡮ࡧࡷࡥࠬࢹ")][l1l111_SBK_ (u"ࠨࡰࡨࡼࡹ࠭ࢺ")]
    l1lll1lll_SBK_ = l111111l_SBK_[l1l111_SBK_ (u"ࠩࡰࡩࡹࡧࠧࢻ")][l1l111_SBK_ (u"ࠪࡴࡷ࡫ࡶࡪࡱࡸࡷࠬࢼ")]
    for l1llll1ll_SBK_ in l111111l_SBK_[l1l111_SBK_ (u"ࠫࡴࡨࡪࡦࡥࡷࡷࠬࢽ")]:
        try:
            title = l1llll1ll_SBK_[l1l111_SBK_ (u"ࠬࡺࡩࡵ࡮ࡨࠫࢾ")]
            l1ll1l111_SBK_ = l1llll1ll_SBK_[l1l111_SBK_ (u"࠭ࡳࡵࡣࡵࡸࡤࡿࡥࡢࡴࠪࢿ")]
            l1ll1111l_SBK_ = __SITE__+l1llll1ll_SBK_[l1l111_SBK_ (u"ࠧࡱࡱࡶࡸࡪࡸࠧࣀ")]
            l1l11l111_SBK_ = l1llll1ll_SBK_[l1l111_SBK_ (u"ࠨࡴࡨࡷࡴࡻࡲࡤࡧࡢࡹࡷ࡯ࠧࣁ")]
            infoLabels = {l1l111_SBK_ (u"ࠩࡗ࡭ࡹࡲࡥࠨࣂ"):title, l1l111_SBK_ (u"ࠪ࡝ࡪࡧࡲࠨࣃ"):l1ll1l111_SBK_}
            l1lll111l_SBK_(title+ l1l111_SBK_ (u"ࠫࠥ࠮ࠧࣄ")+l1ll1l111_SBK_+l1l111_SBK_ (u"ࠬ࠯ࠧࣅ"), __SITE__+l1l11l111_SBK_, 4, l1ll1111l_SBK_, l1l111_SBK_ (u"࠭ࡳࡦࡴ࡬ࡩࠬࣆ"), infoLabels, l1ll1111l_SBK_)
        except:
            pass
    l1lll111l_SBK_(l1l111_SBK_ (u"ࠧࡑࡴࡲࡼ࡮ࡳ࡯ࠡࡀࠪࣇ"), __SITE__+l111lll1_SBK_, 12, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠨࡰࡨࡼࡹ࠴ࡰ࡯ࡩࠪࣈ")))
    l1lll1111_SBK_(l1l111_SBK_ (u"ࠩࡰࡳࡻ࡯ࡥࡴࡡࡶࡩࡷ࡯ࡥࡴࠩࣉ"))
def l1l11l1l1_SBK_(url):
    l1111l1l_SBK_ = l1l1ll1ll_SBK_(url)
    l1ll1111l_SBK_ = __SITE__+l1111l1l_SBK_[l1l111_SBK_ (u"ࠪࡴࡴࡹࡴࡦࡴࠪ࣊")]
    for season in l1111l1l_SBK_[l1l111_SBK_ (u"ࠫࡸ࡫ࡡࡴࡱࡱࡷࠬ࣋")]:
        l1l11lll1_SBK_ = str(season[l1l111_SBK_ (u"ࠬࡹࡥࡢࡵࡲࡲࡤࡴࡵ࡮ࡤࡨࡶࠬ࣌")])
        l1ll1llll_SBK_ = season[l1l111_SBK_ (u"࠭ࡲࡦࡵࡲࡹࡷࡩࡥࡠࡷࡵ࡭ࠬ࣍")]
        l1l1ll1l1_SBK_(l1l111_SBK_ (u"ࠢ࡜ࡄࡠࡘࡪࡳࡰࡰࡴࡤࡨࡦࡡ࠯ࡃ࡟ࠣࠦ࣎")+l1l11lll1_SBK_, __SITE__+l1ll1llll_SBK_, 5, l1ll1111l_SBK_, l1l11lll1_SBK_)
    l1lll1111_SBK_(l1l111_SBK_ (u"ࠨࡵࡨࡥࡸࡵ࡮ࡴ࣏ࠩ"))
def l11111ll_SBK_(url):
    l1l1ll11l_SBK_ = l1l1ll1ll_SBK_(url)
    l1l11lll1_SBK_ = l1l1ll11l_SBK_[l1l111_SBK_ (u"ࠩࡶࡩࡦࡹ࡯࡯ࡡࡱࡹࡲࡨࡥࡳ࣐ࠩ")]
    for episode in l1l1ll11l_SBK_[l1l111_SBK_ (u"ࠪࡩࡵ࡯ࡳࡰࡦࡨࡷ࣑ࠬ")]:
        title = episode[l1l111_SBK_ (u"ࠫࡳࡧ࡭ࡦ࣒ࠩ")]
        l1lll1l11_SBK_ = episode[l1l111_SBK_ (u"ࠬ࡫ࡰࡪࡵࡲࡨࡪࡥ࡮ࡶ࡯ࡥࡩࡷ࣓࠭")]
        l1l1l1l1l_SBK_ = episode[l1l111_SBK_ (u"࠭ࡩ࡮ࡦࡥࡣ࡮ࡪࠧࣔ")]
        try:
            l1lllllll_SBK_ = __SITE__+episode[l1l111_SBK_ (u"ࠧࡴࡶ࡬ࡰࡱ࠭ࣕ")]
        except:
            l1lllllll_SBK_ = __SITE__+l1l111_SBK_ (u"ࠨ࠱ࡶࡸࡦࡺࡩࡤ࠱࡬ࡱ࡬࠵ࡤࡦࡨࡤࡹࡱࡺ࡟ࡴࡶ࡬ࡰࡱ࠴ࡰ࡯ࡩࠪࣖ")
        l1ll11l1l_SBK_ = episode[l1l111_SBK_ (u"ࠩࡲࡺࡪࡸࡶࡪࡧࡺࠫࣗ")]
        l1lll11ll_SBK_ = episode[l1l111_SBK_ (u"ࠪࡥ࡮ࡸ࡟ࡥࡣࡷࡩࠬࣘ")]
        infoLabels = {l1l111_SBK_ (u"࡙ࠫ࡯ࡴ࡭ࡧࠪࣙ"):title, l1l111_SBK_ (u"ࠬࡖ࡬ࡰࡶࠪࣚ"):l1ll11l1l_SBK_, l1l111_SBK_ (u"࠭ࡓࡦࡣࡶࡳࡳ࠭ࣛ"):l1l11lll1_SBK_, l1l111_SBK_ (u"ࠧࡆࡲ࡬ࡷࡴࡪࡥࠨࣜ"):l1lll1l11_SBK_, l1l111_SBK_ (u"ࠨࡃ࡬ࡶࡪࡪࠧࣝ"):l1lll11ll_SBK_}
        l1l1l11l1_SBK_(l1l111_SBK_ (u"ࠩ࡞ࡆࡢࡋࡰࡪࡵࡲࡨ࡮ࡵࠠࠨࣞ")+str(l1lll1l11_SBK_)+l1l111_SBK_ (u"ࠪ࡟࠴ࡈ࡝ࠡࡾࠣࠫࣟ")+title, l1l1l1l1l_SBK_, 3, l1lllllll_SBK_, l1l111_SBK_ (u"ࠫࡪࡶࡩࡴࡱࡧࡩࠬ࣠"), l1l11lll1_SBK_, l1lll1l11_SBK_, infoLabels, l1lllllll_SBK_)
    l1lll1111_SBK_(l1l111_SBK_ (u"ࠬ࡫ࡰࡪࡵࡲࡨࡪࡹࠧ࣡"))
def l1l11ll11_SBK_(url):
    l1ll11l11_SBK_ = [(l1l111_SBK_ (u"࠭࡮ࡦࡹࡨࡷࡹ࠳ࡡࡥࡦࡨࡨࠬ࣢"),l1l111_SBK_ (u"ࠧ࡜ࡐࡒ࡚ࡔ࡙࡝ࠡࡔࡨࡧࡪࡴࡴࡦࡵࣣࠪ")),
                (l1l111_SBK_ (u"ࠨࡱ࡯ࡨࡪࡹࡴ࠮ࡣࡧࡨࡪࡪࠧࣤ"), l1l111_SBK_ (u"ࠩ࡞ࡒࡔ࡜ࡏࡔ࡟ࠣࡅࡳࡺࡩࡨࡱࡶࠫࣥ")),
                (l1l111_SBK_ (u"ࠪࡲࡪࡽࡥࡴࡶ࠰ࡽࡪࡧࡲࠨࣦ"),l1l111_SBK_ (u"ࠫࡠࡇࡎࡐ࡟ࠣࡖࡪࡩࡥ࡯ࡶࡨࡷࠬࣧ")),
                (l1l111_SBK_ (u"ࠬࡵ࡬ࡥࡧࡶࡸ࠲ࡿࡥࡢࡴࠪࣨ"),l1l111_SBK_ (u"࡛࠭ࡂࡐࡒࡡࠥࡇ࡮ࡵ࡫ࡪࡳࡸࣩ࠭")),
                (l1l111_SBK_ (u"ࠧࡣࡧࡶࡸ࠲ࡸࡡࡵ࡫ࡱ࡫ࠬ࣪"),l1l111_SBK_ (u"ࠨ࡝ࡆࡐࡆ࡙ࡓࡊࡈࡌࡇࡆ࣍ࣃࡐ࡟ࠣࡑࡪࡲࡨࡰࡴࠪ࣫")),
                (l1l111_SBK_ (u"ࠩࡺࡳࡷࡹࡥ࠮ࡴࡤࡸ࡮ࡴࡧࠨ࣬"),l1l111_SBK_ (u"ࠪ࡟ࡈࡒࡁࡔࡕࡌࡊࡎࡉࡁࣈࣅࡒࡡࠥࡖࡩࡰࡴ࣭ࠪ")),
                (l1l111_SBK_ (u"ࠫࡲࡵࡳࡵ࠯ࡹ࡭ࡪࡽࡥࡥ࣮ࠩ"),l1l111_SBK_ (u"ࠬࡡࡖࡊ࡜ࡘࡅࡑࡏ࡚ࡂࣉࣘࡉࡘࡣࠠࡎࡣ࡬ࡷࠥ࡜ࡩࡴࡶࡲࡷ࣯ࠬ")),
                (l1l111_SBK_ (u"࠭࡬ࡦࡵࡶ࠱ࡻ࡯ࡥࡸࡧࡧࣰࠫ"),l1l111_SBK_ (u"ࠧ࡜ࡘࡌ࡞࡚ࡇࡌࡊ࡜ࡄ࣋ࣚࡋࡓ࡞ࠢࡐࡩࡳࡵࡳࠡࡘ࡬ࡷࡹࡵࡳࠨࣱ"))]
    for l1lll1l1l_SBK_ in l1ll11l11_SBK_:
        l1l1ll1l1_SBK_(l1lll1l1l_SBK_[1], __SITE__+l1l111_SBK_ (u"ࠨ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡰࡳࡻ࡯ࡥ࠰ࡁ࡯࡭ࡲ࡯ࡴ࠾࠳࠶ࠪࡴࡸࡤࡦࡴࡢࡦࡾࡃࣲࠧ")+l1lll1l1l_SBK_[0], 1, l1l111_SBK_ (u"ࠩࠪࣳ"), l1l111_SBK_ (u"ࠪࠫࣴ"))
    l1lll1111_SBK_(l1l111_SBK_ (u"ࠫࡲ࡫࡮ࡶࠩࣵ"))
def l1l1l1l11_SBK_():
    l1l1l1lll_SBK_ = xbmc.Keyboard(l1l111_SBK_ (u"ࣶࠬ࠭"), l1l111_SBK_ (u"࠭ࡏࠡࡳࡸࡩࠥࡷࡵࡦࡴࠣࡴࡪࡹࡱࡶ࡫ࡶࡥࡷࡅࠧࣷ"))
    l1l1l1lll_SBK_.doModal()
    if l1l1l1lll_SBK_.isConfirmed():
        l1l1lll1l_SBK_ = l1l1l1lll_SBK_.getText()
        l1111ll1_SBK_ = l1l1ll1ll_SBK_(__SITE__+l1l111_SBK_ (u"ࠧ࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡨࡥࡷࡩࡨ࠰ࡁࡴࡹࡪࡸࡹ࠾ࠩࣸ")+l1l1lll1l_SBK_+l1l111_SBK_ (u"ࠨࠨ࡯࡭ࡲ࡯ࡴ࠾࠳࠳ࣹࠫ"))
        for l1l1l1111_SBK_ in l1111ll1_SBK_[l1l111_SBK_ (u"ࠩࡲࡦ࡯࡫ࡣࡵࡵࣺࠪ")]:
            try:
                title = l1l1l1111_SBK_[l1l111_SBK_ (u"ࠪࡸ࡮ࡺ࡬ࡦࠩࣻ")]
                year = l1l1l1111_SBK_[l1l111_SBK_ (u"ࠫࡩࡧࡴࡦࠩࣼ")]
                type = l1l1l1111_SBK_[l1l111_SBK_ (u"ࠬࡺࡹࡱࡧࠪࣽ")]
                l1ll1111l_SBK_ = __SITE__+l1l1l1111_SBK_[l1l111_SBK_ (u"࠭ࡰࡰࡵࡷࡩࡷ࠭ࣾ")]
                l1l1l1l1l_SBK_ = l1l1l1111_SBK_[l1l111_SBK_ (u"ࠧࡪ࡯ࡧࡦࡤ࡯ࡤࠨࣿ")]
                l1l11l111_SBK_ = l1l1l1111_SBK_[l1l111_SBK_ (u"ࠨࡴࡨࡷࡴࡻࡲࡤࡧࡢࡹࡷ࡯ࠧऀ")]
            except:
                pass
            if type == l1l111_SBK_ (u"ࠩࡰࡳࡻ࡯ࡥࠨँ"):
                l1llll11l_SBK_ = l1l1ll1ll_SBK_(__SITE__+l1l111_SBK_ (u"ࠪ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࡲࡵࡶࡪࡧ࠲ࠫं")+l1l1l1l1l_SBK_)
                title = l1llll11l_SBK_[l1l111_SBK_ (u"ࠫࡹ࡯ࡴ࡭ࡧࠪः")]
                year = l1llll11l_SBK_[l1l111_SBK_ (u"ࠬࡿࡥࡢࡴࠪऄ")]
                l1l1l11ll_SBK_ = __SITE__+l1llll11l_SBK_[l1l111_SBK_ (u"࠭ࡣࡰࡸࡨࡶࠬअ")]
                l1ll1111l_SBK_ = __SITE__+l1llll11l_SBK_[l1l111_SBK_ (u"ࠧࡱࡱࡶࡸࡪࡸࠧआ")]
                l1ll11l1l_SBK_ = l1llll11l_SBK_[l1l111_SBK_ (u"ࠨࡱࡹࡩࡷࡼࡩࡦࡹࠪइ")]
                l1l1llll1_SBK_ = l1111lll_SBK_(l1llll11l_SBK_[l1l111_SBK_ (u"ࠩࡪࡩࡳࡸࡥࠨई")])
                l111llll_SBK_ = l1llll11l_SBK_[l1l111_SBK_ (u"ࠪ࡭ࡲࡪࡢࡠࡴࡤࡸ࡮ࡴࡧࠨउ")]
                l1ll11111_SBK_ = l1llll11l_SBK_[l1l111_SBK_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࡳࡷ࠭ऊ")]
                l1l1l1l1l_SBK_ = l1llll11l_SBK_[l1l111_SBK_ (u"ࠬ࡯࡭ࡥࡤࡢ࡭ࡩ࠭ऋ")]
                infoLabels = {l1l111_SBK_ (u"࠭ࡔࡪࡶ࡯ࡩࠬऌ"): title, l1l111_SBK_ (u"࡚ࠧࡧࡤࡶࠬऍ"): year, l1l111_SBK_ (u"ࠨࡉࡨࡲࡷ࡫ࠧऎ"): l1l1llll1_SBK_, l1l111_SBK_ (u"ࠩࡓࡰࡴࡺࠧए"): l1ll11l1l_SBK_, l1l111_SBK_ (u"ࠪࡖࡦࡺࡩ࡯ࡩࠪऐ"): l111llll_SBK_, l1l111_SBK_ (u"ࠫࡉ࡯ࡲࡦࡥࡷࡳࡷ࠭ऑ"): l1ll11111_SBK_ }
                l1l1l11l1_SBK_(l1l111_SBK_ (u"ࠬࡡࡆࡊࡎࡐࡉࡢࠦࠠࠨऒ")+title+l1l111_SBK_ (u"࠭ࠠࠩࠩओ")+year+l1l111_SBK_ (u"ࠧࠪࠩऔ"), l1l1l1l1l_SBK_, 3, l1ll1111l_SBK_, l1l111_SBK_ (u"ࠨࡨ࡬ࡰࡲ࡫ࠧक"), 0, 0, infoLabels, l1ll1111l_SBK_)
            if type == l1l111_SBK_ (u"ࠩࡶࡩࡷ࡯ࡥࠨख"):
                infoLabels = {l1l111_SBK_ (u"ࠪࡘ࡮ࡺ࡬ࡦࠩग"): title, l1l111_SBK_ (u"ࠫ࡞࡫ࡡࡳࠩघ"): year}
                l1lll111l_SBK_(l1l111_SBK_ (u"ࠬࡡࡓࡆࡔࡌࡉࡢࠦࠠࠨङ")+title+ l1l111_SBK_ (u"࠭ࠠࠩࠩच")+year+l1l111_SBK_ (u"ࠧࠪࠩछ"), __SITE__+l1l11l111_SBK_, 4, l1ll1111l_SBK_, l1l111_SBK_ (u"ࠨࡵࡨࡶ࡮࡫ࠧज"), infoLabels, l1ll1111l_SBK_)
        else:
            l1lll111l_SBK_(l1l111_SBK_ (u"ࠩ࠿ࠤ࡛ࡵ࡬ࡵࡣࡵࠫझ"), l1l111_SBK_ (u"ࠪࡹࡷࡲࠧञ"), None, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠫࡵࡸࡥࡷ࡫ࡲࡹࡸ࠴ࡰ࡯ࡩࠪट")))
    l1lll1111_SBK_(l1l111_SBK_ (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࡤࡹࡥࡳ࡫ࡨࡷࠬठ"))
def l1l11l1ll_SBK_():
    __ADDON__.openSettings()
    l1lll111l_SBK_(l1l111_SBK_ (u"࠭ࡅ࡯ࡶࡵࡥࡷࠦ࡮ࡰࡸࡤࡱࡪࡴࡴࡦࠩड"),l1l111_SBK_ (u"ࠧࡶࡴ࡯ࠫढ"),None,os.path.join(__ART_FOLDER__, __SKIN__,l1l111_SBK_ (u"ࠨࡲࡵࡩࡻ࡯࡯ࡶࡵ࠱ࡴࡳ࡭ࠧण")))
    l1lll1111_SBK_(l1l111_SBK_ (u"ࠩࡰࡩࡳࡻࠧत"))
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
def l1lll1111_SBK_(option):
    if option == l1l111_SBK_ (u"ࠪࡱࡴࡼࡩࡦࡵࡢࡷࡪࡸࡩࡦࡵࠪथ"):
        l1ll11ll1_SBK_ = __ADDON__.getSetting(l1l111_SBK_ (u"ࠫ࡫࡯࡬࡮ࡧࡶࡗࡪࡸࡩࡦࡵ࡙࡭ࡪࡽࠧद"))
    elif option == l1l111_SBK_ (u"ࠬࡳࡥ࡯ࡷࠪध"):
        l1ll11ll1_SBK_ = __ADDON__.getSetting(l1l111_SBK_ (u"࠭࡭ࡦࡰࡸ࡚࡮࡫ࡷࠨन"))
    elif option == l1l111_SBK_ (u"ࠧࡴࡧࡤࡷࡴࡴࡳࠨऩ"):
        l1ll11ll1_SBK_ = __ADDON__.getSetting(l1l111_SBK_ (u"ࠨࡵࡨࡥࡸࡵ࡮ࡴࡘ࡬ࡩࡼ࠭प"))
    elif option == l1l111_SBK_ (u"ࠩࡨࡴ࡮ࡹ࡯ࡥࡧࡶࠫफ"):
        l1ll11ll1_SBK_ = __ADDON__.getSetting(l1l111_SBK_ (u"ࠪࡩࡵ࡯ࡳࡰࡦ࡬ࡳࡸ࡜ࡩࡦࡹࠪब"))
    else:
        l1ll11ll1_SBK_ = l1l111_SBK_ (u"ࠫ࠵࠭भ")
    if l1ll11ll1_SBK_:
        if l1ll11ll1_SBK_ == l1l111_SBK_ (u"ࠬ࠶ࠧम"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠨࡃࡰࡰࡷࡥ࡮ࡴࡥࡳ࠰ࡖࡩࡹ࡜ࡩࡦࡹࡐࡳࡩ࡫ࠨ࠶࠲ࠬࠦय"))
        elif l1ll11ll1_SBK_ == l1l111_SBK_ (u"ࠧ࠲ࠩर"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠣࡅࡲࡲࡹࡧࡩ࡯ࡧࡵ࠲ࡘ࡫ࡴࡗ࡫ࡨࡻࡒࡵࡤࡦࠪ࠸࠵࠮ࠨऱ"))
        elif l1ll11ll1_SBK_ == l1l111_SBK_ (u"ࠩ࠵ࠫल"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠥࡇࡴࡴࡴࡢ࡫ࡱࡩࡷ࠴ࡓࡦࡶ࡙࡭ࡪࡽࡍࡰࡦࡨࠬ࠺࠶࠰ࠪࠤळ"))
        elif l1ll11ll1_SBK_ == l1l111_SBK_ (u"ࠫ࠸࠭ऴ"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠧࡉ࡯࡯ࡶࡤ࡭ࡳ࡫ࡲ࠯ࡕࡨࡸ࡛࡯ࡥࡸࡏࡲࡨࡪ࠮࠵࠱࠳ࠬࠦव"))
        elif l1ll11ll1_SBK_ == l1l111_SBK_ (u"࠭࠴ࠨश"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠢࡄࡱࡱࡸࡦ࡯࡮ࡦࡴ࠱ࡗࡪࡺࡖࡪࡧࡺࡑࡴࡪࡥࠩ࠷࠳࠼࠮ࠨष"))
        elif l1ll11ll1_SBK_ == l1l111_SBK_ (u"ࠨ࠷ࠪस"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠤࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡙ࡥࡵࡘ࡬ࡩࡼࡓ࡯ࡥࡧࠫ࠹࠵࠺ࠩࠣह"))
        elif l1ll11ll1_SBK_ == l1l111_SBK_ (u"ࠪ࠺ࠬऺ"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠦࡈࡵ࡮ࡵࡣ࡬ࡲࡪࡸ࠮ࡔࡧࡷ࡚࡮࡫ࡷࡎࡱࡧࡩ࠭࠻࠰࠴ࠫࠥऻ"))
        elif l1ll11ll1_SBK_ == l1l111_SBK_ (u"ࠬ࠽़ࠧ"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠨࡃࡰࡰࡷࡥ࡮ࡴࡥࡳ࠰ࡖࡩࡹ࡜ࡩࡦࡹࡐࡳࡩ࡫ࠨ࠶࠳࠸࠭ࠧऽ"))
def l1111lll_SBK_(list):
    l1ll1l11l_SBK_ = []
    for l1l1llll1_SBK_ in list:
        l1ll1l11l_SBK_.append(l1l1llll1_SBK_[l1l111_SBK_ (u"ࠧ࡯ࡣࡰࡩࠬा")])
    return l1l111_SBK_ (u"ࠨ࠮ࠣࠫि").join(l1ll1l11l_SBK_)
def l1l1ll1ll_SBK_(url, l1l1lll11_SBK_=l1l111_SBK_ (u"ࠩࠪी")):
    l1ll1ll1l_SBK_ = l1l111_SBK_ (u"ࠪࠫु")
    l11111l1_SBK_ = HTMLParser.HTMLParser()
    if l1l1lll11_SBK_:
        email = urllib.quote(l11111l1_SBK_.unescape(__ADDON__.getSetting(l1l111_SBK_ (u"ࠫࡪࡳࡡࡪ࡮ࠪू"))))
        password = urllib.quote(l11111l1_SBK_.unescape(__ADDON__.getSetting(l1l111_SBK_ (u"ࠧࡶࡡࡴࡵࡺࡳࡷࡪࠢृ"))))
        l1ll1ll1l_SBK_ = requests.get(url, params=l1l111_SBK_ (u"࠭࡬ࡰࡩ࡬ࡲࡂ࠭ॄ")+email+l1l111_SBK_ (u"ࠧࠧࡲࡤࡷࡸࡽ࡯ࡳࡦࡀࠫॅ")+password).text
    else:
        username = urllib.quote(l11111l1_SBK_.unescape(__ADDON__.getSetting(l1l111_SBK_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧࠪॆ"))))
        l1ll1ll1l_SBK_ = requests.get(url, params=l1l111_SBK_ (u"ࠩࡤࡴ࡮ࡥ࡫ࡦࡻࡀࠫे")+__ADDON__.getSetting(l1l111_SBK_ (u"ࠪࡥࡵ࡯࡫ࡦࡻࠪै"))+l1l111_SBK_ (u"ࠫࠫࡻࡳࡦࡴࡱࡥࡲ࡫࠽ࠨॉ")+username).text
    return json.loads(l1ll1ll1l_SBK_)
def l1l111ll1_SBK_(name,url,iconimage):
    l1ll1l1l1_SBK_=xbmcgui.ListItem(name, iconImage=l1l111_SBK_ (u"ࠧࡊࡥࡧࡣࡸࡰࡹ࡜ࡩࡥࡧࡲ࠲ࡵࡴࡧࠣॊ"), thumbnailImage=iconimage)
    l1ll1l1l1_SBK_.setProperty(l1l111_SBK_ (u"࠭ࡦࡢࡰࡤࡶࡹࡥࡩ࡮ࡣࡪࡩࠬो"), iconimage)
    l1ll1l1l1_SBK_.setInfo( type=l1l111_SBK_ (u"ࠢࡗ࡫ࡧࡩࡴࠨौ"), infoLabels={ l1l111_SBK_ (u"ࠣࡖ࡬ࡸࡱ࡫्ࠢ"): name } )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=l1ll1l1l1_SBK_)
    return True
def l1lll111l_SBK_(name,url,mode,iconimage,l1l1ll111_SBK_=False,infoLabels=False,l1ll1111l_SBK_=False):
    if infoLabels: infoLabelsAux = infoLabels
    else: infoLabelsAux = {l1l111_SBK_ (u"ࠩࡗ࡭ࡹࡲࡥࠨॎ"): name}
    if l1ll1111l_SBK_: l1llll1l1_SBK_ = l1ll1111l_SBK_
    else: l1llll1l1_SBK_ = iconimage
    u=sys.argv[0]+l1l111_SBK_ (u"ࠥࡃࡺࡸ࡬࠾ࠤॏ")+urllib.quote_plus(url)+l1l111_SBK_ (u"ࠦࠫࡳ࡯ࡥࡧࡀࠦॐ")+str(mode)+l1l111_SBK_ (u"ࠧࠬ࡮ࡢ࡯ࡨࡁࠧ॑")+urllib.quote_plus(name)
    l1lll1ll1_SBK_ = __FANART__
    if l1l1ll111_SBK_ == l1l111_SBK_ (u"࠭ࡦࡪ࡮ࡰࡩ॒ࠬ"):
        l1lll1ll1_SBK_ = l1llll1l1_SBK_
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠧࡎࡱࡹ࡭ࡪࡹࠧ॓"))
    elif l1l1ll111_SBK_ == l1l111_SBK_ (u"ࠨࡵࡨࡶ࡮࡫ࠧ॔"):
        l1lll1ll1_SBK_ = l1llll1l1_SBK_
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪॕ"))
    elif l1l1ll111_SBK_ == l1l111_SBK_ (u"ࠪࡩࡵ࡯ࡳࡰࡦࡨࠫॖ"):
        l1lll1ll1_SBK_ = l1llll1l1_SBK_
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠫࡪࡶࡩࡴࡱࡧࡩࡸ࠭ॗ"))
    else:
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠬࡓ࡯ࡷ࡫ࡨࡷࠬक़"))
    l1ll1l1l1_SBK_=xbmcgui.ListItem(name, iconImage=l1llll1l1_SBK_, thumbnailImage=l1llll1l1_SBK_)
    l1ll1l1l1_SBK_.setProperty(l1l111_SBK_ (u"࠭ࡦࡢࡰࡤࡶࡹࡥࡩ࡮ࡣࡪࡩࠬख़"), l1lll1ll1_SBK_)
    l1ll1l1l1_SBK_.setInfo( type=l1l111_SBK_ (u"ࠢࡗ࡫ࡧࡩࡴࠨग़"), infoLabels=infoLabelsAux )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l1ll1l1l1_SBK_,isFolder=True)
    return True
def l1llll111_SBK_(name,url,mode,iconimage,l1ll1lll1_SBK_):
    u=sys.argv[0]+l1l111_SBK_ (u"ࠣࡁࡸࡶࡱࡃࠢज़")+urllib.quote_plus(url)+l1l111_SBK_ (u"ࠤࠩࡱࡴࡪࡥ࠾ࠤड़")+str(mode)+l1l111_SBK_ (u"ࠥࠪࡳࡧ࡭ࡦ࠿ࠥढ़")+urllib.quote_plus(name)
    l1ll1l1l1_SBK_=xbmcgui.ListItem(name, iconImage=l1l111_SBK_ (u"ࠦ࡫ࡧ࡮ࡢࡴࡷ࠲࡯ࡶࡧࠣफ़"), thumbnailImage=iconimage)
    l1ll1l1l1_SBK_.setProperty(l1l111_SBK_ (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࡤ࡯࡭ࡢࡩࡨࠫय़"), iconimage)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l1ll1l1l1_SBK_,isFolder=l1ll1lll1_SBK_)
    return True
def l1l1ll1l1_SBK_(name,url,mode,iconimage,season):
    u=sys.argv[0]+l1l111_SBK_ (u"ࠨ࠿ࡶࡴ࡯ࡁࠧॠ")+urllib.quote_plus(url)+l1l111_SBK_ (u"ࠢࠧ࡯ࡲࡨࡪࡃࠢॡ")+str(mode)+l1l111_SBK_ (u"ࠣࠨࡱࡥࡲ࡫࠽ࠣॢ")+urllib.quote_plus(name)+l1l111_SBK_ (u"ࠤࠩࡷࡪࡧࡳࡰࡰࡀࠦॣ")+str(season)
    xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠪࡑࡴࡼࡩࡦࡵࠪ।"))
    l1ll1l1l1_SBK_=xbmcgui.ListItem(name, iconImage=l1l111_SBK_ (u"ࠦ࡫ࡧ࡮ࡢࡴࡷ࠲࡯ࡶࡧࠣ॥"), thumbnailImage=iconimage)
    l1ll1l1l1_SBK_.setProperty(l1l111_SBK_ (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࡤ࡯࡭ࡢࡩࡨࠫ०"), __FANART__)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l1ll1l1l1_SBK_,isFolder=True)
    return True
def l1l1l11l1_SBK_(name,url,mode,iconimage,l1l1ll111_SBK_,season,episode,infoLabels,l1ll1111l_SBK_):
    if l1l1ll111_SBK_ == l1l111_SBK_ (u"࠭ࡦࡪ࡮ࡰࡩࠬ१"):
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠧࡎࡱࡹ࡭ࡪࡹࠧ२"))
    elif l1l1ll111_SBK_ == l1l111_SBK_ (u"ࠨࡵࡨࡶ࡮࡫ࠧ३"):
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪ४"))
    elif l1l1ll111_SBK_ == l1l111_SBK_ (u"ࠪࡩࡵ࡯ࡳࡰࡦࡨࠫ५"):
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠫࡪࡶࡩࡴࡱࡧࡩࡸ࠭६"))
    u=sys.argv[0]+l1l111_SBK_ (u"ࠧࡅࡵࡳ࡮ࡀࠦ७")+urllib.quote_plus(url)+l1l111_SBK_ (u"ࠨࠦ࡮ࡱࡧࡩࡂࠨ८")+str(mode)+l1l111_SBK_ (u"ࠢࠧࡵࡨࡥࡸࡵ࡮࠾ࠤ९")+str(season)+l1l111_SBK_ (u"ࠣࠨࡨࡴ࡮ࡹ࡯ࡥࡧࡀࠦ॰")+str(episode)+l1l111_SBK_ (u"ࠤࠩࡲࡦࡳࡥ࠾ࠤॱ")+urllib.quote_plus(name)+l1l111_SBK_ (u"ࠥࠪ࡮ࡩ࡯࡯࡫ࡰࡥ࡬࡫࠽ࠣॲ")+urllib.quote_plus(iconimage)
    l1ll1l1l1_SBK_=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    l1ll1l1l1_SBK_.setProperty(l1l111_SBK_ (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࡣ࡮ࡳࡡࡨࡧࠪॳ"), l1ll1111l_SBK_)
    l1ll1l1l1_SBK_.setInfo( type=l1l111_SBK_ (u"ࠧ࡜ࡩࡥࡧࡲࠦॴ"), infoLabels=infoLabels )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l1ll1l1l1_SBK_,isFolder=False)
    return True
def l1lllll11_SBK_(url,path):
    l1llllll1_SBK_ = requests.get(url).content
    if l1llllll1_SBK_:
        with open(path, l1l111_SBK_ (u"࠭ࡷࠨॵ")) as fh:
            fh.write(l1llllll1_SBK_)
            fh.close()
    return url
def l1l111lll_SBK_(lang):
    if lang == l1l111_SBK_ (u"ࠧࡱࡶࠪॶ"):
        return l1l111_SBK_ (u"ࠨࡒࡲࡶࡹࡻࡧࡶࡧࡶࡩࠬॷ")
    elif lang == l1l111_SBK_ (u"ࠩࡨࡲࠬॸ"):
        return l1l111_SBK_ (u"ࠪࡉࡳ࡭࡬ࡪࡵ࡫ࠫॹ")
    else:
        return None
def l1ll11lll_SBK_(lang):
    l1ll1l1ll_SBK_ = l1l111_SBK_ (u"ࠫ࡮ࡩ࡯࡯࠰ࡳࡲ࡬࠭ॺ")
    language = l1l111_SBK_ (u"ࠬ࠭ॻ")
    if lang == l1l111_SBK_ (u"࠭ࡰࡵࠩॼ"):
        language = l1l111_SBK_ (u"ࠧࡑࡱࡵࡸࡺ࡭ࡵࡦࡵࠪॽ")
        l1ll1l1ll_SBK_ = l1l111_SBK_ (u"ࠨࡲࡲࡶࡹࡻࡧࡶࡧࡶࡩ࠳ࡶ࡮ࡨࠩॾ")
    elif lang == l1l111_SBK_ (u"ࠩࡨࡲࠬॿ"):
        language = l1l111_SBK_ (u"ࠪࡉࡳ࡭࡬ࡪࡵ࡫ࠫঀ")
        l1ll1l1ll_SBK_ = l1l111_SBK_ (u"ࠫࡪࡴࡧ࡭࡫ࡶ࡬࠳ࡶ࡮ࡨࠩঁ")
    else:
        return None
    return xbmc.executebuiltin(l1l111_SBK_ (u"ࠧ࡞ࡂࡎࡅ࠱ࡒࡴࡺࡩࡧ࡫ࡦࡥࡹ࡯࡯࡯ࠪࡖࡩࡲࡈࡩ࡭ࡪࡨࡸࡪ࠴ࡴࡷ࠮ࠣࡐࡪ࡭ࡥ࡯ࡦࡤࠤࡨࡧࡲࡳࡧࡪࡥࡩࡧ࠺ࠡࠤং")+language+l1l111_SBK_ (u"ࠨࠬࠡࠩ࠴࠴࠵࠶࠰ࠨ࠮ࠣࠦঃ")+os.path.join(__ART_FOLDER__, __SKIN__,l1ll1l1ll_SBK_)+l1l111_SBK_ (u"ࠢࠪࠤ঄"))
def l111l1ll_SBK_(name,imdb,iconimage,season,episode,serieNome=l1l111_SBK_ (u"ࠨࠩঅ")):
    l1l11l11l_SBK_ = l1l1ll1ll_SBK_(__SITE__+l1l111_SBK_ (u"ࠩ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡧࡴࡴࡴࡦࡰࡷ࠳ࠬআ")+imdb)
    url = l1l11l11l_SBK_[l1l111_SBK_ (u"ࠪࡹࡷࡲࠧই")]
    l1lll11l1_SBK_ = []
    if len(l1l11l11l_SBK_[l1l111_SBK_ (u"ࠫࡸࡻࡢࡵ࡫ࡷࡰࡪࡹࠧঈ")]) > 0:
        for l111ll1l_SBK_ in l1l11l11l_SBK_[l1l111_SBK_ (u"ࠬࡹࡵࡣࡶ࡬ࡸࡱ࡫ࡳࠨউ")]:
            language = l1l111lll_SBK_(l111ll1l_SBK_[l1l111_SBK_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨঊ")])
            l1111111_SBK_ = os.path.join(xbmc.translatePath(l1l111_SBK_ (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲ࡸࡪࡳࡰࠨঋ")), imdb+l1l111_SBK_ (u"ࠨ࠰ࠪঌ")+language+l1l111_SBK_ (u"ࠩ࠱ࡷࡷࡺࠧ঍"))
            l1lllll11_SBK_(__SITE__+l111ll1l_SBK_[l1l111_SBK_ (u"ࠪࡹࡷࡲࠧ঎")],l1111111_SBK_)
            l1ll11lll_SBK_(l111ll1l_SBK_[l1l111_SBK_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭এ")])
            l1lll11l1_SBK_.append(l1111111_SBK_)
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(name, iconImage=l1l111_SBK_ (u"ࠧࡊࡥࡧࡣࡸࡰࡹ࡜ࡩࡥࡧࡲ࠲ࡵࡴࡧࠣঐ"), thumbnailImage=iconimage)
    listitem.setInfo(l1l111_SBK_ (u"ࠨࡖࡪࡦࡨࡳࠧ঑"), {l1l111_SBK_ (u"ࠢࡵ࡫ࡷࡰࡪࠨ঒"):name})
    listitem.setProperty(l1l111_SBK_ (u"ࠨ࡯࡬ࡱࡪࡺࡹࡱࡧࠪও"), l1l111_SBK_ (u"ࠩࡹ࡭ࡩ࡫࡯࠰ࡺ࠰ࡱࡸࡼࡩࡥࡧࡲࠫঔ"))
    listitem.setProperty(l1l111_SBK_ (u"ࠪࡍࡸࡖ࡬ࡢࡻࡤࡦࡱ࡫ࠧক"), l1l111_SBK_ (u"ࠫࡹࡸࡵࡦࠩখ"))
    playlist.add(url, listitem)
    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
    l111l1ll_SBK_ = Player.Player(url=url, idFilme=imdb, pastaData=l1l111_SBK_ (u"ࠬ࠭গ"), season=season, episode=episode, nome=name, ano=l1l111_SBK_ (u"࠭࠲࠱࠳࠸ࠫঘ"), logo=os.path.join(__ADDON_FOLDER__,l1l111_SBK_ (u"ࠧࡪࡥࡲࡲ࠳ࡶ࡮ࡨࠩঙ")), serieNome=l1l111_SBK_ (u"ࠨࠩচ"))
    l111l1ll_SBK_.play(playlist)
    if len(l1lll11l1_SBK_) > 0:
        for l111ll11_SBK_ in l1lll11l1_SBK_:
            l111l1ll_SBK_.setSubtitles(l111ll11_SBK_)
def get_params():
    param=[]
    l1lllll1l_SBK_=sys.argv[2]
    if len(l1lllll1l_SBK_)>=2:
        params=sys.argv[2]
        l1l1l111l_SBK_=params.replace(l1l111_SBK_ (u"ࠩࡂࠫছ"),l1l111_SBK_ (u"ࠪࠫজ"))
        if (params[len(params)-1]==l1l111_SBK_ (u"ࠫ࠴࠭ঝ")): params=params[0:len(params)-2]
        l111l1l1_SBK_=l1l1l111l_SBK_.split(l1l111_SBK_ (u"ࠬࠬࠧঞ"))
        param={}
        for i in range(len(l111l1l1_SBK_)):
            l111l11l_SBK_={}
            l111l11l_SBK_=l111l1l1_SBK_[i].split(l1l111_SBK_ (u"࠭࠽ࠨট"))
            if (len(l111l11l_SBK_))==2: param[l111l11l_SBK_[0]]=l111l11l_SBK_[1]
    return param
def main():
    params=get_params()
    url=None
    name=None
    mode=None
    iconimage=None
    link=None
    l1ll111ll_SBK_=None
    l1l11ll1l_SBK_=None
    season=None
    episode=None
    try: url=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠢࡶࡴ࡯ࠦঠ")])
    except: pass
    try: link=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠣ࡮࡬ࡲࡰࠨড")])
    except: pass
    try: l1ll111ll_SBK_=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠤ࡯ࡩ࡬࡫࡮ࡥࡣࠥঢ")])
    except: pass
    try: name=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠥࡲࡦࡳࡥࠣণ")])
    except: pass
    try: season=int(params[l1l111_SBK_ (u"ࠦࡸ࡫ࡡࡴࡱࡱࠦত")])
    except: pass
    try: episode=int(params[l1l111_SBK_ (u"ࠧ࡫ࡰࡪࡵࡲࡨࡪࠨথ")])
    except: pass
    try: mode=int(params[l1l111_SBK_ (u"ࠨ࡭ࡰࡦࡨࠦদ")])
    except: pass
    try: l1l11ll1l_SBK_=int(params[l1l111_SBK_ (u"ࠢࡱࡣࡪ࡭ࡳࡧࠢধ")])
    except: pass
    try: iconimage=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠣ࡫ࡦࡳࡳ࡯࡭ࡢࡩࡨࠦন")])
    except: pass
    try : serieNome=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠤࡶࡩࡷ࡯ࡥࡏࡱࡰࡩࠧ঩")])
    except: pass
    if mode==None or url==None or len(url)<1: l1lll1l1l_SBK_()
    elif mode==1: l1l1lllll_SBK_(url)
    elif mode==12: l1111l11_SBK_(url)
    elif mode==2: l111l111_SBK_(url, l1l11ll1l_SBK_)
    elif mode==3: l111l1ll_SBK_(name, url, iconimage, season, episode, serieNome=l1l111_SBK_ (u"ࠪࠫপ"))
    elif mode==4: l1l11l1l1_SBK_(url)
    elif mode==5: l11111ll_SBK_(url)
    elif mode==9: l1l11ll11_SBK_(url)
    elif mode==6: l1l1l1l11_SBK_()
    elif mode==1000: l1l11l1ll_SBK_()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
if __name__ == l1l111_SBK_ (u"ࠦࡤࡥ࡭ࡢ࡫ࡱࡣࡤࠨফ"):
    main()