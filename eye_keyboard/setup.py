import pygame as pg

from os.path import join, abspath, split

import settings as st


def init_font(font_size):
    pg.font.init()
    try:
        fontname = join(
            split(abspath(__file__))[0],
            'resources',
            'roboto_regular-webfont.ttf'
        )
    except:
        fontname = pg.font.get_default_font()
        print "warning: could not find 'roboto_regular-webfont.ttf'"
    return pg.font.Font(fontname, font_size)

SCREEN = pg.display.set_mode(st.SCREEN_SIZE, pg.RESIZABLE)
# SCREEN = pg.display.set_mode(st.SCREEN_SIZE, pg.FULLSCREEN | pg.HWSURFACE | pg.DOUBLEBUF)

pg.mouse.set_visible(True)

SMALL_FONT = init_font(font_size=12)
LARGE_FONT = init_font(font_size=24)
