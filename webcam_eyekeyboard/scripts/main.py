import pygame as pg

from eye_keyboard.calibration.eye_calibration import calibrate
from eye_keyboard import EyeKeyboard
from eye_tracker import EyeTracker


def main():
    eye_tracker = EyeTracker()
    calibrate(eye_tracker)
    EyeKeyboard(eye_tracker).main()


if __name__ == '__main__':
    pg.init()
    main()
