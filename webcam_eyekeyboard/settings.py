# Eye Tracker settings
PUPIL_COLOUR = (0, 0, 0)
THRESHOLD_BACKGROUND_COLOUR = (100, 100, 255, 255)
DEFAULT_THRESHOLD = 45
DEFAULT_PUPIL_WIDTH = 25
DEFAULT_PUPIL_HEIGHT = 12

# Screen settings
SCREEN_SIZE = (1366, 768)
CAMERA_SIZE = (640, 480)
BACKGROUND_COLOUR = (0, 0, 0)
FOREGROUND_COLOUR = (255, 255, 255)

# Colour options
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 128)

# Vocalware settings
VOCALWARE = {
    'EID': '2',
    'LID': '6',
    'VID': '1',
    'EXT': 'mp3',
    'FX_TYPE': '',
    'FX_LEVEL': '',
    'ACC': '5601687',
    'API': '2473353',
    'SESSION': '',
    'HTTP_ERR': '',
    'CS': '36c45a542118d397453d473e16c71d6b'
}

# General settings
NUM_PANELS = 2
OPTION_PANEL = 0
LETTER_PANEL = 1
THINK_TIME = 2.0
ROW_THINK_TIME = 1.0
SPEECH_SPEED = 44100

# Button settings
BUTTON_NAMES = ['1', '2', '3', 'up', 'down', 't', 'space', 'escape']
BUTTON_STATES = ['active', 'inactive']

# Letter panel settings

LINE_WIDTH = 2
NUM_ROWS = 4
NUM_COLS = 7

ROW_COL_TEXT = [
    ['A', 'B', 'C', 'D', 'E', 'F', ''],
    ['G', 'H', 'I', 'J', 'K', 'L', 'M'],
    ['N', 'O', 'P', 'Q', 'R', 'S', ''],
    ['T', 'U', 'V', 'W', 'X', 'Y', 'Z']
]

START_LEFT = 150
START_TOP = 300
FILL_RECT = 0
WIDTH = 100
HEIGHT = 100
FONT_SIZE = 70

FONT_NAME = 'resources/roboto_regular-webfont.ttf'
ALERT_FILE_PATH = 'resources/alert.mp3'

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

pg.mouse.set_visible(True)

SMALL_FONT = init_font(font_size=12)
LARGE_FONT = init_font(font_size=24)
