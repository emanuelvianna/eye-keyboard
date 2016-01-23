import pygame as pg

from eye_keyborad import settings as st

BUTTON_HEIGHT = 50
BUTTON_WIDTH = 50


class Button(object):

    ACTIVE = 'active'
    INACTIVE = 'inactive'
    STATUS = [ACTIVE, INACTIVE]

    def __init__(self, name):
        self.rect = (self.pos[0], self.pos[1],
                     st.BUTTON_HEIGHT, st.BUTTON_WIDTH)
        self.status_image = {
            status: pg.image.load("resources/%s_%s.png" % (name))
            for status in self.STATUS
        }

    def draw(self, screen):
        screen.blit(self.status_image[self.status], self.pos)


class Button1(Button):

    def __init__(self):
        left = int(st.SCREEN_SIZE[0] * (2 / 6.0) - BUTTON_HEIGHT / 2)
        top = st.SCREEN_SIZE[1] / 2 + int(st.CAMERA_SIZE[1] * 0.6)
        self.pos = (left, top)
        Button.__init__(self)


class Button2(Button):

    def __init__(self):
        left = int(st.SCREEN_SIZE[0] * (3 / 6.0) - BUTTON_HEIGHT / 2)
        top = st.SCREEN_SIZE[1] / 2 + int(st.CAMERA_SIZE[1] * 0.6)
        self.pos = (left, top)
        Button.__init__(self)


class Button3(Button):

    def __init__(self):
        left = int(st.SCREEN_SIZE[0] * (4 / 6.0) - BUTTON_HEIGHT / 2)
        top = st.SCREEN_SIZE[1] / 2 + int(st.CAMERA_SIZE[1] * 0.6)
        self.pos = (left, top)
        Button.__init__(self)


class SpaceButton(Button):

    def __init__(self):
        left = int(st.SCREEN_SIZE[0] * (5 / 6.0) - BUTTON_HEIGHT / 2)
        top = st.SCREEN_SIZE[1] / 2 + int(st.CAMERA_SIZE[1] * 0.6)
        self.pos = (left, top)
        Button.__init__(self)


class UpButton(Button):

    def __init__(self):
        left = st.SCREEN_SIZE[0] / 2 + st.CAMERA_SIZE[0] / 2 + BUTTON_HEIGHT
        top = st.SCREEN_SIZE[1] / 2 - BUTTON_WIDTH
        self.pos = (left, top)
        Button.__init__(self)


class DownButton(Button):

    def __init__(self):
        left = st.SCREEN_SIZE[0] / 2 + st.CAMERA_SIZE[0] / 2 + BUTTON_HEIGHT
        top = st.SCREEN_SIZE[1] / 2 + BUTTON_WIDTH
        self.pos = (left, top)
        Button.__init__(self)


class EscapeButton(Button):

    def __init__(self):
        self.pos = (BUTTON_HEIGHT, BUTTON_WIDTH)
        Button.__init__(self)


class TButton(Button):

    def __init__(self):
        left = st.SCREEN_SIZE[0] / 2 - (st.CAMERA_SIZE[0] / 2 + BUTTON_HEIGHT)
        top = st.SCREEN_SIZE[1] / 2 + st.CAMERA_SIZE[1] / 2 - BUTTON_WIDTH / 2
        self.pos = (left, top)
        Button.__init__(self)
