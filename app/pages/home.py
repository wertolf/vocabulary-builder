from framework.core import RuntimeUnit
from framework.ui import StaticLabel, LabelButton, PageWithButtons
from config import color_theme, font_theme
# from .game import Game
from .settings import Settings
# from .letsjump import Demo  # 跳棋游戏演示界面

from framework.globe import scrmgr


class Home(PageWithButtons):
    def __init__(self, rtu: RuntimeUnit) -> None:
        PageWithButtons.__init__(self, rtu)

        # construct controls and add them to corresponding groups
        self.register_controls(
            StaticLabel(
                content="PYGAME游戏开发框架演示", font=font_theme.ui, size=20,
                top=scrmgr.y_min + scrmgr.length_unit * 20,
                centerx=scrmgr.x_mean,
            )
        )
        self.register_controls(
            Button1(
                top=scrmgr.y_mean - scrmgr.length_unit * 10,
                right=scrmgr.x_max - scrmgr.length_unit * 25,
            )
        )
        b = Button2()  # the buttons are defined at the bottom of the file
        b.top = scrmgr.y_mean + scrmgr.length_unit * 10
        b.right = scrmgr.x_max - scrmgr.length_unit * 25  # 右对齐
        self.register_controls(b)
        b = Button3()
        b.top = scrmgr.y_mean + scrmgr.length_unit * 30
        b.right = scrmgr.x_max - scrmgr.length_unit * 25
        self.register_controls(b)
        b = Button4()
        b.top = scrmgr.y_mean + scrmgr.length_unit * 50
        b.right = scrmgr.x_max - scrmgr.length_unit * 25
        self.register_controls(b)


# 之所以重新定义类，是为了在这个脚本内部定制command方法
# 当然，这样做的一个副作用是，可以在__init__方法中将button的参数设置好
# 之所以把 Button 类的定义放在 Page 下面，
# 是因为 Button 的 command 方法的 page 参数
# 在 type hint 时可能需要将类型设置为 Home 而不是 PageWithButtons
class Button1(LabelButton):
    def __init__(self, **kwargs) -> None:
        LabelButton.__init__(
            self,
            content="开始", font=font_theme.ui, size=10,
            **kwargs,
        )

    def command(self, page: PageWithButtons) -> None:
        page.rtu.present_full_screen_fade_out()
        Game(page.rtu).run()

        # 返回之后，需要重新绘制原来的页面
        self.is_focused = False  # 绘制之前，还原自己的颜色
        page.do_sth_before_main_loop_start()


class Button2(LabelButton):
    def __init__(self) -> None:
        LabelButton.__init__(
            self,
            content="设置", font=font_theme.ui, size=10,
        )

        self.is_disabled = True

    def command(self, page: PageWithButtons) -> None:
        # 不同于前两个页面，“设置”页面绘制之前不需要“淡出”原屏幕
        # 当然也完全可以“淡出"，这里是在尝试另一种可能性
        Settings(page.rtu).run()

        # 返回之后，需要重新绘制原来的页面
        self.is_focused = False  # 绘制之前，还原自己的颜色
        page.do_sth_before_main_loop_start()


class Button3(LabelButton):
    def __init__(self) -> None:
        LabelButton.__init__(
            self,
            content="跳棋小游戏", font=font_theme.ui, size=10,
        )

    def command(self, page: PageWithButtons) -> None:
        page.rtu.present_full_screen_fade_out()
        Demo(page.rtu).run()

        # 返回之后，需要重新绘制原来的页面
        self.is_focused = False  # 绘制之前，还原自己的颜色
        page.do_sth_before_main_loop_start()


class Button4(LabelButton):
    def __init__(self) -> None:
        LabelButton.__init__(
            self,
            content="退出", font=font_theme.ui, size=10,
        )

    def command(self, page: PageWithButtons) -> None:
        page.rtu.end_program()
