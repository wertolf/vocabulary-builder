import pygame
from typing import Tuple

from pygame import Rect
from pygame.locals import FULLSCREEN

from config import color_theme

class ScreenManager:
    def __init__(self, width, height):
        self._win_width = width
        self._win_height = height

        self.is_full_screen = False
        self.screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.fps = 30
    
    def update_global(self, delay: int = 0) -> None:
        # cf. self.update_local_area()
        pygame.display.flip()
        pygame.time.delay(delay)
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
    def cam_width(self) -> int:
        return self.win_width * 1  # 在这里设定有效显示区域的长

    @property
    def cam_height(self) -> int:
        return self.win_height * 1  # 在这里设定有效显示区域的宽

    @property
    def center(self) -> Tuple[int, int]:
        return self.x_mean, self.y_mean

    @property
    def length_unit(self) -> int:  # 必须是int，否则在创建Font实例时会报错
        return int(self.win_height / (9 * 20))

    @property
    def resolution(self) -> Tuple[int, int]:
        return self.win_width, self.win_height

    @property
    def temp_win_height(self) -> int:
        return int(self.win_height * 0.75)

    @property
    def temp_win_width(self) -> int:
        return int(self.win_width * 0.75)

    @property
    def win_height(self) -> int:
        return self._win_height

    @property
    def win_width(self) -> int:
        return self._win_width

    @property
    def x_max(self) -> int:
        return self.x_mean + int(self.cam_width * 0.5)

    @property
    def x_mean(self) -> int:
        return int(self.win_width * 0.5)

    @property
    def x_min(self) -> int:
        return self.x_mean - int(self.cam_width * 0.5)

    @property
    def y_max(self) -> int:
        return self.y_mean + int(self.cam_height * 0.5)

    @property
    def y_mean(self) -> int:
        return int(self.win_height * 0.5)

    @property
    def y_min(self) -> int:
        return self.y_mean - int(self.cam_height * 0.5)
