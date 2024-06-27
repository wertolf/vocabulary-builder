"""
跳棋游戏演示界面。
"""

from ....framework.core import RuntimeUnit
from ....framework.io import (
    font_theme
)
from ....framework.ui import (
    LabelButton, PageWithButtons
)
from typing import NoReturn

from . import core
from . import presentation
from . import collision

from .vector import Vector2D

from pygame.event import EventType
from pygame import MOUSEBUTTONUP, MOUSEMOTION

class Demo(PageWithButtons):
    board: presentation.Board
    def __init__(self, rtu: RuntimeUnit) -> None:
        PageWithButtons.__init__(self, rtu)

        core.start_game_2p()
        board = presentation.Board()
        self.register_controls(board)

        self.board = board
    
    def on_mouse_button_up(self, e: EventType):
        if e.type != MOUSEBUTTONUP:
            return
        button, pos = getattr(e, "button"), getattr(e, "pos")

        if self.board.someone_is_holding_a_piece and button == 3:
            self.cancel()
        elif button == 1:
            collided, nearest_point = collision.detect(pos)

            if collided:
                if self.board.someone_is_holding_a_piece:
                    self.confirm(nearest_point)
                else:
                    self.pick(nearest_point)

        return super().on_mouse_button_up(e)
    def on_mouse_motion(self, e: EventType):
        if e.type != MOUSEMOTION:
            return
        if not self.board.someone_is_holding_a_piece:
            return

        pos = getattr(e, "pos")
        self.board.held_piece = pos

        self.update_local_controls(self.board)

        return super().on_mouse_motion(e)
    def pick(self, v: Vector2D):
        """
        剧本触发条件：在未执子状态下，玩家点击鼠标左键
        需要作出的响应：拿起棋子
        """

        if not core.is_valid_pick(v):
            return  # 不能拿起空位或者别人的棋子

        # 更新核心层状态
        core.set_current_piece(v)
        core.calculate_q_set()

        # 更新表示层状态
        self.board.someone_is_holding_a_piece = True
        self.board.snapshot = None
        # 这一步还需要配合Board类在surf的getter里面调用self._update_surf方法
        self.update_local_controls(self.board)
    def cancel(self):
        """
        剧本触发条件：玩家已经拿起棋子，此时点击鼠标右键
        需要作出的响应：放下棋子，即把拿起的棋子放回原位

        此函数相当于pick()的逆操作，实现时，对应pick()函数更新相应的状态即可。
        并且由于不需要计算q_set，所以比pick()简单。
        """

        # 更新核心层状态
        core.set_current_piece(None)

        # 更新表示层状态
        self.board.someone_is_holding_a_piece = False

        self.update_local_controls(self.board)
    def confirm(self, v: Vector2D):
        """
        剧本触发条件：玩家已经拿起棋子，此时点击鼠标左键
        需要作出的响应：落子

        注意“放下棋子”和“落子”的区别，前者是放回原处，后者是放到新的地方
        然而两者确实有相同之处，所以修改此函数时需参考pick()
        """
        if not core.is_valid_move(v):
            return  # 如果落子点非法，do nothing，继续保持拿起棋子的状态

        # 更新核心层状态
        player = core.get_current_player()
        piece = core.get_current_piece()
        player.move_piece(_from=piece, _to=v)

        # 更新表示层状态
        self.board.someone_is_holding_a_piece = False

        # 绘制棋子的移动轨迹（动画）
        # pre.show_trace()

        # 切换到下一回合
        core.next_turn()

        # 更新表示层状态
        self.update_local_controls(self.board)
