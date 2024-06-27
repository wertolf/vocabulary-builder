# 脚本最后会按照字母顺序排列脚本中定义的所有类，方便查阅
# 根据我的记忆，之所以把这么多 Class 放进同一个文件中，可能是因为使用 Type Hint 时可能出现循环引用的问题
from framework.core import RuntimeUnit
# from . import ExternalRuntimeData
from config import color_theme
from framework.io import FontStream

from pygame import Color, Rect, Surface
from pygame.event import EventType
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame.sprite import Group, Sprite
from typing import Dict, List, NoReturn, Optional, Tuple, Union
import pygame


class _Focusable:
    def __init__(self): self._is_focused = False
    @property
    def is_focused(self) -> bool: return self._is_focused
    @is_focused.setter
    def is_focused(self, value: bool) -> None: self._is_focused = value


class _Pressable:
    def __init__(self): self._is_pressed = False
    @property
    def is_pressed(self) -> bool: return self._is_pressed
    @is_pressed.setter
    def is_pressed(self, value: bool) -> None: self._is_pressed = value


class _AbstractControl:
    # 如果Button类直接继承下面的Control类，
    # 那么LabelButton的构造函数中，
    # Label的构造函数和Button的构造函数就会发生冲突

    # 为了解决这一问题，同时也为了保证逻辑没有疏漏，
    # 所以定义了这么一个类
    pass


class _Control(Sprite, _AbstractControl):
    def __init__(
            self, *groups,
            bottom: float = None, centerx: float = None, centery: float = None,
            left: float = None,
            name: str = None,
            right: float = None, top: float = None,
            **kwargs
    ) -> None:
        """

        :param groups:
        :param bottom:
        :param centerx:
        :param centery:
        :param left:
        :param name:
        :param right:
        :param top:
        :param kwargs: 目前这个kwargs主要是为了容错（子类可能传入多余的参数）
        """
        Sprite.__init__(self, *groups)

        if name is None:
            self._name = pygame.time.get_ticks()  # 使用当前时间作为实例的name，这样就不会出现重复的情况
        else:
            self._name = name
        self._surf = self._get_surf()

        self._position_info = self._get_position_info(bottom, centerx, centery, left, right, top)
        self._rect = self._get_rect()

    def _get_rect(self) -> Rect:
        return self._surf.get_rect(**self.position_info)

    def _get_surf(self) -> Surface: pass
    def _update_rect(self) -> None: self._rect = self._get_rect()

    def _update_surf(self) -> None:
        self._surf = self._get_surf()
        self._update_rect()

    def blit_myself(self, target_surf: Surface) -> None:
        target_surf.blit(self.image, self.rect)

    # 存储位置信息的(1+6)个属性
    @property
    def position_info(self) -> dict: return self._position_info
    @property
    def bottom(self) -> int: return self.rect.bottom
    @property
    def centerx(self) -> int: return self.rect.centerx
    @property
    def centery(self) -> int: return self.rect.centery
    @property
    def left(self) -> int: return self.rect.left
    @property
    def right(self) -> int: return self.rect.right
    @property
    def top(self) -> int: return self.rect.top

    @bottom.setter
    def bottom(self, value: int) -> None:
        self.position_info["bottom"] = value
        self._update_rect()

    @centerx.setter
    def centerx(self, value: int) -> None:
        self.position_info["centerx"] = value
        self._update_rect()

    @centery.setter
    def centery(self, value: int) -> None:
        self.position_info["centery"] = value
        self._update_rect()

    @left.setter
    def left(self, value: int) -> None:
        self.position_info["left"] = value
        self._update_rect()

    @right.setter
    def right(self, value: int) -> None:
        self.position_info["right"] = value
        self._update_rect()

    @top.setter
    def top(self, value: int) -> None:
        self.position_info["top"] = value
        self._update_rect()

    # 其他属性
    @property
    def image(self) -> Surface:
        # 这个属性是只读的
        # 仅用于这个Sprite(Control的父类)所属的Group的draw()方法
        return self.surf

    @property
    def name(self) -> str: return self._name
    @property
    def rect(self) -> Rect: return self._rect
    @property
    def surf(self) -> Surface: return self._surf

    @name.setter
    def name(self, value: str) -> None: self._name = value

    @staticmethod
    def _get_position_info(bottom, centerx, centery, left, right, top) -> dict:
        position_info = {}
        # 下面的if系列语句的目的：
        # 只把赋了值的位置参数传入self._get_rect
        # 注意：不能把这些语句的逻辑改成if/elif，原因自己想一想
        if bottom is not None:
            position_info["bottom"] = bottom
        if centerx is not None:
            position_info["centerx"] = centerx
        if centery is not None:
            position_info["centery"] = centery
        if left is not None:
            position_info["left"] = left
        if right is not None:
            position_info["right"] = right
        if top is not None:
            position_info["top"] = top
        return position_info


