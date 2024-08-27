import random
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.gridlayout import GridLayout
from cross_react_programs import cross_react_programs, random_program, to_int_arr, to_human_readable_str
from kivy_ui import StandardUI
from kivy.uix.widget import Widget

LENGTH = 20
WIDTH = 20
PRINTS_FREQUENCY = 100

def update_state(grid):
    ordered_pairs = [(a, b) for a in range(len(grid)) for b in range(len(grid[0]))]
    random.shuffle(ordered_pairs)
    visited = [[False] * LENGTH] * WIDTH
    for coordinate in ordered_pairs:
        x, y = coordinate
        program1 = grid[x][y]
        if visited[x][y]:
            continue
        x2, y2 = (x + random.randint(-2, 2), y + random.randint(-2, 2))
        if x2 < 0 or y2 < 0 or x2 >= len(grid) or y2 >= len(grid[0]):
            continue
        program2 = grid[x2][y2]
        new_program1, new_program2 = cross_react_programs(program1, program2)
        grid[x][y] = new_program1
        grid[x2][y2] = new_program2
        visited[x][y] = True
        visited[x2][y2] = True
    return grid


class ColorfulCell(Widget):
    def __init__(self, **kwargs):
        super(ColorfulCell, self).__init__(**kwargs)
        with self.canvas:
            self.color = Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        # keep rectangle in sync with widget
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def set_color(self, rgb_tuple):
        self.color.rgb = rgb_tuple
        self.color.a = 1


class ProgramCell(GridLayout):

    def __init__(self, **kwargs):
        super(ProgramCell, self).__init__(**kwargs)
        self.cells = []
        self.cols = 8
        self.rows = 8

        for _ in range(8 * 8):
            cell = ColorfulCell()
            self.add_widget(cell)
            self.cells.append(cell)

        self.color_mapping = {
            # white = 0
            0: (0.9375, 0.94921875, 0.953125),
            # red = <
            1: (0.90234375, 0.296875, 0.234375),
            # orange = >
            2: (0.94921875, 0.609375, 0.0703125),
            # yellow = {
            3: (0.953125, 0.8125, 0.24609375),
            # brown = }
            4: (0.48046875, 0.24609375, 0.0),
            # dark green = -
            5: (0.078125, 0.3515625, 0.1953125),
            # light green = +
            6: (0.6328125, 0.84765625, 0.8046875),
            # dark blue = .
            7: (0.1015625, 0.3203125, 0.4609375),
            # cyan = ,
            8: (0.63671875, 0.890625, 0.83984375),
            # purple = [
            9: (0.5546875, 0.265625, 0.67578125),
            # pink = ]
            10: (0.68359375, 0.4765625, 0.76953125),
        }

    def int_to_color(self, num):
        if num in self.color_mapping:
            return self.color_mapping[num]
        elif num < 0:
            x = 1 + (num / 256)
            x = max(0, x)
            return x, x, x
        elif num > 10:
            x = 1 - (num / 256)
            x = max(0, x)
            # subtract from r to differentiate from negatives
            r = x - 10
            return r, x, x

    def set_color(self, program):
        as_int_arr = to_int_arr(program)
        for cell, num in zip(self.cells, as_int_arr):
            color_tuple = self.int_to_color(num)
            cell.set_color(color_tuple)


class BoardExecutor:
    def init_state(self, starting_board):
        self.epoch = 0
        global LENGTH, WIDTH
        if starting_board is not None:
            self.grid_data = starting_board
            return
        self.grid_data = [[None] * LENGTH for _ in range(WIDTH)]
        for x in range(LENGTH):
            for y in range(WIDTH):
                self.grid_data[x][y] = random_program()

    def init_content(self, layout):
        global WIDTH, LENGTH
        grid_layout = GridLayout(cols=WIDTH, rows=LENGTH)
        self.grid_cells = [[None] * LENGTH for _ in range(WIDTH)]
        for x in range(WIDTH):
            for y in range(LENGTH):
                cell = ProgramCell()
                grid_layout.add_widget(cell)
                self.grid_cells[x][y] = cell
        layout.add_widget(grid_layout)
        self.update_content()

    def update_state(self):
        self.epoch += 1
        self.grid_data = update_state(self.grid_data)
        if self.epoch % PRINTS_FREQUENCY == 0:
            print([[to_human_readable_str(x, False) for x in y] for y in self.grid_data])

    def update_content(self):
        print(self.epoch)
        for x, row in enumerate(self.grid_data):
            for y, cell in enumerate(row):
                self.grid_cells[x][y].set_color(cell)


if __name__ == '__main__':
    initial_state = None
    speed = 100
    StandardUI(BoardExecutor(), initial_state, speed=1.0/10.0).run()
