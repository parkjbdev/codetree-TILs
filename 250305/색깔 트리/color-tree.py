from collections import deque
class Node:
    def __init__(self, parent, color, max_depth):
        self.parent = parent
        self.color = color
        self.max_depth = max_depth if parent is None else min(parent.max_depth - 1, max_depth)
        self.children = []
        self.depth = 1 if self.parent is None else self.parent.depth + 1

    def add_child(self, node):
        if self.max_depth == 1: return False
        else:
            self.children.append(node)
            return True

    def change_subtree_color(self, color):
        self.color = color
        # BFS
        q = deque()
        q.extend(self.children)
        
        while q:
            node = q.popleft()
            node.color = color
            q.extend(node.children)

    def get_value(self):
        color = [False] * 5
        color[self.color - 1] = True
        
        q = deque()
        q.extend(self.children)

        while q:
            node = q.popleft()
            color[node.color - 1] = True
            if sum(color) == 5: return 5
            q.extend(node.children)

        return sum(color)

def solution(CMDS):
    TREE_ROOT = None
    nodes = {}

    for cmd in CMDS:
        # 노드 추가
        if cmd[0] == 100:
            id, pid, color, max_depth = cmd[1:]
            if pid == -1:
                nodes[id] = Node(None, color, max_depth)
                TREE_ROOT = nodes[id]
            else:
                nodes[id] = Node(nodes[pid], color, max_depth)
                if not nodes[pid].add_child(nodes[id]):
                    del nodes[id]

        # 색깔 변경 (서브 트리의 모든 노드를 color로 변경)
        elif cmd[0] == 200:
            id, color = cmd[1:]
            nodes[id].change_subtree_color(color)

        elif cmd[0] == 300:
            mid = cmd[1]
            print(nodes[mid].color)

        # 모든 노드들의 가치 제곱의 합
        elif cmd[0] == 400:
            sum = 0
            for node in nodes.values():
                sum += node.get_value() ** 2
            print(sum)

Q = int(input())
CMDS = [list(map(int, input().split())) for _ in range(Q)]
solution(CMDS)