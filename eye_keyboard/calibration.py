import os.path

import pygame

from collections import defaultdict

from eye_tracker import EyeTracker
import settings as st

BACKGROUND_COLOUR = (0, 0, 0)
FOREGROUND_COLOUR = (255, 255, 255)

BUTTON_NAMES = ['1', '2', '3', 'up', 'down', 't', 'space', 'escape']
BUTTON_STATES = ['active', 'inactive']
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 50


def calibrate(camera_size, display_size):
    """
    Calibrate an eye tracker.
    Parameters
    ----------
    camera_size: (int, int)
        camera resolution height and width
    display_size: (int, int)
        display resolution height and width
    """
    tracker = EyeTracker(camera_size)
    img = pygame.surface.Surface(tracker.camera_size)
    font, sfont = _init_fonts()
    disp = _init_display(display_size)
    btn = _init_buttons(camera_size, display_size)
    tracker.pupil_pos = (tracker.camera_size[0] / 2, tracker.camera_size[1] / 2)
    _draw_stage(disp, btn, font, display_size, camera_size)
    pygame.mouse.set_visible(True)
    _run_gui(disp, btn, font, img, tracker, sfont, display_size, camera_size)
    return tracker


def _init_fonts():
    pygame.font.init()
    try:
        fontname = os.path.join(
            os.path.split(os.path.abspath(__file__))[0],
            'resources',
            'roboto_regular-webfont.ttf')
    except:
        fontname = pygame.font.get_default_font()
        print "warning: could not find 'roboto_regular-webfont.ttf'"
    font = pygame.font.Font(fontname, 24)
    sfont = pygame.font.Font(fontname, 12)
    return font, sfont


def _init_display(display_size):
    # disp = pygame.display.set_mode(display_size, pygame.RESIZABLE)
    disp = pygame.display.set_mode(display_size, pygame.FULLSCREEN |
                                   pygame.HWSURFACE | pygame.DOUBLEBUF)
    disp.fill(BACKGROUND_COLOUR)
    return disp


def _init_buttons(camera_size, display_size):
    btn_img = _load_button_images()
    btn_pos = _compute_button_positions(camera_size[0], camera_size[1],
                                        display_size[0], display_size[1])
    return _merge_button_data(btn_img, btn_pos)


def _load_button_images():
    resdir = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'resources')
    if not os.path.exists(resdir):
        raise Exception("could not find 'resources' directory")
    btn_img = defaultdict(lambda: {})
    for bn in BUTTON_NAMES:
        for bs in BUTTON_STATES:
            filename = "%s_%s.png" % (bn, bs)
            btn_img[bn][bs] = os.path.join(resdir, filename)
            if not os.path.isfile(btn_img[bn][bs]):
                print "warning: image file '%s' was not found in resources!" % filename
                btn_img[bn][bs] = os.path.join(resdir, "blank_%s.png" % bs)
    return btn_img


def _compute_button_positions(camera_height, camera_width, display_height, display_width):
    btn_pos = {}
    y = display_width / 2 + int(camera_width * 0.6)
    btn_pos['1'] = int(display_height * (2 / 6.0) - BUTTON_HEIGHT / 2), y
    btn_pos['2'] = int(display_height * (3 / 6.0) - BUTTON_HEIGHT / 2), y
    btn_pos['3'] = int(display_height * (4 / 6.0) - BUTTON_HEIGHT / 2), y
    btn_pos['space'] = int(display_height * (5 / 6.0) - BUTTON_HEIGHT / 2), y
    leftx = display_height / 2 - (camera_height / 2 + BUTTON_HEIGHT)
    rightx = display_height / 2 + camera_height / 2 + BUTTON_HEIGHT
    btn_pos['up'] = rightx, display_width / 2 - BUTTON_WIDTH
    btn_pos['down'] = rightx, display_width / 2 + BUTTON_WIDTH
    btn_pos['t'] = leftx, display_width / 2 + camera_width / 2 - BUTTON_WIDTH / 2
    btn_pos['escape'] = BUTTON_HEIGHT, BUTTON_WIDTH
    return btn_pos


def _merge_button_data(btn_img, btn_pos):
    btn = defaultdict(lambda: defaultdict(lambda: {}))
    for bn in btn_img.keys():
        btn_pos[bn] = btn_pos[bn][0] - BUTTON_HEIGHT / 2, btn_pos[bn][1] - BUTTON_WIDTH / 2
        for bs in btn_img[bn].keys():
            btn[bn][bs]['img'] = pygame.image.load(btn_img[bn][bs])
            btn[bn][bs]['pos'] = btn_pos[bn]
            btn[bn][bs]['rect'] = btn_pos[bn][0], btn_pos[bn][1], BUTTON_HEIGHT, BUTTON_WIDTH
    return btn


def _draw_stage(disp, btn, font, display_size, camera_size, stage=None):
    disp.fill(BACKGROUND_COLOUR)
    title, inactive_btn, active_btn = _get_stage_buttons_and_title(stage, btn)
    _draw_buttons(disp, btn, inactive_btn, active_btn)
    _draw_title(disp, font, title, display_size, camera_size)


