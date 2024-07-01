"""
Animations.
"""
import logging
import pygame

from lega.event_manager import common_handlers
from pygame.locals import MOUSEBUTTONUP
from pygame.locals import KEYUP
from pygame.locals import K_F5
from pygame.event import EventType


class Animation:
    def __init__(self):
        self._is_waiting = False
        self._should_return_at_once = False

        self._handlers = common_handlers + [self.on_clicked_or_pressed]

    @property
    def is_waiting(self) -> bool:
        return self._is_waiting

    def start_waiting(self) -> None:
        pygame.event.clear()  # 为了防止之前遗留的事件意外地结束waiting
        self._is_waiting = True

    def stop_waiting(self) -> None:
        self._is_waiting = False

    @property
    def should_return_at_once(self) -> bool:
        return self._should_return_at_once

    @should_return_at_once.setter
    def should_return_at_once(self, value: bool):
        logging.debug(f"[gs.should_return_at_once.setter] value: {value}")
        self._should_return_at_once = value

    def on_clicked_or_pressed(self, e: EventType) -> None:
        """
        一个特殊的事件处理器。用于跳过动画前的等待或动画本身。
        """
        if e.type not in (MOUSEBUTTONUP, KEYUP):
            return

        if e.type == KEYUP:
            key = getattr(e, "key")
            if key in (K_F5, ):
                return  # ignore irrelevant key pressing
        
        if self.is_waiting:
            # 提前结束动画前的等待
            self.stop_waiting()
        if not self.should_return_at_once:
            # 在动画进行过程中，提前结束动画
            self.should_return_at_once = True


    def play(self):
        """
        Play the animation. Override this method in subclass.
        """
        raise NotImplementedError()
