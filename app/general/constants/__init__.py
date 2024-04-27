"""
CAUTION
This module must not import any part of the project
which is outside the package "constants",
otherwise there will be a "mutual import" error.
"""
# 脚本最后会按照字母顺序排列脚本中定义的所有类，方便查阅
from .colors import (
    BLACK, BLUE, CYAN, GREEN,
    GREY, RED, WHITE, YELLOW,
)
from pygame import Color
from typing import NoReturn, Tuple
import io
import zipfile


class _ColorTheme:
    def __init__(self) -> NoReturn:
        self._background = BLACK
        self._blurring = Color(0, 0, 0, 160)  # 用于TemporaryPage
        self._disabled = GREY
        self._focus = YELLOW  # 控件被focus时的颜色
        self._foreground = WHITE
        self._normal = WHITE  # 控件正常状态下（没有被focus）的颜色
        self._player_black = BLACK
        self._player_white = WHITE
        self._press = CYAN  # 控件被press时的颜色

    @property
    def background(self) -> Color: return self._background
    @property
    def blurring(self) -> Color: return self._blurring
    @property
    def disabled(self) -> Color: return self._disabled
    @property
    def focus(self) -> Color: return self._focus
    @property
    def foreground(self) -> Color: return self._foreground
    @property
    def normal(self) -> Color: return self._normal
    @property
    def player_black(self) -> Color: return self._player_black
    @property
    def player_white(self) -> Color: return self._player_white
    @property
    def press(self) -> Color: return self._press


class _ResolutionInfo:
    def __init__(self) -> NoReturn:
        self._win_width = 1280  # 在这里设定屏幕的长
        self._win_height = 720  # 在这里设定屏幕的宽

    @property
    def cam_width(self) -> float:
        return self.win_width * 1  # 在这里设定有效显示区域的长

    @property
    def cam_height(self) -> float:
        return self.win_height * 1  # 在这里设定有效显示区域的宽

    @property
    def center(self) -> Tuple[float, float]: return self.x_mean, self.y_mean

    @property
    def length_unit(self) -> int:  # 必须是int，否则在创建Font实例时会报错
        return int(self.win_height / (9 * 20))

    @property
    def resolution(self) -> Tuple[int, int]: return self.win_width, self.win_height
    @property
    def temp_win_height(self) -> int: return int(self.win_height * 0.75)
    @property
    def temp_win_width(self) -> int: return int(self.win_width * 0.75)
    @property
    def win_height(self) -> int: return self._win_height
    @property
    def win_width(self) -> int: return self._win_width
    @property
    def x_max(self) -> int: return self.x_mean + int(self.cam_width * 0.5)
    @property
    def x_mean(self) -> int: return int(self.win_width * 0.5)
    @property
    def x_min(self) -> int: return self.x_mean - int(self.cam_width * 0.5)
    @property
    def y_max(self) -> int: return self.y_mean + int(self.cam_height * 0.5)
    @property
    def y_mean(self) -> int: return int(self.win_height * 0.5)
    @property
    def y_min(self) -> int: return self.y_mean - int(self.cam_height * 0.5)


class _FileLikeObject(io.IOBase):
    def __init__(self) -> NoReturn:
        self._content = None
        self._position = 0

    def close(self) -> NoReturn:
        # 我希望自己写的这个类不需要这个方法
        # 这样就可以让实例在内存中长期存在，而不是仅仅存在于with/as语句之中
        pass

    def flush(self) -> NoReturn: self.position = 0

    def read(self, size: int = -1) -> bytes:
        if size == -1:
            cont = self.content[self.position:]
            self.position = -1  # EOF(end of file)
        else:
            cont = self.content[self.position:self.position+size]
            self.position += size
        return cont

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        if whence == io.SEEK_SET:
            self.position = offset
        elif whence == io.SEEK_CUR:
            self.position += offset
        elif whence == io.SEEK_END:
            self.position = self.length + offset
        return self.position

    def seekable(self) -> bool: return True
    @property
    def content(self): return self._content
    @property
    def length(self) -> int: return len(self.content)
    @property
    def position(self) -> int: return self._position
    @content.setter
    def content(self, value) -> NoReturn: self._content = value
    @position.setter
    def position(self, value) -> NoReturn: self._position = value


class _BinaryFileLikeObject(_FileLikeObject):
    def __init__(self, content: bytes = bytes()) -> NoReturn:
        _FileLikeObject.__init__(self)
        self.content: bytes = content

    @property
    def bytes(self) -> bytes: return self.content
    @bytes.setter
    def bytes(self, value: bytes) -> NoReturn: self.content = value


class _StringFileLikeObject(_FileLikeObject):
    def __init__(self, content: str = str()) -> NoReturn:
        _FileLikeObject.__init__(self)
        self.content: str = content

    @property
    def str(self) -> str: return self.content
    @str.setter
    def str(self, value: str) -> NoReturn: self.content = value


class _ExternalAssets:
    def __init__(self) -> NoReturn:
        with open(r"font.zip", "rb") as file:
            self._font = file.read()

    @property
    def font(self) -> bytes: return self._font


_external_assets = _ExternalAssets()


class _FontStream(_BinaryFileLikeObject):
    def __init__(self, file_name: str) -> NoReturn:
        _BinaryFileLikeObject.__init__(self)

        self._file_name = file_name
        with io.BytesIO(_external_assets.font) as bio:
            with zipfile.ZipFile(bio, "r") as zip_file:
                self.bytes = zip_file.read(self.file_name)
        print(f"[Font.__init__][END] name: {file_name}, bytes length: {self.length}")

    @property
    def file_name(self) -> str: return self._file_name


class _FontTheme:
    dict = {
        "Segoe Print": _FontStream("SegoePrint.ttf"),
        "Segoe Script": _FontStream("SegoeScript.ttf"),
        "黄金时代细体": _FontStream("MFTheGoldenEra-Light.ttf"),
        "文悦后现代体": _FontStream("WenYue-HouXianDaiTi-W4.otf"),
    }

    def __init__(self) -> NoReturn:
        self._logo = self.dict["Segoe Script"]
        self._text = self.dict["黄金时代细体"]
        self._ui = self.dict["文悦后现代体"]

    @property
    def logo(self) -> _FontStream: return self._logo
    @property
    def text(self) -> _FontStream: return self._text
    @property
    def ui(self) -> _FontStream: return self._ui


class BinaryFileLikeObject(_BinaryFileLikeObject): pass
class ColorTheme(_ColorTheme): pass
class ExternalAssets(_ExternalAssets): pass
class FileLikeObject(_FileLikeObject): pass
class FontTheme(_FontTheme): pass
class FontStream(_FontStream): pass
class ResolutionInfo(_ResolutionInfo): pass
class StringFileLikeObject(_StringFileLikeObject): pass


color_theme = ColorTheme()
font_theme = FontTheme()
resolution_info = ResolutionInfo()
