import pygame as pg

from collections import defaultdict

from eye_keyboard import settings as st


class BasePanel(object):

    def __init__(self, selector):
        self.selector = selector
        self.row_col_item = defaultdict()
        top = self.TOP_START
        for row_num, labels in enumerate(self.LABELS):
            left = self.LEFT_START
            for col_num, label in enumerate(labels):
                item = self.__Item__(label, left, top, self.DEFAULT_ACTIVE)
                self.row_col_item[row_num][col_num] = item
                left += self.__Item__.WIDTH
            top += self.__Item__.HEIGHT

    @property
    @classmethod
    def num_rows(cls):
        return len(cls.LABELS)

    @property
    @classmethod
    def num_cols(cls):
        return len(cls.LABELS[0]) if len(cls.LABELS) > 0 else 0

    def draw(self, screen):
        for i, col_item in self.row_col_item.iteritem():
            for j, item in col_item.iteritems():
                item.draw(screen)


class BaseItem(object):

    ANTIALIAS = True
    FILL_RECT = 0
    LINE_WIDTH = 2

    def __init__(self, label, left, top, active):
        self.label = label
        self.left = left
        self.top = top
        self.active = active
        self.font = pg.font.Font(st.FONT_NAME, self.FONT_SIZE)
        font_width, font_height = self.font.size(self.label)
        font_left = self.left + self.WIDTH // 2 - self.font_width // 2
        font_top = self.top + self.HEIGHT // 2 - self.font_height // 2
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
        rect = pg.Rect(self.left, self.TOP, self.WIDTH, self.HEIGHT)
        pg.draw.rect(screen, self.cell_colour, rect, self.FILL_RECT)
        pg.draw.rect(screen, self.line_colour, rect, self.LINE_WIDTH)
        font_surface = self.font.render(self.label, self.ANTIALIAS,
                                        self.text_colour)
        screen.blit(font_surface, self.font_position)


class OptionItem(BaseItem):

    WIDTH = 117
    HEIGHT = 100
    FONT_SIZE = 26


class OptionPanel(BasePanel):

    __Item__ = OptionItem

    TOP_START = 100
    LEFT_START = 150
    DEFAULT_ACTIVE = True

    ERASE = 'VOLTAR'
    CLEAN = 'LIMPAR'
    READ = 'LER'
    ALERT = 'SOM'
    PHRASE = 'FRASE'
    QUIT = 'SAIR'

    LABELS = [
        [ERASE, CLEAN, READ, ALERT, PHRASE, QUIT]
    ]


class LetterItem(BaseItem):

    WIDTH = 100
    HEIGHT = 100
    FONT_SIZE = 70


class LetterPanel(BasePanel):

    __Item__ = LetterItem

    TOP_START = 300
    LEFT_START = 150
    DEFAULT_ACTIVE = False

    LABELS = [
        ['A', 'B', 'C', 'D', 'E', 'F', ''],
        ['G', 'H', 'I', 'J', 'K', 'L', 'M'],
        ['N', 'O', 'P', 'Q', 'R', 'S', ''],
        ['T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    ]
