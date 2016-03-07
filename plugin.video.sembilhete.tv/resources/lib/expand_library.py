# coding: UTF-8
import sys
l1l1ll_SBK_ = sys.version_info [0] == 2
l11ll_SBK_ = 2048
l1l_SBK_ = 7
def l1ll1l_SBK_ (l1_SBK_):
	global l11l1_SBK_
	l1111_SBK_ = ord (l1_SBK_ [-1])
	l111_SBK_ = l1_SBK_ [:-1]
	l1ll_SBK_ = l1111_SBK_ % len (l111_SBK_)
	l1l1_SBK_ = l111_SBK_ [:l1ll_SBK_] + l111_SBK_ [l1ll_SBK_:]
	if l1l1ll_SBK_:
		l1l1l_SBK_ = unicode () .join ([unichr (ord (char) - l11ll_SBK_ - (l11l_SBK_ + l1111_SBK_) % l1l_SBK_) for l11l_SBK_, char in enumerate (l1l1_SBK_)])
	else:
		l1l1l_SBK_ = str () .join ([chr (ord (char) - l11ll_SBK_ - (l11l_SBK_ + l1111_SBK_) % l1l_SBK_) for l11l_SBK_, char in enumerate (l1l1_SBK_)])
	return eval (l1l1l_SBK_)
import requests
import random
import math
import base64
import re
headers = {l1ll1l_SBK_ (u"࡚ࠫࡹࡥࡳ࠯ࡄ࡫ࡪࡴࡴࠨࠀ"): l1ll1l_SBK_ (u"ࠬࡓ࡯ࡻ࡫࡯ࡰࡦ࠵࠵࠯࠲ࠣࠬ࡜࡯࡮ࡥࡱࡺࡷࠥࡔࡔࠡ࠸࠱࠷ࡀࠦࡗࡐ࡙࠹࠸ࡀࠦࡲࡷ࠼࠷࠸࠳࠶ࠩࠡࡉࡨࡧࡰࡵ࠯࠳࠲࠴࠴࠵࠷࠰࠲ࠢࡉ࡭ࡷ࡫ࡦࡰࡺ࠲࠸࠹࠴࠰ࠨࠁ")}
def ll_SBK_():
    num = (917902221 * random.random() + 10000000)
    return int(math.floor(num))
