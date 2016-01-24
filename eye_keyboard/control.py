from __future__ import division

import pygame as pg

from string import lowercase, uppercase
from sys import exit
from time import time
from os.path import join

from eye_keyboard import settings as st
from eye_keyboard.components.table import Table
from eye_keyboard.components.phrase import Phrase
from eye_keyboard.components.eye_preview import EyePreview


class Control(object):

    THINK_TIME = 3.0
    CAPTURE_TIME = 2.5

    def __init__(self, tracker):
        self.row_num = 0
        self.col_num = -1
        self.chosen = False
        self.sum_pupil_y = 0
        self.num_frames = 0
        self.press_enter = False
        self.done = False
        self.wait_time = self.CAPTURE_TIME
        self.tracker = tracker
        self.eye_threshold = tracker.settings[st.PUPIL_POSITION][1]
        self.screen = self._init_screen()
        self.table = Table()
        self.eye_preview = EyePreview(tracker)
        self.phrase = Phrase()

    def _init_screen(self):
        screen = pg.display.set_mode(st.SCREEN_SIZE, pg.RESIZABLE)
        screen.fill(st.BLACK)
        return screen

    def start(self):
        while not self.done:
            self._play_step_sound()
            self._wait_loop()
            if self.press_enter or self._move_eyes_upwards():
                self._execute_choice()
            else:
                self._move_table_forward()

    def _play_step_sound(self):
        sound_dir = join('resources', 'sounds')
        if self.col_num == -1:
            file_name = '{}.wav'.format(self.row_num + 1)
            file_path = join(sound_dir, 'numbers', file_name)
        else:
            letter = self.table.cells[self.row_num][self.col_num].label.lower()
            if not letter or letter not in lowercase:
                return
            file_name = '{}.wav'.format(letter)
            file_path = join(sound_dir, 'letters', file_name)
        pg.mixer.music.load(file_path)
        pg.mixer.music.play()

    def _wait_loop(self):
        last_time = time()
        while (time() - last_time) < self.wait_time:
            self._update_table()
            self._update_eye_preview()
            self._redraw_screen()
            self._event_loop()

    def _update_table(self):
        for row_num, col_item in self.table.cells.iteritems():
            for col_num, item in col_item.iteritems():
                item.active = False
                if row_num == self.row_num:
                    if self.col_num == -1 or col_num == self.col_num:
                        item.active = True

    def _update_eye_preview(self):
        result = self.tracker.give_me_all(pupilrect=True)
        self.sum_pupil_y += self.tracker.settings[st.PUPIL_POSITION][1]
        self.num_frames += 1
        self.eye_preview.update(
            snapshot=result[0],
            pupil_pos=self.tracker.settings[st.PUPIL_POSITION],
            pupil_rect=self.tracker.settings[st.PUPIL_RECTANGLE]
        )

    def _redraw_screen(self):
        self.screen.fill(st.BLACK)
        self.table.draw(self.screen)
        self.phrase.draw(self.screen)
        self.eye_preview.draw(self.screen)
        pg.display.flip()

    def _event_loop(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if pg.key.name(event.key) == 'return':
                    self.press_enter = True
                if pg.key.name(event.key) == 'escape':
                    self.done = True

    def _move_eyes_upwards(self):
        avg_pupil_y = self.sum_pupil_y / self.num_frames
        self.sum_pupil_y = 0.0
        self.num_frames = 0
        return avg_pupil_y <= self.eye_threshold

    def _move_table_forward(self):
        if self.col_num == -1:
            self.row_num = (self.row_num + 1) % self.table.num_rows
        else:
            self.col_num += 1
            if self.col_num == self.table.num_cols:
                self.row_num = 0
                self.col_num = -1
        print self.row_num, self.col_num

    def _execute_choice(self):
        if self.col_num == -1:
            self.col_num = 0
        else:
            cell = self.table.cells[self.row_num].get(self.col_num)
            if cell.label in uppercase:
                self.phrase.text += cell.label
            if cell.label == Table.SPACE:
                self.phrase.add_space()
            elif cell.label == Table.CLEAN:
                self.phrase.erase_all()
            elif cell.label == Table.ERASE:
                self.phrase.erase_one()
            elif cell.label == Table.ALERT:
                self._play_alert_sound()
            elif cell.label == Table.READ:
                self.phrase.read()
            elif cell.label == Table.QUIT:
                exit(0)
            self.row_num = 0
            self.col_num = -1
        self.press_enter = False

    def _play_alert_sound(self):
        file_path = join('resources', 'sounds', st.ALERT_FILE_NAME)
        pg.init()
        pg.mixer.init()
        sounda = pg.mixer.Sound(file_path)
        sounda.play()
