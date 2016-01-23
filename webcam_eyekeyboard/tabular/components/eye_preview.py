import pygame as pg

from eye_keyboard import settings as st


class EyePreview(object):

    LINE_WIDTH = 1
    CIRCLE_RADIUS = 3
    FILL_CIRCLE = 0
    BLIT_POS = (950, 100)

    def __init__(self, eye_tracker):
        self.snapshot = None
        self.pupil_rect = None
        self.pupil_pos = None
        pupil_left, pupil_top = eye_tracker.pupil_pos
        self.line_start = (pupil_left - 50, pupil_top)
        self.line_end = (pupil_left + 50, pupil_top)
        rect_left, rect_top, rect_width, rect_height = eye_tracker.pupil_rect
        self.crop_pos = (rect_left - 20, rect_top - 20,
                         rect_width + 40, rect_height + 40)

    def draw(self, screen):
        pg.draw.line(self.eye_tracker.snapshot, st.RED,
                     self.line_start, self.line_end)
        pg.draw.rect(self.eye_tracker.snapshot, st.GREEN,
                     self.eye_tracker.pupil_rect, self.LINE_WIDTH)
        pg.draw.circle(self.eye_tracker.snapshot, st.RED,
                       self.eye_tracker.pupil_pos, self.CIRCLE_RADIUS,
                       self.FILL_CIRCLE)
        crop = pg.Surface((160, 320))
        crop.blit(self.eye_tracker.snapshot, (0, 0), self.crop_pos)
        scale = pg.transform.scale(crop, (500, 1000))
        screen.blit(scale, self.BLIT_POS)
