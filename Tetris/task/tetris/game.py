import numpy as np
import sys


class PlayGrid:
    grid = []

    def __init__(self, mx=10, nx=20):
        PlayGrid.grid = np.array([['-'] * mx] * nx)
        Tetrimino.width = mx
        Tetrimino.height = nx


def check_lines_width():
    test_list = []
    for i in range(len(PlayGrid.grid)):
        for j in range(len(PlayGrid.grid[i])):
            if PlayGrid.grid[i][j] == '0':
                test_list.append(True)
            else:
                test_list.append(False)
        if all(test_list):
            PlayGrid.grid = np.delete(PlayGrid.grid, i, axis=0)
            PlayGrid.grid = np.vstack((np.array(['-'] * Tetrimino.width), PlayGrid.grid))
        test_list.clear()

def check_lines_height():
    for i in range(Tetrimino.width):
        check_fail = list(PlayGrid.grid[:,i])
        for j in range(len(check_fail)):
            if check_fail[j] == '-':
                check_fail[j] = False
            else:
                check_fail[j] = True
        if all(check_fail):
            print_grid(PlayGrid.grid)
            print()
            print('Game Over!')
            sys.exit()

def print_grid(list_to_grid):
    for line in list_to_grid:
        print(' '.join(line))


def input_figure(figure):
    if figure == 'I':
        return Ifigure()
    elif figure == 'S':
        return Sfigure()
    elif figure == 'Z':
        return Zfigure()
    elif figure == 'O':
        return Ofigure()
    elif figure == 'T':
        return Tfigure()
    elif figure == 'L':
        return Lfigure()
    elif figure == 'J':
        return Jfigure()

