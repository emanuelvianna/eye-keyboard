from __future__ import division

import pygame

from os.path import join, split, abspath, exists
from time import time
from collections import defaultdict
import settings as st

BACKGROUND_COLOUR = (0, 0, 0)
THINK_TIME = 2.0
ROW_THINK_TIME = 1.0
SPEECH_SPEED = 44100
INTERMEDIATE = 210

STATES = {
    0: [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
    1: [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
    2: [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
}


# TODO: add docstring
def launch_keyboard(tracker, display_size):
    disp = _init_display(display_size)
    font = _init_fonts()
    pygame.mixer.init(SPEECH_SPEED)
    _run_gui(tracker, font, disp)


def _init_fonts():
    pygame.font.init()
    try:
        fontname = join(
            split(abspath(__file__))[0],
            'resources',
            'roboto_regular-webfont.ttf'
        )
    except:
        fontname = pygame.font.get_default_font()
        print "warning: could not find 'roboto_regular-webfont.ttf'"
    font = pygame.font.Font(fontname, 60)
    return font


def _init_display(display_size):
    # disp = pygame.display.set_mode(display_size, pygame.FULLSCREEN |
    #                                pygame.HWSURFACE | pygame.DOUBLEBUF)
    disp = pygame.display.set_mode(display_size, pygame.RESIZABLE)
    disp.fill(BACKGROUND_COLOUR)
    return disp


# TODO: create a Keyboard component class
def _update_keyboard(screen, row_idx, col_idx):
    top = st.START_TOP
    for i in xrange(st.NUM_ROWS):
        left = st.START_LEFT
        for j in xrange(st.NUM_COLS):
            if i == row_idx:
                if col_idx == -1 or j == col_idx:
                    cell_colour = st.DARK_BLUE
                    text_colour = st.WHITE
                    line_colour = st.WHITE
                else:
                    cell_colour = st.WHITE
                    text_colour = st.DARK_BLUE
                    line_colour = st.DARK_BLUE
            else:
                cell_colour = st.WHITE
                text_colour = st.DARK_BLUE
                line_colour = st.DARK_BLUE
            rect = pygame.Rect(left, top, st.WIDTH, st.HEIGHT)
            pygame.draw.rect(screen, cell_colour, rect, st.FILL_RECT)
            pygame.draw.rect(screen, line_colour, rect, st.LINE_WIDTH)
            text = st.ROW_COL_TEXT[i][j]
            font = pygame.font.Font(st.FONT_NAME, st.FONT_SIZE)
            surf = font.render(text, True, text_colour)
            font_width, font_height = font.size(text)
            screen.blit(surf, (left + st.WIDTH / 2 - font_width / 2,
                        top + st.HEIGHT / 2 - font_height / 2))
            left += st.WIDTH
        top += st.HEIGHT


def _play_sound(row_idx, col_idx):
    if col_idx == -1:
        number = row_idx + 1
        file_name = '{}.wav'.format(number)
    else:
        letter = st.ROW_COL_TEXT[row_idx][col_idx].lower()
        file_name = '{}.wav'.format(letter)
    file_path = join('resources', file_name)
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


def _run_gui(tracker, font, disp):
    row, col = 0, -1
    intermediate = tracker.pupil_pos
    blitpos = (
        tracker.pupil_rect[0] - 20,
        tracker.pupil_rect[1] - 20,
        tracker.pupil_rect[2] + 40,
        tracker.pupil_rect[3] + 40
    )
    _play_sound(row, col)
    _update_keyboard(disp, row, col)
    phrase = ""
    cnt, sum_pupil_y = 0, 0
    start = time()
    start_row = None
    while True:
        if _check_escape():
            break
        if (time() - start) > THINK_TIME:
            if start_row is None:
                avg_pupil_y = sum_pupil_y / cnt
                answer = avg_pupil_y < intermediate[1]
                if col == -1:
                    if answer is True:
                        col = 0
                        start_row = time()
                    else:
                        row = (row + 1) % st.NUM_ROWS
                else:
                    if answer is True:
                        phrase += st.ROW_COL_TEXT[row][col]
                        row, col = 0, -1
                    else:
                        col += 1
                        if (col + 1) == st.NUM_COLS:
                            col = -1
            if start_row is not None:
                if (time() - start_row) > ROW_THINK_TIME:
                    start_row = None
                    _play_sound(row, col)
                    _update_keyboard(disp, row, col)
                    surf = font.render(phrase, True, (255, 255, 255))
                    disp.blit(surf, (110, 610))
                    cnt, sum_pupil_y = 0, 0
                    start = time()
            else:
                _play_sound(row, col)
                _update_keyboard(disp, row, col)
                surf = font.render(phrase, True, (255, 255, 255))
                disp.blit(surf, (110, 610))
                cnt, sum_pupil_y = 0, 0
                start = time()
        img, thresholded = tracker.give_me_all(use_prect=True)
        sum_pupil_y += tracker.pupil_pos[1]
        cnt += 1
        pygame.draw.line(
            img, (255, 0, 0), (intermediate[0] - 50, intermediate[1]),
            (intermediate[0] + 50, intermediate[1]))
        pygame.draw.rect(img, (0, 255, 0), tracker.pupil_rect, 1)
        pygame.draw.circle(img, (255, 0, 0), tracker.pupil_pos, 3, 0)
        crop = pygame.Surface((160, 320))
        crop.blit(img, (0, 0), blitpos)
        scale = pygame.transform.scale(crop, (500, 1000))
        disp.blit(scale, (800, 50))
        if start_row is None:
            _update_keyboard(disp, row, col)
        pygame.display.flip()


def _check_escape():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == 'escape':
                return True
    return False
