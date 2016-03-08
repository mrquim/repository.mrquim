# coding: UTF-8
import sys
l11l1_SBK_ = sys.version_info [0] == 2
l1111_SBK_ = 2048
l1l_SBK_ = 7
def l1ll11_SBK_ (ll_SBK_):
	global l1ll1l_SBK_
	l1llll_SBK_ = ord (ll_SBK_ [-1])
	l11ll_SBK_ = ll_SBK_ [:-1]
	l1lll_SBK_ = l1llll_SBK_ % len (l11ll_SBK_)
	l1ll1_SBK_ = l11ll_SBK_ [:l1lll_SBK_] + l11ll_SBK_ [l1lll_SBK_:]
	if l11l1_SBK_:
		l111_SBK_ = unicode () .join ([unichr (ord (char) - l1111_SBK_ - (l1l1l_SBK_ + l1llll_SBK_) % l1l_SBK_) for l1l1l_SBK_, char in enumerate (l1ll1_SBK_)])
	else:
		l111_SBK_ = str () .join ([chr (ord (char) - l1111_SBK_ - (l1l1l_SBK_ + l1llll_SBK_) % l1l_SBK_) for l1l1l_SBK_, char in enumerate (l1ll1_SBK_)])
	return eval (l111_SBK_)
import requests
import random
import math
import base64
import re
from packer.packer import unpack
headers = {l1ll11_SBK_ (u"࡚ࠫࡹࡥࡳ࠯ࡄ࡫ࡪࡴࡴࠨࠀ"): l1ll11_SBK_ (u"ࠬࡓ࡯ࡻ࡫࡯ࡰࡦ࠵࠵࠯࠲ࠣࠬ࡜࡯࡮ࡥࡱࡺࡷࠥࡔࡔࠡ࠳࠳࠲࠵ࡁࠠࡘ࡫ࡱ࠺࠹ࡁࠠࡹ࠸࠷࠭ࠥࡇࡰࡱ࡮ࡨ࡛ࡪࡨࡋࡪࡶ࠲࠹࠸࠽࠮࠴࠸ࠣࠬࡐࡎࡔࡎࡎ࠯ࠤࡱ࡯࡫ࡦࠢࡊࡩࡨࡱ࡯ࠪࠢࡆ࡬ࡷࡵ࡭ࡦ࠱࠷࠽࠳࠶࠮࠳࠸࠵࠷࠳࠽࠵ࠡࡕࡤࡪࡦࡸࡩ࠰࠷࠶࠻࠳࠹࠶ࠨࠁ")}
def l1_SBK_():
    num = (917902221 * random.random() + 10000000)
    return int(math.floor(num))
def l1l1_SBK_():
    l1l11_SBK_ = requests.get(l1ll11_SBK_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡳࡴ࡮࠱࡬ࡸࡺࡰ࡯ࡧࡷࡻࡴࡸ࡫࠯ࡥࡲࡱ࠴ࡪ࡯ࡤࡣ࡯ࡰࡧࡧ࡫ࡤ࡫ࡱࡪࡴ࠴ࡪࡴࠩࠂ"), headers=headers)
    l1lll1_SBK_ = unpack(l1l11_SBK_.text)
    l11l_SBK_ = re.search(l1ll11_SBK_ (u"ࠧ࡝ࡽࠫ࠲࠯࠯࡜ࡾࠩࠃ"), l1lll1_SBK_)
    l1ll_SBK_ = l1ll11_SBK_ (u"ࠨࡽࠪࠄ")+l11l_SBK_.group(1)+l1ll11_SBK_ (u"ࠩࢀࠫࠅ")
    return base64.b64encode(l1ll_SBK_)
def main():
    payload = {
    l1ll11_SBK_ (u"ࠪࡴࡵࡻࡣࠨࠆ"): 1,
    l1ll11_SBK_ (u"ࠫࡵࡶࡵࠨࠇ"): 0,
    l1ll11_SBK_ (u"ࠬ࡯ࡤࠨࠈ"): 117446,
    l1ll11_SBK_ (u"࠭ࡲࡦࡨࠪࠉ") : l1ll11_SBK_ (u"ࠧࡢࡊࡕ࠴ࡨࡎࡍ࠷ࡎࡼ࠽ࡿࡠࡗ࠲࡫ࡤ࡛ࡽࡵ࡚࡙ࡔ࡯ࡐࡳࡘ࠲ࡍࡹࡀࡁࠬࠊ"),
    l1ll11_SBK_ (u"ࠨࡴࡸࡶ࡮࠭ࠋ"): l1ll11_SBK_ (u"ࠩࠪࠌ"),
    l1ll11_SBK_ (u"ࠪࡶࠬࠍ"): l1_SBK_(),
    l1ll11_SBK_ (u"ࠫࡹࡵ࡫ࠨࠎ"): 134527060316725431,
    l1ll11_SBK_ (u"ࠬࡺࡳࠨࠏ") : random.uniform(5, 20),
    l1ll11_SBK_ (u"࠭ࡣࡵࡴࠪࠐ"): l1ll11_SBK_ (u"ࠧࡑࡖࠪࠑ"),
    l1ll11_SBK_ (u"ࠨࡵࡽࠫࠒ") : 905,
    l1ll11_SBK_ (u"ࠩࡺࡲࠬࠓ") : l1ll11_SBK_ (u"ࠪࠫࠔ"),
    l1ll11_SBK_ (u"ࠫࡷ࡫ࡳࠨࠕ") : l1ll11_SBK_ (u"ࠬ࠷࠶࠹࠸ࡻ࠽࠵࠻ࠧࠖ")}
    cookie = {l1ll11_SBK_ (u"࠭ࡨࡴࡶࡳࡺ࠹ࡻࡳࡦࡴࠪࠗ"): l1l1_SBK_()}
    l111l_SBK_ = requests.get(l1ll11_SBK_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡴࡵ࡯࠲࡭ࡹࡴࡱࡰࡨࡸࡼࡵࡲ࡬࠰ࡦࡳࡲ࠵ࡴࡳࡣࡱࡷࡵࡵࡲࡵࡧࡵ࠳࠶࠷࠸࠷࠲࠱ࡴ࡭ࡶࠧ࠘"), params=payload, headers=headers, cookies=cookie)
    return l111l_SBK_