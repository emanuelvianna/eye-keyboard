from __future__ import division

import pygame

from os.path import join, split, abspath, exists
from time import time
from collections import defaultdict

BACKGROUND_COLOUR = (0, 0, 0)
THINK_TIME = 2.0
SPEECH_SPEED = 44100
INTERMEDIATE = 210
NUM_ROWS = 3
NUM_COLS = 9
STATES = {
    0: [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
    1: [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
    2: [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
}
LETTER = {
    0: {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I'},
    1: {0: 'J', 1: 'K', 2: 'L', 3: 'M', 4: 'N', 5: 'O', 6: 'P', 7: 'Q', 8: 'Q'},
    2: {0: 'S', 1: 'T', 2: 'U', 3: 'V', 4: 'X', 5: 'W', 6: 'Y', 7: 'Z', 8: ' '},
}


def launch_keyboard(tracker, display_size):
    """
    Display a keyboard controlled by pupils.

    Parameters
    ----------
    eye_tracker: EyeTracker
        webcam eye tracker

    Raises
    ------
    """
    disp = _init_display(display_size)
    imgs = _init_images()
    snd = _init_sounds()
    font = _init_fonts()
    _run_gui(snd, tracker, font, disp, imgs)


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


def _init_images():
    kb_imgs = defaultdict(lambda: {})
    pygame.mixer.init()
    resdir = join(split(abspath(__file__))[0], 'resources')
    if not exists(resdir):
        raise Exception("could not find 'resources' directory")
    for row, cols in STATES.iteritems():
        for col in cols:
            if col == -1:
                filename = "{0}.png".format(row)
            else:
                filename = "{0}_{1}.png".format(row, col)
            filepath = join(resdir, filename)
            kb_imgs[row][col] = pygame.image.load(filepath)
    return kb_imgs


def _init_sounds():
    snd = defaultdict(lambda: {})
    pygame.mixer.init(SPEECH_SPEED)
    resdir = join(split(abspath(__file__))[0], 'resources')
    if not exists(resdir):
        raise Exception("could not find 'resources' directory")
    for row, cols in STATES.iteritems():
        for col in cols:
            if col == -1:
                filename = "{0}.wav".format(row)
            else:
                filename = "{0}_{1}.wav".format(row, col)
            snd[row][col] = join(resdir, filename)
    return snd


def _run_gui(snd, tracker, font, disp, kb_imgs):
    row, col = 0, -1
    intermediate = tracker.settings['pupilpos']
    pupilbounds = tracker.settings['pupilbounds']
    blitpos = (pupilbounds[0] - 20, pupilbounds[1] - 20, pupilbounds[2] + 40, pupilbounds[3] + 40)
    pygame.mixer.music.load(snd[row][col])
    pygame.mixer.music.play()
    disp.blit(kb_imgs[row][col], (100, 250))
    phrase = ""
    cnt, sum_pupil_y = 0, 0
    start = time()
    while True:
        if _check_escape():
            break
        if (time() - start) > THINK_TIME:
            avg_pupil_y = sum_pupil_y / cnt
            answer = avg_pupil_y < intermediate[1]
            if col == -1:
                if answer is True:
                    col = 0
                else:
                    row = (row + 1) % NUM_ROWS
            else:
                if answer is True:
                    phrase += LETTER[row][col]
                    row, col = 0, -1
                else:
                    col += 1
                    if (col + 1) == NUM_COLS:
                        col = -1
            cnt, sum_pupil_y = 0, 0
            start = time()
            pygame.mixer.music.load(snd[row][col])
            pygame.mixer.music.play()
            disp.blit(kb_imgs[row][col], (100, 250))
            surf = font.render(phrase, True, (255, 255, 255))
            disp.blit(surf, (110, 610))
        img, thresholded, pupilpos, pupilsize, pupilbounds = tracker.give_me_all(pupilrect=True)
        sum_pupil_y += pupilpos[1]
        cnt += 1
        pygame.draw.line(img, (255, 0, 0), (intermediate[0] - 50, intermediate[1]), (intermediate[0] + 50, intermediate[1]))
        pygame.draw.rect(img, (0, 255, 0), pupilbounds, 1)
        pygame.draw.circle(img, (255, 0, 0), pupilpos, 3, 0)
        crop = pygame.Surface((160, 320))
        crop.blit(img, (0, 0), blitpos)
        scale = pygame.transform.scale(crop, (500, 1000))
        disp.blit(scale, (800, 50))
        disp.blit(kb_imgs[row][col], (100, 250))
        pygame.display.flip()


def _check_escape():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == 'escape':
                return True
    return False
