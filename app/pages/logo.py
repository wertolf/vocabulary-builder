from lega.core import RuntimeUnit
from lega.ui import StaticLabel, Page
from lega.an.fade_out import FadeOut

from config import font_theme

from lega.globe import scrmgr


class Logo(Page):
    def __init__(self):
        Page.__init__(self)

        self.register_controls(
            # construct "presented by" label
            StaticLabel(
                content="presented by", font=font_theme.logo, size=10,
                centerx=scrmgr.center.x, bottom=scrmgr.center.y,
            ),
            # construct "WERTech" label
            StaticLabel(
                content="WERTech", font=font_theme.logo, size=20,
                centerx=scrmgr.center.x, top=scrmgr.center.y,
            ),
        )

    def loop_once(self):
        """
        Logo 是一个没有循环的特殊页面，
        为了保持设计上的统一，依然通过重写 loop_once 方法的方式达成目的，
        进入第 1 次循环后立即将循环变量设置为 False 以达成目的
        """
        self.is_alive = False
