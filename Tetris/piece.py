import settings
import random
import numpy
import grid

SIZE = 4  # --- piece size ---


class GridData:
    # --- Hold Grid Data ---
    def __init__(self, spawn_data):
        self.spawn_data = spawn_data
        self.right_data = max([x[1] for x in self.spawn_data])
        self.left_data = min([x[1] for x in self.spawn_data])
        self.bottom_data = max([x[0] for x in self.spawn_data])


class Piece:
    # --- Piece object ---
    def __init__(self, type: str, color=None):
        # --- piece settings ---
        self.size = None
        self.grid_data: GridData
        self.type = type.upper()
        self.color = random.choice(settings.rand_colors) if color is None else color
        self.grid_data = GridData(self.init_by_type())
        self.grid_pos = (0, 0)

    def init_by_type(self):
        # --- create by type ---
        # --- returns piece data ---
        for block in settings.current_blocks:
            block.color(self.color)
        data = self.size = data_by_type(self.type)
        self.size = data[1]
        return data[0]

    def spawn(self, grid_pos):
        # --- spawn on grid ---
        self.grid_pos = grid_pos
        self.add_to_grid()

    @staticmethod
    def is_valid_data(spawn_data, grid_pos, allowed=(), not_allowed=()):
        # --- return True if spawn_data on grid_pos is available ---
        # --- param allowed - blocks which can be overwritten ---
        # For example: A blank block can be overwritten any time.
        # --- param not allowed - blocks which cannot be overwritten ---
        # For example: A border block cannot be overwritten to limit the game area.
        for row, col in spawn_data:
            # --- check value ---
            future_value = grid.grid[row + grid_pos[0], col + grid_pos[1]]
            if future_value not in allowed or future_value in not_allowed:
                # --- invalid ---
                return False
        # --- valid ---
        return True

    def rotate(self):
        # --- rotate and update grid data ---
        if self.type == 'O':
            # --- O piece has only 1 state ---
            return
        mat = numpy.full((self.size,) * 2, settings.BLANK)  # --- wrap the piece with matrix ---
        for x, y in self.grid_data.spawn_data:
            mat[x, y] = 1  # --- mark blocks ---
        '''
        [[1,2], [3,4]]
        1. unpack the matrix and reverse the data [3,4], [1,2]
        2. zip values with same index [3,1], [4,2]
        3. convert to list object
        '''
        mat = numpy.array(list(zip(*mat[::-1])))
        data = []  # --- new grid data ---
        for i in range(len(mat)):
            for j in range(len(mat)):
                if mat[i, j] == 1:
                    # --- add blocks spawn position ---
                    data.append((i, j))
        if self.is_valid_data(data, self.grid_pos, allowed=(settings.BLANK, settings.CURRENT)):
            # --- update data if valid ---
            self.grid_data.__init__(data)
            # Note: can't rotate when collapses with border\other objects

    def can_step(self):
        # --- returns True if can step down ---
        if self.grid_data.bottom_data + self.grid_pos[0] >= 27:
            return False
        return self.can_move(add_row=1)

    def step(self):
        # --- step down ---
        self.spawn((self.grid_pos[0] + 1, self.grid_pos[1]))

    def can_move(self, add_row=0, add_col=0):
        # --- returns True if can move:
        # {add_row units down, add_col units right}
        return self.is_valid_data(
            self.grid_data.spawn_data, (self.grid_pos[0] + add_row, self.grid_pos[1] + add_col),
            [settings.BLANK, settings.CURRENT], []
        )

    def can_left(self):
        # --- can move left ---
        return self.can_move(add_col=-1)

    def can_right(self):
        # --- can move right ---
        return self.can_move(add_col=1)

    def add_to_grid(self):
        # --- add to grid  ---
        # --- overwrite with CURRENT block ---
        new_grid = grid.grid.copy()
        for x, y in self.grid_data.spawn_data:
            # --- calculate location using spawn_data & current pos ---
            new_grid[x + self.grid_pos[0], y + self.grid_pos[1]] = settings.CURRENT
        # --- add changes to queue ---
        grid.commit_grid_changes(new_grid)

    def remove_from_grid(self):
        # --- remove to grid ---
        # --- overwrite with settings.BLANK ---
        new_grid = grid.grid.copy()
        for row, col in self.grid_data.spawn_data:
            new_grid[row + self.grid_pos[0], col + self.grid_pos[1]] = settings.BLANK
        # --- add changes to queue ---
        grid.commit_grid_changes(new_grid)


def data_by_type(type: str):
    # --- return spawn data by type ---
    # --- according to super rotation system ---
    if type == 'I':
        return [
                   [0, 1],
                   [1, 1],
                   [2, 1],
                   [3, 1]
               ], 4
    if type == 'J':
        return [
                   [0, 1],
                   [1, 1],
                   [2, 0],
                   [2, 1]
               ], 3
    if type == 'L':
        return [
                   [0, 0],
                   [0, 1],
                   [1, 1],
                   [2, 1]
               ], 3
    if type == 'O':
        return [
                   [0, 1],
                   [0, 2],
                   [1, 1],
                   [1, 2]
               ], 4
    if type == 'S':
        return [
                   [0, 0],
                   [1, 0],
                   [1, 1],
                   [2, 1]
               ], 3
    if type == 'T':
        return [
                   [0, 1],
                   [1, 0],
                   [1, 1],
                   [2, 1]
               ], 3
    if type == 'Z':
        return [
                   [0, 1],
                   [1, 0],
                   [1, 1],
                   [2, 0]
               ], 3