def l1lll1_SBK_():
    l1llll_SBK_ = requests.get(l1ll1l_SBK_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡳࡴ࡮࠱࡬ࡸࡺࡰ࡯ࡧࡷࡻࡴࡸ࡫࠯ࡥࡲࡱ࠴ࡪ࡯ࡤࡣ࡯ࡰࡧࡧ࡫ࡤ࡫ࡱࡪࡴ࠴ࡪࡴࠩࠂ"), headers=headers)
    l111l_SBK_ = re.search(l1ll1l_SBK_ (u"ࠧࡊࡆ࡟ࢀ࠭࠴ࠪࠪ࡞ࡿࡶࡪࡳ࡯ࡵࡧࡢࡥࡩࡪࡲࠨࠃ"), l1llll_SBK_.text)
    l11_SBK_ = re.search(l1ll1l_SBK_ (u"ࠨࡇࡻࡩࡨࡢࡼࠩ࠰࠭࠭ࡡࢂ࡮ࡰࡥࡤࡧ࡭࡫ࠧࠄ"), l1llll_SBK_.text)
    l1l11_SBK_ = re.search(l1ll1l_SBK_ (u"ࠩ࡫ࡷࡹࡶࡣࡰࡰࡩ࡭࡬ࡢࡼࠩ࠰࠭࠭ࡡࢂࡅࡹࡧࡦࠫࠅ"), l1llll_SBK_.text)
    l1lll_SBK_ = {
    l1ll1l_SBK_ (u"ࠥࡍࡉࠨࠆ"):str(l111l_SBK_.group(1)),
    l1ll1l_SBK_ (u"ࠦࡈ࡚ࡒࠣࠇ"):l1ll1l_SBK_ (u"ࠧࡖࡔࠣࠈ"),
    l1ll1l_SBK_ (u"ࠨࡒࡦࡩ࡬ࡳࡳࠨࠉ"): None,
    l1ll1l_SBK_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࠣࠊ"):l1ll1l_SBK_ (u"ࠣࡈ࡬ࡶࡪ࡬࡯ࡹࠤࠋ"),
    l1ll1l_SBK_ (u"ࠤࡓࡰࡦࡺࡦࡰࡴࡰࠦࠌ"):l1ll1l_SBK_ (u"࡛ࠥ࡮ࡴ࠱࠱ࠤࠍ"),
    l1ll1l_SBK_ (u"ࠦࡒࡵࡢࡪ࡮ࡨࠦࠎ"):0,
    l1ll1l_SBK_ (u"ࠧࡈ࡯ࡵࠤࠏ"):0,
    l1ll1l_SBK_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡥࡡࡥࡦࡵࠦࠐ"): int(l11_SBK_.group(1)),
    l1ll1l_SBK_ (u"ࠢࡍࡣࡶࡸ࡚ࡶࡤࡢࡶࡨࠦࠑ"): int(l1l11_SBK_.group(1))}
    l1ll11_SBK_ = str(l1lll_SBK_).replace(l1ll1l_SBK_ (u"ࠣࠩࠥࠒ"), l1ll1l_SBK_ (u"ࠤ࡟ࠦࠧࠓ")).replace(l1ll1l_SBK_ (u"ࠥࠤࠧࠔ"), l1ll1l_SBK_ (u"ࠦࠧࠕ")).replace(l1ll1l_SBK_ (u"ࠧࡔ࡯࡯ࡧࠥࠖ"), l1ll1l_SBK_ (u"ࠨ࡮ࡶ࡮࡯ࠦࠗ"))
    return base64.b64encode(l1ll11_SBK_)
def main():
    payload = {
    l1ll1l_SBK_ (u"ࠧࡱࡲࡸࡧࠬ࠘"): 1,
    l1ll1l_SBK_ (u"ࠨࡲࡳࡹࠬ࠙"): 0,
    l1ll1l_SBK_ (u"ࠩ࡬ࡨࠬࠚ"): 117446,
    l1ll1l_SBK_ (u"ࠪࡶࡪ࡬ࠧࠛ") : l1ll1l_SBK_ (u"ࠫࡦࡎࡒ࠱ࡥࡋࡑ࠻ࡒࡹ࠺ࡼ࡝࡛࠶࡯ࡡࡘࡺࡲ࡞࡝ࡘ࡬ࡍࡰࡕ࠶ࡑࡽ࠽࠾ࠩࠜ"),
    l1ll1l_SBK_ (u"ࠬࡸࡵࡳ࡫ࠪࠝ"): l1ll1l_SBK_ (u"࠭ࠧࠞ"),
    l1ll1l_SBK_ (u"ࠧࡳࠩࠟ"): ll_SBK_(),
    l1ll1l_SBK_ (u"ࠨࡶࡲ࡯ࠬࠠ"): 134527060316725431,
    l1ll1l_SBK_ (u"ࠩࡷࡷࠬࠡ") : random.uniform(5, 20),
    l1ll1l_SBK_ (u"ࠪࡧࡹࡸࠧࠢ"): l1ll1l_SBK_ (u"ࠫࡕ࡚ࠧࠣ"),
    l1ll1l_SBK_ (u"ࠬࡹࡺࠨࠤ") : 905,
    l1ll1l_SBK_ (u"࠭ࡷ࡯ࠩࠥ") : l1ll1l_SBK_ (u"ࠧࠨࠦ"),
    l1ll1l_SBK_ (u"ࠨࡴࡨࡷࠬࠧ") : l1ll1l_SBK_ (u"ࠩ࠴࠺࠽࠼ࡸ࠺࠲࠸ࠫࠨ")}
    cookie = {l1ll1l_SBK_ (u"ࠪ࡬ࡸࡺࡰࡷ࠶ࡸࡷࡪࡸࠧࠩ"): l1lll1_SBK_()}
    l1l1l1_SBK_ = requests.get(l1ll1l_SBK_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡸࡹ࡬࠯ࡪࡶࡸࡵࡴࡥࡵࡹࡲࡶࡰ࠴ࡣࡰ࡯࠲ࡸࡷࡧ࡮ࡴࡲࡲࡶࡹ࡫ࡲ࠰࠳࠴࠼࠻࠶࠮ࡱࡪࡳࠫࠪ"), params=payload, headers=headers, cookies=cookie)
    return l1l1l1_SBK_