class _Container:
    # 放置Control的容器
    pass


class _Page:
    def __init__(self, rtu: RuntimeUnit) -> None:
        self._dict_of_controls = {}
        self._event_handlers = []
        self._is_alive = True  # 值变为False时，这个页面的生命周期结束
        self._rtu = rtu

        self.register_events(*rtu.list_of_universal_handlers)

    def do_sth_after_each_loop(self) -> None:
        self.handle_events()

    def do_sth_before_each_loop(self) -> None:
        pass

    def do_sth_before_main_loop_start(self) -> None:
        self.rtu.clear_screen_without_flipping()  # clear screen
        self.draw_and_flip()

    def draw(self) -> None:
        self.group_of_all_sprites.draw(self.rtu.screen)

    def draw_and_flip(self, **kwargs) -> None:
        self.draw()
        self.flip()

    def flip(self, **kwargs): self.rtu.flip(**kwargs)

    def handle_events(self) -> None:
        # 注意，不同于RuntimeUnit.handle_events，
        # Page.handle_events不再是静态方法
        self.rtu.handle_events(*self.event_handlers)

    def loop_once(self) -> None:  # 循环体，可以在Page的子类中自定义
        pass

    def register_controls(self, *controls: _Control) -> None:
        for c in controls:
            self.dict_of_controls[c.name] = c

    def register_events(self, *event_handlers) -> None:
        for event_handler in event_handlers:
            self.event_handlers.append(event_handler)

    def run(self) -> None:
        self.do_sth_before_main_loop_start()
        while self.is_alive:
            self.do_sth_before_each_loop()
            self.loop_once()
            self.do_sth_after_each_loop()

    def update_a_local_control(self, c: _Control) -> None:
        c.blit_myself(self.screen)
        self.rtu.update_a_local_area_of_screen(c.rect)

    def update_local_controls(self, *controls: _Control) -> None:
        for c in controls:
            self.update_a_local_control(c)

    @property
    def dict_of_controls(self) -> Dict[str, _Control]: return self._dict_of_controls
    @property
    def event_handlers(self) -> list: return self._event_handlers
    @ property
    def is_alive(self) -> bool: return self._is_alive

    @ property
    def group_of_all_sprites(self) -> Group:
        g = Group()
        for c in self.dict_of_controls.values():
            g.add(c)
        return g

    @ property
    def length_unit(self) -> float: return self.rtu.length_unit
    @ property
    def rtu(self) -> RuntimeUnit: return self._rtu
    @ property
    def screen(self) -> Surface: return self.rtu.screen
    @ property
    def x_max(self) -> int: return self.rtu.x_max
    @ property
    def x_mean(self) -> int: return self.rtu.x_mean
    @ property
    def x_min(self) -> int: return self.rtu.x_min
    @ property
    def y_max(self) -> int: return self.rtu.y_max
    @ property
    def y_mean(self) -> int: return self.rtu.y_mean
    @ property
    def y_min(self) -> int: return self.rtu.y_min

    @ is_alive.setter
    def is_alive(self, value: bool) -> None: self._is_alive = value


