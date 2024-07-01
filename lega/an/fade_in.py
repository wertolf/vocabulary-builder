from lega.an.animation import Animation
from lega.core import RuntimeUnit

from lega.globe import sttmgr

from config import color_theme

from typing import Union, Tuple

from pygame import Surface, Rect


class FadeIn(Animation):
    """
    实现内容从屏幕上“淡出”的效果。
    """
    def __init__(
            self, rtu: RuntimeUnit,
            variable_surf: Surface,
            destination: Union[Rect, Tuple[int, int]] = (0, 0),
            speed: int = 20,
    ):
        """
        rtu之后的两个参数同Surface.blit保持一致
        :param variable_surf:
        :param destination:
        :param speed:
        :return:
        """
        Animation.__init__(self, rtu)

        self.variable_surf = variable_surf
        self.destination = destination
        self.speed = speed

    def play(self):
        for alpha in range(0, 255, self.speed):
            self.rtu.screen.fill(color_theme.background)
            self.variable_surf.set_alpha(alpha)
            self.rtu.screen.blit(self.variable_surf, self.destination)
            self.rtu.flip()

            self.rtu.handle_universal_events_during_each_animation_frame()

            if sttmgr.should_return_at_once:
                sttmgr.should_return_at_once = False  # 还原状态
                return