class Tetrimino:
    width = 10
    height = 20

    def __init__(self, positions):
        self.positions = np.array([np.array(x) for x in positions])
        self.pos_number = 0
        self.current_position = self.positions[self.pos_number]
        self.blocks = []
        self.status = True
        self.push_pos_to_blocks()
        self.draw_figure()
        self.blocks.clear()

    def push_pos_to_blocks(self):
        for i in self.current_position:
            self.blocks.append([i // 10, i % 10])

    def draw_figure(self):
        for i in self.blocks:
            PlayGrid.grid[i[0]][i[1]] = '0'

    def erase_figure(self):
        for i in self.blocks:
            PlayGrid.grid[i[0]][i[1]] = '-'

    def any_turn(self):
        if not self.status:
            print_grid(PlayGrid.grid)
            return
        self.current_position = self.positions[self.pos_number]
        self.blocks.clear()
        self.push_pos_to_blocks()
        y_coords = []
        self.erase_figure()
        self.blocks.clear()
        self.positions += Tetrimino.width
        self.current_position = self.positions[self.pos_number]
        self.push_pos_to_blocks()
        self.draw_figure()
        for block in self.blocks:
            y_coords.append(int(block[0]))
        for i in y_coords:
            if i == Tetrimino.height - 1:
                self.status = False
                print_grid(PlayGrid.grid)
                return
        self.blocks.clear()
        self.check_for_freeze()
        print_grid(PlayGrid.grid)

    def rotate(self):
        if not self.status:
            print_grid(PlayGrid.grid)
            return
        self.current_position = self.positions[self.pos_number]
        current_pos = self.current_position
        if self.pos_number == len(self.positions) - 1:
            next_pos_num = 0
        else:
            next_pos_num = self.pos_number + 1
        next_position = self.positions[next_pos_num]
        self.push_pos_to_blocks()
        self.erase_figure()
        self.blocks.clear()
        self.current_position = next_position
        self.push_pos_to_blocks()
        chooser = 1
        for block in self.blocks:
            if block[1] >= Tetrimino.width - 1 or block[0] >= Tetrimino.height - 1:
                chooser = 0
                break
            elif PlayGrid.grid[block[0]][block[1]] == 'O':
                chooser = 0
                break
        self.blocks.clear()
        if chooser == 1:
            self.pos_number = next_pos_num
            self.current_position = next_position
        else:
            self.current_position = current_pos
        self.any_turn()

    def move_left(self):
        if not self.status:
            print_grid(PlayGrid.grid)
            return
        self.current_position = self.positions[self.pos_number]
        self.blocks.clear()
        self.push_pos_to_blocks()
        x_coords = []
        for block in self.blocks:
            x_coords.append(int(block[1]))
        chooser = 1
        for i in x_coords:
            if i == 0:
                chooser = 0
                break
        if chooser == 1:
            self.erase_figure()
            self.blocks.clear()
            self.positions -= 1
            self.current_position = self.positions[self.pos_number]
            self.push_pos_to_blocks()
            self.draw_figure()
            self.blocks.clear()
        self.any_turn()

    def move_right(self):
        if not self.status:
            print_grid(PlayGrid.grid)
            return
        self.current_position = self.positions[self.pos_number]
        self.blocks.clear()
        self.push_pos_to_blocks()
        x_coords = []
        for block in self.blocks:
            x_coords.append(int(block[1]))
        chooser = 1
        for i in x_coords:
            if i == Tetrimino.width - 1:
                chooser = 0
                break
        if chooser == 1:
            self.erase_figure()
            self.blocks.clear()
            self.positions += 1
            self.current_position = self.positions[self.pos_number]
            self.push_pos_to_blocks()
            self.draw_figure()
            self.blocks.clear()
        self.any_turn()

    def check_for_freeze(self):
        if not self.status:
            return
        self.push_pos_to_blocks()
        check_under_figure = set()
        check_current_figure = set()
        for block in self.blocks:
            check_current_figure.add(tuple(block))
            block[0] += 1
            check_under_figure.add(tuple(block))
        check_under_figure = check_under_figure.difference(check_current_figure)
        for block in check_under_figure:
            if PlayGrid.grid[block[0]][block[1]] == '0':
                self.status = False
                return
        self.blocks.clear()




class Ofigure(Tetrimino):

    def __init__(self):
        super().__init__(positions=[[4, 14, 15, 5]])


class Ifigure(Tetrimino):

    def __init__(self):
        super().__init__(positions=[[4, 14, 24, 34], [3, 4, 5, 6]])


class Sfigure(Tetrimino):

    def __init__(self):
        super().__init__(positions=[[5, 4, 14, 13], [4, 14, 15, 25]])


class Zfigure(Tetrimino):

    def __init__(self):
        super().__init__(positions=[[4, 5, 15, 16], [5, 15, 14, 24]])


class Lfigure(Tetrimino):

    def __init__(self):
        super().__init__(positions=[[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]])


class Jfigure(Tetrimino):

    def __init__(self):
        super().__init__(positions=[[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]])


class Tfigure(Tetrimino):

    def __init__(self):
        super().__init__(positions=[[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]])



command = input()
if command == '':
    newgrid = PlayGrid()
else:
    m, n = command.split()
    m = int(m)
    n = int(n)
    newgrid = PlayGrid(m, n)
print_grid(PlayGrid.grid)
print()


command = input()
while command != 'exit':
    while command not in ('I', 'S', 'Z', 'L', 'J', 'O', 'T'):
        command = input()
    current_figure = input_figure(command)
    print_grid(PlayGrid.grid)
    print()
    command = input()
    while command != 'piece':
        if command == 'right':
            check_lines_height()
            current_figure.move_right()
        elif command == 'left':
            check_lines_height()
            current_figure.move_left()
        elif command == 'rotate':
            check_lines_height()
            current_figure.rotate()
        elif command == 'down':
            check_lines_height()
            current_figure.any_turn()
        elif command == 'exit':
            sys.exit()
        elif command == 'break':
            check_lines_width()
            print_grid(PlayGrid.grid)
        print()
        command = input()
    if command == 'exit':
        sys.exit()
