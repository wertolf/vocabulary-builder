# 脚本最后会按照字母顺序排列脚本中定义的所有类，方便查阅
from config import color_theme, resolution
from framework.resolution import ResolutionManager

from framework.globl import gs

from pygame import Color, Rect, Surface
from pygame.event import EventType
from pygame.locals import (
    KEYUP, MOUSEBUTTONUP, QUIT,
    K_F5,
    FULLSCREEN,
)
from typing import NoReturn, Tuple, Union
import pickle
import pygame
import sys
import logging


class _RuntimeUnit:
    """
    the unit of run-time dataset & operations.
    """
    def __init__(self) -> None:
        self._resolution_manager = ResolutionManager(resolution.win_width, resolution.win_height)

        self.screen = pygame.display.set_mode(self.resolution)  # 这个变量只能通过在整个程序的不同函数中不断传入rtu来保持，不能存储在外部，所以rtu这个类的存在是必要的
        self.is_full_screen = False
        self.clock = pygame.time.Clock()
        self.fps = 30

    def blits_on_the_screen_and_flip_it(self, *blit_params, **kwargs) -> None:
        self.screen.blits(blit_params)
        self.flip(**kwargs)

    # 特殊的事件处理器(event handlers)，统一以check if开头
    def check_if_user_clicked_or_pressed(self, e: EventType) -> None:
        if e.type in (MOUSEBUTTONUP, KEYUP):
            if e.type == KEYUP:
                assert hasattr(e, "key")
                key = getattr(e, "key")
                if key in (K_F5, ):
                    return  # ignore irrelevant key pressing
            self.stop_waiting()

    def check_if_user_pressed_f5(self, e: EventType) -> None:
        """切换屏幕状态（全屏/窗口）。"""
        if e.type != KEYUP:
            return
        assert hasattr(e, "key")
        key = getattr(e, "key")
        if key != K_F5:
            return

        self.is_full_screen = not self.is_full_screen
        content_backup = self.screen.copy()
        if self.is_full_screen:
            self.screen = pygame.display.set_mode(self.resolution, FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.resolution)

        # 修正屏幕切换所导致的显示问题。方法很简单，重新绘制一下原来的内容
        self.screen.fill(self.background)
        self.screen.blit(content_backup, self.rect)
        self.flip()

    def clear_screen_without_flipping(self) -> None:
        self.screen.fill(color_theme.background)

    def clear_screen_and_flip(self) -> None:
        self.clear_screen_without_flipping()
        self.flip()

    def flip(self, delay: int = 0) -> None:
        # cf. self.update_a_local_area_of_screen()
        pygame.display.flip()
        pygame.time.delay(delay)
        self.clock.tick(self.fps)

    def handle_universal_events_during_each_animation_frame(self) -> None:
        self.handle_events(
            *self.list_of_universal_handlers,
            self.handle_mouse_button_up_during_animation,
        )

    def sleep(self, count_down: int) -> None:
        # 这个方法是为了弥补pygame.time.delay运行期间无法响应退出事件的问题
        time_when_waiting_began = pygame.time.get_ticks()
        while True:
            time_at_the_moment = pygame.time.get_ticks()
            time_passed = time_at_the_moment - time_when_waiting_began
            if time_passed >= count_down:
                break
            self.handle_events(
                *self.list_of_universal_handlers,
                self.handle_mouse_button_up_during_animation,
            )
            if gs.should_return_at_once:
                break

    def start_waiting(self) -> None:
        pygame.event.clear()  # 为了防止之前遗留的事件意外地结束waiting
        gs.is_waiting = True

    def stop_waiting(self) -> None:
        gs.is_waiting = False

    def update_a_local_area_of_screen(self, area: Rect) -> None:
        # cf. self.flip()
        pygame.display.update(area)
        self.clock.tick(self.fps)

    @property
    def length_unit(self) -> float: return self.resolution_info.length_unit

    @property
    def list_of_universal_handlers(self) -> list:
        return [
            self.on_quit,
            self.check_if_user_pressed_f5,
        ]

    @property
    def rect(self) -> Rect: return self.rectangle
    @property
    def rectangle(self) -> Rect: return self.screen.get_rect()
    @property
    def resolution(self) -> Tuple[int, int]: return self.resolution_info.resolution
    @property
    def resolution_info(self) -> ResolutionManager: return self._resolution_manager
    @property
    def x_max(self) -> int: return self.resolution_info.x_max
    @property
    def x_mean(self) -> int: return self.resolution_info.x_mean
    @property
    def x_min(self) -> int: return self.resolution_info.x_min
    @property
    def y_max(self) -> int: return self.resolution_info.y_max
    @property
    def y_mean(self) -> int: return self.resolution_info.y_mean
    @property
    def y_min(self) -> int: return self.resolution_info.y_min

    @staticmethod
    def end_program() -> None:

        # 回复默认值
        # erd = _ExternalRuntimeData()
        # erd.is_waiting = False
        # erd.should_return_at_once = False

        pygame.quit()
        sys.exit()

    @staticmethod
    def handle_events(*handlers) -> None:
        for e in pygame.event.get():
            for event_handler in handlers:
                event_handler(e)

    @staticmethod
    def handle_mouse_button_up_during_animation(e: EventType) -> None:
        # 在动画进行过程中，按下鼠标左键或右键可以提前结束动画
        if e.type != MOUSEBUTTONUP:
            return
        gs.should_return_at_once = True
        logging.debug(f"[handle_mouse_button_up][END] should_return_at_once: {gs.should_return_at_once}")

    # 事件处理器(event handlers)，统一以on开头
    @staticmethod
    def on_quit(e: EventType) -> None:
        """
        Caution: Should be called inside every event handler.
        :param: e: a pygame EventType object
        """
        if e.type == QUIT:
            _RuntimeUnit.end_program()


class RuntimeUnit(_RuntimeUnit): pass
