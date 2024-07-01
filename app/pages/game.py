from ...lega.core import RuntimeUnit
from ...lega.io import (
    color_theme, font_theme, resolution_info,
    StringFileLikeObject,
)
from ...lega.ui import (
    DynamicLabel, LabelButton, PageWithButtons
)
from pygame import Surface
from pygame.event import EventType
from pygame.locals import KEYDOWN, KEYUP, K_BACKSPACE, K_RETURN
from typing import NoReturn, Optional
import openpyxl
import pygame
import random
import string
import sys


class Game(PageWithButtons):
    def __init__(self, rtu: RuntimeUnit) -> None:
        PageWithButtons.__init__(self, rtu)
        self.register_events(self.on_key_down, self.on_key_up)

        self._all_words: list = []
        self._current_word: dict = {}
        self._my_answer: str = ""
        self._words_to_be_answered: list = []

        self._cursor_is_visible: bool = False
        self._moment_when_cursor_changed_last_time: int = pygame.time.get_ticks()

        # construct controls and add them to corresponding groups
        self.register_controls(
            DynamicLabel(
                name="word", content="null",
                font=font_theme.text, size=20,
                bottom=self.y_mean - self.length_unit * 20,
                centerx=self.x_mean,
            ),
            DynamicLabel(
                name="answer", content="",
                font=font_theme.text, size=20,
                centerx=self.x_mean,
                top=self.y_mean + self.length_unit * 20,
                # top, centery, bottom三个参数中，
                # 只有固定top，在content改变时不会上下浮动
            ),
        )
        b = Button1(name="more")
        b.bottom = self.y_max - self.length_unit * 10
        b.left = self.x_min + self.length_unit * 25
        self.register_controls(b)
        b = Button3(name="submit")
        b.top = self.y_mean + self.length_unit * 30
        b.right = self.x_max - self.length_unit * 25
        self.register_controls(b)
        b = Button4()
        b.bottom = self.y_max - self.length_unit * 10
        b.right = self.x_max - self.length_unit * 25
        self.register_controls(b)

        self.collect_words()
        self.select_some_words()
        self.current_word = self.words_to_be_answered.pop(0)
        print(f"[Game.__init__] current word: {self.current_word}")

    def collect_words(self) -> None:
        book = openpyxl.load_workbook(r"微型词库.xlsx")
        sheet = book.get_sheet_by_name("汉译英")
        how_many_rows = len(sheet["A"][1:])  # 第一个元素是表头
        for row_number in range(how_many_rows):
            row_number += 1
            d = {}
            for column_number in "AB":
                key = sheet[f"{column_number}1"].value  # 列的第一个元素是表头
                value = sheet[f"{column_number}{row_number}"].value
                d[key] = value

            self.all_words.append(d)

    def loop_once(self) -> None:
        now = pygame.time.get_ticks()
        if (now - self._moment_when_cursor_changed_last_time) > 300:
            self.cursor_is_visible = not self.cursor_is_visible

    def on_key_down(self, e: EventType) -> None:
        if e.type != KEYDOWN:
            return
        key = getattr(e, "key")
        for letter in string.ascii_lowercase:
            exec(f"from pygame.locals import K_{letter}")
            is_letter = eval(f"key == K_{letter}")
            if is_letter:
                self.my_answer += letter
                self.cursor_is_visible = True
        if key == K_BACKSPACE:
            self.my_answer = self.my_answer[:-1]
            self.cursor_is_visible = True
        if key == K_RETURN:
            b = self.dict_of_controls["submit"]
            assert isinstance(b, Button3)
            if b.is_disabled:
                b = self.dict_of_controls["more"]
                assert isinstance(b, Button1)
            b.is_pressed = True
            self.update_a_local_control(b)

    def on_key_up(self, e: EventType) -> None:
        if e.type != KEYUP:
            return
        key = getattr(e, "key")
        if key == K_RETURN:
            b = self.dict_of_controls["submit"]
            assert isinstance(b, Button3)
            if b.is_disabled:
                b = self.dict_of_controls["more"]
                assert isinstance(b, Button1)
            b.command(self)
            b.is_pressed = False
            b.is_focused = True
            self.current_focus = b
            self.update_a_local_control(b)

    def select_some_words(self, times=5) -> None:
        for t in range(times):
            length = len(self.all_words)
            index = random.randint(0, length-1)
            self.words_to_be_answered.append(
                self.all_words.pop(index)
            )

    @property
    def all_words(self) -> list: return self._all_words
    @property
    def current_word(self) -> dict: return self._current_word
    @property
    def cursor_is_visible(self) -> bool: return self._cursor_is_visible

    @property
    def cursor(self) -> Surface:
        surf = Surface((self.length_unit*5, self.length_unit))
        surf.fill(self.rtu.foreground)
        return surf

    @property
    def my_answer(self) -> str: return self._my_answer
    @property
    def words_to_be_answered(self) -> list: return self._words_to_be_answered

    @current_word.setter
    def current_word(self, value: dict) -> None:
        self._current_word = value

        self.rtu.clear_screen_without_flipping()
        label = self.dict_of_controls["word"]
        assert isinstance(label, DynamicLabel)
        label.content = value["Chinese"]
        self.draw_and_flip()
        print(f"[Game.current_word.setter][END] current word: {value}")

    @cursor_is_visible.setter
    def cursor_is_visible(self, value: bool) -> None:
        self._cursor_is_visible = value

        rect = self.cursor.get_rect()
        label = self.dict_of_controls["answer"]
        assert isinstance(label, DynamicLabel)
        rect.left = label.right
        rect.bottom = label.top + label.size * self.length_unit
        if self._cursor_is_visible:  # 绘制cursor
            self.screen.blit(self.cursor, rect)
            self.rtu.update_a_local_area_of_screen(rect)
        else:  # 绘制和cursor同样大小的黑块
            surf = self.cursor.convert_alpha()
            surf.fill(self.rtu.background)
            self.screen.blit(surf, rect)
            self.rtu.update_a_local_area_of_screen(rect)

        self._moment_when_cursor_changed_last_time = pygame.time.get_ticks()

    @my_answer.setter
    def my_answer(self, value: str) -> None:
        self._my_answer = value

        self.rtu.clear_screen_without_flipping()
        label = self.dict_of_controls["answer"]
        assert isinstance(label, DynamicLabel)
        label.content = value
        self.draw_and_flip()


