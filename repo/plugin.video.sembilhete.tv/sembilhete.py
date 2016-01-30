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
def l1lll1ll1_SBK_():
    l1ll111ll_SBK_ = l1l1lll1l_SBK_()
    if l1ll111ll_SBK_:
        l1lll11l1_SBK_(l1l111_SBK_ (u"ࠪࡊ࡮ࡲ࡭ࡦࡵࠪࡨ"), __SITE__+l1l111_SBK_ (u"ࠫ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡳ࡯ࡷ࡫ࡨ࠳ࡄࡲࡩ࡮࡫ࡷࡁ࠶࠹ࠧࡩ"), 1, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠬࡳ࡯ࡷ࡫ࡨࡷ࠳ࡶ࡮ࡨࠩࡪ")))
        l1lll11l1_SBK_(l1l111_SBK_ (u"࠭ࡓ࣪ࡴ࡬ࡩࡸ࠭࡫"), __SITE__+l1l111_SBK_ (u"ࠧ࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡨࡶ࡮࡫࠯ࡀ࡮࡬ࡱ࡮ࡺ࠽࠲࠵ࠪ࡬"), 12, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠨࡵࡨࡶ࡮࡫ࡳ࠯ࡲࡱ࡫ࠬ࡭")))
        l1lll11l1_SBK_(l1l111_SBK_ (u"ࠩࠪ࡮"), l1l111_SBK_ (u"ࠪࠫ࡯"), l1l111_SBK_ (u"ࠫࠬࡰ"), os.path.join(__ADDON_FOLDER__,l1l111_SBK_ (u"ࠬ࡯ࡣࡰࡰ࠱࡮ࡵ࡭ࠧࡱ")), 0)
        l1lll11l1_SBK_(l1l111_SBK_ (u"࠭ࡌࡪࡵࡷࡥࡷࠦࡆࡪ࡮ࡰࡩࡸ࠭ࡲ"), l1l111_SBK_ (u"ࠧࡶࡴ࡯ࠫࡳ"), 9, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠨ࡯ࡲࡺ࡮࡫ࡳ࠯ࡲࡱ࡫ࠬࡴ")))
        l1lll11l1_SBK_(l1l111_SBK_ (u"ࠩࡓࡩࡸࡷࡵࡪࡵࡤࠫࡵ"), __SITE__, 6, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠪࡷࡪࡧࡲࡤࡪ࠱ࡴࡳ࡭ࠧࡶ")))
        l1lll11l1_SBK_(l1l111_SBK_ (u"ࠫࠬࡷ"), l1l111_SBK_ (u"ࠬ࠭ࡸ"), l1l111_SBK_ (u"࠭ࠧࡹ"), os.path.join(__ADDON_FOLDER__,l1l111_SBK_ (u"ࠧࡪࡥࡲࡲ࠳ࡰࡰࡨࠩࡺ")), 0)
        l1lll11l1_SBK_(l1l111_SBK_ (u"ࠨࡆࡨࡪ࡮ࡴࡩࣨࣷࡨࡷࠬࡻ"), l1l111_SBK_ (u"ࠩࡸࡶࡱ࠭ࡼ"), 1000, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷ࠳ࡶ࡮ࡨࠩࡽ")))
        l1lll111l_SBK_(l1l111_SBK_ (u"ࠫࡲ࡫࡮ࡶࠩࡾ"))
    else:
        l1lll11l1_SBK_(l1l111_SBK_ (u"ࠬࡇ࡬ࡵࡧࡵࡥࡷࠦࡄࡦࡨ࡬ࡲ࡮࣭ࣵࡦࡵࠪࡿ"), l1l111_SBK_ (u"࠭ࡵࡳ࡮ࠪࢀ"), 1000, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴ࠰ࡳࡲ࡬࠭ࢁ")))
        l1lll11l1_SBK_(l1l111_SBK_ (u"ࠨࡇࡱࡸࡷࡧࡲࠡࡰࡲࡺࡦࡳࡥ࡯ࡶࡨࠫࢂ"), l1l111_SBK_ (u"ࠩࡸࡶࡱ࠭ࢃ"), None, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠪࡴࡷ࡫ࡶࡪࡱࡸࡷ࠳ࡶ࡮ࡨࠩࢄ")))
        l1lll111l_SBK_(l1l111_SBK_ (u"ࠫࡲ࡫࡮ࡶࠩࢅ"))
l1l111_SBK_ (u"ࠬ࠭ࠧࠋࡦࡨࡪࠥࡳࡩ࡯ࡪࡤࡇࡴࡴࡴࡢࠪࠬ࠾ࠏࠦࠠࠡࠢࡤࡨࡩࡊࡩࡳࠪࠪࡊࡦࡼ࡯ࡳ࡫ࡷࡳࡸ࠭ࠬࠡࡡࡢࡗࡎ࡚ࡅࡠࡡ࠮ࠫࠬ࠲ࠠ࠲࠳࠯ࠤࡴࡹ࠮ࡱࡣࡷ࡬࠳ࡰ࡯ࡪࡰࠫࡣࡤࡇࡒࡕࡡࡉࡓࡑࡊࡅࡓࡡࡢ࠰ࠥࡥ࡟ࡔࡍࡌࡒࡤࡥࠬࠡࠩࡩࡥࡻࡵࡲࡪࡶࡲࡷ࠳ࡶ࡮ࡨࠩࠬ࠭ࠏࠦࠠࠡࠢࡤࡨࡩࡊࡩࡳࠪࠪࡅ࡬࡫࡮ࡥࡣࡧࡳࡸ࠭ࠬࠡࡡࡢࡗࡎ࡚ࡅࡠࡡ࠮ࠫࠬ࠲ࠠ࠲࠳࠯ࠤࡴࡹ࠮ࡱࡣࡷ࡬࠳ࡰ࡯ࡪࡰࠫࡣࡤࡇࡒࡕࡡࡉࡓࡑࡊࡅࡓࡡࡢ࠰ࠥࡥ࡟ࡔࡍࡌࡒࡤࡥࠬࠡࠩࡤ࡫ࡪࡴࡤࡢࡦࡲࡷ࠳ࡶ࡮ࡨࠩࠬ࠭ࠏࠦࠠࠡࠢࡤࡨࡩࡊࡩࡳࠪࠪࣞࡱࡺࡩ࡮ࡱࡶࠤࡋ࡯࡬࡮ࡧࡶࠤ࡛࡯ࡳࡵࡱࡶࠫ࠱ࠦ࡟ࡠࡕࡌࡘࡊࡥ࡟ࠬࠩࠪ࠰ࠥ࠷࠱࠭ࠢࡲࡷ࠳ࡶࡡࡵࡪ࠱࡮ࡴ࡯࡮ࠩࡡࡢࡅࡗ࡚࡟ࡇࡑࡏࡈࡊࡘ࡟ࡠ࠮ࠣࡣࡤ࡙ࡋࡊࡐࡢࡣ࠱ࠦࠧࡶ࡮ࡷ࡭ࡲࡵࡳ࠯ࡲࡱ࡫ࠬ࠯ࠩࠋࠢࠣࠤࠥࡼࡩࡦࡹࡢࡴࡦ࡭ࡥࠩࠩࡰࡩࡳࡻࠧࠪࠌࠪࠫࠬࢆ")
def l1l1lll1l_SBK_():
    l1l1l1lll_SBK_ = l1l1lll11_SBK_(__SITE__+l1l111_SBK_ (u"࠭࠯ࡢࡲ࡬࠳ࡻ࠷࠯࡭ࡱࡪ࡭ࡳ࠵࠿࡭ࡱࡪ࡭ࡳࡃࠧࢇ")+__ADDON__.getSetting(l1l111_SBK_ (u"ࠧࡦ࡯ࡤ࡭ࡱ࠭࢈"))+l1l111_SBK_ (u"ࠨࠨࡳࡥࡸࡹࡷࡰࡴࡧࡁࠬࢉ")+__ADDON__.getSetting(l1l111_SBK_ (u"ࠤࡳࡥࡸࡹࡷࡰࡴࡧࠦࢊ")))
    if __ADDON__.getSetting(l1l111_SBK_ (u"ࠥࡴࡦࡹࡳࡸࡱࡵࡨࠧࢋ")) == l1l111_SBK_ (u"ࠫࠬࢌ") or __ADDON__.getSetting(l1l111_SBK_ (u"ࠬ࡫࡭ࡢ࡫࡯ࠫࢍ")) == l1l111_SBK_ (u"࠭ࠧࢎ"):
        __ALERTA__(l1l111_SBK_ (u"ࠧࡔࡧࡰࡆ࡮ࡲࡨࡦࡶࡨ࠲ࡹࡼࠧ࢏"), l1l111_SBK_ (u"ࠨࡒࡵࡩࡨ࡯ࡳࡢࠢࡧࡩࠥࡪࡥࡧ࡫ࡱ࡭ࡷࠦࡵ࡮ࡣࠣࡧࡴࡴࡴࡢ࠰ࠪ࢐"))
        return False
    else:
        try:
            l1l1l1lll_SBK_ = l1l1lll11_SBK_(__SITE__+l1l111_SBK_ (u"ࠩ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡰࡴ࡭ࡩ࡯࠱ࡂࡰࡴ࡭ࡩ࡯࠿ࠪ࢑")+__ADDON__.getSetting(l1l111_SBK_ (u"ࠪࡩࡲࡧࡩ࡭ࠩ࢒"))+l1l111_SBK_ (u"ࠫࠫࡶࡡࡴࡵࡺࡳࡷࡪ࠽ࠨ࢓")+__ADDON__.getSetting(l1l111_SBK_ (u"ࠧࡶࡡࡴࡵࡺࡳࡷࡪࠢ࢔")))
        except:
            __ALERTA__(l1l111_SBK_ (u"࠭ࡓࡦ࡯ࡅ࡭ࡱ࡮ࡥࡵࡧ࠱ࡸࡻ࠭࢕"), l1l111_SBK_ (u"ࠧࡏࣥࡲࠤ࡫ࡵࡩࠡࡲࡲࡷࡸࣳࡶࡦ࡮ࠣࡥࡧࡸࡩࡳࠢࡤࠤࡵࣧࡧࡪࡰࡤ࠲ࠥࡖ࡯ࡳࠢࡩࡥࡻࡵࡲࠡࡶࡨࡲࡹ࡫ࠠ࡯ࡱࡹࡥࡲ࡫࡮ࡵࡧࠪ࢖"))
            return False
        else:
            try:
                l1l1l1lll_SBK_[l1l111_SBK_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧࠪࢗ")]
            except:
                __ALERTA__(l1l111_SBK_ (u"ࠩࡖࡩࡲࡈࡩ࡭ࡪࡨࡸࡪ࠴ࡴࡷࠩ࢘"), l1l111_SBK_ (u"ࠪࡉࡲࡧࡩ࡭ࠢࡨ࠳ࡴࡻࠠࡑࡣࡶࡷࡼࡵࡲࡥࠢ࡬ࡲࡨࡵࡲࡳࡧࡷࡳࡸ࢙࠭"))
                return False
            else:
                __ADDON__.setSetting(l1l111_SBK_ (u"ࠫࡦࡶࡩ࡬ࡧࡼ࢚ࠫ"), l1l1l1lll_SBK_[l1l111_SBK_ (u"ࠬࡧࡰࡪࡡ࡮ࡩࡾ࢛࠭")])
                __ADDON__.setSetting(l1l111_SBK_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨ࢜"), l1l1l1lll_SBK_[l1l111_SBK_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ࢝")])
                xbmc.executebuiltin(l1l111_SBK_ (u"࡚ࠣࡅࡑࡈ࠴ࡎࡰࡶ࡬ࡪ࡮ࡩࡡࡵ࡫ࡲࡲ࡙࠭ࡥ࡮ࡄ࡬ࡰ࡭࡫ࡴࡦ࠰ࡷࡺ࠱ࠦࡓࡦࡵࡶࡥࡴࠦࡩ࡯࡫ࡦ࡭ࡦࡪࡡࠡࡥࡲࡱࡴࡀࠠࠣ࢞")+l1l1l1lll_SBK_[l1l111_SBK_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ࢟")]+l1l111_SBK_ (u"ࠥ࠰ࠥ࠭࠱࠱࠲࠳࠴ࠬ࠲ࠠࠣࢠ")+__ADDON_FOLDER__+l1l111_SBK_ (u"ࠦ࠴࡯ࡣࡰࡰ࠱ࡴࡳ࡭ࠩࠣࢡ"))
                return True
def l1ll11111_SBK_(url):
    l1l1l1111_SBK_ = l1l1lll11_SBK_(url)
    l111lll1_SBK_ = l1l1l1111_SBK_[l1l111_SBK_ (u"ࠬࡳࡥࡵࡣࠪࢢ")][l1l111_SBK_ (u"࠭࡮ࡦࡺࡷࠫࢣ")]
    l1llll111_SBK_ = l1l1l1111_SBK_[l1l111_SBK_ (u"ࠧ࡮ࡧࡷࡥࠬࢤ")][l1l111_SBK_ (u"ࠨࡲࡵࡩࡻ࡯࡯ࡶࡵࠪࢥ")]
    for l1l11l1l1_SBK_ in l1l1l1111_SBK_[l1l111_SBK_ (u"ࠩࡲࡦ࡯࡫ࡣࡵࡵࠪࢦ")]:
            l1llll1l1_SBK_ = l1l1lll11_SBK_(__SITE__+l1l111_SBK_ (u"ࠪ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࡲࡵࡶࡪࡧ࠲ࠫࢧ")+l1l11l1l1_SBK_[l1l111_SBK_ (u"ࠫ࡮ࡳࡤࡣࡡ࡬ࡨࠬࢨ")])
            try:
                title = l1llll1l1_SBK_[l1l111_SBK_ (u"ࠬࡺࡩࡵ࡮ࡨࠫࢩ")]
                year = l1llll1l1_SBK_[l1l111_SBK_ (u"࠭ࡹࡦࡣࡵࠫࢪ")]
                l1l1l1l11_SBK_ = __SITE__+l1llll1l1_SBK_[l1l111_SBK_ (u"ࠧࡤࡱࡹࡩࡷ࠭ࢫ")]
                l1ll111l1_SBK_ = __SITE__+l1llll1l1_SBK_[l1l111_SBK_ (u"ࠨࡲࡲࡷࡹ࡫ࡲࠨࢬ")]
                l1ll11ll1_SBK_ = l1llll1l1_SBK_[l1l111_SBK_ (u"ࠩࡲࡺࡪࡸࡶࡪࡧࡺࠫࢭ")]
                l1l1lllll_SBK_ = l1111lll_SBK_(l1llll1l1_SBK_[l1l111_SBK_ (u"ࠪ࡫ࡪࡴࡲࡦࠩࢮ")])
                l111llll_SBK_ = l1llll1l1_SBK_[l1l111_SBK_ (u"ࠫ࡮ࡳࡤࡣࡡࡵࡥࡹ࡯࡮ࡨࠩࢯ")]
                l1ll1111l_SBK_ = l1llll1l1_SBK_[l1l111_SBK_ (u"ࠬࡪࡩࡳࡧࡦࡸࡴࡸࠧࢰ")]
                l1l1l1ll1_SBK_ = l1llll1l1_SBK_[l1l111_SBK_ (u"࠭ࡩ࡮ࡦࡥࡣ࡮ࡪࠧࢱ")]
                infoLabels = {l1l111_SBK_ (u"ࠧࡕ࡫ࡷࡰࡪ࠭ࢲ"): title, l1l111_SBK_ (u"ࠨ࡛ࡨࡥࡷ࠭ࢳ"): year, l1l111_SBK_ (u"ࠩࡊࡩࡳࡸࡥࠨࢴ"): l1l1lllll_SBK_, l1l111_SBK_ (u"ࠪࡔࡱࡵࡴࠨࢵ"): l1ll11ll1_SBK_, l1l111_SBK_ (u"ࠫࡗࡧࡴࡪࡰࡪࠫࢶ"): l111llll_SBK_, l1l111_SBK_ (u"ࠬࡊࡩࡳࡧࡦࡸࡴࡸࠧࢷ"): l1ll1111l_SBK_}
                l1l1l11ll_SBK_(title+l1l111_SBK_ (u"࠭ࠠࠩࠩࢸ")+year+l1l111_SBK_ (u"ࠧࠪࠩࢹ"), l1l1l1ll1_SBK_, 3, l1ll111l1_SBK_, l1l111_SBK_ (u"ࠨࡨ࡬ࡰࡲ࡫ࠧࢺ"), 0, 0, infoLabels, l1l1l1l11_SBK_)
            except:
                pass
    l1lll11l1_SBK_(l1l111_SBK_ (u"ࠩࡓࡶࡴࡾࡩ࡮ࡱࠣࡂࠬࢻ"), __SITE__+l111lll1_SBK_, 1, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠪࡲࡪࡾࡴ࠯ࡲࡱ࡫ࠬࢼ")))
    l1lll111l_SBK_(l1l111_SBK_ (u"ࠫࡲࡵࡶࡪࡧࡶࡣࡸ࡫ࡲࡪࡧࡶࠫࢽ"))
def l1111l11_SBK_(url):
    l11111l1_SBK_ = l1l1lll11_SBK_(url)
    l111lll1_SBK_ = l11111l1_SBK_[l1l111_SBK_ (u"ࠬࡳࡥࡵࡣࠪࢾ")][l1l111_SBK_ (u"࠭࡮ࡦࡺࡷࠫࢿ")]
    l1llll111_SBK_ = l11111l1_SBK_[l1l111_SBK_ (u"ࠧ࡮ࡧࡷࡥࠬࣀ")][l1l111_SBK_ (u"ࠨࡲࡵࡩࡻ࡯࡯ࡶࡵࠪࣁ")]
    for l1lllll11_SBK_ in l11111l1_SBK_[l1l111_SBK_ (u"ࠩࡲࡦ࡯࡫ࡣࡵࡵࠪࣂ")]:
        try:
            title = l1lllll11_SBK_[l1l111_SBK_ (u"ࠪࡸ࡮ࡺ࡬ࡦࠩࣃ")]
            l1ll1l11l_SBK_ = l1lllll11_SBK_[l1l111_SBK_ (u"ࠫࡸࡺࡡࡳࡶࡢࡽࡪࡧࡲࠨࣄ")]
            l1ll111l1_SBK_ = __SITE__+l1lllll11_SBK_[l1l111_SBK_ (u"ࠬࡶ࡯ࡴࡶࡨࡶࠬࣅ")]
            l1l11l11l_SBK_ = l1lllll11_SBK_[l1l111_SBK_ (u"࠭ࡲࡦࡵࡲࡹࡷࡩࡥࡠࡷࡵ࡭ࠬࣆ")]
            infoLabels = {l1l111_SBK_ (u"ࠧࡕ࡫ࡷࡰࡪ࠭ࣇ"):title, l1l111_SBK_ (u"ࠨ࡛ࡨࡥࡷ࠭ࣈ"):l1ll1l11l_SBK_}
            l1lll11l1_SBK_(title+ l1l111_SBK_ (u"ࠩࠣࠬࠬࣉ")+l1ll1l11l_SBK_+l1l111_SBK_ (u"ࠪ࠭ࠬ࣊"), __SITE__+l1l11l11l_SBK_, 4, l1ll111l1_SBK_, l1l111_SBK_ (u"ࠫࡸ࡫ࡲࡪࡧࠪ࣋"), infoLabels, l1ll111l1_SBK_)
        except:
            pass
    l1lll11l1_SBK_(l1l111_SBK_ (u"ࠬࡖࡲࡰࡺ࡬ࡱࡴࠦ࠾ࠨ࣌"), __SITE__+l111lll1_SBK_, 12, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"࠭࡮ࡦࡺࡷ࠲ࡵࡴࡧࠨ࣍")))
    l1lll111l_SBK_(l1l111_SBK_ (u"ࠧ࡮ࡱࡹ࡭ࡪࡹ࡟ࡴࡧࡵ࡭ࡪࡹࠧ࣎"))
def l1l11l1ll_SBK_(url):
    l1111l1l_SBK_ = l1l1lll11_SBK_(url)
    l1ll111l1_SBK_ = __SITE__+l1111l1l_SBK_[l1l111_SBK_ (u"ࠨࡲࡲࡷࡹ࡫ࡲࠨ࣏")]
    for season in l1111l1l_SBK_[l1l111_SBK_ (u"ࠩࡶࡩࡦࡹ࡯࡯ࡵ࣐ࠪ")]:
        l1l11llll_SBK_ = str(season[l1l111_SBK_ (u"ࠪࡷࡪࡧࡳࡰࡰࡢࡲࡺࡳࡢࡦࡴ࣑ࠪ")])
        l1lll1111_SBK_ = season[l1l111_SBK_ (u"ࠫࡷ࡫ࡳࡰࡷࡵࡧࡪࡥࡵࡳ࡫࣒ࠪ")]
        l1l1ll1ll_SBK_(l1l111_SBK_ (u"ࠧࡡࡂ࡞ࡖࡨࡱࡵࡵࡲࡢࡦࡤ࡟࠴ࡈ࡝ࠡࠤ࣓")+l1l11llll_SBK_, __SITE__+l1lll1111_SBK_, 5, l1ll111l1_SBK_, l1l11llll_SBK_)
    l1lll111l_SBK_(l1l111_SBK_ (u"࠭ࡳࡦࡣࡶࡳࡳࡹࠧࣔ"))
def l11111ll_SBK_(url):
    l1l1ll1l1_SBK_ = l1l1lll11_SBK_(url)
    l1l11llll_SBK_ = l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠧࡴࡧࡤࡷࡴࡴ࡟࡯ࡷࡰࡦࡪࡸࠧࣕ")]
    for episode in l1l1ll1l1_SBK_[l1l111_SBK_ (u"ࠨࡧࡳ࡭ࡸࡵࡤࡦࡵࠪࣖ")]:
        title = episode[l1l111_SBK_ (u"ࠩࡱࡥࡲ࡫ࠧࣗ")]
        l1lll1l1l_SBK_ = episode[l1l111_SBK_ (u"ࠪࡩࡵ࡯ࡳࡰࡦࡨࡣࡳࡻ࡭ࡣࡧࡵࠫࣘ")]
        l1l1l1ll1_SBK_ = episode[l1l111_SBK_ (u"ࠫ࡮ࡳࡤࡣࡡ࡬ࡨࠬࣙ")]
        try:
            l1111111_SBK_ = __SITE__+episode[l1l111_SBK_ (u"ࠬࡹࡴࡪ࡮࡯ࠫࣚ")]
        except:
            l1111111_SBK_ = __SITE__+l1l111_SBK_ (u"࠭࠯ࡴࡶࡤࡸ࡮ࡩ࠯ࡪ࡯ࡪ࠳ࡩ࡫ࡦࡢࡷ࡯ࡸࡤࡹࡴࡪ࡮࡯࠲ࡵࡴࡧࠨࣛ")
        l1ll11ll1_SBK_ = episode[l1l111_SBK_ (u"ࠧࡰࡸࡨࡶࡻ࡯ࡥࡸࠩࣜ")]
        l1lll1l11_SBK_ = episode[l1l111_SBK_ (u"ࠨࡣ࡬ࡶࡤࡪࡡࡵࡧࠪࣝ")]
        infoLabels = {l1l111_SBK_ (u"ࠩࡗ࡭ࡹࡲࡥࠨࣞ"):title, l1l111_SBK_ (u"ࠪࡔࡱࡵࡴࠨࣟ"):l1ll11ll1_SBK_, l1l111_SBK_ (u"ࠫࡘ࡫ࡡࡴࡱࡱࠫ࣠"):l1l11llll_SBK_, l1l111_SBK_ (u"ࠬࡋࡰࡪࡵࡲࡨࡪ࠭࣡"):l1lll1l1l_SBK_, l1l111_SBK_ (u"࠭ࡁࡪࡴࡨࡨࠬ࣢"):l1lll1l11_SBK_}
        l1l1l11ll_SBK_(l1l111_SBK_ (u"ࠧ࡜ࡄࡠࡉࡵ࡯ࡳࡰࡦ࡬ࡳࣣࠥ࠭")+str(l1lll1l1l_SBK_)+l1l111_SBK_ (u"ࠨ࡝࠲ࡆࡢࠦࡼࠡࠩࣤ")+title, l1l1l1ll1_SBK_, 3, l1111111_SBK_, l1l111_SBK_ (u"ࠩࡨࡴ࡮ࡹ࡯ࡥࡧࠪࣥ"), l1l11llll_SBK_, l1lll1l1l_SBK_, infoLabels, l1111111_SBK_)
    l1lll111l_SBK_(l1l111_SBK_ (u"ࠪࡩࡵ࡯ࡳࡰࡦࡨࡷࣦࠬ"))
def l1l11ll1l_SBK_(url):
    l1ll11l1l_SBK_ = [(l1l111_SBK_ (u"ࠫࡳ࡫ࡷࡦࡵࡷ࠱ࡦࡪࡤࡦࡦࠪࣧ"),l1l111_SBK_ (u"ࠬࡡࡎࡐࡘࡒࡗࡢࠦࡒࡦࡥࡨࡲࡹ࡫ࡳࠨࣨ")),
                (l1l111_SBK_ (u"࠭࡯࡭ࡦࡨࡷࡹ࠳ࡡࡥࡦࡨࡨࣩࠬ"), l1l111_SBK_ (u"ࠧ࡜ࡐࡒ࡚ࡔ࡙࡝ࠡࡃࡱࡸ࡮࡭࡯ࡴࠩ࣪")),
                (l1l111_SBK_ (u"ࠨࡰࡨࡻࡪࡹࡴ࠮ࡻࡨࡥࡷ࠭࣫"),l1l111_SBK_ (u"ࠩ࡞ࡅࡓࡕ࡝ࠡࡔࡨࡧࡪࡴࡴࡦࡵࠪ࣬")),
                (l1l111_SBK_ (u"ࠪࡳࡱࡪࡥࡴࡶ࠰ࡽࡪࡧࡲࠨ࣭"),l1l111_SBK_ (u"ࠫࡠࡇࡎࡐ࡟ࠣࡅࡳࡺࡩࡨࡱࡶ࣮ࠫ")),
                (l1l111_SBK_ (u"ࠬࡨࡥࡴࡶ࠰ࡶࡦࡺࡩ࡯ࡩ࣯ࠪ"),l1l111_SBK_ (u"࡛࠭ࡄࡎࡄࡗࡘࡏࡆࡊࡅࡄ࣋ࣈࡕ࡝ࠡࡏࡨࡰ࡭ࡵࡲࠨࣰ")),
                (l1l111_SBK_ (u"ࠧࡸࡱࡵࡷࡪ࠳ࡲࡢࡶ࡬ࡲ࡬ࣱ࠭"),l1l111_SBK_ (u"ࠨ࡝ࡆࡐࡆ࡙ࡓࡊࡈࡌࡇࡆ࣍ࣃࡐ࡟ࠣࡔ࡮ࡵࡲࠨࣲ")),
                (l1l111_SBK_ (u"ࠩࡰࡳࡸࡺ࠭ࡷ࡫ࡨࡻࡪࡪࠧࣳ"),l1l111_SBK_ (u"ࠪ࡟࡛ࡏ࡚ࡖࡃࡏࡍ࡟ࡇࣇࣖࡇࡖࡡࠥࡓࡡࡪࡵ࡚ࠣ࡮ࡹࡴࡰࡵࠪࣴ")),
                (l1l111_SBK_ (u"ࠫࡱ࡫ࡳࡴ࠯ࡹ࡭ࡪࡽࡥࡥࠩࣵ"),l1l111_SBK_ (u"ࠬࡡࡖࡊ࡜ࡘࡅࡑࡏ࡚ࡂࣉࣘࡉࡘࡣࠠࡎࡧࡱࡳࡸࠦࡖࡪࡵࡷࡳࡸࣶ࠭"))]
    for l1lll1ll1_SBK_ in l1ll11l1l_SBK_:
        l1l1ll1ll_SBK_(l1lll1ll1_SBK_[1], __SITE__+l1l111_SBK_ (u"࠭࠯ࡢࡲ࡬࠳ࡻ࠷࠯࡮ࡱࡹ࡭ࡪ࠵࠿࡭࡫ࡰ࡭ࡹࡃ࠱࠴ࠨࡲࡶࡩ࡫ࡲࡠࡤࡼࡁࠬࣷ")+l1lll1ll1_SBK_[0], 1, l1l111_SBK_ (u"ࠧࠨࣸ"), l1l111_SBK_ (u"ࠨࣹࠩ"))
    l1lll111l_SBK_(l1l111_SBK_ (u"ࠩࡰࡩࡳࡻࣺࠧ"))
def l1l1l1l1l_SBK_():
    l1l1ll111_SBK_ = xbmc.Keyboard(l1l111_SBK_ (u"ࠪࠫࣻ"), l1l111_SBK_ (u"ࠫࡔࠦࡱࡶࡧࠣࡵࡺ࡫ࡲࠡࡲࡨࡷࡶࡻࡩࡴࡣࡵࡃࠬࣼ"))
    l1l1ll111_SBK_.doModal()
    if l1l1ll111_SBK_.isConfirmed():
        l1l1llll1_SBK_ = l1l1ll111_SBK_.getText()
        l1111ll1_SBK_ = l1l1lll11_SBK_(__SITE__+l1l111_SBK_ (u"ࠬ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡦࡣࡵࡧ࡭࠵࠿ࡲࡷࡨࡶࡾࡃࠧࣽ")+l1l1llll1_SBK_+l1l111_SBK_ (u"࠭ࠦ࡭࡫ࡰ࡭ࡹࡃ࠱࠱ࠩࣾ"))
        for l1l1l111l_SBK_ in l1111ll1_SBK_[l1l111_SBK_ (u"ࠧࡰࡤ࡭ࡩࡨࡺࡳࠨࣿ")]:
            try:
                title = l1l1l111l_SBK_[l1l111_SBK_ (u"ࠨࡶ࡬ࡸࡱ࡫ࠧऀ")]
                year = l1l1l111l_SBK_[l1l111_SBK_ (u"ࠩࡧࡥࡹ࡫ࠧँ")]
                type = l1l1l111l_SBK_[l1l111_SBK_ (u"ࠪࡸࡾࡶࡥࠨं")]
                l1ll111l1_SBK_ = __SITE__+l1l1l111l_SBK_[l1l111_SBK_ (u"ࠫࡵࡵࡳࡵࡧࡵࠫः")]
                l1l1l1ll1_SBK_ = l1l1l111l_SBK_[l1l111_SBK_ (u"ࠬ࡯࡭ࡥࡤࡢ࡭ࡩ࠭ऄ")]
                l1l11l11l_SBK_ = l1l1l111l_SBK_[l1l111_SBK_ (u"࠭ࡲࡦࡵࡲࡹࡷࡩࡥࡠࡷࡵ࡭ࠬअ")]
            except:
                pass
            if type == l1l111_SBK_ (u"ࠧ࡮ࡱࡹ࡭ࡪ࠭आ"):
                l1llll1l1_SBK_ = l1l1lll11_SBK_(__SITE__+l1l111_SBK_ (u"ࠨ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡰࡳࡻ࡯ࡥ࠰ࠩइ")+l1l1l1ll1_SBK_)
                title = l1llll1l1_SBK_[l1l111_SBK_ (u"ࠩࡷ࡭ࡹࡲࡥࠨई")]
                year = l1llll1l1_SBK_[l1l111_SBK_ (u"ࠪࡽࡪࡧࡲࠨउ")]
                l1l1l1l11_SBK_ = __SITE__+l1llll1l1_SBK_[l1l111_SBK_ (u"ࠫࡨࡵࡶࡦࡴࠪऊ")]
                l1ll111l1_SBK_ = __SITE__+l1llll1l1_SBK_[l1l111_SBK_ (u"ࠬࡶ࡯ࡴࡶࡨࡶࠬऋ")]
                l1ll11ll1_SBK_ = l1llll1l1_SBK_[l1l111_SBK_ (u"࠭࡯ࡷࡧࡵࡺ࡮࡫ࡷࠨऌ")]
                l1l1lllll_SBK_ = l1111lll_SBK_(l1llll1l1_SBK_[l1l111_SBK_ (u"ࠧࡨࡧࡱࡶࡪ࠭ऍ")])
                l111llll_SBK_ = l1llll1l1_SBK_[l1l111_SBK_ (u"ࠨ࡫ࡰࡨࡧࡥࡲࡢࡶ࡬ࡲ࡬࠭ऎ")]
                l1ll1111l_SBK_ = l1llll1l1_SBK_[l1l111_SBK_ (u"ࠩࡧ࡭ࡷ࡫ࡣࡵࡱࡵࠫए")]
                l1l1l1ll1_SBK_ = l1llll1l1_SBK_[l1l111_SBK_ (u"ࠪ࡭ࡲࡪࡢࡠ࡫ࡧࠫऐ")]
                infoLabels = {l1l111_SBK_ (u"࡙ࠫ࡯ࡴ࡭ࡧࠪऑ"): title, l1l111_SBK_ (u"ࠬ࡟ࡥࡢࡴࠪऒ"): year, l1l111_SBK_ (u"࠭ࡇࡦࡰࡵࡩࠬओ"): l1l1lllll_SBK_, l1l111_SBK_ (u"ࠧࡑ࡮ࡲࡸࠬऔ"): l1ll11ll1_SBK_, l1l111_SBK_ (u"ࠨࡔࡤࡸ࡮ࡴࡧࠨक"): l111llll_SBK_, l1l111_SBK_ (u"ࠩࡇ࡭ࡷ࡫ࡣࡵࡱࡵࠫख"): l1ll1111l_SBK_ }
                l1l1l11ll_SBK_(l1l111_SBK_ (u"ࠪ࡟ࡋࡏࡌࡎࡇࡠࠤࠥ࠭ग")+title+l1l111_SBK_ (u"ࠫࠥ࠮ࠧघ")+year+l1l111_SBK_ (u"ࠬ࠯ࠧङ"), l1l1l1ll1_SBK_, 3, l1ll111l1_SBK_, l1l111_SBK_ (u"࠭ࡦࡪ࡮ࡰࡩࠬच"), 0, 0, infoLabels, l1ll111l1_SBK_)
            if type == l1l111_SBK_ (u"ࠧࡴࡧࡵ࡭ࡪ࠭छ"):
                infoLabels = {l1l111_SBK_ (u"ࠨࡖ࡬ࡸࡱ࡫ࠧज"): title, l1l111_SBK_ (u"ࠩ࡜ࡩࡦࡸࠧझ"): year}
                l1lll11l1_SBK_(l1l111_SBK_ (u"ࠪ࡟ࡘࡋࡒࡊࡇࡠࠤࠥ࠭ञ")+title+ l1l111_SBK_ (u"ࠫࠥ࠮ࠧट")+year+l1l111_SBK_ (u"ࠬ࠯ࠧठ"), __SITE__+l1l11l11l_SBK_, 4, l1ll111l1_SBK_, l1l111_SBK_ (u"࠭ࡳࡦࡴ࡬ࡩࠬड"), infoLabels, l1ll111l1_SBK_)
        else:
            l1lll11l1_SBK_(l1l111_SBK_ (u"ࠧ࠽࡙ࠢࡳࡱࡺࡡࡳࠩढ"), l1l111_SBK_ (u"ࠨࡷࡵࡰࠬण"), None, os.path.join(__ART_FOLDER__, __SKIN__, l1l111_SBK_ (u"ࠩࡳࡶࡪࡼࡩࡰࡷࡶ࠲ࡵࡴࡧࠨत")))
    l1lll111l_SBK_(l1l111_SBK_ (u"ࠪࡱࡴࡼࡩࡦࡵࡢࡷࡪࡸࡩࡦࡵࠪथ"))
def l1l11ll11_SBK_():
    __ADDON__.openSettings()
    l1lll11l1_SBK_(l1l111_SBK_ (u"ࠫࡊࡴࡴࡳࡣࡵࠤࡳࡵࡶࡢ࡯ࡨࡲࡹ࡫ࠧद"),l1l111_SBK_ (u"ࠬࡻࡲ࡭ࠩध"),None,os.path.join(__ART_FOLDER__, __SKIN__,l1l111_SBK_ (u"࠭ࡰࡳࡧࡹ࡭ࡴࡻࡳ࠯ࡲࡱ࡫ࠬन")))
    l1lll111l_SBK_(l1l111_SBK_ (u"ࠧ࡮ࡧࡱࡹࠬऩ"))
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
def l1lll111l_SBK_(option):
    if option == l1l111_SBK_ (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࡠࡵࡨࡶ࡮࡫ࡳࠨप"):
        l1ll11lll_SBK_ = __ADDON__.getSetting(l1l111_SBK_ (u"ࠩࡩ࡭ࡱࡳࡥࡴࡕࡨࡶ࡮࡫ࡳࡗ࡫ࡨࡻࠬफ"))
    elif option == l1l111_SBK_ (u"ࠪࡱࡪࡴࡵࠨब"):
        l1ll11lll_SBK_ = __ADDON__.getSetting(l1l111_SBK_ (u"ࠫࡲ࡫࡮ࡶࡘ࡬ࡩࡼ࠭भ"))
    elif option == l1l111_SBK_ (u"ࠬࡹࡥࡢࡵࡲࡲࡸ࠭म"):
        l1ll11lll_SBK_ = __ADDON__.getSetting(l1l111_SBK_ (u"࠭ࡳࡦࡣࡶࡳࡳࡹࡖࡪࡧࡺࠫय"))
    elif option == l1l111_SBK_ (u"ࠧࡦࡲ࡬ࡷࡴࡪࡥࡴࠩर"):
        l1ll11lll_SBK_ = __ADDON__.getSetting(l1l111_SBK_ (u"ࠨࡧࡳ࡭ࡸࡵࡤࡪࡱࡶ࡚࡮࡫ࡷࠨऱ"))
    else:
        l1ll11lll_SBK_ = l1l111_SBK_ (u"ࠩ࠳ࠫल")
    if l1ll11lll_SBK_:
        if l1ll11lll_SBK_ == l1l111_SBK_ (u"ࠪ࠴ࠬळ"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠦࡈࡵ࡮ࡵࡣ࡬ࡲࡪࡸ࠮ࡔࡧࡷ࡚࡮࡫ࡷࡎࡱࡧࡩ࠭࠻࠰ࠪࠤऴ"))
        elif l1ll11lll_SBK_ == l1l111_SBK_ (u"ࠬ࠷ࠧव"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠨࡃࡰࡰࡷࡥ࡮ࡴࡥࡳ࠰ࡖࡩࡹ࡜ࡩࡦࡹࡐࡳࡩ࡫ࠨ࠶࠳ࠬࠦश"))
        elif l1ll11lll_SBK_ == l1l111_SBK_ (u"ࠧ࠳ࠩष"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠣࡅࡲࡲࡹࡧࡩ࡯ࡧࡵ࠲ࡘ࡫ࡴࡗ࡫ࡨࡻࡒࡵࡤࡦࠪ࠸࠴࠵࠯ࠢस"))
        elif l1ll11lll_SBK_ == l1l111_SBK_ (u"ࠩ࠶ࠫह"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠥࡇࡴࡴࡴࡢ࡫ࡱࡩࡷ࠴ࡓࡦࡶ࡙࡭ࡪࡽࡍࡰࡦࡨࠬ࠺࠶࠱ࠪࠤऺ"))
        elif l1ll11lll_SBK_ == l1l111_SBK_ (u"ࠫ࠹࠭ऻ"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠧࡉ࡯࡯ࡶࡤ࡭ࡳ࡫ࡲ࠯ࡕࡨࡸ࡛࡯ࡥࡸࡏࡲࡨࡪ࠮࠵࠱࠺़ࠬࠦ"))
        elif l1ll11lll_SBK_ == l1l111_SBK_ (u"࠭࠵ࠨऽ"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠢࡄࡱࡱࡸࡦ࡯࡮ࡦࡴ࠱ࡗࡪࡺࡖࡪࡧࡺࡑࡴࡪࡥࠩ࠷࠳࠸࠮ࠨा"))
        elif l1ll11lll_SBK_ == l1l111_SBK_ (u"ࠨ࠸ࠪि"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠤࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡙ࡥࡵࡘ࡬ࡩࡼࡓ࡯ࡥࡧࠫ࠹࠵࠹ࠩࠣी"))
        elif l1ll11lll_SBK_ == l1l111_SBK_ (u"ࠪ࠻ࠬु"): xbmc.executebuiltin(l1l111_SBK_ (u"ࠦࡈࡵ࡮ࡵࡣ࡬ࡲࡪࡸ࠮ࡔࡧࡷ࡚࡮࡫ࡷࡎࡱࡧࡩ࠭࠻࠱࠶ࠫࠥू"))
def l1111lll_SBK_(list):
    l1ll1l1l1_SBK_ = []
    for l1l1lllll_SBK_ in list:
        l1ll1l1l1_SBK_.append(l1l1lllll_SBK_[l1l111_SBK_ (u"ࠬࡴࡡ࡮ࡧࠪृ")])
    return l1l111_SBK_ (u"࠭ࠬࠡࠩॄ").join(l1ll1l1l1_SBK_)
def l1l1lll11_SBK_(url):
    l1ll1lll1_SBK_ = requests.get(url, headers={l1l111_SBK_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧॅ"): l1l111_SBK_ (u"ࠨࡃࡳ࡭ࡐ࡫ࡹࠡࠩॆ")+__ADDON__.getSetting(l1l111_SBK_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫे"))+l1l111_SBK_ (u"ࠪ࠾ࠬै")+__ADDON__.getSetting(l1l111_SBK_ (u"ࠫࡦࡶࡩ࡬ࡧࡼࠫॉ"))}).text
    return json.loads(l1ll1lll1_SBK_)
def l1l111lll_SBK_(name,url,iconimage):
    l1ll1l1ll_SBK_=xbmcgui.ListItem(name, iconImage=l1l111_SBK_ (u"ࠧࡊࡥࡧࡣࡸࡰࡹ࡜ࡩࡥࡧࡲ࠲ࡵࡴࡧࠣॊ"), thumbnailImage=iconimage)
    l1ll1l1ll_SBK_.setProperty(l1l111_SBK_ (u"࠭ࡦࡢࡰࡤࡶࡹࡥࡩ࡮ࡣࡪࡩࠬो"), iconimage)
    l1ll1l1ll_SBK_.setInfo( type=l1l111_SBK_ (u"ࠢࡗ࡫ࡧࡩࡴࠨौ"), infoLabels={ l1l111_SBK_ (u"ࠣࡖ࡬ࡸࡱ࡫्ࠢ"): name } )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=l1ll1l1ll_SBK_)
    return True
def l1lll11l1_SBK_(name,url,mode,iconimage,l1l1ll11l_SBK_=False,infoLabels=False,l1ll111l1_SBK_=False):
    if infoLabels: infoLabelsAux = infoLabels
    else: infoLabelsAux = {l1l111_SBK_ (u"ࠩࡗ࡭ࡹࡲࡥࠨॎ"): name}
    if l1ll111l1_SBK_: l1llll1ll_SBK_ = l1ll111l1_SBK_
    else: l1llll1ll_SBK_ = iconimage
    u=sys.argv[0]+l1l111_SBK_ (u"ࠥࡃࡺࡸ࡬࠾ࠤॏ")+urllib.quote_plus(url)+l1l111_SBK_ (u"ࠦࠫࡳ࡯ࡥࡧࡀࠦॐ")+str(mode)+l1l111_SBK_ (u"ࠧࠬ࡮ࡢ࡯ࡨࡁࠧ॑")+urllib.quote_plus(name)
    l1lll1lll_SBK_ = __FANART__
    if l1l1ll11l_SBK_ == l1l111_SBK_ (u"࠭ࡦࡪ࡮ࡰࡩ॒ࠬ"):
        l1lll1lll_SBK_ = l1llll1ll_SBK_
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠧࡎࡱࡹ࡭ࡪࡹࠧ॓"))
    elif l1l1ll11l_SBK_ == l1l111_SBK_ (u"ࠨࡵࡨࡶ࡮࡫ࠧ॔"):
        l1lll1lll_SBK_ = l1llll1ll_SBK_
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪॕ"))
    elif l1l1ll11l_SBK_ == l1l111_SBK_ (u"ࠪࡩࡵ࡯ࡳࡰࡦࡨࠫॖ"):
        l1lll1lll_SBK_ = l1llll1ll_SBK_
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠫࡪࡶࡩࡴࡱࡧࡩࡸ࠭ॗ"))
    else:
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠬࡓ࡯ࡷ࡫ࡨࡷࠬक़"))
    l1ll1l1ll_SBK_=xbmcgui.ListItem(name, iconImage=l1llll1ll_SBK_, thumbnailImage=l1llll1ll_SBK_)
    l1ll1l1ll_SBK_.setProperty(l1l111_SBK_ (u"࠭ࡦࡢࡰࡤࡶࡹࡥࡩ࡮ࡣࡪࡩࠬख़"), l1lll1lll_SBK_)
    l1ll1l1ll_SBK_.setInfo( type=l1l111_SBK_ (u"ࠢࡗ࡫ࡧࡩࡴࠨग़"), infoLabels=infoLabelsAux )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l1ll1l1ll_SBK_,isFolder=True)
    return True
def l1llll11l_SBK_(name,url,mode,iconimage,l1ll1llll_SBK_):
    u=sys.argv[0]+l1l111_SBK_ (u"ࠣࡁࡸࡶࡱࡃࠢज़")+urllib.quote_plus(url)+l1l111_SBK_ (u"ࠤࠩࡱࡴࡪࡥ࠾ࠤड़")+str(mode)+l1l111_SBK_ (u"ࠥࠪࡳࡧ࡭ࡦ࠿ࠥढ़")+urllib.quote_plus(name)
    l1ll1l1ll_SBK_=xbmcgui.ListItem(name, iconImage=l1l111_SBK_ (u"ࠦ࡫ࡧ࡮ࡢࡴࡷ࠲࡯ࡶࡧࠣफ़"), thumbnailImage=iconimage)
    l1ll1l1ll_SBK_.setProperty(l1l111_SBK_ (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࡤ࡯࡭ࡢࡩࡨࠫय़"), iconimage)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l1ll1l1ll_SBK_,isFolder=l1ll1llll_SBK_)
    return True
def l1l1ll1ll_SBK_(name,url,mode,iconimage,season):
    u=sys.argv[0]+l1l111_SBK_ (u"ࠨ࠿ࡶࡴ࡯ࡁࠧॠ")+urllib.quote_plus(url)+l1l111_SBK_ (u"ࠢࠧ࡯ࡲࡨࡪࡃࠢॡ")+str(mode)+l1l111_SBK_ (u"ࠣࠨࡱࡥࡲ࡫࠽ࠣॢ")+urllib.quote_plus(name)+l1l111_SBK_ (u"ࠤࠩࡷࡪࡧࡳࡰࡰࡀࠦॣ")+str(season)
    xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠪࡑࡴࡼࡩࡦࡵࠪ।"))
    l1ll1l1ll_SBK_=xbmcgui.ListItem(name, iconImage=l1l111_SBK_ (u"ࠦ࡫ࡧ࡮ࡢࡴࡷ࠲࡯ࡶࡧࠣ॥"), thumbnailImage=iconimage)
    l1ll1l1ll_SBK_.setProperty(l1l111_SBK_ (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࡤ࡯࡭ࡢࡩࡨࠫ०"), __FANART__)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l1ll1l1ll_SBK_,isFolder=True)
    return True
def l1l1l11ll_SBK_(name,url,mode,iconimage,l1l1ll11l_SBK_,season,episode,infoLabels,l1ll111l1_SBK_):
    if l1l1ll11l_SBK_ == l1l111_SBK_ (u"࠭ࡦࡪ࡮ࡰࡩࠬ१"):
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠧࡎࡱࡹ࡭ࡪࡹࠧ२"))
    elif l1l1ll11l_SBK_ == l1l111_SBK_ (u"ࠨࡵࡨࡶ࡮࡫ࠧ३"):
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪ४"))
    elif l1l1ll11l_SBK_ == l1l111_SBK_ (u"ࠪࡩࡵ࡯ࡳࡰࡦࡨࠫ५"):
        xbmcplugin.setContent(int(sys.argv[1]), l1l111_SBK_ (u"ࠫࡪࡶࡩࡴࡱࡧࡩࡸ࠭६"))
    u=sys.argv[0]+l1l111_SBK_ (u"ࠧࡅࡵࡳ࡮ࡀࠦ७")+urllib.quote_plus(url)+l1l111_SBK_ (u"ࠨࠦ࡮ࡱࡧࡩࡂࠨ८")+str(mode)+l1l111_SBK_ (u"ࠢࠧࡵࡨࡥࡸࡵ࡮࠾ࠤ९")+str(season)+l1l111_SBK_ (u"ࠣࠨࡨࡴ࡮ࡹ࡯ࡥࡧࡀࠦ॰")+str(episode)+l1l111_SBK_ (u"ࠤࠩࡲࡦࡳࡥ࠾ࠤॱ")+urllib.quote_plus(name)+l1l111_SBK_ (u"ࠥࠪ࡮ࡩ࡯࡯࡫ࡰࡥ࡬࡫࠽ࠣॲ")+urllib.quote_plus(iconimage)
    l1ll1l1ll_SBK_=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    l1ll1l1ll_SBK_.setProperty(l1l111_SBK_ (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࡣ࡮ࡳࡡࡨࡧࠪॳ"), l1ll111l1_SBK_)
    l1ll1l1ll_SBK_.setInfo( type=l1l111_SBK_ (u"ࠧ࡜ࡩࡥࡧࡲࠦॴ"), infoLabels=infoLabels )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l1ll1l1ll_SBK_,isFolder=False)
    return True
def l1lllll1l_SBK_(url,path):
    l1lllllll_SBK_ = requests.get(url).content
    if l1lllllll_SBK_:
        with open(path, l1l111_SBK_ (u"࠭ࡷࠨॵ")) as fh:
            fh.write(l1lllllll_SBK_)
            fh.close()
    return url
def l1l11l111_SBK_(lang):
    if lang == l1l111_SBK_ (u"ࠧࡱࡶࠪॶ"):
        return l1l111_SBK_ (u"ࠨࡒࡲࡶࡹࡻࡧࡶࡧࡶࡩࠬॷ")
    elif lang == l1l111_SBK_ (u"ࠩࡨࡲࠬॸ"):
        return l1l111_SBK_ (u"ࠪࡉࡳ࡭࡬ࡪࡵ࡫ࠫॹ")
    else:
        return None
def l1ll1l111_SBK_(lang):
    l1ll1ll11_SBK_ = l1l111_SBK_ (u"ࠫ࡮ࡩ࡯࡯࠰ࡳࡲ࡬࠭ॺ")
    language = l1l111_SBK_ (u"ࠬ࠭ॻ")
    if lang == l1l111_SBK_ (u"࠭ࡰࡵࠩॼ"):
        language = l1l111_SBK_ (u"ࠧࡑࡱࡵࡸࡺ࡭ࡵࡦࡵࠪॽ")
        l1ll1ll11_SBK_ = l1l111_SBK_ (u"ࠨࡲࡲࡶࡹࡻࡧࡶࡧࡶࡩ࠳ࡶ࡮ࡨࠩॾ")
    elif lang == l1l111_SBK_ (u"ࠩࡨࡲࠬॿ"):
        language = l1l111_SBK_ (u"ࠪࡉࡳ࡭࡬ࡪࡵ࡫ࠫঀ")
        l1ll1ll11_SBK_ = l1l111_SBK_ (u"ࠫࡪࡴࡧ࡭࡫ࡶ࡬࠳ࡶ࡮ࡨࠩঁ")
    else:
        return None
    return xbmc.executebuiltin(l1l111_SBK_ (u"ࠧ࡞ࡂࡎࡅ࠱ࡒࡴࡺࡩࡧ࡫ࡦࡥࡹ࡯࡯࡯ࠪࡖࡩࡲࡈࡩ࡭ࡪࡨࡸࡪ࠴ࡴࡷ࠮ࠣࡐࡪ࡭ࡥ࡯ࡦࡤࠤࡨࡧࡲࡳࡧࡪࡥࡩࡧ࠺ࠡࠤং")+language+l1l111_SBK_ (u"ࠨࠬࠡࠩ࠴࠴࠵࠶࠰ࠨ࠮ࠣࠦঃ")+os.path.join(__ART_FOLDER__, __SKIN__,l1ll1ll11_SBK_)+l1l111_SBK_ (u"ࠢࠪࠤ঄"))
def l111l1ll_SBK_(name,imdb,iconimage,season,episode,serieNome=l1l111_SBK_ (u"ࠨࠩঅ")):
    l1l11l1l1_SBK_ = l1l1lll11_SBK_(__SITE__+l1l111_SBK_ (u"ࠩ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡧࡴࡴࡴࡦࡰࡷ࠳ࠬআ")+imdb)
    url = l1l11l1l1_SBK_[l1l111_SBK_ (u"ࠪࡹࡷࡲࠧই")]
    l1lll11ll_SBK_ = []
    if len(l1l11l1l1_SBK_[l1l111_SBK_ (u"ࠫࡸࡻࡢࡵ࡫ࡷࡰࡪࡹࠧঈ")]) > 0:
        for l111ll1l_SBK_ in l1l11l1l1_SBK_[l1l111_SBK_ (u"ࠬࡹࡵࡣࡶ࡬ࡸࡱ࡫ࡳࠨউ")]:
            language = l1l11l111_SBK_(l111ll1l_SBK_[l1l111_SBK_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨঊ")])
            l111111l_SBK_ = os.path.join(xbmc.translatePath(l1l111_SBK_ (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲ࡸࡪࡳࡰࠨঋ")), imdb+l1l111_SBK_ (u"ࠨ࠰ࠪঌ")+language+l1l111_SBK_ (u"ࠩ࠱ࡷࡷࡺࠧ঍"))
            l1lllll1l_SBK_(__SITE__+l111ll1l_SBK_[l1l111_SBK_ (u"ࠪࡹࡷࡲࠧ঎")],l111111l_SBK_)
            l1ll1l111_SBK_(l111ll1l_SBK_[l1l111_SBK_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭এ")])
            l1lll11ll_SBK_.append(l111111l_SBK_)
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
    if len(l1lll11ll_SBK_) > 0:
        for l111ll11_SBK_ in l1lll11ll_SBK_:
            l111l1ll_SBK_.setSubtitles(l111ll11_SBK_)
def get_params():
    param=[]
    l1llllll1_SBK_=sys.argv[2]
    if len(l1llllll1_SBK_)>=2:
        params=sys.argv[2]
        l1l1l11l1_SBK_=params.replace(l1l111_SBK_ (u"ࠩࡂࠫছ"),l1l111_SBK_ (u"ࠪࠫজ"))
        if (params[len(params)-1]==l1l111_SBK_ (u"ࠫ࠴࠭ঝ")): params=params[0:len(params)-2]
        l111l1l1_SBK_=l1l1l11l1_SBK_.split(l1l111_SBK_ (u"ࠬࠬࠧঞ"))
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
    l1ll11l11_SBK_=None
    l1l11lll1_SBK_=None
    season=None
    episode=None
    try: url=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠢࡶࡴ࡯ࠦঠ")])
    except: pass
    try: link=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠣ࡮࡬ࡲࡰࠨড")])
    except: pass
    try: l1ll11l11_SBK_=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠤ࡯ࡩ࡬࡫࡮ࡥࡣࠥঢ")])
    except: pass
    try: name=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠥࡲࡦࡳࡥࠣণ")])
    except: pass
    try: season=int(params[l1l111_SBK_ (u"ࠦࡸ࡫ࡡࡴࡱࡱࠦত")])
    except: pass
    try: episode=int(params[l1l111_SBK_ (u"ࠧ࡫ࡰࡪࡵࡲࡨࡪࠨথ")])
    except: pass
    try: mode=int(params[l1l111_SBK_ (u"ࠨ࡭ࡰࡦࡨࠦদ")])
    except: pass
    try: l1l11lll1_SBK_=int(params[l1l111_SBK_ (u"ࠢࡱࡣࡪ࡭ࡳࡧࠢধ")])
    except: pass
    try: iconimage=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠣ࡫ࡦࡳࡳ࡯࡭ࡢࡩࡨࠦন")])
    except: pass
    try : serieNome=urllib.unquote_plus(params[l1l111_SBK_ (u"ࠤࡶࡩࡷ࡯ࡥࡏࡱࡰࡩࠧ঩")])
    except: pass
    if mode==None or url==None or len(url)<1: l1lll1ll1_SBK_()
    elif mode==1: l1ll11111_SBK_(url)
    elif mode==12: l1111l11_SBK_(url)
    elif mode==2: l111l111_SBK_(url, l1l11lll1_SBK_)
    elif mode==3: l111l1ll_SBK_(name, url, iconimage, season, episode, serieNome=l1l111_SBK_ (u"ࠪࠫপ"))
    elif mode==4: l1l11l1ll_SBK_(url)
    elif mode==5: l11111ll_SBK_(url)
    elif mode==9: l1l11ll1l_SBK_(url)
    elif mode==6: l1l1l1l1l_SBK_()
    elif mode==1000: l1l11ll11_SBK_()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
if __name__ == l1l111_SBK_ (u"ࠦࡤࡥ࡭ࡢ࡫ࡱࡣࡤࠨফ"):
    main()