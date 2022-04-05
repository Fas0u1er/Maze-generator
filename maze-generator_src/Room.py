class Room:
    states = ('*', '⦿', '⊛')

    def __init__(self, adj_size: int) -> None:
        self.hasPassage = [False for _ in range(adj_size)]
        self.state = ' '
        # ' ' - empty room, '*' - path goes here, '⦿' - start/finish, '⊛' - you are here
        self.markedPassage = None

    def get_linked(self) -> list:
        return [i for i in range(len(self.hasPassage)) if self.hasPassage[i]]

    def link(self, idx: int) -> None:
        self.hasPassage[idx] = True

    def unlink(self, idx: int) -> None:
        self.hasPassage[idx] = False
