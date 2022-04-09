from RectangleMaze import RectangleMaze
from Room import Room
import random


class Console:
    @staticmethod
    def get_option(message: str, options: dict):
        Console.print(message)
        options_set = dict(zip([i for i in range(1, len(options) + 1)], options.keys()))
        Console.print(*['({}) {}'.format(str(number), str(option)) for number, option in options_set.items()], sep='\n')
        try:
            idx = int(input())
        except ValueError:
            Console.print("Invalid input, you should type one of these:")
            Console.print(*options_set.keys())
            return Console.get_option("", options)

        if idx not in options_set.keys():
            Console.print("Invalid input, you should type one of these:")
            Console.print(*options_set.keys())
            return Console.get_option("", options)

        return options[options_set[idx]]

    @staticmethod
    def get_point(message: str) -> (int, int):
        Console.print(message)
        try:
            x, y = map(int, input().split())
        except ValueError:
            Console.print("Invalid input, you should type two integers")
            return Console.get_point("")

        return x, y

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
