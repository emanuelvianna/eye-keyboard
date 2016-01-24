import pygame as pg

from hashlib import md5
from datetime import datetime
from os.path import join
from requests import get

from eye_keyboard import settings as st


class Phrase(object):

    ANTIALIAS = True
    FONT_SIZE = 80
    BLIT_POS = (100, 50)

    def __init__(self):
        self.text = ''
        self.font = pg.font.Font(st.FONT_NAME, self.FONT_SIZE)

    def erase_one(self):
        self.text = self.text[:-1]

    def erase_all(self):
        self.text = ''

    def add_space(self):
        self.text += ' '

    def read(self):
        file_name = datetime.now().strftime('speech-%Y%m%d%H%M%S.mp3')
        file_path = join('/', 'tmp', file_name)
        with open(file_path, 'w') as f:
            params = st.VOCALWARE_PARAMS
            params[st.VOCALWARE_TXT] = self.text
            checksum = md5(st.VOCALWARE_MD5_KEY.format(**params)).hexdigest()
            params[st.VOCALWARE_CHECKSUM] = checksum
            response = get(st.VOCALWARE_URL, params)
            assert response.status_code == 200
            f.write(response.content)
        pg.mixer.music.load(file_path)
        pg.mixer.music.play()
        from time import sleep
        sleep(5)

    def draw(self, screen):
        phrase_surface = self.font.render(self.text, self.ANTIALIAS, st.WHITE)
        screen.blit(phrase_surface, self.BLIT_POS)
