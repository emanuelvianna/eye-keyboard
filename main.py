import webcam_eyetracker.camtracker as ct

from eye_keyboard.control import Control


def main():
    setup = ct.Setup()
    tracker = setup.start()
    control = Control(tracker)
    control.start()


if __name__ == '__main__':
    main()
