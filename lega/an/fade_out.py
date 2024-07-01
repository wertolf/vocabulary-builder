from config import color_theme
from lega.an.animation import Animation

from lega.globe import scrmgr

import pygame.time
from pygame import Surface

from lega.event_manager import handle_events


class FadeOut(Animation):
    """
    实现内容从屏幕上“淡出”的效果。
    """
    def __init__(
            self, surf: Surface,
            destination=(0, 0), speed=20,
            click_needed: bool = False,
            click_optional: bool = False, count_down: int = 1000,
            time_delayed: int = 300,
    ):
        """
        :param surf: 如果赋值为self.screen，就是全屏淡出
        Below are parameters which have a default value.
        :param destination:
        :param speed:
        :param click_needed: 如果赋值为True，将一直等待，直到用户点击屏幕
        :param click_optional: 在倒计时count_down结束之前，点击屏幕可以提前开始动画
        :param count_down: 如果click_optional为True，倒计时结束之后自动开始动画
        :param time_delayed: 在“淡出”动画开始前，内容在屏幕上停留的时间（单位：ms）
        :return: None
        """
        Animation.__init__(self)

        assert (click_needed and click_optional) is not True, "click_needed and click_optional should not both be True."
        self.click_needed = click_needed
        self.click_optional = click_optional
        self.count_down = count_down
        self.time_delayed = time_delayed
        self.speed = speed
        self.surf = surf
        self.destination = destination

    def play(self):
        if self.click_needed or self.click_optional:
            self.start_waiting()
            time_when_waiting_began = pygame.time.get_ticks()
            while self.is_waiting:
                if self.click_optional:
                    time_at_the_moment = pygame.time.get_ticks()
                    time_passed = time_at_the_moment - time_when_waiting_began
                    if time_passed >= self.count_down:
                        self.stop_waiting()
                        break
                handle_events(*self._handlers)
        pygame.time.delay(self.time_delayed)
        surf = self.surf.copy()
        for alpha in range(255, 0, -self.speed):
            scrmgr.screen.fill(color_theme.background)
            surf.set_alpha(alpha)
            scrmgr.screen.blit(surf, self.destination)
            scrmgr.update_global()

            handle_events(*self._handlers)
            if self.should_return_at_once:
                self.should_return_at_once = False  # 还原状态
                return
