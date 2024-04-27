import math
import pygame

from .vector import Vector2D

from ...general.constants import resolution_info as res

o: Vector2D  # 棋盘坐标系的原点，像素坐标系的中心

d: int  # 棋盘上两个圆圈在屏幕上的距离，单位：像素
r: int  # 圆圈的半径

# 单位向量。
# x轴的单位向量i_hat指向屏幕右方
# y轴的单位向量j_hat由i_hat逆时针旋转120度而得
i_hat: Vector2D
j_hat: Vector2D

def draw(surface, color, *args):
    for p in args:
        x = o.x + (p.x * i_hat.x) + (p.y * j_hat.x)
        y = o.y - (p.x * i_hat.y) + (p.y * j_hat.y)
        pygame.draw.circle(surface, color, (x, y), r, 0)


def draw_out_of_board(surface, color, center):
    """
    在棋盘之外绘制圆圈，用于追踪MOUSEMOTION
    """
    pygame.draw.circle(surface, color, center, r, 0)


def reset_unit():
    """
    基于分辨率，重置长度单位。
    """
    global d
    global i_hat
    global j_hat
    global o
    global r

    w = res.win_width
    h = res.win_height

    o = Vector2D(w // 2, h // 2)

    if (w, h) == (800, 600):
        d = 40 
        r = 10
    elif (w, h) == (1280, 720):
        d = 50
        r = 15
    elif (w, h) == (1920, 1080):
        d = 60
        r = 20

    # 注意：
    # 屏幕坐标系的y轴方向朝下，而我定义的棋盘坐标系的y轴方向朝上，
    # 所以j_hat的y坐标前面要乘以(-1)，这跟x坐标前面乘以(-1)的原因不同
    i_hat = Vector2D(d, 0)
    j_hat = Vector2D((-1) * d / 2, (-1) * d * math.sqrt(3) / 2)

