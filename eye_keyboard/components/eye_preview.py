import pygame as pg

from eye_keyboard import settings as st


class EyePreview(object):

    LINE_WIDTH = 1
    CIRCLE_RADIUS = 3
    FILL_CIRCLE = 0
    BLIT_POS = (950, 100)

    def __init__(self, tracker):
        self.snapshot = None
        self.pupil_rect = None
        self.pupil_pos = None
        pupil_left, pupil_top = tracker.settings[st.PUPIL_POSITION]
        self.line_start = (pupil_left - 50, pupil_top)
        self.line_end = (pupil_left + 50, pupil_top)
        left, top, width, height = tracker.settings[st.PUPIL_RECTANGLE]
        self.crop_pos = (left - 20, top - 20, width + 40, height + 40)

    def update(self, snapshot, pupil_pos, pupil_rect):
        self.snapshot = snapshot
        self.pupil_pos = pupil_pos
        self.pupil_rect = pupil_rect

    def draw(self, screen):
        pg.draw.line(self.snapshot, st.RED,
                     self.line_start, self.line_end)
        pg.draw.rect(self.snapshot, st.GREEN,
                     self.pupil_rect, self.LINE_WIDTH)
        pg.draw.circle(self.snapshot, st.RED,
                       self.pupil_pos, self.CIRCLE_RADIUS,
                       self.FILL_CIRCLE)
        crop = pg.Surface((160, 320))
        crop.blit(self.snapshot, (0, 0), self.crop_pos)
        scale = pg.transform.scale(crop, (500, 1000))
        screen.blit(scale, self.BLIT_POS)
