from argparse import ArgumentParser

from calibration import calibrate
from keyboard import launch_keyboard


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


if __name__ == '__main__':
    args = parse_args()
    camera_size = (args.camera_height, args.camera_width)
    display_size = (args.display_height, args.display_width)
    tracker = calibrate(camera_size, display_size)
    launch_keyboard(tracker, display_size)
