import math

from .vector import Vector2D

from . import core
from . import dot

def screen2board(pos):
    """
    将屏幕坐标转换为棋盘坐标。

    具体的公式推导不难，就是一个二元一次方程组，
    可以用小学方法求解，也可以用线性代数的工具求解。
    不过由于涉及到屏幕坐标系的转换，容易出错，
    我是在debugger的帮助下重新检查了一遍纸上的推导然后才发现错误的
    """

    # 先将原点从屏幕的左上角（这是屏幕坐标系的原点）移到屏幕的中心（这是棋盘坐标系的原点）
    pos_normalized = Vector2D(pos[0] - dot.o.x, pos[1] - dot.o.y)

    x = (pos_normalized.x / dot.d) + (pos_normalized.y / dot.d) * (1 / math.sqrt(3)) * (-1)
    y = (pos_normalized.y / dot.d) * (2 / math.sqrt(3)) * (-1)
    return Vector2D(x, y)

def detect(pos):
    """
    碰撞检测。

    检测当前鼠标所在位置是否位于棋盘上的某点（圆圈）内，
    如果是，返回该点在棋盘上的坐标。

    我没有在数学上证明点p的坐标就近取整后所得坐标即为距离p最近的圆圈，
    只是一个猜想，不知道可不可行
    """
    p = screen2board(pos)
    nearest_point = Vector2D(round(p.x), round(p.y))

    # 碰撞发生的前提1：nearest_point在棋盘上
    # 碰撞发生的前提2：p在以nearest_point为圆心，以dot.r为半径的圆圈内
    collided = False
    if core.is_inside_board(nearest_point):

        inside_circle = \
            ((p.x - nearest_point.x) ** 2 + (p.y - nearest_point.y) ** 2) \
            <= (dot.r ** 2)

        if inside_circle:
            collided = True

    return (collided, nearest_point)
