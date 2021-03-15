import settings
import random
import numpy
from queue import Queue

# --- grid settings ---
grid_size = (0, 0)
grid = numpy.full(grid_size, settings.BLANK)
grid_changes = Queue()


def clear():
    global grid, grid_size
    # --- fill grid with settings.BLANK ---
    grid_size = int(settings.HEIGHT / 25), int(settings.WIDTH / 25)
    grid = numpy.full(grid_size, settings.BLANK)  # [16,28]


def to_game_pos(row, col) -> tuple:
    global grid_size
    # --- convert grid position to game position ---
    # [row, col] -> [x, y]
    game_x = settings.BLOCK_SIZE * (col - grid_size[1] / 2 + 0.5)
    game_y = settings.BLOCK_SIZE * (grid_size[0] / 2 - row - 0.5)
    # --- return game position ---
    return game_x, game_y


def draw_random_border(size, border_block):
    global grid, grid_size
    # --- draw random colorful border ---
    # --- setup border limits ---
    neg_size = size * (-1)
    grid[:, 0:size - 1], grid[:, neg_size + 1:-1], grid[:, -1] = (settings.FILL,) * size
    grid[:, size - 1], grid[:, neg_size] = (settings.BORDER,) * 2
    for row in range(grid_size[0]):
        for col in range(grid_size[1]):
            if grid[row, col] == settings.BORDER:
                # --- create and show a border block ---
                ### white ###
                clone = border_block.clone()
                clone.goto(to_game_pos(row, col))
                clone.showturtle()
            elif grid[row, col] == settings.FILL:
                # --- create and show a fill block ---
                ### colorful ###
                clone = border_block.clone()
                clone.goto(to_game_pos(row, col))
                clone.color(random.choice(settings.rand_colors))
                clone.showturtle()


def commit_grid_changes(new_grid):
    # --- add changes to queue ---
    grid_changes.put(new_grid)
