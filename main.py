import pygame

import lega.core as core
import app.pages

if __name__ == "__main__":
    pygame.init()

    app.pages.Logo().run()
    while True:
        app.pages.Home().run()
