from MyGraph import Graph
from RectangleMaze import RectangleMaze
from ConsoleGui import Console
import sys
import time
from datetime import datetime
from os import system
import tty
import termios


def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def process_new_maze(arg: str) -> None:
    def show_maze(tree: Graph) -> None:
        system('clear')
        maze = RectangleMaze(m, n)
        maze.build_on_graph(tree)
        Console.print_rectangle_maze(maze, pathColour, wallColour)

    def show_path(tree: Graph) -> None:
        Console.print('Choose two points, 1-indexation, first width, second height')

        i, j = Console.get_point('Start:')
        k, l = Console.get_point('Finish:')

        from_ = (j - 1) * m + (i - 1)
        to_ = (l - 1) * m + (k - 1)

        system('clear')
        tree.mark_start_and_finish(from_, to_)
        tree.mark_path(from_, to_)

        show_maze(tree)
        tree.clear_marks()

    def animate_path(tree: Graph) -> None:
        Console.print('Choose two points, 1-indexation, first width, second height')

        i, j = Console.get_point('Start:')
        k, l = Console.get_point('Finish:')

        from_ = (j - 1) * m + (i - 1)
        to_ = (l - 1) * m + (k - 1)

        tree.mark_path(from_, to_)

        path_nodes = [from_]
        v = from_
        while tree.nodes[v].nextInPath != -1:
            v = tree.nodes[v].nextInPath
            path_nodes.append(v)

        tree.clear_marks()

        for u in path_nodes:
            system('clear')
            tree.mark_start_and_finish(from_, to_)
            tree.mark_path(from_, u)
            show_maze(tree)
            time.sleep(0.1)
            tree.clear_marks()

    def exit_(tree: Graph) -> None:
        system('clear')
        exit(0)

    def save_maze_txt(tree: Graph) -> None:
        maze = RectangleMaze(m, n)
        maze.build_on_graph(tree)

        Console.print('write name for file:')
        name = input()
        with open(name, mode='w') as f:
            f.write(str(wallColour) + '\n')
            f.write(str(pathColour) + '\n')
            for line in maze.get_str():
                for c in line:
                    f.write(c)
                f.write('\n')

    def restart(tree: Graph) -> None:
        Console.print('Chose file with maze, or generate new one with one of the algorithms.')

        d = dict(zip(tree_maker.keys(), tree_maker.keys()))
        d['file'] = 'file'

        newArg = Console.get_option('', d)
        if newArg in tree_maker.keys():
            process_new_maze(newArg)
        else:
            Console.print('Write file name:')
            file_name = input()
            process_new_maze(file_name)

    def play(tree: Graph) -> None:
        def get_dir() -> int:
            c = get_char()
            direction = {
                'w': 0,
                'd': 1,
                's': 2,
                'a': 3,
            }
            if c == '\x1b':
                return -1

            if c == '\x1a' or c == '\x18':
                exit_(g)

            return direction[c]

        Console.print('Choose two points, 1-indexation, first width, second height')

        i, j = Console.get_point('Start:')
        k, l = Console.get_point('Finish:')

        from_ = (j - 1) * m + (i - 1)
        to_ = (l - 1) * m + (k - 1)

        tree.mark_start_and_finish(from_, to_)
        maze = RectangleMaze(m, n)
        maze.build_on_graph(tree)

        maze.start_run()
        tin = datetime.now()
        while True:
            system('clear')
            Console.print('Use WASD to control your movements, or Esc to leave')
            Console.print_rectangle_maze(maze, pathColour, wallColour)
            direction = get_dir()
            if direction == -1:
                return

            inFinish = maze.make_turn(direction)

            if inFinish:
                system('clear')
                Console.print_rectangle_maze(maze, pathColour, wallColour)
                Console.print('Your time is {}. Not bad!'.format(datetime.now() - tin))
                return

    tree_maker = {'dfs': Graph.make_tree_dfs,
                  'bfs': Graph.make_tree_bfs,
                  'kruskal': Graph.make_tree_kruskal}
    themes = {
        'Classic': (208, 8),
        'Pony': (201, -1),
        'Doom': (196, 208),
        'Cosmos': (99, 123),
        'B&W': (15, 15),
        'Chaos': (-1, -1)
    }

    options_with_maze = {
        'show maze': show_maze,
        'give me a try': play,
        'show path': show_path,
        'animate path': animate_path,
        'get new maze': restart,
        'save maze': save_maze_txt,
        'exit': exit_
    }

    g = Graph(0)
    if arg in tree_maker:
        construct_tree = tree_maker[arg]

        system('clear')
        Console.print('You have chosen ' + arg + ' algorithm to make maze. Now set width, height and colour theme.')

        m, n = Console.get_point("Type width and height:\n(normally not more than 30 and 15 respectively)")

        wallColour, pathColour = Console.get_option('Theme:', themes)

        g.construct_from_rectangle(m, n)
        construct_tree(g)
    else:
        maze_txt = []
        with open(arg, mode='r') as f:
            wallColour = int(f.readline())
            pathColour = int(f.readline())
            for line in f:
                maze_txt.append(list(line))
            m = (len(maze_txt[0]) - 1) // 2
            n = (len(maze_txt) - 1) // 2
        g.construct_from_rectangle_txt(maze_txt)
        g.make_tree_dfs()

    Console.print("Maze is ready!")

    while True:
        Console.print("Width: ", m)
        Console.print("Height: ", n)
        Console.get_option("What do you want to do next?", options_with_maze)(g)


if len(sys.argv) > 1:
    process_new_maze(sys.argv[1])
else:
    process_new_maze('dfs')
