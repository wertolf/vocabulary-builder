from collections import namedtuple

RGBColor = namedtuple("RGBColor", ["r", "g", "b"])

black = (0, 0, 0)
white = (255, 255, 255)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

yellow = (255, 255, 0)

# 增加alpha维度
trans = (0, 0, 0, 0)  # transparent

# 特定用途的颜色
high = yellow

# 玩家的颜色
i = -1  # 用于记录已经分配的颜色数，防止重复
color_list = \
[
    blue,
    red,
    green,
]

def get_color():
    global i

    i += 1
    i %= len(color_list)

    return color_list[i]
