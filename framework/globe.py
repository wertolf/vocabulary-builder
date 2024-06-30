"""
Global State
"""
from pygame import Surface
import logging

from framework.screen import ScreenManager

import config.resolution

# initialization
scrmgr = ScreenManager(config.resolution.win_width, config.resolution.win_height)

class GlobalState():
    def __init__(self):
        self._is_waiting = False
        self._should_return_at_once = False

    @property
    def is_waiting(self) -> bool:
        return self._is_waiting

    @property
    def should_return_at_once(self) -> bool:
        return self._should_return_at_once

    @is_waiting.setter
    def is_waiting(self, value: bool):
        self._is_waiting = value

    @should_return_at_once.setter
    def should_return_at_once(self, value: bool):
        logging.debug(f"[gs.should_return_at_once.setter] value: {value}")
        self._should_return_at_once = value

gs = GlobalState()
