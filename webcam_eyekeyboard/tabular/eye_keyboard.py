from __future__ import division

import pygame as pg

from requests import get
from sys import exit
from time import time
from os.path import join
from datetime import datetime

from eye_keyboard import settings as st
from eye_keyboard.tabular.components.panel import (OptionPanel, LetterPanel,
                                                   LetterItem, OptionItem)
from eye_keyboard.tabular.components.phrase import Phrase
from eye_keyboard.tabular.components.eye_preview import EyePreview


class EyeKeyboard(object):

    THINK_TIME = 2.0

    def __init__(self, eye_tracker):
        self.done = False
        self.panel_num = 0
        self.row_num = -1
        self.col_num = -1
        self.last_time = time()
        self.chosen = False
        self.sum_pupil_y = 0
        self.num_frames = 0
        self.screen = self._init_screen()
        self.panels = [OptionPanel(), LetterPanel()]
        self.eye_preview = EyePreview(eye_tracker)
        self.eye_tracker = eye_tracker
        self.phrase = Phrase()
        self.threshold = eye_tracker.pupil_pos[1]

    def _init_screen(self):
        screen = pg.display.set_mode(st.SCREEN_SIZE, pg.RESIZABLE)
        screen.fill(st.BLACK)
        return screen

    def main(self):
        while not self.done:
            self._adjust_pointers()
            self._update_phrase()
            self._update_panels()
            self._redraw_screen()
            self._play_step_sound()
            self._event_loop()
            self._eye_movement_loop()
            self._execute_options()

    def _adjust_pointers(self):
        if self.chosen:
            if self.row_num == -1:
                self.row_num = 0
                if self.panel_num == st.OPTION_PANEL:
                    self.col_num = 0
            else:
                if self.col_num == -1:
                    self.col_num = 0
                else:
                    self.panel_num = 0
                    self.row_num = -1
                    self.col_num = -1
        else:
            if self.row_num == -1:
                self.panel_num = (self.panel_num + 1) % st.NUM_PANELS
            elif self.col_num == -1:
                num_rows = self.panels[self.panel_num].num_rows
                self.row_num = (self.row_num + 1) % num_rows
            else:
                self.col_num += 1
                num_cols = self.panels[self.panel_num].num_cols
                if (self.col_num + 1) == num_cols:
                    self.panel_num = 0
                    self.row_num = -1
                    self.col_num = -1

    def _update_phrase(self):
        panel = self.panels[self.panel_num]
        item = panel.row_col_item[self.row_num][self.col_num]
        if isinstance(item, LetterItem):
            self.phrase.text += item.label
        elif isinstance(item, OptionItem):
            if item.label == OptionItem.CLEAN:
                self.phrase.text = ''
            elif item.label == OptionItem.ERASE:
                self.phrase.text = self.phrase.text[:-1]

    def _update_panels(self):
        for panel in self.panels:
            for row_num, col_item in self.row_col_item.iteritem():
                for col_num, item in col_item.iteritems():
                    if self.panel_num == st.LETTER_PANEL:
                        if self.col_num == -1:
                            item.active = True
                        elif (row_num == self.row_num and
                              col_num == self.col_num):
                            item.active = True
                        else:
                            item.active = False
                    else:
                        item.active = False

    def _redraw_screen(self):
        self.option_panel.draw(self.screen)
        self.letter_panel.draw(self.screen)
        self.phrase.draw()
        self.eye_preview.draw()
        pg.display.flip()

    def _play_step_sound(self):
        if self.panel == st.OPTION_PANEL:
            return
        if self.col_num == -1:
            number = self.row_num + 1
            file_name = '{}.wav'.format(number)
        else:
            letter = st.ROW_COL_TEXT[self.row_num][self.col_num].lower()
            file_name = '{}.wav'.format(letter)
        file_path = join('resources', file_name)
        pg.mixer.music.load(file_path)
        pg.mixer.music.play()

    def _event_loop(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if pg.key.name(event.key) == 'escape':
                    self.done = True
                if pg.key.name(event.key) == 'return':
                    self.chosen = True

    def _eye_movement_loop(self):
        self.give_me_all(use_prect=True)
        if (time() - self.last_time) >= st.THINK_TIME:
            avg_pupil_y = self.sum_pupil_y / self.num_frames
            if avg_pupil_y >= self.threshold:
                self.chosen = True
            self.last_time = time()
            self.sum_pupil_y = 0.0
            self.num_frames = 0
        self.sum_pupil_y += self.eye_tracker.pupil_pos[1]
        self.num_frames += 1

    def _execute_options(self):
        panel = self.panels[self.panel_num]
        item = panel.row_col_item[self.row_num][self.col_num]
        if isinstance(item, OptionItem):
            if item.label == OptionItem.ALERT:
                pg.mixer.music.load(st.ALERT_FILE_PATH)
                pg.mixer.music.play()
            elif item.label == OptionItem.READ:
                file_path = datetime.now().strftime('speech-%Y%m%d%H%M%S')
                with open(file_path, 'w') as f:
                    payload = dict(TXT=self.phrase.text, **st.VOCALWARE)
                    response = get("http://www.vocalware.com/tts/gen.php", params=payload)
                    assert response.status_code == 200
                    f.write(response.content)
                pg.mixer.music.load(file_path)
                pg.mixer.music.play()
            elif item.label == OptionItem.QUIT:
                exit(0)
