from pygame.event import EventType

from lega.globe import end_program, scrmgr

from pygame.locals import QUIT
from pygame.locals import KEYUP
from pygame.locals import K_F5

import pygame
import logging

def handle_events(*handlers) -> None:
    for e in pygame.event.get():
        for func in handlers:
            func(e)


"""
事件处理器(event handlers)，统一以on开头
"""
def on_quit(e: EventType) -> None:
    """
    :param: e: a pygame EventType object
    """
    if e.type == QUIT:
        end_program()
    

def on_key_up(e: EventType) -> None:
    if e.type != KEYUP:
        return

    key = getattr(e, "key")
    if key == K_F5:
        scrmgr.toggle_fullscreen()


common_handlers = [
    on_quit,
    on_key_up,
]
