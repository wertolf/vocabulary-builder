from framework.core import RuntimeUnit
from config import color_theme, font_theme
from framework.ui import (
    StaticLabel, LabelButton, Page, TemporaryPageWithButtons,
)


class Settings(TemporaryPageWithButtons):
    def __init__(self, rtu: RuntimeUnit) -> None:
        TemporaryPageWithButtons.__init__(self, rtu)

        # construct controls and add them to corresponding groups
        self.register_controls(
            StaticLabel(
                content="设置", font=font_theme.ui, size=20,
                top=self.y_min + self.length_unit * 0,
                centerx=self.x_mean,
            ),
            StaticLabel(
                content="是否全屏", font=font_theme.ui, size=15,
                left=self.x_min + self.length_unit * 10,
                top=self.y_min + self.length_unit * 40,
            ),
            StaticLabel(
                content="Tips: 你可以通过F5键在游戏中随时切换屏幕状态。",
                font=font_theme.ui, size=8,
                centerx=self.x_mean,
                top=self.y_min + self.length_unit * 60,
            )
        )
        b = Button1()
        b.top = self.y_min + self.length_unit * 40
        b.right = self.x_max - self.length_unit * 50
        self.register_controls(b)
        b = Button2()
        b.top = self.y_min + self.length_unit * 40
        b.right = self.x_max - self.length_unit * 10
        self.register_controls(b)
        b = Button3()
        b.top = self.y_mean + self.length_unit * 50
        b.centerx = self.x_mean
        self.register_controls(b)


# 之所以重新定义类，是为了在这个脚本内部定制command方法
# 当然，这样做的一个副作用是，可以在__init__方法中将button的参数设置好
class Button1(LabelButton):
    def __init__(self) -> None:
        # 在Settings.__init__中配置按钮的位置参数
        LabelButton.__init__(
            self,
            content="是", font=font_theme.ui, size=10,
        )

    def command(self, page: Page) -> None:
        pass


class Button2(LabelButton):
    def __init__(self) -> None:
        # 在Settings.__init__中配置按钮的位置参数
        LabelButton.__init__(
            self,
            content="否", font=font_theme.ui, size=10,
        )

    def command(self, page: Page) -> None:
        pass


class Button3(LabelButton):
    def __init__(self) -> None:
        # 在Settings.__init__中配置按钮的位置参数
        LabelButton.__init__(
            self,
            content="返回", font=font_theme.ui, size=10,
        )

    def command(self, page: Page) -> None:
        print(f"[Button3] clicked.")
        page.is_alive = False
