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

    def run(self):
        self.draw_and_flip()

        # full-screen fade-out
        FadeOut(scrmgr.screen, click_optional=True, count_down=1000).play()
