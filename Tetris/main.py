import gc
import json
import random
import time
import turtle
import numpy
import grid
import piece
import settings
import sys
import setup

# --- packages settings ---
numpy.set_printoptions(linewidth=numpy.inf)
turtle.colormode(255)
# setup.play("Resources/sounds/music.mp3") # --- music setup ---
setup.load_colors()  # --- load random colors ---


# --- rotation system ---
### super rotation system ###

class Game:
    def __init__(self, title, size: tuple):
        # --- init Game ---
        grid.clear()  # --- clear global grid ---
        self.delay = settings.DELAY  # --- set delay ---
        self.wn = setup.setup_wn(size=size, title=title, bg_color="black")  # --- create window ---
        self.keyboard_binding()  # --- bind keyboard ---
        self.current: piece.Piece
        self.timer, self.stats_timer, self.round_timer = setup.gen_timers(3)  # --- create timers ---
        # --- declare ---
        self.current, self.clone_color, self.game_state, \
        self.target_blocks, self.stats = (None,) * 5
        self.ms = setup.gen_image(wn=self.wn, file_name="Resources/graphics/main_screen.gif",
                                  pos=(0, 0))  # --- setup main screen ---
        self.logo = setup.gen_image(wn=self.wn, file_name="Resources/graphics/tetris.gif",
                                    pos=(0, int(settings.HEIGHT / 2.8)))  # --- setup tetris logo ---
        self.border_block = setup.gen_standard_block()  # --- create border block ---
        self.pen = setup.gen_pen()  # --- pen ---
        self.score, self.level = 0, 1  # --- stats variables ---

    def launch(self):
        # --- launch game ---
        try:
            self.round_setup()  # --- create new round ---
        except Exception as e:
            raise e
            sys.exit(-1)

    def round_setup(self):
        # --- round setup ---
        settings.current_blocks = setup.gen_standard_blocks(count=piece.SIZE)  # --- create piece blocks ---
        self.current = None  # --- init current piece ---
        self.target_blocks = setup.gen_standard_blocks(count=piece.SIZE,
                                                       rgb=settings.TARGET_RGB)  # --- create target blocks ---
        for block in self.target_blocks + settings.current_blocks:
            block.hideturtle()  # --- hide all blocks ---
        grid.clear()  # --- clear grid ---
        self.pen.clear()  # --- clear pen ---
        setup.create_stats()  # --- create json file ---
        grid.draw_random_border(size=settings.BORDER_SIZE, border_block=self.border_block)  # --- draw the border ---
        self.timer.stop()  # --- reset the timer ---
        self.score, self.level = 0, 1  # --- define stats variables ---
        self.game_state = "main"  # --- set game state ---
        self.main_screen()  # --- start main screen ---

    def main_screen(self):
        # --- main screen setup ---
        self.wn.bgcolor("white")  # --- change background ---
        # --- show main screen objects ---
        self.logo.showturtle()
        self.ms.showturtle()
        self.main_write()
        with open(settings.DATA_PATH, ) as f:
            # --- load stats from json ---
            self.stats = json.load(f)
        while self.game_state == "main":
            # --- wait for [ENTER] ---
            self.wn.update()
        # --- hide main screen objects ---
        self.logo.hideturtle()
        self.ms.hideturtle()
        self.pen.clear()
        self.start_round()  # --- start the round ---

    def main_write(self):
        # --- write stats ---
        self.pen.color("black")
        data = setup.load_stats()
        self.pen.goto(0, -235)
        # --- fill stats string with values ---
        stats = settings.STATS_FORMAT.format(
            *list(data["Best"][0].values()),
            *list(data["Last"][0].values()),
            data["Avg."][0]
        )
        # --- write credits ---
        self.pen.write(stats, align="center", font=("Ariel", 11, "normal"))
        self.pen.color("green")
        self.write_center(
            self.pen,
            (0, -300),
            settings.CREDITS
        )

    def to_game_state(self):
        self.game_state = "game"  # --- change game state

    @staticmethod
    def write_center(pen, pos, st):
        # --- write text aligned center ---
        for line in st.split('\n'):
            pen.goto(*pos)
            pen.write(line, align="center", font=("Helvetica", 11, "normal"))
            pos = pos[0], pos[1] - 22.5

    def keyboard_binding(self):
        # --- bind keyboard ---
        setup.setup_keyboard(self.wn, {self.to_game_state: "Return"})  # --- Enter ---
        setup.setup_keyboard_press(
            self.wn,
            {
                self.left: "Left",
                self.right: "Right",
                self.try_step_current: "Down",
                self.go_down: 'space',
                self.rotate: "z",
            }
        )

    def show_stats(self):
        # --- write game score, level, time. ---
        self.pen.clear()
        self.pen.color("green")
        self.pen.goto(grid.to_game_pos(1, settings.BORDER_SIZE))  # --- write score & level ---
        stats = [self.round_timer.tostr(), "Score: " + str(self.score), "Level: " + str(self.level)]
        self.pen.write('\n'.join(stats[:-1]), align="left", font=("Helvetica", 12, "normal"))
        self.pen.goto(grid.to_game_pos(0.25, grid.grid_size[1] - settings.BORDER_SIZE - 1))  # --- write time ---
        self.pen.write(stats[-1], align="right", font=("Helvetica", 12, "normal"))

    @staticmethod
    def remove_block(game_pos: tuple):
        # --- remove block in position game_pos ---
        for block in turtle.Screen().turtles():
            if block.pos() == game_pos and block not in settings.current_blocks:
                block.hideturtle()  # --- hide block ---

    def update_grid(self):
        # update grid changes on screen
        self.update_target_loc()  # --- update target blocks ---
        if not grid.grid_changes.empty():
            new_grid = numpy.copy(grid.grid_changes.get())  # get changes from queue
            block_index = 0  # current block index [0,4)
            for row in range(grid.grid_size[0]):
                for col in range(grid.grid_size[1]):
                    # --- detect changes ---
                    if new_grid[row, col] != grid.grid[row, col]:
                        game_pos = grid.to_game_pos(row, col)  # --- convert grid pos to grid pos
                        if new_grid[row, col] == settings.BLANK:
                            # --- update to blank block ---
                            self.remove_block(game_pos)
                        elif new_grid[row, col] == settings.CURRENT:
                            # --- update current piece location ---
                            # --- one block at a time ---
                            settings.current_blocks[block_index].goto(game_pos)
                            settings.current_blocks[block_index].showturtle()
                            block_index += 1  # --- next current block
                        elif new_grid[row, col] == settings.CLONE:
                            # --- update to a clone block ---
                            # --- create a clone ---
                            block = setup.gen_standard_block(self.clone_color)
                            block.goto(game_pos)
                            block.showturtle()
            grid.grid = numpy.copy(new_grid)  # --- update memory ---

    def rotate(self):
        # --- rotate current piece ---
        if self.current is not None:
            self.current.remove_from_grid()  # --- remove piece ---
            self.update_grid()  # --- update changes ---
            self.current.rotate()  # --- rotate current ---
            self.current.add_to_grid()  # --- add rotated ---
            self.update_grid()  # --- update changes ---

    def turn_current(self, offset):
        self.current.remove_from_grid()  # --- remove piece ---
        self.update_grid()  # --- update changes ---
        self.current.spawn((self.current.grid_pos[0], self.current.grid_pos[1] + offset))  # --- spawn ---
        self.update_grid()  # --- update changes ---

    def left(self):
        # --- go left ---
        if self.current is not None and self.current.can_left():
            self.turn_current(-1)

    def right(self):
        # --- go right ---
        if self.current is not None and self.current.can_right():
            self.turn_current(1)

    def try_step_current(self):
        # --- check if step is possible ---
        if self.current is not None and self.current.can_step():
            self.step_current()

    def step_current(self):
        # --- step down ---
        if self.current is not None:
            self.current.remove_from_grid()  # --- remove piece ---
            self.update_grid()  # --- update changes ---
            self.current.step()  # --- step current ---
            self.update_grid()  # --- update changes ---
            self.timer.start()  # --- start timer ---

    def go_down(self):
        # --- place piece immediately ---
        if self.current is not None:
            self.current.remove_from_grid()  # --- remove piece ---
            self.update_grid()  # --- update changes ---
            while self.current.can_step():
                self.step_current()  # --- step current while possible---
            self.current.add_to_grid()
            self.update_grid()  # --- update changes ---
            self.score += settings.SCORE  # --- inc score ---
            self.respawn()  # --- respawn ---

    def spawn_new(self):
        # --- spawn new piece ---
        self.current = piece.Piece(random.choice(settings.TYPES))  # --- new piece object ---
        grid_base_pos = settings.BASE_ROW, settings.BASE_COL
        self.current.spawn(grid_base_pos)  # --- spawn ---
        self.update_grid()  # --- update changes ---

    def hide_target(self):
        # --- hide target blocks ---
        for block in self.target_blocks:
            block.hideturtle()

    def update_target_loc(self):
        # --- update target blocks location ---
        row, col = self.current.grid_data.bottom_data + 1, self.current.grid_pos[1]  # --- first possible location ---
        target_blocks = self.current.grid_data.spawn_data  # --- spawn data ---
        index = 0
        while row < grid.grid_size[0] - self.current.grid_data.bottom_data and self.current.is_valid_data(
                target_blocks, (row, col), allowed=(settings.BLANK, 4)):
            # --- while a position is valid: test next one ---
            row += 1
        row -= 1  # --- last valid position
        if row - self.current.grid_pos[0] < piece.data_by_type(self.current.type)[1]:
            self.hide_target()  # --- hide target blocks when done ---
        elif row > 1:
            for init_row, init_col in target_blocks:
                self.target_blocks[index].goto(
                    grid.to_game_pos(row + init_row, col + init_col))  # --- set new position ---
                self.target_blocks[index].showturtle()  # --- show target block ---
                index += 1

    def clone_blocks(self, spawn_data, grid_pos):
        # --- create a clone of spawn_data in grid_pos
        new_grid = grid.grid.copy()  # --- temp ---
        for row, col in spawn_data:
            # --- set clone location ---
            new_grid[row + grid_pos[0], col + grid_pos[1]] = settings.CLONE
        # --- update changes ---
        grid.commit_grid_changes(new_grid)
        self.update_grid()

    def crash_blocks(self):
        # --- crash a completed row ---
        for row_to_crash in range(grid.grid_size[0]):
            if settings.BLANK not in grid.grid[row_to_crash] and settings.CURRENT not in grid.grid[row_to_crash]:
                self.current.remove_from_grid()  # --- remove piece ---
                self.update_grid()  # --- update changes ---
                new_grid = grid.grid.copy()  # --- temp ---
                # --- crash a row ---
                for row in range(1, row_to_crash + 1)[::-1]:
                    new_grid[row][settings.MID_STARTS:settings.MID_ENDS + 1] = new_grid[row - 1][
                                                                               settings.MID_STARTS:settings.MID_ENDS + 1
                                                                               ]
                new_grid[0, settings.MID_STARTS:settings.MID_ENDS + 1] = 0  # --- clear the first row ---
                # --- update changes ---
                grid.commit_grid_changes(new_grid)
                self.update_grid()
                self.current.add_to_grid()
                self.update_grid()
                self.score += settings.SCORE * 15  # --- inc score --

    def respawn(self):
        # --- handle each spawn ---
        self.hide_target()  # --- hide target blocks ---
        self.clone_color = self.current.color  # --- save piece color ---
        self.clone_blocks(self.current.grid_data.spawn_data, self.current.grid_pos)  # --- create a clone ---
        self.spawn_new()  # --- spawn new piece ---
        self.update_grid()  # --- update changes ---

    @staticmethod
    def show_current_blocks():
        # --- show piece ---
        for block in settings.current_blocks:
            block.showturtle()

    def update_level(self):
        # --- update level ---
        if self.score > list(settings.LEVEL_SCORE.values())[-1]:
            # --- special case for high level ---
            self.level = list(settings.LEVEL_SCORE.keys())[-1]  # --- last level ---
            self.delay = self.delay = settings.DELAY - settings.LEVEL_DEC[self.level]  # --- update delay ---
            return

        for level in settings.LEVEL_SCORE:
            # set level in range 1-6
            if self.score < settings.LEVEL_SCORE[level]:
                self.level = level - 1  # update level ---
                self.delay = settings.DELAY - settings.LEVEL_DEC[self.level]  # --- update delay ---
                return

    def start_round(self):
        # --- main loop ---
        self.spawn_new()  # --- spawn new ---
        self.timer.start()  # --- handle delay ---
        self.show_current_blocks()  # --- show piece ---
        self.wn.bgcolor("black")  # --- set bg ---
        self.round_timer.start()  # --- count surviving time ---
        while True:
            if self.timer.value() > self.delay:
                if self.current.can_step():
                    # --- step piece ---
                    self.step_current()
                else:
                    if self.current.grid_pos[0] <= 0:
                        # --- game over ---
                        self.exit_round()
                        return
                    # placed
                    self.score += settings.SCORE  # --- inc score ---
                    self.respawn()  # --- spawn new piece ---
                self.timer.start()  # --- start the timer again ---
            self.update_target_loc()  # --- update target blocks ---
            self.crash_blocks()  # --- try crash blocks ---
            self.update_level()  # update level
            self.show_stats()  # write stats
            self.wn.update()  # --- update window ---

            gc.collect()

    def exit_round(self):
        # --- exit ---
        data = setup.load_stats()  # --- load stats from json ---
        current = {"Score": self.score, "Level:": self.level, "Time": self.round_timer.tostr()}  # --- round score ---
        best = data["Best"][0]
        if current["Score"] > best["Score"]:
            # --- update best round ---
            data["Best"][0] = current
        data["Last"][0] = current  # --- update last round stats ---
        data["Avg."][0] = int((data["Avg."][0] * data["Count"][0] + self.score) / (
                data["Count"][0] + 1))  # --- update average ---
        data["Count"][0] += 1  # inc rounds
        with open(settings.DATA_PATH, 'w') as f:
            # --- update data ---
            json.dump(data, f)
        self.game_state = "main"  # --- change game state ---
        self.restart_round()  # --- restart ---

    def restart_round(self):
        grid.commit_grid_changes(numpy.full(grid.grid_size, settings.BLANK))  # --- init the grid ---
        self.update_grid()  # --- update changes ---
        # --- start a new round
        for block in turtle.Screen().turtles():
            block.hideturtle()  # --- hide turtles ---
        # --- launch a new round ---
        time.sleep(0.5)
        self.round_setup()


def main():
    # --- TETRIS GAME ! ---
    tetris = Game("Tetris", (
        settings.WIDTH + 4,
        settings.HEIGHT + 8
    ))
    # --- launch tetris ---
    tetris.launch()


if __name__ == '__main__':
    main()
