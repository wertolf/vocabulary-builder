from lega.an.animation import Animation

from config import color_theme

from typing import Union, Tuple

from pygame import Surface, Rect

from lega.globe import scrmgr
from lega.event_manager import handle_events


class FadeIn(Animation):
    """
    实现内容从屏幕上“淡出”的效果。
    """
    def __init__(
            self,
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
        Animation.__init__(self)

        self.variable_surf = variable_surf
        self.destination = destination
        self.speed = speed

    def play(self):
        surf = self.variable_surf.copy()
        for alpha in range(0, 255, self.speed):
            scrmgr.screen.fill(color_theme.background)
            surf.set_alpha(alpha)
            scrmgr.screen.blit(surf, self.destination)
            scrmgr.update_global()

            """
            # FadeIn 似乎不需要下面这部分逻辑
            handle_events(*self._handlers)
            if self.should_return_at_once:
                self.should_return_at_once = False  # 还原状态
                return
            """
