import pygame as pg

from eye_keyboard import settings as st


class Phrase(object):

    ANTIALIAS = True
    FONT_SIZE = 60
    BLIT_POS = (110, 610)

    def __init__(self):
        self.text = ''
        self.font = pg.font.Font(st.FONT_NAME, self.FONT_SIZE)

    def draw(self, screen):
        phrase_surface = self.font.render(self.text, self.ANTIALIAS, st.WHITE)
        screen.blit(phrase_surface, self.BLIT_POS)
