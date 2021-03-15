# --- game settings ---
DELAY = 0.2
WIDTH = 400
HEIGHT = 700
BLOCK_SIZE = 25  # --- default block size ---
# --- spawn grid position ---
BASE_ROW = 0
BASE_COL = 7
# --- game area index ---
MID_STARTS = int((WIDTH / BLOCK_SIZE - 10) / 2)
MID_ENDS = int(WIDTH / BLOCK_SIZE - (WIDTH / BLOCK_SIZE - 10) / 2 - 1)
TARGET_RGB = (45, 45, 45)
SCORE = 5  # --- crash score = score * 15 ---
BORDER_SIZE = 3

# --- blocks state ---
BLANK = 0  # --- blank ---
BORDER = 2  # --- white border ---
FILL = 3  # --- border fill ---
CURRENT = 4  # --- current block ---
CLONE = 5  # --- block clone ---

TYPES = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']  # --- piece types --
current_blocks = []  # --- current blocks ---
rand_colors = []  # --- color ---

DATA_PATH = "Resources\\Data\\data.json"  # --- path to json file ---
CREDITS = "www.github.com/orid2004\norid2004@gmail.com"  # --- credits  string ---
# --- stats format string ---
STATS_FORMAT = "Best  [ {} ]  [ L{} ]  [ {} ]\n" \
               "Last  [ {} ]  [ L{} ]  [ {} ]\n" \
               "Avg. Score:  [ {} ]\n"

# --- delay = DELAY - DEC ---
# --- each level lowers the delay ---
LEVEL_DEC = {
    1: 0,
    2: 0.01,
    3: 0.02,
    4: 0.04,
    5: 0.08,
    6: 0.13,
    7: 0.16
}

# --- levels by score ---
LEVEL_SCORE = {
    1: 0,  # 0-150
    2: 150,  # 150-500
    3: 500,  # 500-2500
    4: 2500,  # 2500-5000
    5: 7500,  # 5000-10000
    6: 25000,  # 10000+
}
