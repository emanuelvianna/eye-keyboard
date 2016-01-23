import pygame as pg

from eye_keyboard import settings as st


class Title(object):

    ANTIALIAS = True
    FONT_SIZE = 24

    def __init__(self, label):
        self.label = label
        self.font = pg.font.Font(st.FONT_NAME, self.FONT_SIZE)
        title_size = st.LARGE_FONT.size(self.label)
        title_left = st.DISPLAY_SIZE[0] / 2 - title_size[0] / 2
        title_top = st.DISPLAY_SIZE[1] / 2 - (st.CAMERA_SIZE[1] / 2 + title_size[1])
        self.title_pos = (title_left, title_top)

    def draw(self):
        title_surface = self.font.render(self.label, self.ANTIALIAS, st.WHITE)
        st.SCREEN.blit(title_surface, self.title_pos)
