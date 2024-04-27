import pygame
from .general import RuntimeUnit


def run() -> None:
    # 这个函数一定是从main.py/main.exe运行的
    # 所以下面两个import语句才成立
    from . import pages
    pygame.init()
    rtu = RuntimeUnit()
    pages.Logo(rtu).run()
    while True:
        pages.Home(rtu).run()
