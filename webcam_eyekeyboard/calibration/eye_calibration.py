import pygame as pg

from collections import defaultdict

from eye_keyboard import settings as st
from eye_keyboard.calibration.components.button import Button


class Calibration(object):

    def __init__(self, eye_tracker):
        self.eye_tracker = eye_tracker
        self.buttons = []
        for name in st.BUTTON_NAMES:
            button = Button(name)
            self.buttons.append(button)

    # def _init_buttons():
    #     btn_img = _load_button_images()
    #     btn_pos = _compute_button_positions(st.CAMERA_SIZE[0], st.CAMERA_SIZE[1],
    #                                         st.SCREEN_SIZE[0], st.SCREEN_SIZE[1])
    #     return _merge_button_data(btn_img, btn_pos)

    def main(self):
        stage = 1
        stagevars = defaultdict(lambda: {})
        stagevars[0]['show_threshimg'] = False
        stagevars[0]['use_prect'] = True
        stagevars[1]['thresholdchange'] = None
        stagevars[2]['clickpos'] = 0, 0
        stagevars[2]['prectsize'] = 25, 12
        stagevars[2]['prect'] = pg.Rect(
            stagevars[2]['clickpos'][0],
            stagevars[2]['clickpos'][1],
            stagevars[2]['prectsize'][0],
            stagevars[2]['prectsize'][1]
        )
        stagevars[2]['vprectchange'] = None
        stagevars[2]['hprectchange'] = None
        stagevars[3]['confirmed'] = False
        running = True
        img_size = tracker.camera_size
        blitpos = (st.SCREEN_SIZE[0] / 2 - img_size[0] / 2, st.SCREEN_SIZE[1] / 2 - img_size[1] / 2)
        while running:
            _draw_stage(btn, st.SCREEN_SIZE, st.CAMERA_SIZE, stage)
            use_prect = stagevars[0]['use_prect'] and stage > 1
            img, thresholded = tracker.give_me_all(use_prect)
            _draw_threshold_button(btn, stagevars)
            inp, inptype = _capture_input()
            stage, stagevars = _handle_input(btn, inptype, inp, stage, stagevars)
            if stage == 1:
                _handle_threshold(tracker, stagevars)
            elif stage == 2:
                if inptype == 'mouseclick':
                    _place_rectangle_at_click_position(
                        blitpos, img_size, stagevars, inp, tracker)
                elif stagevars[2]['vprectchange'] or stagevars[2]['hprectchange']:
                    _update_rectangle_size(stagevars, tracker)
                _draw_green_rectangle(img, tracker, thresholded)
            elif stage == 3:
                _handle_threshold(tracker, stagevars)
                _draw_green_rectangle(img, tracker, thresholded)
                _draw_pupil_circle(img, thresholded, tracker)
                if stagevars[3]['confirmed']:
                    running = False
            _draw_legend(st.SCREEN_SIZE, img_size, tracker)
            _draw_thresholded_image(img, thresholded, blitpos, stagevars)
            pg.display.flip()

# def _load_button_images():
#     resdir = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'resources')
#     if not os.path.exists(resdir):
#         raise Exception("could not find 'resources' directory")
#     btn_img = defaultdict(lambda: {})
#     for bn in st.BUTTON_NAMES:
#         for bs in st.BUTTON_STATES:
#             filename = "%s_%s.png" % (bn, bs)
#             btn_img[bn][bs] = os.path.join(resdir, filename)
#             if not os.path.isfile(btn_img[bn][bs]):
#                 print "warning: image file '%s' was not found in resources!" % filename
#                 btn_img[bn][bs] = os.path.join(resdir, "blank_%s.png" % bs)
#     return btn_img


# def _compute_button_positions(camera_height, camera_width, display_height, display_width):
#     btn_pos = {}
#     y = display_width / 2 + int(camera_width * 0.6)
#     btn_pos['1'] = int(display_height * (2 / 6.0) - st.BUTTON_HEIGHT / 2), y
#     btn_pos['2'] = int(display_height * (3 / 6.0) - st.BUTTON_HEIGHT / 2), y
#     btn_pos['3'] = int(display_height * (4 / 6.0) - st.BUTTON_HEIGHT / 2), y
#     btn_pos['space'] = int(display_height * (5 / 6.0) - st.BUTTON_HEIGHT / 2), y
#     leftx = display_height / 2 - (camera_height / 2 + st.BUTTON_HEIGHT)
#     rightx = display_height / 2 + camera_height / 2 + st.BUTTON_HEIGHT
#     btn_pos['up'] = rightx, display_width / 2 - st.BUTTON_WIDTH
#     btn_pos['down'] = rightx, display_width / 2 + st.BUTTON_WIDTH
#     btn_pos['t'] = leftx, display_width / 2 + camera_width / 2 - st.BUTTON_WIDTH / 2
#     btn_pos['escape'] = st.BUTTON_HEIGHT, st.BUTTON_WIDTH
#     return btn_pos


# def _merge_button_data(btn_img, btn_pos):
#     btn = defaultdict(lambda: defaultdict(lambda: {}))
#     for bn in btn_img.keys():
#         btn_pos[bn] = btn_pos[bn][0] - st.BUTTON_HEIGHT / 2, btn_pos[bn][1] - st.BUTTON_WIDTH / 2
#         for bs in btn_img[bn].keys():
#             btn[bn][bs]['img'] = pg.image.load(btn_img[bn][bs])
#             btn[bn][bs]['pos'] = btn_pos[bn]
#             btn[bn][bs]['rect'] = btn_pos[bn][0], btn_pos[bn][1], st.BUTTON_HEIGHT, st.BUTTON_WIDTH
#     return btn


