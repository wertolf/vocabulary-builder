from framework.core import RuntimeUnit
from framework.ui import StaticLabel, Page
from framework.an.fade_out import FadeOut

from config import font_theme

from framework.globe import scrmgr


class Logo(Page):
    def __init__(self, rtu: RuntimeUnit):
        Page.__init__(self, rtu)

        self.register_controls(
            # construct "presented by" label
            StaticLabel(
                content="presented by", font=font_theme.logo, size=10,
                centerx=scrmgr.x_mean, bottom=scrmgr.y_mean,
            ),
            # construct "WERTech" label
            StaticLabel(
                content="WERTech", font=font_theme.logo, size=20,
                centerx=scrmgr.x_mean, top=scrmgr.y_mean,
            ),
        )

    def run(self):
        self.draw_and_flip()

        # full-screen fade-out
        FadeOut(self.rtu, scrmgr.screen, click_optional=True, count_down=1000).play()