def _get_stage_buttons_and_title(stage, btn):
    active_btn = []
    inactive_btn = ['1', '2', '3', 'space', 'escape', 't']
    if stage == 1:
        title = "set pupil detection threshold"
        inactive_btn.extend(['up', 'down'])
        active_btn.append('1')
    elif stage == 2:
        title = "select pupil and set pupil detection bounds"
        inactive_btn.extend(['up', 'down'])
        active_btn.append('2')
    elif stage == 3:
        title = "confirmation"
        inactive_btn.extend(['up', 'down'])
        active_btn.append('3')
    else:
        title = "loading, please wait..."
    return title, inactive_btn, active_btn


def _draw_title(disp, font, title, display_size, camera_size):
    title_size = font.size(title)
    title_pos = (display_size[0] / 2 - title_size[0] / 2,
                 display_size[1] / 2 - (camera_size[1] / 2 + title_size[1]))
    title_surf = font.render(title, True, FOREGROUND_COLOUR)
    disp.blit(title_surf, title_pos)


def _draw_buttons(disp, btn, inactive_btn, active_btn):
    for bn in inactive_btn:
        disp.blit(btn[bn]['inactive']['img'], btn[bn]['inactive']['pos'])
    for bn in active_btn:
        disp.blit(btn[bn]['active']['img'], btn[bn]['active']['pos'])


def _run_gui(disp, btn, font, img, tracker, sfont, display_size, camera_size):
    stage = 1
    stagevars = defaultdict(lambda: {})
    stagevars[0]['show_threshimg'] = False
    stagevars[0]['use_prect'] = True
    stagevars[1]['thresholdchange'] = None
    stagevars[2]['clickpos'] = 0, 0
    stagevars[2]['prectsize'] = 25, 12
    stagevars[2]['prect'] = pygame.Rect(
        stagevars[2]['clickpos'][0],
        stagevars[2]['clickpos'][1],
        stagevars[2]['prectsize'][0],
        stagevars[2]['prectsize'][1])
    stagevars[2]['vprectchange'] = None
    stagevars[2]['hprectchange'] = None
    stagevars[3]['confirmed'] = False
    running = True
    img_size = img.get_size()
    blitpos = (display_size[0] / 2 - img_size[0] / 2, display_size[1] / 2 - img_size[1] / 2)
    while running:
        _draw_stage(disp, btn, font, display_size, camera_size, stage)
        pupilrect = stagevars[0]['use_prect'] and stage > 1
        img, thresholded, pupilsize = tracker.give_me_all(pupilrect)
        settings = tracker.settings
        _draw_threshold_button(disp, btn, stagevars)
        inp, inptype = _capture_input()
        stage, stagevars = _handle_input(btn, inptype, inp, stage, stagevars)
        if stage == 1:
            _handle_threshold(tracker, settings, stagevars)
        elif stage == 2:
            if inptype == 'mouseclick':
                _place_rectangle_at_click_position(
                    blitpos, img_size, stagevars, inp, tracker, settings)
            elif stagevars[2]['vprectchange'] or stagevars[2]['hprectchange']:
                _update_rectangle_size(stagevars, settings)
            _draw_red_rectangle(img, tracker, thresholded)
        elif stage == 3:
            _handle_threshold(tracker, settings, stagevars)
            _draw_red_rectangle(img, tracker, thresholded)
            _draw_pupil_circle(img, thresholded, tracker)
            if stagevars[3]['confirmed']:
                running = False
        _draw_legend(display_size, img_size, tracker, settings, sfont, disp)
        _draw_thresholded_image(disp, img, thresholded, blitpos, stagevars)
        pygame.display.flip()
        tracker.settings = settings
    return tracker


def _handle_input(btn, inptype, inp, stage, stagevars):
    if inptype == 'mouseclick':
        pos = inp[:]
        for button_name in btn.keys():
            rect = btn[button_name]['inactive']['rect']
            if (
                pos[0] > rect[0] and pos[0] < rect[0] + rect[2] and
                pos[1] > rect[1] and pos[1] < rect[1] + rect[3]
            ):
                inp = button_name
                break
    if stage == 1:
        if inp in ['up', 'down']:
            stagevars[1]['thresholdchange'] = inp
    elif stage == 2:
        if inp in ['up', 'down']:
            stagevars[2]['vprectchange'] = inp
        elif inp in ['left', 'right']:
            stagevars[2]['hprectchange'] = inp
    elif stage == 3:
        if inp in ['up', 'down']:
            stagevars[1]['thresholdchange'] = inp
        if inp == 'space':
            stagevars[3]['confirmed'] = True
    if inp == 'space' and stage < 3:
        stage += 1
    if inp in ['1', '2', '3']:
        stage = int(inp)
    if inp == 't':
        stagevars[0]['show_threshimg'] = not stagevars[0]['show_threshimg']
    if inp == 'r':
        if stagevars[0]['use_prect']:
            stagevars[0]['use_prect'] = False
        else:
            stagevars[0]['use_prect'] = True
    if inp == 'escape':
        pygame.display.quit()
        raise Exception("camtracker.Setup: Escape was pressed")
    return stage, stagevars


