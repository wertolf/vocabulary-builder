# 设计文档 v0.1

## ui

之所以定义了一个 UniformTextPresenter 类，是因为 StaticLabel 和 TextBlock 都继承了它

之所以在 UniformTextPresenter 和 StaticLabel 的构造函数的末尾触发父类的构造函数，是因为 Control 的构造函数中需要初始化 _surf 和 _rect 属性，而这只有在要绘制的内容确定之后才能确定

## RuntimeUnit

如果没记错，最初引入 rtu 是因为 DCL 里面 display 被放在一个模块中，同时模块里面包含了初始化 display 的代码，这样就导致无法动态地改变 display

rtu 的特点是在 top-level 的脚本中创建，然后作为参数传入所有 ui 相关类的构造函数，这样就能够通过 rtu 获取到一切想要的全局状态

## 关键问题

### type hint

如果我没记错的话，之所以把同一大类的 class 的定义全部放进一个文件中，是因为在某些 method 的参数中要想进行 type hint 可能需要引用之前定义的类

但是本质上，这似乎是因为我对于 Python 的 type hint 系统没有很好的了解

```py
from pages.home import Home  # 导入一个包含 implementation 的 Home 类
from ??? import Home  # 如何只导入一个 Home 类的 Type Hint
```

实际上这个问题目前在 home.py 中并不存在，打开 game.py 看看就知道我说的是什么意思了

### callback

图形化开发框架中一种主流的对 Button 行为的解决方案应该是 callback 的概念

但是在使用这种机制时，怎样灵活地向 callback 函数传递参数，是一个问题

关键在于我不理解 method 和 function 在 Python 中的一个比较底层的差异


所以说，这个项目目前对于我的意义，更多的是**意识到**自己对面向对象设计 (OOD) 以及图形化开发框架的主流实现的相关知识的欠缺，而不是它做到的这些很有限的东西
