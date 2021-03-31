# Monitor parameters
MON_DISTANCE = 60             # Distance between subject's eyes and monitor
MON_WIDTH = 50                # Width of your monitor in cm
MON_SIZE = [1920, 1080]        # Pixel-dimensions of your monitor
SAVE_FOLDER = 'log'           # Log is saved to this folder. The folder is created if it does not exist.

# Window parameters
MESSAGE_POS = [0, 3]   # [x, y]
MESSAGE_HEIGHT = 1     # Height of the text, still in degrees visual angle
MESSAGE_WIDTH = 35

# Visual frame rate
FRAME_RATE = 60             # need to check your monitor
VISUAL_DUR = FRAME_RATE     # 60 frames ~1 second
VISUAL_ISI = FRAME_RATE     # 60 frames 1 second
MIN_RT = FRAME_RATE/10      # 6 frames 0.1 min reaction time
RESP_DUR = int(FRAME_RATE*1.25)  # 75 frames Respond duration
JITTER = 30                 # 30 frames ~500ms Jitter for timme duration
IBI = 1

# Trial list definition
NUM_BLOCKS = 2
NUM_RARE = 5
NUM_COMMON = 15
NUM_REPT = 2

# Stimulus and direction set up
STIMS = ['X', 'O']
RESPS = ['F','J']
RESPS_L = ['f','j']
MODES = ['X', 'O']
CONDS = ['common']*NUM_COMMON + ['rare']*NUM_RARE

# Experimental flow control
instruct = True
visual = True
sync_paral = False
use_ptbKey = False

# KeyPress Setup
KEYS_QUIT = ['escape'] # Keys that quits the experiment
COND_KEYS = ['space']

# Parapellal Port PIN configuration
INIT_PIN = 9
END_PIN = 9
TB_PIN = 7
BB_PIN = 8
STIM_PIN = 1
RESP_PIN = 2