def _draw_threshold_button(disp, btn, stagevars):
    if stagevars[0]['show_threshimg']:
        disp.blit(btn['t']['active']['img'], btn['t']['active']['pos'])
    else:
        disp.blit(btn['t']['inactive']['img'], btn['t']['inactive']['pos'])


def _capture_input():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            return pygame.mouse.get_pos(), 'mouseclick'
        elif event.type == pygame.KEYDOWN:
            return pygame.key.name(event.key), 'keypress'
    return None, None


def _handle_threshold(tracker, settings, stagevars):
    if stagevars[1]['thresholdchange'] is not None:
        if stagevars[1]['thresholdchange'] == 'up' and tracker.threshold < 255:
            tracker.threshold += 1
        elif stagevars[1]['thresholdchange'] == 'down' and tracker.threshold > 0:
            tracker.threshold -= 1
        stagevars[1]['thresholdchange'] = None


def _draw_red_rectangle(img, tracker, thresholded):
    try:
        pygame.draw.rect(img, (0, 255, 0), tracker.detection_bounds, 1)
        pygame.draw.rect(thresholded, (0, 255, 0), tracker.detection_bounds, 1)
    except:
        print("pupilbounds=%s" % tracker.detection_bounds)


def _draw_pupil_circle(img, thresholded, tracker):
    try:
        pygame.draw.circle(img, (255, 0, 0), tracker.pupil_pos, 3, 0)
        pygame.draw.circle(thresholded, (255, 0, 0), tracker.pupil_pos, 3, 0)
    except:
        print("pupilpos=%s" % tracker.pupil_pos)


def _draw_thresholded_image(disp, img, thresholded, blitpos, stagevars):
    if stagevars[0]['show_threshimg']:
        disp.blit(thresholded, blitpos)
    else:
        disp.blit(img, blitpos)


def _place_rectangle_at_click_position(blitpos, img_size, stagevars, inp, tracker, settings):
    mouse_pos = pygame.mouse.get_pos()
    if (
        mouse_pos[0] > blitpos[0] and mouse_pos[0] < blitpos[0] + img_size[0] and
        mouse_pos[1] > blitpos[1] and mouse_pos[1] < blitpos[1] + img_size[1]
    ):
        stagevars[2]['clickpos'] = (inp[0] - blitpos[0], inp[1] - blitpos[1])
        tracker.pupil_pos = stagevars[2]['clickpos'][:]
        x = stagevars[2]['clickpos'][0] - stagevars[2]['prectsize'][0] / 2
        y = stagevars[2]['clickpos'][1] - stagevars[2]['prectsize'][1] / 2
        stagevars[2]['prect'] = pygame.Rect(
            x, y, stagevars[2]['prectsize'][0], stagevars[2]['prectsize'][1])
        settings['pupilrect'] = stagevars[2]['prect']


def _update_rectangle_size(stagevars, settings):

    if stagevars[2]['vprectchange'] is not None:
        if stagevars[2]['vprectchange'] == 'up':
            stagevars[2]['prectsize'] = (stagevars[2]['prectsize'][0],
                                         stagevars[2]['prectsize'][1] + 1)
        elif stagevars[2]['vprectchange'] == 'down':
            stagevars[2]['prectsize'] = (stagevars[2]['prectsize'][0],
                                         stagevars[2]['prectsize'][1] - 1)
        stagevars[2]['vprectchange'] = None
    if stagevars[2]['hprectchange'] is not None:
        if stagevars[2]['hprectchange'] == 'right':
            stagevars[2]['prectsize'] = (stagevars[2]['prectsize'][0] + 1,
                                         stagevars[2]['prectsize'][1])
        elif stagevars[2]['hprectchange'] == 'left':
            stagevars[2]['prectsize'] = (stagevars[2]['prectsize'][0] - 1,
                                         stagevars[2]['prectsize'][1])
        stagevars[2]['hprectchange'] = None
    x = settings['pupilrect'][0]
    y = settings['pupilrect'][1]
    stagevars[2]['prect'] = pygame.Rect(
        x, y, stagevars[2]['prectsize'][0], stagevars[2]['prectsize'][1])
    settings['pupilrect'] = stagevars[2]['prect']


def _draw_legend(display_size, img_size, tracker, settings, sfont, disp):
    starty = display_size[1] / 2 - img_size[1] / 2
    vtx = display_size[0] / 2 - img_size[0] / 2 - 10
    vals = [
        'pupil colour', str(st.PUPIL_COLOUR),
        'threshold', str(tracker.threshold),
        'pupil position', str(tracker.pupil_pos),
        'pupil rect', str(settings['pupilrect'])]
    for i in range(len(vals)):
        tsize = sfont.size(vals[i])
        tpos = vtx - tsize[0], starty + i * 20
        tsurf = sfont.render(vals[i], True, FOREGROUND_COLOUR)
        disp.blit(tsurf, tpos)
