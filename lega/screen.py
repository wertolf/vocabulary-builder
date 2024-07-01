import pygame
from typing import Tuple

from pygame import Rect
from pygame.locals import FULLSCREEN

from config import color_theme

from lega.vector import Vector2D

class ScreenManager:
    def __init__(self, width, height):
        self._win_width = width
        self._win_height = height

        self.is_full_screen = False
        self.screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.fps = 30
    
    def clear_screen_without_update(self) -> None:
        self.screen.fill(color_theme.background)

    def clear_screen_with_update(self) -> None:
        """
        idiom
        """
        self.clear_screen_without_update()
        self.update_global()

    def update_global(self) -> None:
        # cf. self.update_local_area()
        pygame.display.flip()
        self.clock.tick(self.fps)

    def update_local_area(self, area: Rect) -> None:
        # cf. self.update_global()
        pygame.display.update(area)
        self.clock.tick(self.fps)

    def toggle_fullscreen(self) -> None:
        self.is_full_screen = not self.is_full_screen
        content_backup = self.screen.copy()
        if self.is_full_screen:
            self.screen = pygame.display.set_mode(self.resolution, FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.resolution)

        # 修正屏幕切换所导致的显示问题。方法很简单，重新绘制一下原来的内容
        self.screen.fill(color_theme.background)
        self.screen.blit(content_backup, self.screen.get_rect())
        self.update_global()

    @property
    def center(self) -> Vector2D:
        return Vector2D(self.win_width // 2, self.win_height // 2)

    @property
    def length_unit(self) -> int:  # 必须是int，否则在创建Font实例时会报错
        return int(self.win_height / (9 * 20))

    @property
    def resolution(self) -> Tuple[int, int]:
        return self.win_width, self.win_height

    @property
    def win_height(self) -> int:
        return self._win_height

    @property
    def win_width(self) -> int:
        return self._win_width

    @property
    def x_max(self) -> int:
        return self.win_width

    @property
    def x_min(self) -> int:
        return 0

    @property
    def y_max(self) -> int:
        return self.win_height

    @property
    def y_min(self) -> int:
        return 0