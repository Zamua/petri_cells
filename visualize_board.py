import random
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.gridlayout import GridLayout
from cross_react_programs import cross_react_programs, random_program, to_int_arr, to_human_readable_str
from kivy_ui import StandardUI
from kivy.uix.widget import Widget

LENGTH = 100
WIDTH = 100
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


def slice_array(arr, num_segments):
    n = len(arr)
    slice_size = n // num_segments
    remainder = n % num_segments
    slices = []
    start = 0
    for i in range(num_segments):
        end = start + slice_size + (1 if i < remainder else 0)
        slices.append(arr[start:end])
        start = end
    return slices


def to_color(program):
    def to_hash(in_slice):
        res = 0
        for sub_slice in slice_array(in_slice, 8):
            res <<= 1
            res += sum(sub_slice) % 2
        return res
    as_int_arr = to_int_arr(program)
    three_slices = slice_array(as_int_arr, 3)
    three_slices[0] = three_slices[0][::-1]
    r, g, b = [to_hash(cur_slice) / 256 for cur_slice in three_slices]
    return r, g, b


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
                cell = ColorfulCell()
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
        if self.epoch % PRINTS_FREQUENCY == 0:
            print([[to_color(x) for x in y] for y in self.grid_data])
        for x, row in enumerate(self.grid_data):
            for y, cell in enumerate(row):
                color = to_color(cell)
                self.grid_cells[x][y].set_color(color)


if __name__ == '__main__':
    initial_state = None
    speed = 100
    StandardUI(BoardExecutor(), initial_state, speed=1.0/10.0).run()
