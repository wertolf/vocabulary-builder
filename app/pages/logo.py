from framework.core import RuntimeUnit
from framework.ui import StaticLabel, Page

from config import font_theme


class Logo(Page):
    def __init__(self, rtu: RuntimeUnit):
        Page.__init__(self, rtu)

        self.register_controls(
            # construct "presented by" label
            StaticLabel(
                content="presented by", font=font_theme.logo, size=10,
                centerx=self.x_mean, bottom=self.y_mean,
            ),
            # construct "OurDreams" label
            StaticLabel(
                content="OurDreams", font=font_theme.logo, size=20,
                centerx=self.x_mean, top=self.y_mean,
            ),
        )

    def run(self):
        self.draw_and_flip()

        # full-screen fade-out
        self.rtu.present_fade_out(self.screen, click_optional=True, count_down=1500)