# 之所以重新定义类，是为了在这个脚本内部定制command方法
# 当然，这样做的一个副作用是，可以在__init__方法中将button的参数设置好
class Button1(LabelButton):
    def __init__(self, **kwargs) -> None:
        LabelButton.__init__(
            self,
            content="再来5个", font=font_theme.ui, size=10,
            **kwargs,
        )
        self.is_disabled = True

    def command(self, page: Game) -> None:
        page.select_some_words()

        # 检查答案是否正确
        answer = page.current_word["English"]
        is_correct = (answer == page.my_answer)
        print(f"[Button1.command] correct: {is_correct}")
        if is_correct:
            page.current_word = page.words_to_be_answered.pop(0)
            page.my_answer = ""  # 清空答题框
        else:
            pass

        self.is_disabled = True
        b = page.dict_of_controls["submit"]
        assert isinstance(b, Button3)
        b.is_disabled = False
        page.update_local_controls(self, b)


class Button3(LabelButton):
    def __init__(self, **kwargs) -> None:
        LabelButton.__init__(
            self,
            content="提交", font=font_theme.ui, size=10,
            **kwargs,
        )

    def command(self, page: Game) -> None:
        if self.is_disabled:
            return

        # 检查答案是否正确
        answer = page.current_word["English"]
        is_correct = (answer == page.my_answer)
        print(f"[Button3.command] correct: {is_correct}")
        if is_correct:
            page.current_word = page.words_to_be_answered.pop(0)
            page.my_answer = ""  # 清空答题框
        else:
            pass

        if len(page.words_to_be_answered) == 0:
            self.is_disabled = True
            b = page.dict_of_controls["more"]
            assert isinstance(b, Button1)
            b.is_disabled = False
            page.update_local_controls(self, b)


class Button4(LabelButton):
    def __init__(self, **kwargs) -> None:
        LabelButton.__init__(
            self,
            content="返回标题", font=font_theme.ui, size=10,
            **kwargs,
        )

    def command(self, page: PageWithButtons) -> None:
        page.is_alive = False
