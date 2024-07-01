import pygame


class RuntimeUnit:
    """
    the unit of run-time dataset & operations.
    """
    def __init__(self) -> None:
        pass

    def sleep(self, count_down: int) -> None:
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
            if sttmgr.should_return_at_once:
                break
