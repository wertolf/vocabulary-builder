# 脚本最后会按照字母顺序排列脚本中定义的所有类，方便查阅
from .constants import (
    color_theme, resolution_info,
    ColorTheme, ResolutionInfo,
)
from pygame import Color, Rect, Surface
from pygame.event import EventType
from pygame.locals import (
    KEYUP, MOUSEBUTTONUP, QUIT,
    K_F5,
    FULLSCREEN,
)
from typing import NoReturn, Tuple, Union
import pickle
import pygame
import sys


class _ExternalRuntimeData:
    def __init__(self) -> NoReturn:
        # 下面的变量不方便通过传入rtu在脚本之间沟通数据，所以通过外置文件的方式存储和读取
        # 由于每次调用、更新都需要重构整个实例，为了保证运行速度，不要给这个实例定义太多属性
        try:
            with open(r"runtime_data.pkl", "rb") as file:
                erd = pickle.load(file)
            assert isinstance(erd, _ExternalRuntimeData)
            self._is_waiting = erd.is_waiting
            self._should_return_at_once = erd.should_return_at_once
        except (
            AssertionError, AttributeError,
            FileNotFoundError,
        ):
            # 程序第一次运行，或者数据文件损坏时，使用默认值重构risd
            self._is_waiting = False  # when waiting for user's interaction, set to True
            self._should_return_at_once = False  # use inside an animation
            # 重构完成后，将数据存储到外部文件中
            self.save()

    def save(self) -> NoReturn:
        # 将数据存储到外部文件中
        with open(r"runtime_data.pkl", "wb") as file:
            pickle.dump(self, file)

    @property
    def is_waiting(self) -> bool: return self._is_waiting
    @property
    def should_return_at_once(self) -> bool: return self._should_return_at_once

    @is_waiting.setter
    def is_waiting(self, value: bool) -> NoReturn:
        self._is_waiting = value
        self.save()

    @should_return_at_once.setter
    def should_return_at_once(self, value: bool) -> NoReturn:
        print(f"[ERD.should_return_at_once.setter] value: {value}")
        self._should_return_at_once = value
        self.save()


