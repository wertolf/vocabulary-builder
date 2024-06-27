"""
You can customize fonts used in the app here.
"""

from framework.io import FontStream

fonts = {
    "Segoe Print": FontStream("assets/fonts/SegoePrint.ttf"),
    "Segoe Script": FontStream("assets/fonts/SegoeScript.ttf"),
    "黄金时代细体": FontStream("assets/fonts/MFTheGoldenEra-Light.ttf"),
    "文悦后现代体": FontStream("assets/fonts/WenYue-HouXianDaiTi-W4.otf"),
}

logo = fonts["Segoe Script"]
text = fonts["黄金时代细体"]
ui = fonts["文悦后现代体"]
