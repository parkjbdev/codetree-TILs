from heapq import heappush, heappop


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
                        best = min(best, (-len(result), rot, j, i, result))

        score, rot, y, x, q = best
        score = -score

        if score < 3:
            break

        MAP = rotated(x, y, rot)

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

        turn += 1

    print(*answer)

K, M = map(int, input().split())
MAP = [list(map(int, input().split())) for _ in range(5)]
MS = list(map(int, input().split()))

solution(K, M, MAP, MS)