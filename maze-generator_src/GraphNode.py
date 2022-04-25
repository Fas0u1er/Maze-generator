class Node:
    def __init__(self) -> None:
        self.idx = -1
        self.adj = []
        self.visited = False
        self.treeSons = []
        self.treeParent = -1
        self.inPath = False
        self.nextInPath = -1
