from typing import Tuple

class ResolutionManager:
    def __init__(self, width, height):
        self._win_width = width
        self._win_height = height

    @property
    def cam_width(self) -> float:
        return self.win_width * 1  # 在这里设定有效显示区域的长

    @property
    def cam_height(self) -> float:
        return self.win_height * 1  # 在这里设定有效显示区域的宽

    @property
    def center(self) -> Tuple[float, float]:
        return self.x_mean, self.y_mean

    @property
    def length_unit(self) -> int:  # 必须是int，否则在创建Font实例时会报错
        return int(self.win_height / (9 * 20))

    @property
    def resolution(self) -> Tuple[int, int]:
        return self.win_width, self.win_height

    @property
    def temp_win_height(self) -> int:
        return int(self.win_height * 0.75)

    @property
    def temp_win_width(self) -> int:
        return int(self.win_width * 0.75)

    @property
    def win_height(self) -> int:
        return self._win_height

    @property
    def win_width(self) -> int:
        return self._win_width

    @property
    def x_max(self) -> int:
        return self.x_mean + int(self.cam_width * 0.5)

    @property
    def x_mean(self) -> int:
        return int(self.win_width * 0.5)

    @property
    def x_min(self) -> int:
        return self.x_mean - int(self.cam_width * 0.5)

    @property
    def y_max(self) -> int:
        return self.y_mean + int(self.cam_height * 0.5)

    @property
    def y_mean(self) -> int:
        return int(self.win_height * 0.5)

    @property
    def y_min(self) -> int:
        return self.y_mean - int(self.cam_height * 0.5)
