from RectangleMaze import RectangleMaze
from Room import Room
import random

class Console:
    @staticmethod
    def get_option(message: str, options: dict):
        Console.print(message)
        options_set = dict(zip([i for i in range(1, len(options) + 1)], options.keys()))
        Console.print(*['({}) {}'.format(str(number), str(option)) for number, option in options_set.items()], sep='\n')
        idx = int(input())

        return options[options_set[idx]]

    @staticmethod
    def print(*args, **kwargs) -> None:
        print('\033[38;5;149m', end='')
        print(*args, **kwargs)
        print('\033[0;0m', end='')

    @staticmethod
    def print_rectangle_maze(maze: RectangleMaze, path_colour: int, wall_colour: int) -> None:
        output = maze.get_str()

        for line in output:
            to_print = ''
            for c in line:
                if c not in Room.states and c not in ('^', '>', 'v', '<'):
                    to_print += '\033[38;5;{}m'.format(str(wall_colour if wall_colour != -1
                                                           else random.randint(0, 255))) + c + '\033[0;0m'
                else:
                    to_print += '\033[38;5;{}m'.format(str(path_colour if path_colour != -1
                                                           else random.randint(0, 255))) + c + '\033[0;0m'
            print(to_print)
