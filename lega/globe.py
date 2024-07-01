"""
Global State
"""
from lega.screen import ScreenManager

import config.resolution

import pygame
import sys

"""
Initialization.
"""
# initialize screen lastly
scrmgr = ScreenManager(config.resolution.win_width, config.resolution.win_height)


def end_program() -> None:
    pygame.quit()
    sys.exit()
