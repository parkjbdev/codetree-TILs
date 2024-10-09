# 고대 문명 유적 탐사
# https://www.codetree.ai/training-field/frequent-problems/problems/ancient-ruin-exploration/description?page=1&pageSize=20

# (1) 유물 1차 획득 가치를 최대화
# (2) 회전한 각도가 가장 작은 방법을 선택합니다.
# (3) 회전 중심 좌표의 열이 가장 작은 구간을, 그리고 열이 같다면 행이 가장 작은 구간을 선택합니다.

from heapq import heappush, heappop


def print2(arr):
    print(*arr, sep="\n")


def solution(K, M, MAP, MS):
    def rotated(x, y, n=1):
        def _rotate(x, y, arr):
            # fmt: off
            return list(map(list, zip(*[row for row in arr][::-1])))

        subrot = [row[y - 1 : y + 2] for row in MAP[x - 1 : x + 2]]
        for _ in range(n):
            subrot = _rotate(x, y, subrot)

        ret = [row.copy() for row in MAP]
        for i in range(3):
            for j in range(3):
                ret[i + x - 1][j + y - 1] = subrot[i][j]

        return ret

    def search_treasure(map):
        treasures = []
        visited = [[False] * 5 for _ in range(5)]
        for i in range(5):
            for j in range(5):
                result = bfs(i, j, map, visited, map[i][j])
                if len(result) >= 3:
                    for x, y in result:
                        heappush(treasures, (y, -x))

        return treasures

    def bfs(x, y, map, visited, search_for):
        if visited[x][y]:
            return []

        dx = [-1, 0, 0, 1]
        dy = [0, -1, 1, 0]

        q = []
        heappush(q, (x, y))
        visited[x][y] = True

        # TODO
        ret = []

        while q:
            x, y = heappop(q)
            heappush(ret, (x, y))
            for ddx, ddy in zip(dx, dy):
                nx, ny = x + ddx, y + ddy
                if not 0 <= nx < 5 or not 0 <= ny < 5:
                    continue
                if visited[nx][ny]:
                    continue
                if map[nx][ny] == search_for:
                    heappush(q, (nx, ny))
                    visited[nx][ny] = True

        return ret

    answer = []
    turn = 0
    next_idx = 0

    while turn < K:
        # finding the best rotation
        best = (0, 3, 4, 4, [])
        for i in range(1, 4):
            for j in range(1, 4):
                for rot in range(4):
                    ROTMAP = rotated(i, j, rot)
                    result = search_treasure(ROTMAP)
                    if len(result) >= 3:
                        best = min(best, (-len(result), rot, i, j, result))

        score, rot, x, y, q = best
        score = -score

        if score < 3:
            break

        # print()
        # print("best(score, rot, x, y, q): ", score, rot, x, y, q)
        MAP = rotated(x, y, rot)
        # print2(MAP)

        answer.append(0)
        answer[turn] += score

        while next_idx < len(MS):
            while q:
                j, i = heappop(q)
                i = -i
                MAP[i][j] = MS[next_idx]
                next_idx += 1

            q = search_treasure(MAP)
            if len(q) < 3:
                break
            answer[turn] += len(q)

            # print("combo", q)
            # print2(MAP)

        turn += 1

    print(*answer)


# K, M = 2, 20
# MAP = [
#     list(map(int, "7 6 7 6 7".split())),
#     list(map(int, "6 7 6 7 6".split())),
#     list(map(int, "6 7 1 5 4".split())),
#     list(map(int, "7 6 3 2 1".split())),
#     list(map(int, "5 4 3 2 7".split())),
# ]
# MS = list(map(int, "3 2 3 5 2 4 6 1 3 2 5 6 2 1 5 6 7 1 2 3".split()))
# K, M = 1, 18
# MAP = [
#     [3, 5, 6, 7, 3],
#     [7, 7, 5, 7, 4],
#     [2, 6, 1, 5, 2],
#     [2, 7, 2, 7, 5],
#     [6, 2, 6, 7, 6],
# ]
# MS = [5, 2, 4, 3, 1, 5, 5, 1, 1, 7, 3, 5, 7, 4, 3, 5, 4, 2]

# K, M = 9, 52
# MAP = [
#     [6, 7, 5, 5, 7],
#     [3, 7, 3, 6, 2],
#     [7, 2, 3, 2, 1],
#     [3, 6, 7, 1, 5],
#     [1, 5, 5, 2, 1],
# ]
# # fmt: off
# MS = [3,1,5,4,6,3,3,6,5,3,3,6,3,4,3,1,1,2,3,1,3,4,2,4,1,1,4,4,1,1,4,4,2,3,4,6,6,3,6,2,2,2,4,3,1,3,1,5,4,5,6,4]
K, M = map(int, input().split())
MAP = [list(map(int, input().split())) for _ in range(5)]
MS = list(map(int, input().split()))

solution(K, M, MAP, MS)