class _RuntimeUnit:
    """
    the unit of run-time dataset & operations.
    """
    def __init__(self) -> NoReturn:
        self._resolution_info = resolution_info
        self._color_theme = color_theme

        self.screen = pygame.display.set_mode(self.resolution)  # 这个变量只能通过在整个程序的不同函数中不断传入rtu来保持，不能存储在外部，所以rtu这个类的存在是必要的
        self.is_full_screen = False
        self.clock = pygame.time.Clock()
        self.fps = 30

    def blits_on_the_screen_and_flip_it(self, *blit_params, **kwargs) -> NoReturn:
        self.screen.blits(blit_params)
        self.flip(**kwargs)

    # 特殊的事件处理器(event handlers)，统一以check if开头
    def check_if_user_clicked_or_pressed(self, e: EventType) -> NoReturn:
        if e.type in (MOUSEBUTTONUP, KEYUP):
            if e.type == KEYUP:
                assert hasattr(e, "key")
                key = getattr(e, "key")
                if key in (K_F5, ):
                    return  # ignore irrelevant key pressing
            self.stop_waiting()

    def check_if_user_pressed_f5(self, e: EventType) -> NoReturn:
        """切换屏幕状态（全屏/窗口）。"""
        if e.type != KEYUP:
            return
        assert hasattr(e, "key")
        key = getattr(e, "key")
        if key != K_F5:
            return

        self.is_full_screen = not self.is_full_screen
        content_backup = self.screen.copy()
        if self.is_full_screen:
            self.screen = pygame.display.set_mode(self.resolution, FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.resolution)

        # 修正屏幕切换所导致的显示问题。方法很简单，重新绘制一下原来的内容
        self.screen.fill(self.background)
        self.screen.blit(content_backup, self.rect)
        self.flip()

    def clear_screen_without_flipping(self) -> NoReturn:
        self.screen.fill(self.background)

    def clear_screen_and_flip(self) -> NoReturn:
        self.clear_screen_without_flipping()
        self.flip()

    def flip(self, delay: int = 0) -> NoReturn:
        # cf. self.update_a_local_area_of_screen()
        pygame.display.flip()
        pygame.time.delay(delay)
        self.clock.tick(self.fps)

    def handle_universal_events_during_each_animation_frame(self) -> NoReturn:
        self.handle_events(
            *self.list_of_universal_handlers,
            self.handle_mouse_button_up_during_animation,
        )

    # 动画(animations)，统一以present开头
    def present_full_screen_fade_in(
            self,
            variable_surf: Surface,
            destination: Union[Rect, Tuple[int, int]] = (0, 0),
            speed: int = 20,
    ) -> NoReturn:
        """
        实现全屏“淡入”，前两个参数同Surface.blit保持一致
        :param variable_surf:
        :param destination:
        :param speed:
        :return:
        """
        for alpha in range(0, 255, speed):
            self.screen.fill(self.background)
            variable_surf.set_alpha(alpha)
            self.screen.blit(variable_surf, destination)
            self.flip()

            self.handle_universal_events_during_each_animation_frame()
            erd = _ExternalRuntimeData()
            if erd.should_return_at_once:
                erd.should_return_at_once = False  # 还原状态
                return

    def present_full_screen_fade_out(self) -> NoReturn: self.present_fade_out(self.screen, time_delayed=0)

    def present_fade_out(
            self, surf: Surface,
            destination=(0, 0), speed=20,
            click_needed: bool = False,
            click_optional: bool = False, count_down: int = 1000,
            time_delayed: int = 300,
    ) -> NoReturn:
        """
        实现内容从屏幕上“淡出”的效果。
        :param surf: 如果赋值为self.screen，就是全屏淡出
        Below are parameters which have a default value.
        :param destination:
        :param speed:
        :param click_needed: 如果赋值为True，将一直等待，直到用户点击屏幕
        :param click_optional: 在倒计时count_down结束之前，点击屏幕可以提前开始动画
        :param count_down: 如果click_optional为True，倒计时结束之后自动开始动画
        :param time_delayed: 在“淡出”动画开始前，内容在屏幕上停留的时间（单位：ms）
        :return: None
        """
        assert (click_needed and click_optional) is not True, "click_needed and click_optional should not both be True."
        if click_needed or click_optional:
            self.start_waiting()
            time_when_waiting_began = pygame.time.get_ticks()
            while self.is_waiting:
                if click_optional:
                    time_at_the_moment = pygame.time.get_ticks()
                    time_passed = time_at_the_moment - time_when_waiting_began
                    if time_passed >= count_down:
                        self.stop_waiting()
                        break
                self.handle_events(
                    self.check_if_user_clicked_or_pressed,
                    *self.list_of_universal_handlers,
                )
        pygame.time.delay(time_delayed)
        surf = surf.copy()
        for alpha in range(255, 0, -speed):
            self.screen.fill(self.background)
            surf.set_alpha(alpha)
            self.screen.blit(surf, destination)
            self.flip()

            self.handle_universal_events_during_each_animation_frame()
            erd = _ExternalRuntimeData()
            if erd.should_return_at_once:
                erd.should_return_at_once = False  # 还原状态
                return

    def sleep(self, count_down: int) -> NoReturn:
        # 这个方法是为了弥补pygame.time.delay运行期间无法响应退出事件的问题
        time_when_waiting_began = pygame.time.get_ticks()
        while True:
            time_at_the_moment = pygame.time.get_ticks()
            time_passed = time_at_the_moment - time_when_waiting_began
            if time_passed >= count_down:
                break
            self.handle_events(
                *self.list_of_universal_handlers,
                self.handle_mouse_button_up_during_animation,
            )
            if _ExternalRuntimeData().should_return_at_once:
                break

    def start_waiting(self) -> NoReturn:
        pygame.event.clear()  # 为了防止之前遗留的事件意外地结束waiting
        self.is_waiting = True

    def stop_waiting(self) -> NoReturn: self.is_waiting = False

    def update_a_local_area_of_screen(self, area: Rect) -> NoReturn:
        # cf. self.flip()
        pygame.display.update(area)
        self.clock.tick(self.fps)

    @property
    def background(self) -> Color: return self.color_theme.background
    @property
    def color_theme(self) -> ColorTheme: return self._color_theme
    @property
    def foreground(self) -> Color: return self.color_theme.foreground

    @property
    def is_waiting(self) -> bool:
        # 这是一个特殊的属性，
        # 因为它不是通过self的被保护的属性(以"_"开头)获取自己的值
        return _ExternalRuntimeData().is_waiting

    @property
    def length_unit(self) -> float: return self.resolution_info.length_unit

    @property
    def list_of_universal_handlers(self) -> list:
        return [
            self.on_quit,
            self.check_if_user_pressed_f5,
        ]

    @property
    def rect(self) -> Rect: return self.rectangle
    @property
    def rectangle(self) -> Rect: return self.screen.get_rect()
    @property
    def resolution(self) -> Tuple[int, int]: return self.resolution_info.resolution
    @property
    def resolution_info(self) -> ResolutionInfo: return self._resolution_info
    @property
    def x_max(self) -> int: return self.resolution_info.x_max
    @property
    def x_mean(self) -> int: return self.resolution_info.x_mean
    @property
    def x_min(self) -> int: return self.resolution_info.x_min
    @property
    def y_max(self) -> int: return self.resolution_info.y_max
    @property
    def y_mean(self) -> int: return self.resolution_info.y_mean
    @property
    def y_min(self) -> int: return self.resolution_info.y_min

    @is_waiting.setter
    def is_waiting(self, value: bool) -> NoReturn:
        # 这是一个特殊的属性，
        # 因为它不是通过self的被保护的属性(以"_"开头)设定自己的值
        _ExternalRuntimeData().is_waiting = value

    @staticmethod
    def end_program() -> NoReturn:

        # 回复默认值
        erd = _ExternalRuntimeData()
        erd.is_waiting = False
        erd.should_return_at_once = False

        pygame.quit()
        sys.exit()

    @staticmethod
    def handle_events(*handlers) -> NoReturn:
        for e in pygame.event.get():
            for event_handler in handlers:
                event_handler(e)

    @staticmethod
    def handle_mouse_button_up_during_animation(e: EventType) -> NoReturn:
        # 在动画进行过程中，按下鼠标左键或右键可以提前结束动画
        if e.type != MOUSEBUTTONUP:
            return
        _ExternalRuntimeData().should_return_at_once = True
        print(f"[handle_mouse_button_up][END] should_return_at_once: {_ExternalRuntimeData().should_return_at_once}")

    # 事件处理器(event handlers)，统一以on开头
    @staticmethod
    def on_quit(e: EventType) -> NoReturn:
        """
        Caution: Should be called inside every event handler.
        :param: e: a pygame EventType object
        """
        if e.type == QUIT:
            _RuntimeUnit.end_program()


class ExternalRuntimeData(_ExternalRuntimeData): pass
class RuntimeUnit(_RuntimeUnit): pass
