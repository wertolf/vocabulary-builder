# 待办事项

* [ ] 以技术博客的形式发布一些针对此项目的讲解文章，顺便也重新整理（甚至是重新学习）一下相关的技术点。一些可以做的点
  * 装饰器
  * 字节流与 Python 的 `io` 标准库
    * 顺便看看 APUE 里面讲标准输入输出的章节 (?)
* [ ] 新建 animation.py 文件，定义一个 Animation 类及其子类，在这些类的构造函数中传入 rtu，这样就可以将 rtu 的一部分方法解耦出来

## 一些想法

让 Control 和 Page 等常用基类继承 IdentifiableObject，该类拥有 id 和 type 属性，用于在构造结束时通过 logging.debug 输出调试信息

Sprite 作为 Control 的属性就可以避免多重继承

使用 xaml 或其他标记语言描述页面布局信息，并编写一个 parser
