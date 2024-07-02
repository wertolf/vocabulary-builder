## v0.5 (not finished)

* 取消 Control 对 Sprite 的继承
* 使用 list/dict/set 取代 Group
* 剔除冗余
  * Control
    * blit_myself
  * Page
    * draw
    * draw_and_flip
* 将 Page.update_a_local_control 整合进 Page.update_local_controls 并重命名为 Page.update_page_component
* 追加 Page.do_sth_after_main_loop_ends 以使 Logo 和其他页面一样只需重写 loop_once 方法
* 令 FadeIn 适配调整后的框架并通过测试

## v0.4

* 将 framework 改名为 lega
* 善用 Find in File 功能剔除冗余
  * ScreenManager
    * cam_width, cam_height, temp_win_width, temp_win_height
  * RuntimeUnit
    * blits_on_the_screen_and_flip_it
* 引入 Vector2D
* 把 x_mean 改成 center.x
* 定义 on_key_up
* 将 check_if_user_pressed_f5 放进 on_key_up
* 将 end_program 从 RuntimeUnit 移到 globe
* 将 GlobalState 整合进 Animation
* 将 start_waiting 和 stop_waiting 移入 Animation
* 将事件处理相关方法从 RuntimeUnit 中解耦，形成单独的 event_manager 模块
* 使用 handle_events 进行动画过程中的事件处理，而不额外定义专门的 handle_events_during_animation 函数

### 关于 lega 的命名

取自 legacy 的前四个字母，表示这个框架诞生于对一个老旧项目的维护

同时与“雷迦”谐音，带有一定的中二色彩

## v0.3

* 剔除冗余
  * ui.Page
    * handle_events
    * length_unit, x_max, x_mean, x_min, y_max, y_mean, y_min
    * screen
* 将 resolution 相关计算以及 screen 从 RuntimeUnit 中解耦，放入 ScreenManager 类中
  * 详见 ScreenManager 的 class diagram

## v0.2

最终状态
* 可以显示 Logo
* 可以进入 Home
* 可以从 Home 按“退出”键退出

具体修改
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
* 去除没有必要的 runtime_data.pkl 的读写逻辑
  * 由于暂时回想不起来 ExternalRuntimeData 这个类的必要性，因此暂时予以保留，但是改名为 GlobalState
  * 相应地去除 RuntimeUnit 的 is_waiting 属性
* 将动画功能从 RuntimeUnit 中解耦出来

## v0.1

* 集成跳棋逻辑
  * 前面的更改忘记做记录了
  * 移植`cancel`的逻辑
  * 移植`confirm`的逻辑
