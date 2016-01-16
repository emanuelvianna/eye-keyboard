from argparse import ArgumentParser

from calibration import calibrate
from keyboard import launch_keyboard
from eye_tracker import EyeTracker


def parse_args():
    parser = ArgumentParser(description='Control a keyboard with pupils.')
    parser.add_argument('--camera-height', type=int, default=640,
                        help='Camera resolution height')
    parser.add_argument('--camera-width', type=int, default=480,
                        help='Camera resolution width')
    parser.add_argument('--display-height', type=int, default=1024,
                        help='Screen resolution height')
    parser.add_argument('--display-width', type=int, default=768,
                        help='Screen resolution width')
    return parser.parse_args()


def main():
    args = parse_args()
    camera_size = (args.camera_height, args.camera_width)
    display_size = (args.display_height, args.display_width)
    tracker = EyeTracker(camera_size)
    calibrate(tracker, camera_size, display_size)
    launch_keyboard(tracker, display_size)


if __name__ == '__main__':
    main()
