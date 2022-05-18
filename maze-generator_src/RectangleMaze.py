from Room import Room
from MyGraph import Graph


class RectangleMaze:
    def __init__(self, width: int, height: int) -> None:
        self.grid = [[Room(4) for _ in range(width)] for _ in range(height)]
        # each room has 4 possible neighbours: above(0), right(1), below(2), left(3)
        self.width = width
        self.height = height
        self.path_finish = None
        self.path_start = None
        self.current_player_pos = None

    def set_current_player_pos(self, pos):
        self.current_player_pos = pos
        i, j = pos
        self.grid[i][j].state = '⊛'

    def get_current_player_pos(self):
        return self.current_player_pos

    def build_on_graph(self, graph: Graph) -> None:
        m = self.width
        n = self.height
        self.__init__(m, n)

        for i in range(n):
            for j in range(m):
                if graph.nodes[i * m + j].inPath:
                    self.grid[i][j].state = '*'

                if i * m + j == graph.path_start:
                    self.grid[i][j].state = '⦿'
                    self.path_start = (i, j)

                if i * m + j == graph.path_finish:
                    self.grid[i][j].state = '⦿'
                    self.path_finish = (i, j)

                for u in graph.nodes[i * m + j].adj:
                    if u == (i - 1) * m + j:
                        self.grid[i][j].link(0)
                    if u == i * m + j + 1:
                        self.grid[i][j].link(1)
                    if u == (i + 1) * m + j:
                        self.grid[i][j].link(2)
                    if u == i * m + j - 1:
                        self.grid[i][j].link(3)

        # marking passages in path:
        for i in range(n):
            for j in range(m):
                u = graph.nodes[i * m + j].nextInPath
                if u == (i - 1) * m + j:
                    self.grid[i][j].markedPassage = 0
                if u == i * m + j + 1:
                    self.grid[i][j].markedPassage = 1
                if u == (i + 1) * m + j:
                    self.grid[i][j].markedPassage = 2
                if u == i * m + j - 1:
                    self.grid[i][j].markedPassage = 3

    def get_str(self) -> [[str]]:
        m = self.width
        n = self.height

        output = []
        output.append(list('┌' + '─┬' * (m - 1) + '─┐'))
        output.append(list('│' + ' │' * (m - 1) + ' │'))
        for i in range(n - 1):
            output.append(list('├' + '─┼' * (m - 1) + '─┤'))
            output.append(list('│' + ' │' * (m - 1) + ' │'))

        output.append(list('└' + ('─┴' * (m - 1)) + '─┘'))

        def remove_wall(wall: str, side: int) -> str:
            rm_above = {'┴': '─', '└': '─', '┘': '─', '┼': '┬', '┤': '┐', '├': '┌', '│': '│'}
            rm_below = {'┬': '─', '┐': '─', '┌': '─', '┼': '┴', '┤': '┘', '├': '└', '│': '│'}
            rm_right = {'┬': '┐', '┌': '│', '┼': '┤', '├': '│', '─': '─', '└': '│', '┴': '┘'}
            rm_left = {'┬': '┌', '┘': '│', '┼': '├', '┤': '│', '─': '─', '┐': '│', '┴': '└'}

            if side == 0:
                if wall in rm_above:
                    return rm_above[wall]
            if side == 1:
                if wall in rm_right:
                    return rm_right[wall]
            if side == 2:
                if wall in rm_below:
                    return rm_below[wall]
            if side == 3:
                if wall in rm_left:
                    return rm_left[wall]
            return wall

        for i in range(n):
            for j in range(m):
                output[2 * i + 1][2 * j + 1] = self.grid[i][j].state
                for direction in self.grid[i][j].get_linked():
                    passageChars = ('^', '>', 'v', '<') if \
                        self.grid[i][j].markedPassage == direction \
                        else (' ', ' ', ' ', ' ')
                    if direction == 0:
                        if output[2 * i][2 * j + 1] not in ('^', '>', 'v', '<'):
                            output[2 * i][2 * j + 1] = passageChars[0]
                        output[2 * i][2 * j + 2] = remove_wall(output[2 * i][2 * j + 2], 3)
                        output[2 * i][2 * j] = remove_wall(output[2 * i][2 * j], 1)
                    if direction == 1:
                        if output[2 * i + 1][2 * j + 2] not in ('^', '>', 'v', '<'):
                            output[2 * i + 1][2 * j + 2] = passageChars[1]
                        output[2 * i + 2][2 * j + 2] = remove_wall(output[2 * i + 2][2 * j + 2], 0)
                        output[2 * i][2 * j + 2] = remove_wall(output[2 * i][2 * j + 2], 2)
                    if direction == 2:
                        if output[2 * i + 2][2 * j + 1] not in ('^', '>', 'v', '<'):
                            output[2 * i + 2][2 * j + 1] = passageChars[2]
                        output[2 * i + 2][2 * j + 2] = remove_wall(output[2 * i + 2][2 * j + 2], 3)
                        output[2 * i + 2][2 * j] = remove_wall(output[2 * i + 2][2 * j], 1)
                    if direction == 3:
                        if output[2 * i + 1][2 * j] not in ('^', '>', 'v', '<'):
                            output[2 * i + 1][2 * j] = passageChars[3]
                        output[2 * i + 2][2 * j] = remove_wall(output[2 * i + 2][2 * j], 0)
                        output[2 * i][2 * j] = remove_wall(output[2 * i][2 * j], 2)
        return output


    def make_turn(self, direction: int) -> bool:
        i, j = self.current_player_pos
        if direction not in self.grid[i][j].get_linked():
            return False

        self.grid[i][j].state = '⦿' if self.current_player_pos == self.path_start else ' '

        if direction == 0:
            i -= 1
        if direction == 1:
            j += 1
        if direction == 2:
            i += 1
        if direction == 3:
            j -= 1

        self.current_player_pos = (i, j)
        self.grid[i][j].state = '⊛'

        if self.current_player_pos == self.path_finish:
            return True

        return False
