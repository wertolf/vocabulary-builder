import pygame

import framework.core as core
import app.pages

if __name__ == "__main__":
    pygame.init()

    rtu = core.RuntimeUnit()

    app.pages.Logo(rtu).run()

    while True:
        app.pages.Home(rtu).run()