class _TemporaryPage(_Page):
    # 临时页面
    def __init__(
            self, rtu: RuntimeUnit,
            centerx: int = None, centery: int = None,
            window_height: int = None, window_width: int = None,
    ) -> None:
        _Page.__init__(self, rtu)
        self._background_surf = self.rtu.screen.convert_alpha()
        self._background_surf.fill(color_theme.blurring)

        if window_height is None:
            window_height = rtu.resolution_info.temp_win_height
        if window_width is None:
            window_width = rtu.resolution_info.temp_win_width
        self._window_surf = Surface((window_width, window_height))

        if centerx is None:
            centerx = rtu.resolution_info.x_mean
        if centery is None:
            centery = rtu.resolution_info.y_mean
        self._window_rect = self._window_surf.get_rect(centerx=centerx, centery=centery)

    def do_sth_before_main_loop_start(self) -> None:
        # cf. Page.doing_sth_before_main_loop_start
        # 不需要clear screen
        self.screen.blit(self.background_surf, (0, 0))
        self.draw_and_flip()

    def update_a_local_control(self, c: _Control) -> None:
        # 注意：TemporaryPage不需要重写Page的这个方法
        # 因为它的x_min，y_min等位置参数已经作出了相应的调整
        # 所以只要给控件配置位置参数时调用了self.x_min等属性，
        # 就不需要另外操纵self._window_surf
        _Page.update_a_local_control(self, c)

    @ property
    def background_surf(self) -> Surface: return self._background_surf
    @ property
    def window_rect(self) -> Rect: return self._window_rect
    @ property
    def window_surf(self) -> Surface: return self._window_surf
    @ property
    def x_max(self) -> int: return self.window_rect.right
    @ property
    def x_mean(self) -> int: return self.window_rect.centerx
    @ property
    def x_min(self) -> int: return self.window_rect.left
    @ property
    def y_max(self) -> int: return self.window_rect.bottom
    @ property
    def y_mean(self) -> int: return self.window_rect.centery
    @ property
    def y_min(self) -> int: return self.window_rect.top


class _UniformTextPresenter(_Control):
    """present text in the same anti_alias, font, size, color"""
    def __init__(
            self, font: FontStream, size: int,
            anti_alias: bool = False,
            color: Color = color_theme.foreground,
            groups: Union[List[Group], Tuple[Group]] = (),
            **kwargs,
    ) -> None:
        """
        第一次设置控件的属性。
        :param font:
        :param size: in relative pixels (actual pixel = size * resolution_info.length_unit)
        Below are parameters with default values:
        :param anti_alias:
        :param color:
        :param groups:

        :param kwargs: see _Control.__init__
        """
        self._anti_alias = anti_alias
        self._color = color
        self._font = font
        self._size = size
        _Control.__init__(self, *groups, **kwargs)  # 和通常情况不同，把父类的构造函数放在后边

    @property
    def anti_alias(self) -> bool: return self._anti_alias
    @property
    def color(self) -> Color: return self._color
    @property
    def font(self) -> FontStream: return self._font
    @property
    def size(self) -> int: return self._size


class _StaticLabel(_UniformTextPresenter):
    # 单行文本控件
    def __init__(
            self, content: str, **kwargs,
    ) -> None:
        """
        第一次设置控件的属性。
        :param content:
        :param kwargs: see _UniformTextPresenter.__init__
        """
        self._content = content
        _UniformTextPresenter.__init__(self, **kwargs)  # 和通常情况不同，把父类的构造函数放在后边

    def _get_surf(self) -> Surface:

        # TODO: 思考如何支持动态调整分辨率
        # actual_pixel = self.size * resolution_info.length_unit  # 必要的转换
        actual_pixel = self.size * 4

        font_format = [self.font, actual_pixel]
        render_format = [self.content, self.anti_alias, self.color]
        font_object = pygame.font.Font(*font_format)
        surf = font_object.render(*render_format)
        self.font.flush()  # 这一步很重要，否则用这个Font实例画完一次之后，之后就画不出来了
        return surf

    @property
    def content(self) -> str: return self._content


class _DynamicLabel(_StaticLabel):
    # 不仅能改变颜色，还能改变content, font, size的单行文本控件
    @property
    def color(self) -> Color: return self._color
    @property
    def content(self) -> str: return self._content
    @property
    def font(self) -> FontStream: return self._font
    @property
    def size(self) -> int: return self._size

    # 下面的getter是dynamic的关键所在
    @property
    def surf(self) -> Surface:
        self._update_surf()
        return self._surf

    @color.setter
    def color(self, value: Color): self._color = value
    @content.setter
    def content(self, value: str): self._content = value
    @font.setter
    def font(self, value: FontStream): self._font = value
    @size.setter
    def size(self, value: int): self._size = value


