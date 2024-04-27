from .vector import Vector2D

from .color import get_color
from .name import get_name

class Player:
    type: str  # human or bot
    color: tuple
    name: str
    occupied_location_set: set  # set是基于散列表实现的，在进行in运算时性能应该要优于list
    goal_location_set: set

    def __init__(self):
        self.name = get_name()
        self.color = get_color()
    
    def move_piece(self, _from: Vector2D, _to: Vector2D):
        """
        在底层逻辑上（与表示层无关）将棋子从_from处移动到_to处。
        """

        # 这一操作的合理性（比如下面的断言为真）由调用者保证
        assert _from in self.occupied_location_set

        self.occupied_location_set.discard(_from)
        self.occupied_location_set.add(_to)


class Human(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "human"


class Bot(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "bot"
