from GraphNode import Node
import random
from collections import deque


class Graph:
    def __init__(self, size: int) -> None:
        self.path_start = None
        self.path_finish = None
        self.nodes = [Node() for _ in range(size)]
        cnt = 0
        for u in self.nodes:
            u.idx = cnt
            cnt += 1

    def construct_from_rectangle(self, width: int, height: int) -> None:
        m = width
        n = height
        self.__init__(n * m)
        for i in range(n):
            for j in range(m):
                if 0 <= j + 1 < m:
                    self.nodes[m * i + j].adj.append(m * i + j + 1)
                if 0 <= j - 1 < m:
                    self.nodes[m * i + j].adj.append(m * i + j - 1)
                if 0 <= i + 1 < n:
                    self.nodes[m * i + j].adj.append(m * (i + 1) + j)
                if 0 <= i - 1 < n:
                    self.nodes[m * i + j].adj.append(m * (i - 1) + j)

    def construct_from_rectangle_txt(self, txt: [[str]]) -> None:
        m = (len(txt[0]) - 1) // 2
        n = (len(txt) - 1) // 2
        self.__init__(n * m)
        for i in range(n):
            for j in range(m):
                if 0 <= j + 1 < m and txt[2 * i + 1][2 * j + 2] == ' ':
                    self.nodes[m * i + j].adj.append(m * i + j + 1)
                if 0 <= j - 1 < m and txt[2 * i + 1][2 * j] == ' ':
                    self.nodes[m * i + j].adj.append(m * i + j - 1)
                if 0 <= i + 1 < n and txt[2 * i + 2][2 * j + 1] == ' ':
                    self.nodes[m * i + j].adj.append(m * (i + 1) + j)
                if 0 <= i - 1 < n and txt[2 * i][2 * j + 1] == ' ':
                    self.nodes[m * i + j].adj.append(m * (i - 1) + j)

    def make_tree_dfs(self) -> None:
        self._dfs(random.randint(0, len(self.nodes) - 1))
        for v in self.nodes:
            if v.treeParent != -1:
                v.treeSons.append(v.treeParent)
            v.adj = v.treeSons

    def make_tree_bfs(self) -> None:
        self._bfs(random.randint(0, len(self.nodes) - 1))
        for v in self.nodes:
            if v.treeParent != -1:
                v.treeSons.append(v.treeParent)
            v.adj = v.treeSons

    def make_tree_kruskal(self):
        self._kruskal()
        for v in self.nodes:
            v.adj = v.treeSons.copy()
            v.treeSons.clear()
            v.treeParent = -1
            #     to make tree-structure
        self._dfs(random.randint(0, len(self.nodes)))

    def mark_start_and_finish(self, from_: int, to_: int) -> None:
        self.path_start = from_
        self.path_finish = to_

    def mark_path(self, from_: int, to_: int) -> None:
        u = from_
        v = to_
        while u != -1:
            self.nodes[u].inPath = True
            self.nodes[u].nextInPath = self.nodes[u].treeParent
            u = self.nodes[u].treeParent
        while not self.nodes[v].inPath:
            nextNode = self.nodes[v].treeParent
            self.nodes[v].inPath = True
            self.nodes[nextNode].nextInPath = v
            v = nextNode

        v = self.nodes[v].treeParent
        while v != -1:
            self.nodes[v].inPath = False
            self.nodes[v].nextInPath = -1
            v = self.nodes[v].treeParent

    def clear_marks(self) -> None:
        self.path_start = None
        self.path_finish = None
        for u in self.nodes:
            u.inPath = False
            u.nextInPath = -1

    def _dfs(self, v: int) -> None:
        q = deque()
        q.append((v, -1))

        while len(q) != 0:
            v, p = q.popleft()
            if self.nodes[v].visited:
                continue
            self.nodes[v].visited = True
            self.nodes[v].treeParent = p
            if p != -1:
                self.nodes[p].treeSons.append(v)

            random.shuffle(self.nodes[v].adj)
            for u in self.nodes[v].adj:
                if self.nodes[u].visited:
                    continue
                q.appendleft((u, v))

    def _bfs(self, v: int) -> None:
        q = deque()
        q.append(v)
        self.nodes[v].visited = True
        while len(q) != 0:
            v = q.popleft()
            random.shuffle(self.nodes[v].adj)
            for u in self.nodes[v].adj:
                if self.nodes[u].visited:
                    continue
                self.nodes[v].treeSons.append(u)
                self.nodes[u].treeParent = v
                self.nodes[u].visited = True
                q.append(u)

    def _kruskal(self) -> None:
        edges = [(u, v.idx) for v in self.nodes for u in v.adj]
        random.shuffle(edges)
        for v in self.nodes:
            v.set_parent = v.idx
            v.set_size = 1

        # DSU functions:
        def get_set_head(v: int) -> int:
            while self.nodes[v].set_parent != v:
                v = self.nodes[v].set_parent
            return v

        def union(v: int, u: int) -> None:
            if self.nodes[v].set_size < self.nodes[u].set_size:
                v, u = u, v
            self.nodes[u].set_parent = v
            self.nodes[v].set_size += self.nodes[u].set_size

        for u, v in edges:
            head1 = get_set_head(v)
            head2 = get_set_head(u)
            if head2 == head1:
                continue

            self.nodes[u].treeSons.append(v)
            self.nodes[v].treeSons.append(u)
            union(head1, head2)