class _TextBlock(_UniformTextPresenter):
    def __init__(
            self, lines: Union[List[str]],
            line_width: int = 20,
            horizontal_alignment: str = "left",
            **kwargs
    ) -> None:
        """
        :param lines: ["line1", "line2", ...]
        Below are parameters with default values
        :param line_width: 一行有多少个字，超过后自动换行
        :param horizontal_alignment: left, center, right

        :param kwargs: see StaticLabel.__init__
        """
        self._horizontal_alignment = horizontal_alignment
        self._lines = lines
        self._line_width = line_width
        _UniformTextPresenter.__init__(self, **kwargs)  # 和通常情况不同，把父类的构造函数放在后边

    def _get_surf(self) -> Surface:
        surf_after_previous_enlargement: \
            Optional[Surface] = None
        rect_after_previous_enlargement: \
            Optional[Rect] = None
        for label in self.line_surfs:
            surf_to_be_appended = label.surf
            rect_to_be_united: Rect = label.rect

            if rect_after_previous_enlargement is None:
                # 第一次迭代的情况比较特殊
                rect_after_previous_enlargement = label.rect
                surf_after_previous_enlargement = label.surf
            else:
                # 之后的迭代逻辑相同

                # 按照self.horizontal_alignment进行水平方向的对齐
                if self.horizontal_alignment == "left":
                    rect_to_be_united.left = rect_after_previous_enlargement.left
                elif self.horizontal_alignment == "center":
                    rect_to_be_united.centerx = rect_after_previous_enlargement.centerx
                elif self.horizontal_alignment == "right":
                    rect_to_be_united.right = rect_after_previous_enlargement.right
                # 上下相接
                rect_to_be_united.top = rect_after_previous_enlargement.bottom

                # 创建这一loop的union
                union: Rect = Rect.union(rect_after_previous_enlargement, rect_to_be_united)
                # 创建一个和union尺寸相同的空白Surface
                surf: Surface = Surface([union.width, union.height])
                surf.blit(surf_after_previous_enlargement, rect_after_previous_enlargement)
                surf.blit(surf_to_be_appended, rect_to_be_united)

                # 循环结束前更新状态
                rect_after_previous_enlargement = union
                surf_after_previous_enlargement = surf
            continue

        return surf_after_previous_enlargement

    @ property
    def horizontal_alignment(self) -> str: return self._horizontal_alignment

    @ property
    def line_surfs(self) -> List[_StaticLabel]:
        return [
            _StaticLabel(
                content=line,
                anti_alias=self.anti_alias, color=self.color,
                font=self.font, size=self.size,
            ) for line in self.wrapped_lines
        ]

    @ property
    def lines(self) -> List[str]: return self._lines
    @ property
    def line_width(self) -> int: return self._line_width

    @ property
    def wrapped_lines(self) -> List[str]:
        wrapped_lines = []
        for line in self.lines:
            while len(line) > self.line_width:
                wrapped_lines.append(line[:self.line_width])
                line = line[self.line_width:]
            wrapped_lines.append(line)
        return wrapped_lines


class _Button(_AbstractControl, _Focusable, _Pressable):
    # 由于Button总要依附在某个具体的控件上完成自己的功能
    # 所以Button自己不需要成为Control的子类

    # 这实际上也是为了解决LabelButton的构造函数中发生的问题
    def __init__(self) -> None:
        # 构造函数的签名中不开放（不能传入）is_disabled这个变量
        # 这是为了保证对is_disabled属性的修改只能发生在该属性的setter中
        self._is_disabled = False
        _Focusable.__init__(self)
        _Pressable.__init__(self)

    def command(self) -> None:
        # Button和Label真正本质的区别
        if self.is_disabled:
            return
        pass

    @property
    def is_disabled(self) -> bool: return self._is_disabled
    @is_disabled.setter
    def is_disabled(self, value: bool) -> None: self._is_disabled = value


class _LabelButton(_DynamicLabel, _Button):
    def __init__(self, **kwargs) -> None:
        # 这里必须把Button的构造函数放在Label前面，
        # 否则Label的构造函数通过Control的构造函数调用self._get_surf时，
        # 会因为self._is_disabled还不存在而报错
        _Button.__init__(self)
        _DynamicLabel.__init__(
            self,
            color=color_theme.normal,  # 注意这里规定了默认颜色
            **kwargs,
        )

    @property
    def color(self) -> Color:
        # 注意下面if/else语句的先后顺序，不能随意改变
        if self.is_disabled:
            return color_theme.disabled
        elif self.is_pressed:
            return color_theme.press
        elif self.is_focused:
            return color_theme.focus
        else:
            return self._color


