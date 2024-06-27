"""
CAUTION
This module must not import any part of the project
which is outside the package "constants",
otherwise there will be a "mutual import" error.
"""
# 脚本最后会按照字母顺序排列脚本中定义的所有类，方便查阅
import io
import logging
from typing import Any


class _FileLikeObject(io.IOBase):
    def __init__(self) -> None:
        self._content = None
        self._position = 0

    def close(self) -> None:
        # 我希望自己写的这个类不需要这个方法
        # 这样就可以让实例在内存中长期存在，而不是仅仅存在于with/as语句之中
        pass

    def flush(self) -> None:
        self.position = 0

    def read(self, size: int = -1) -> bytes:
        if size == -1:
            cont = self.content[self.position:]
            self.position = -1  # EOF (end of file)
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

    def seekable(self) -> bool:
        return True

    @property
    def content(self) -> Any:
        return self._content

    @property
    def length(self) -> int:
        return len(self.content)

    @property
    def position(self) -> int:
        return self._position

    @content.setter
    def content(self, value) -> None:
        self._content = value

    @position.setter
    def position(self, value) -> None:
        self._position = value


class _BinaryFileLikeObject(_FileLikeObject):
    def __init__(self, content: bytes = bytes()) -> None:
        _FileLikeObject.__init__(self)
        self.content = content

    @property
    def bytes(self) -> bytes:
        return self.content

    @bytes.setter
    def bytes(self, value: bytes) -> None:
        self.content = value


class _StringFileLikeObject(_FileLikeObject):
    def __init__(self, content: str = str()) -> None:
        _FileLikeObject.__init__(self)
        self.content = content

    @property
    def str(self) -> str:
        return self.content

    @str.setter
    def str(self, value: str) -> None:
        self.content = value


class _FontStream(_BinaryFileLikeObject):
    def __init__(self, file_name: str) -> None:
        _BinaryFileLikeObject.__init__(self)

        with open(file_name, "rb") as f:
            self.bytes = f.read()

        logging.info(f"[Font.__init__][END] name: {file_name}, bytes length: {self.length}")

    @property
    def file_name(self) -> str:
        return self._file_name

class BinaryFileLikeObject(_BinaryFileLikeObject): pass
class FileLikeObject(_FileLikeObject): pass
class FontStream(_FontStream): pass
class StringFileLikeObject(_StringFileLikeObject): pass
