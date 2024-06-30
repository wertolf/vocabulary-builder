## v0.2 (not finished)

* 将 app/__init__.py 中的内容移至 main.py
* bug fix: NoReturn
  * NoReturn 表示这个函数不应该有返回值，所以 Pylance 看到这样的声明之后会将之后的代码标记为 unreachable
  * 使用 VSCode 的 Replace in Files 功能将 NoReturn 批量修改为 None
* 调整项目结构
* 在根目录下新建 config 子目录，存放可以由用户自定义的内容，如颜色主题和字体主题，以与框架相分离
  * 也可以用 json 乃至于任何一种描述数据的语法实现，但是既然能用 Python 实现，何必用其他方式呢
  * 相应的类也被转换成模块
    * ColorTheme -> color_theme.py
    * FontTheme -> font_theme.py
    * ResolutionInfo -> resolution.py
* 删除无用的类
  * io
    * ExternalAssets
* 删除无用的逻辑
  * 将字体文件打包成 zip 然后再调用 Python 的 zipfile 进行读取
* 用 PPT 绘制模块之间的关系图以及部分类之间的继承关系
* 学习使用 UML 类图

## v0.1

* 集成跳棋逻辑
  * 前面的更改忘记做记录了
  * 移植`cancel`的逻辑
  * 移植`confirm`的逻辑
