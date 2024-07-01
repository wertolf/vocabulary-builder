"""
表示层(presentation)主模块。
"""
import pygame

from pygame import Surface

from .color import RGBColor
from .vector import Vector2D

from . import board
from . import core
from . import color
from . import dot

from ....lega.core import RuntimeUnit
from ....lega.ui import resolution_info as res
from ....lega.ui import Control


# pygame时钟，与fps结合，用于控制刷新频率
clock = pygame.time.Clock()
fps = 30

# 为了将letsjump整合到这个项目中，需要创建一个继承自Control类的Board类
class Board(Control):
    raw_board: Surface  # 预先绘制好的空棋盘，用于提高重绘速度
    snapshot: Surface  # 对不变的内容进行快照，减少重复绘制
    held_piece: Vector2D  # 被拿起的棋子在屏幕上的坐标
    def __init__(self, **kwargs):
        dot.reset_unit()
        self.reset_raw_board()
        self.someone_is_holding_a_piece = False

        # Control的构造函数需要传入一个groups参数
        # 根据UniformTextPresenter的构造函数，这里图省事，直接传入一个空的元组
        Control.__init__(self, *(), **kwargs)
    def _get_surf(self) -> Surface:
        """
        全局绘制。原先的draw_global函数。
        """
        if self.someone_is_holding_a_piece and self.snapshot != None:
            surf = self.snapshot
            # self.held_piece的值会在Demo类的on_mouse_motion方法中更新
            dot.draw_out_of_board(surf, core.get_current_color(), center=self.held_piece)

            # 快速完成绘制
            return surf

        surf = Surface(res.resolution)

        # 第一层：纯色背景
        # 以当前玩家的颜色为底色，以提醒每位玩家现在是谁的回合
        r, g, b = core.get_current_color()
        surf.fill(RGBColor(r // 3, g // 3, b // 3))  # 淡化颜色

        # 第二层：白棋盘
        surf.blit(self.raw_board, (0, 0))

        # 第三层：绘制玩家的棋子
        for player in core.player_list:
            dot.draw(surf, player.color, *player.occupied_location_set)

        # 第四层：当前玩家拿起棋子时，绘制落点
        if self.someone_is_holding_a_piece:
            dot.draw(surf, color.high, *core.q_set)
            dot.draw(surf, color.white, core.get_current_piece())  # 那个被拿起的棋子处要画成白色

        # 拍摄快照以加速绘制
        self.snapshot = take_snapshot(surf)

        return surf
    # 图省事把这一段从DynamicLabel类直接复制过来
    @property
    def surf(self) -> Surface:
        self._update_surf()
        return self._surf
    def reset_raw_board(self):
        # SRCALPHA是一个flag，
        # 为Surface的每个像素增加一个alpha维度（透明度），且初始为0
        self.raw_board = Surface(res.resolution, pygame.SRCALPHA)
        dot.draw(self.raw_board, color.white, *board.board)

        # 初始化snapshot变量，防止出现意外情况
        # 除了这里之外，snapshot的值还可能在当前类的_get_surf方法中更新
        # 也可能在Demo类的pick方法中更新
        self.snapshot = None


def toggle():

    res.toggle_resolution()

    reset()

    draw_global()
    refresh()


def refresh():
    pygame.display.update()
    clock.tick(fps)


def take_snapshot(surf: Surface):
    return surf.copy()


def replay():
    global screen

    screen.blit(snapshot, (0, 0))


def show_trace():
    pass

