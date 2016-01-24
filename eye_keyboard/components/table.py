# encoding: utf8

import pygame as pg

from collections import defaultdict

from eye_keyboard import settings as st


class Cell(object):

    ANTIALIAS = True
    FILL_RECT = 0
    LINE_WIDTH = 2
    WIDTH = 120
    HEIGHT = 100

    def __init__(self, label, left, top, active, font_size):
        self.label = label
        self.left = left
        self.top = top
        self.active = active
        self.font = pg.font.Font(st.FONT_NAME, font_size)
        font_width, font_height = self.font.size(self.label)
        font_left = self.left + self.WIDTH // 2 - font_width // 2
        font_top = self.top + self.HEIGHT // 2 - font_height // 2
        self.font_position = (font_left, font_top)

    @property
    def cell_colour(self):
        return st.DARK_BLUE if self.active else st.WHITE

    @property
    def line_colour(self):
        return st.WHITE if self.active else st.DARK_BLUE

    @property
    def text_colour(self):
        return st.WHITE if self.active else st.DARK_BLUE

    def draw(self, screen):
        rect = pg.Rect(self.left, self.top, self.WIDTH, self.HEIGHT)
        pg.draw.rect(screen, self.cell_colour, rect, self.FILL_RECT)
        pg.draw.rect(screen, self.line_colour, rect, self.LINE_WIDTH)
        font_surface = self.font.render(self.label, self.ANTIALIAS,
                                        self.text_colour)
        screen.blit(font_surface, self.font_position)


class Table(object):

    TOP_START = 200
    LEFT_START = 80
    DEFAULT_ACTIVE = False

    SMALL_FONT = 26
    LARGE_FONT = 70

    ERASE = 'VOLTAR'
    CLEAN = 'LIMPAR'
    READ = 'LER'
    ALERT = 'SOM'
    QUIT = 'SAIR'
    SPACE = 'ESPACO'

    LABELS = [
        ['A', 'B', 'C', 'D', 'E', 'F', SPACE],
        ['G', 'H', 'I', 'J', 'K', 'L', 'M'],
        ['N', 'O', 'P', 'Q', 'R', 'S', ''],
        ['T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
        [ERASE, CLEAN, READ, ALERT, QUIT, '', '']
    ]

    def __init__(self):
        top = self.TOP_START
        self.cells = defaultdict(dict)
        self.num_rows = len(self.LABELS)
        for row_num in xrange(self.num_rows):
            left = self.LEFT_START
            labels = self.LABELS[row_num]
            self.num_cols = len(labels)
            for col_num in xrange(self.num_cols):
                label = labels[col_num]
                font_size = self.LARGE_FONT
                if len(label) > 1:
                    font_size = self.SMALL_FONT
                active = False
                if row_num == 0:
                    active = True
                item = Cell(label, left, top, active, font_size)
                self.cells[row_num][col_num] = item
                left += Cell.WIDTH
            top += Cell.HEIGHT

    def draw(self, screen):
        for i in xrange(self.num_rows):
            for j in xrange(self.num_cols):
                self.cells[i][j].draw(screen)
