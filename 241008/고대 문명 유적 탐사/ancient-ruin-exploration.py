# 고대 문명 유적 탐사
# https://www.codetree.ai/training-field/frequent-problems/problems/ancient-ruin-exploration/description?page=1&pageSize=20

# (1) 유물 1차 획득 가치를 최대화
# (2) 회전한 각도가 가장 작은 방법을 선택합니다.
# (3) 회전 중심 좌표의 열이 가장 작은 구간을, 그리고 열이 같다면 행이 가장 작은 구간을 선택합니다.

from heapq import heappop as pop, heappush as push


def print2d(arr):
    print(*arr, sep="\n")


def solution(K, M, MAP, MS):
    best = (0, 0, 0, 0, 0)

    for i in range(1, 4):
        for j in range(1, 4):
            for rotate_cnt in range(4):
                MAP.init_visit()
                ts = MAP.treasure_coords()
                best = min(best, (-len(ts), rotate_cnt, i, j, ts))
                MAP.rotate(i, j)

    score, r, rx, ry, ts = best
    score = -score
    MAP.rotate(rx, ry, r)

    # fill up
    itercnt=  0
    mscnt = 0
    ans = 0

    while mscnt < M and itercnt < K:
        ans += len(ts)
        while ts:
            (y, x) = pop(ts)
            x = -x
            MAP.set(x, y, MS[mscnt])
            mscnt += 1

        MAP.init_visit()
        ts = MAP.treasure_coords()
        itercnt += 1
    ans += len(ts)
    print(ans)


class TreasureMap:
    def __init__(self, MAP):
        self.MAP = MAP

    def rotate(self, x, y, n=1):
        ROTATED = [self.MAP[i][y - 1 : y + 2] for i in range(x - 1, x + 2)]

        for i in range(n):
            ROTATED = [x for x in map(list, zip(*ROTATED[::-1]))]

        for i in range(0, 3):
            for j in range(0, 3):
                self.MAP[x - 1 + i][y - 1 + j] = ROTATED[i][j]

    def init_visit(self):
        self.visited = [[False] * 5 for _ in range(5)]

    def set(self, x, y, value):
        self.MAP[x][y] = value

    def bfs(self, x, y):
        from collections import deque

        q = deque([(x, y)])
        history = []
        dxs = [0, 0, 1, -1]
        dys = [1, -1, 0, 0]

        if self.visited[x][y]:
            return history

        self.visited[x][y] = True

        while q:
            cand = q.popleft()
            push(history, (cand[1], -cand[0]))

            for dx, dy in zip(dxs, dys):
                newx, newy = cand[0] + dx, cand[1] + dy
                if not 0 <= newx < 5 or not 0 <= newy < 5:
                    continue
                if self.visited[newx][newy]:
                    continue
                if self.MAP[x][y] == self.MAP[newx][newy]:
                    q.append((newx, newy))
                    self.visited[newx][newy] = True

        return history

    def treasure_coords(self):
        treasures = []

        self.init_visit()
        for i in range(5):
            for j in range(5):
                treasure = MAP.bfs(i, j)
                if len(treasure) >= 3:
                    for t in treasure:
                        push(treasures, t)

        return treasures


# K, M = 2, 20
# MAP = TreasureMap([
#     list(map(int, "7 6 7 6 7".split())),
#     list(map(int, "6 7 6 7 6".split())),
#     list(map(int, "6 7 1 5 4".split())),
#     list(map(int, "7 6 3 2 1".split())),
#     list(map(int, "5 4 3 2 7".split())),
# ])
# MS = list(map(int, "3 2 3 5 2 4 6 1 3 2 5 6 2 1 5 6 7 1 2 3".split()))
K, M = map(int, input().split())
MAP = [list(map(int, input().split())) for _ in range(5)]
MS = list(map(int, input().split()))

solution(K, M, MAP, MS)