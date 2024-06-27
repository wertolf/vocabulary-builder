# 背单词软件

## 启动软件（Windows平台）

你需要安装最新版本的 [Python 解释器](https://www.python.org/downloads/)和 [`pygame` 第三方库](https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation)。

安装完成后，只需要打开命令行，输入
```
python main.py
```
即可进入软件界面。

你可以在软件的运行过程中随时按右上角的 `X` 按钮退出。如果无法退出，可以在命令行界面按 `Ctrl` 加 `C` 组合键发送键盘中断。

### 调试

```
python -m pdb main.py
```

## 设计思想概述 & 点评 & 经验总结

虽然本作相比于[上一部作品](https://github.com/wertolf/draw-card-life)在
* UI 的响应时间
* 项目的结构、代码的可重用性

上有了明显的进步，但是，它距离一个优秀的应用开发实践仍然存在很大差距。

* 引入 RTU (Runtime Unit) 一定程度上解决了上一部作品中“全局变量泛滥以致代码难以重用于开发其他应用/游戏”的问题，但是其 monolithic 的 nature 还是显得不够灵活；理论上说，存在更为合理的模块化方案：
  * 低耦合：不同方面的功能分别归属于不同的模块
  * 高内聚
* 这部作品的编写很大程度上受到了 [`pyglet`](https://github.com/pyglet/pyglet) 的影响，包括
  * 极简的 `main.py` 入口脚本
  * 装饰器的泛滥
* 虽然不一定有效/有意义，但确实能够看到一些高级技巧/技术的使用痕迹，除了前面提到的装饰器之外，还有
  * 将字体文件以字节流的形式读入内存，再传给 `pygame.font.Font` 类的[构造函数](https://www.pygame.org/docs/ref/font.html#pygame.font.Font)
    * 参见 `app/general/constants/__init__.py` 文件中的 [`FontStream`](./app/general/constants/__init__.py#L171) 类
  * 在包含类定义的文件末尾按照字母顺序重新排列该文件所定义的所有类
    * 这主要是为了在 IDE 不支持“跳转到特定标识符的定义”功能的情况下提高编程效率/降低查找类定义所需的时间成本
    * 这个做法当然值得争议：即使 IDE 不够强大，也完全可以使用 `grep` 和 `egrep` 等程序来查找文本文件中的内容（当年写这个项目时，我还不知道 `grep` 和 `egrep` 的存在）
  * 使用 `zipfile` 标准库向用户隐藏对 `font.zip` 文件的解压过程
  * 使用 `pickle` 标准库对数据进行持久化
  * 使用 `openpyxl` 第三方库读取 xlsx 文件

本质上来说，它仍然只是一个用来练手的作品：
* 在很多方面达不到业界的要求
* 很多技术的使用是为了练习/炫技，而并非是针对需求场景的最优解决方案