def _draw_stage(btn, display_size, camera_size, stage=None):
    st.SCREEN.fill(st.BACKGROUND_COLOUR)
    title, inactive_btn, active_btn = _get_stage_buttons_and_title(stage, btn)
    _draw_buttons(btn, inactive_btn, active_btn)
    _draw_title(title, display_size, camera_size)


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


# def _draw_title(title, display_size, camera_size):
#     title_size = st.LARGE_FONT.size(title)
#     title_pos = (display_size[0] / 2 - title_size[0] / 2,
#                  display_size[1] / 2 - (camera_size[1] / 2 + title_size[1]))
#     title_surf = st.LARGE_FONT.render(title, True, st.FOREGROUND_COLOUR)
#     st.SCREEN.blit(title_surf, title_pos)


# def _draw_buttons(btn, inactive_btn, active_btn):
#     for bn in inactive_btn:
#         st.SCREEN.blit(btn[bn]['inactive']['img'], btn[bn]['inactive']['pos'])
#     for bn in active_btn:
#         st.SCREEN.blit(btn[bn]['active']['img'], btn[bn]['active']['pos'])


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
        pg.display.quit()
        raise Exception("camtracker.Setup: Escape was pressed")
    return stage, stagevars


def _draw_threshold_button(btn, stagevars):
    if stagevars[0]['show_threshimg']:
        st.SCREEN.blit(btn['t']['active']['img'], btn['t']['active']['pos'])
    else:
        st.SCREEN.blit(btn['t']['inactive']['img'], btn['t']['inactive']['pos'])


def _capture_input():
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            return pg.mouse.get_pos(), 'mouseclick'
        elif event.type == pg.KEYDOWN:
            return pg.key.name(event.key), 'keypress'
    return None, None


def _handle_threshold(tracker, stagevars):
    if stagevars[1]['thresholdchange'] is not None:
        if stagevars[1]['thresholdchange'] == 'up' and tracker.threshold < 255:
            tracker.threshold += 1
        elif stagevars[1]['thresholdchange'] == 'down' and tracker.threshold > 0:
            tracker.threshold -= 1
        stagevars[1]['thresholdchange'] = None


def _draw_green_rectangle(img, tracker, thresholded):
    try:
        pg.draw.rect(img, (0, 255, 0), tracker.pupil_rect, 1)
        pg.draw.rect(thresholded, (0, 255, 0), tracker.pupil_rect, 1)
    except:
        print("pupilbounds=%s" % tracker.pupil_rect)


def _draw_pupil_circle(img, thresholded, tracker):
    try:
        pg.draw.circle(img, (255, 0, 0), tracker.pupil_pos, 3, 0)
        pg.draw.circle(thresholded, (255, 0, 0), tracker.pupil_pos, 3, 0)
    except:
        print("pupilpos=%s" % tracker.pupil_pos)


def _draw_thresholded_image(img, thresholded, blitpos, stagevars):
    if stagevars[0]['show_threshimg']:
        st.SCREEN.blit(thresholded, blitpos)
    else:
        st.SCREEN.blit(img, blitpos)


def _place_rectangle_at_click_position(blitpos, img_size, stagevars, inp, tracker):
    x, y = pg.mouse.get_pos()
    if (
        x > blitpos[0] and x < blitpos[0] + img_size[0] and
        y > blitpos[1] and y < blitpos[1] + img_size[1]
    ):
        stagevars[2]['clickpos'] = (inp[0] - blitpos[0], inp[1] - blitpos[1])
        tracker.pupil_pos = stagevars[2]['clickpos'][:]
        x = stagevars[2]['clickpos'][0] - stagevars[2]['prectsize'][0] / 2
        y = stagevars[2]['clickpos'][1] - stagevars[2]['prectsize'][1] / 2
        stagevars[2]['prect'] = pg.Rect(
            x, y, stagevars[2]['prectsize'][0], stagevars[2]['prectsize'][1])
        tracker.pupil_rect = stagevars[2]['prect']


def _update_rectangle_size(stagevars, tracker):
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
    x = tracker.pupil_rect[0]
    y = tracker.pupil_rect[1]
    stagevars[2]['prect'] = pg.Rect(
        x, y, stagevars[2]['prectsize'][0], stagevars[2]['prectsize'][1])
    tracker.pupil_rect = stagevars[2]['prect']


def _draw_legend(display_size, img_size, tracker):
    starty = display_size[1] / 2 - img_size[1] / 2
    vtx = display_size[0] / 2 - img_size[0] / 2 - 10
    vals = [
        'pupil colour', str(st.PUPIL_COLOUR),
        'threshold', str(tracker.threshold),
        'pupil position', str(tracker.pupil_pos),
        'pupil rect', str(tracker.pupil_rect)]
    for i in range(len(vals)):
        tsize = st.SMALL_FONT.size(vals[i])
        tpos = vtx - tsize[0], starty + i * 20
        tsurf = st.SMALL_FONT.render(vals[i], True, st.FOREGROUND_COLOUR)
        st.SCREEN.blit(tsurf, tpos)
