# Webcam-eyetracker contants
PUPIL_POSITION = 'pupilpos'
PUPIL_RECTANGLE = 'pupilrect'

# Eye Tracker settings
PUPIL_COLOUR = (0, 0, 0)
THRESHOLD_BACKGROUND_COLOUR = (100, 100, 255, 255)
DEFAULT_THRESHOLD = 45
DEFAULT_PUPIL_WIDTH = 25
DEFAULT_PUPIL_HEIGHT = 12

# Screen settings
SCREEN_SIZE = (1366, 768)
CAMERA_SIZE = (640, 480)
BACKGROUND_COLOUR = (0, 0, 0)
FOREGROUND_COLOUR = (255, 255, 255)

# Colour options
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 128)

# Vocalware settings (1-Gabriela, 2-Amalia, 4-Fernanda)
VOCALWARE_URL = "http://www.vocalware.com/tts/gen.php"
VOCALWARE_CHECKSUM = 'CS'
VOCALWARE_MD5_KEY = "{EID}{LID}{VID}{TXT}{EXT}{FX_TYPE}{FX_LEVEL}{ACC}{API}{SESSION}{HTTP_ERR}{SECRET}"  # noqa
VOCALWARE_TXT = 'TXT'
VOCALWARE_EID = '2'
VOCALWARE_LID = '6'
VOCALWARE_VID = '1'
VOCALWARE_EXT = 'mp3'
VOCALWARE_FX_TYPE = 'S'
VOCALWARE_FX_LEVEL = '2'
VOCALWARE_ACC = '5601687'
VOCALWARE_API = '2473353'
VOCALWARE_SESSION = ''
VOCALWARE_HTTP_ERR = ''
VOCALWARE_SECRET = '8047f795fac6819b0a7097b108013fb8'
VOCALWARE_PARAMS = {
    'EID': VOCALWARE_EID,
    'LID': VOCALWARE_LID,
    'VID': VOCALWARE_VID,
    'EXT': VOCALWARE_EXT,
    'FX_TYPE': VOCALWARE_FX_TYPE,
    'FX_LEVEL': VOCALWARE_ACC,
    'ACC': VOCALWARE_ACC,
    'API': VOCALWARE_API,
    'SESSION': VOCALWARE_SESSION,
    'HTTP_ERR': VOCALWARE_HTTP_ERR,
    'SECRET': VOCALWARE_SECRET
}

# General settings
NUM_PANELS = 2
OPTION_PANEL = 0
LETTER_PANEL = 1
THINK_TIME = 2.0
ROW_THINK_TIME = 1.0
SPEECH_SPEED = 44100

# Button settings
BUTTON_NAMES = ['1', '2', '3', 'up', 'down', 't', 'space', 'escape']
BUTTON_STATES = ['active', 'inactive']

# Letter panel settings

LINE_WIDTH = 2
NUM_ROWS = 4
NUM_COLS = 7

START_LEFT = 150
START_TOP = 300
FILL_RECT = 0
WIDTH = 100
HEIGHT = 100
FONT_SIZE = 70

FONT_NAME = 'resources/roboto_regular-webfont.ttf'
ALERT_FILE_NAME = 'alert.wav'
