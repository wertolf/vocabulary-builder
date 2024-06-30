# 脚本最后会按照字母顺序排列脚本中定义的所有类，方便查阅
from config import color_theme, resolution

from framework.globe import gs, scrmgr

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
        pass

    def blits_on_the_screen_and_flip_it(self, *blit_params, **kwargs) -> None:
        scrmgr.screen.blits(blit_params)
        scrmgr.update_global(**kwargs)

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
        
        scrmgr.toggle_fullscreen()

    def clear_screen_without_flipping(self) -> None:
        scrmgr.screen.fill(color_theme.background)

    def clear_screen_and_flip(self) -> None:
        self.clear_screen_without_flipping()
        scrmgr.update_global()

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

    @property
    def list_of_universal_handlers(self) -> list:
        return [
            self.on_quit,
            self.check_if_user_pressed_f5,
        ]

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