class _PageWithButtons(_Page):
    def __init__(self, rtu: RuntimeUnit) -> None:
        _Page.__init__(self, rtu)
        self.register_events(
            self.on_mouse_button_down,
            self.on_mouse_button_up,
            self.on_mouse_motion,
        )

        # 下面的变量是这个Page的全局变量
        # 把它们放在Page类的子类的实例中，使函数间传递变量成为可能
        # 这不一定是唯一的方法，但是比较方便、清晰
        self._current_focus: Optional[_LabelButton] = \
            None  # 现在的焦点，没有时为None，有时为LabelButton实例

    # event handlers, 以on开头
    def on_mouse_button_down(self, e: EventType) -> None:
        if e.type != MOUSEBUTTONDOWN:
            return
        if self.current_focus is None:
            return  # 只有current_focus不为None时，才需要处理MOUSEBUTTONDOWN
        button, pos = getattr(e, "button"), getattr(e, "pos")
        if button != 1:
            return
        self.current_focus.is_pressed = True  # 更新状态
        self.update_a_local_control(self.current_focus)

    def on_mouse_button_up(self, e: EventType) -> None:
        if e.type != MOUSEBUTTONUP:
            return
        if self.current_focus is None:
            return  # 只有current_focus不为None时，才需要处理MOUSEBUTTONDOWN
        button, pos = getattr(e, "button"), getattr(e, "pos")
        if button != 1:
            return
        self.current_focus.is_pressed = False  # 更新状态
        self.update_a_local_control(self.current_focus)
        self.current_focus.command(self)  # 既然完成了按下和抬起的全过程，就要执行command了

    def on_mouse_motion(self, e: EventType) -> None:
        if e.type != MOUSEMOTION:
            return
        pos = getattr(e, "pos")
        # 下面的if/else语句应该考虑封装成某个类的某个方法
        # 因为显然它很常用，不可能只出现在Home这一页（Page）中
        if self.current_focus is None:
            # 如果此时没有焦点，就检查鼠标是否移动到了某个potential focus上
            for b in self.group_of_enabled_buttons:
                assert isinstance(b, _LabelButton)
                if b.rect.collidepoint(pos):
                    b.is_focused = True
                    self.update_a_local_control(b)
                    self.current_focus = b  # 更新状态
        else:
            # 如果此时有焦点，就检查鼠标移动是否导致鼠标离开了焦点
            if not self.current_focus.rect.collidepoint(pos):
                self.current_focus.is_focused = False  # 更新按钮的状态
                self.update_a_local_control(self.current_focus)
                self.current_focus = None  # 更新页面的状态

    @ property
    def current_focus(self) -> _LabelButton:
        # 现在正focus的button，没有时为None，有时为Button实例
        return self._current_focus

    @ property
    def group_of_all_buttons(self) -> Group:
        g = Group()
        for b in self.dict_of_controls.values():
            if isinstance(b, _LabelButton):
                g.add(b)
        return g

    @ property
    def group_of_enabled_buttons(self) -> Group:
        g = Group()
        for b in self.group_of_all_buttons:
            assert isinstance(b, _LabelButton)
            if not b.is_disabled:
                g.add(b)
        return g

    @ current_focus.setter
    def current_focus(self, value: _LabelButton) -> None: self._current_focus = value


class _TemporaryPageWithButtons(_TemporaryPage, _PageWithButtons):
    def __init__(self, rtu: RuntimeUnit) -> None:
        _TemporaryPage.__init__(self, rtu)
        _PageWithButtons.__init__(self, rtu)


class AbstractControl(_AbstractControl): pass
class Button(_Button): pass
class Control(_Control): pass
class DynamicLabel(_DynamicLabel): pass
class StaticLabel(_StaticLabel): pass
class LabelButton(_LabelButton): pass
class Page(_Page): pass
class PageWithButtons(_PageWithButtons): pass
class TemporaryPage(_TemporaryPage): pass
class TemporaryPageWithButtons(_TemporaryPageWithButtons): pass
class TextBlock(_TextBlock): pass
class UniformTextPresenter(_UniformTextPresenter): pass
