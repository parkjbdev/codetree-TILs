import sys
import os
from collections import deque


def solution(R, C, K, GOLEMS):
    def is_movable(x, y):
        return (
            is_south_movable(x, y) or is_west_rotatable(x, y) or is_east_rotatable(x, y)
        )

    def is_south_movable(x, y):
        nx, ny = x + 1, y
        if nx < -1:
            raise Exception
        elif nx == -1:  # 머리만 체크
            return MAP[nx + 1][ny] == 0  # 머리부분
        else:
            return (
                0 <= nx + 1 < R
                and MAP[nx + 1][ny] == 0  # 머리부분
                and MAP[nx][ny - 1] == 0  # 왼쪽
                and MAP[nx][ny + 1] == 0  # 오른쪽
            )

    def is_west_movable(x, y):
        nx, ny = x, y - 1
        if nx < -2:
            raise Exception
        if ny - 1 < 0:
            return False
        elif nx == -2:
            return True
        elif nx == -1:
            return MAP[nx + 1][ny] == 0  # 왼쪽 (남쪽)
        elif nx == 0:
            return (
                MAP[nx][ny - 1] == 0  # 머리부분 (서쪽)
                and MAP[nx + 1][ny] == 0  # 왼쪽 (남쪽)
            )
        else:
            return (
                MAP[nx][ny - 1] == 0  # 머리부분 (서쪽)
                and MAP[nx + 1][ny] == 0  # 왼쪽 (남쪽)
                and MAP[nx - 1][ny] == 0  # 오른쪽 (북쪽)
            )

    def is_east_movable(x, y):
        nx, ny = x, y + 1
        if nx < -2:
            raise Exception
        if ny + 1 >= C:
            return False
        elif nx == -2:
            return True
        elif nx == -1:
            return MAP[nx + 1][ny] == 0
        elif nx == 0:
            return (
                MAP[nx][ny + 1] == 0  # 머리부분 (동쪽)
                and MAP[nx + 1][ny] == 0  # 오른쪽 (남쪽)
            )
        else:
            return (
                MAP[nx][ny + 1] == 0  # 머리부분 (동쪽)
                and MAP[nx - 1][ny] == 0  # 왼쪽 (북쪽)
                and MAP[nx + 1][ny] == 0  # 오른쪽 (남쪽)
            )

    def is_west_rotatable(x, y):
        return is_west_movable(x, y) and is_south_movable(x, y - 1)

    def is_east_rotatable(x, y):
        return is_east_movable(x, y) and is_south_movable(x, y + 1)

    def move(x, y, d):
        while is_movable(x, y):
            if is_south_movable(x, y):
                x += 1
                print(f"-- Move South: {x}, {y}, {d}")
            elif is_west_rotatable(x, y):
                x += 1
                y -= 1
                d += 3
                d %= 4
                print(f"-- Rotate West: {x}, {y}, {d}")
            elif is_east_rotatable(x, y):
                x += 1
                y += 1
                d += 1
                d %= 4
                print(f"-- Rotate East: {x}, {y}, {d}")

        return x, y, d

    answer = 0
    MAP = [[0] * C for _ in range(R)]
    SCORE = [0 for _ in range(K)]

    dxs = [-1, 0, 1, 0]
    dys = [0, 1, 0, -1]

    for i, golem in enumerate(GOLEMS):
        x, y = -2, golem[0] - 1
        d = golem[1]

        # score_count = True
        print(f"Golem #{i} Start: ({x}, {y}), {d}")
        x, y, d = move(x, y, d)

        # 아직 밖일 경우
        if x - 1 < 0:
            MAP = [[0] * C for _ in range(R)]
            continue

        GOLEMS[i][1] = d

        MAP[x][y] = i + 1
        MAP[x][y - 1] = i + 1
        MAP[x][y + 1] = i + 1
        MAP[x - 1][y] = i + 1
        MAP[x + 1][y] = i + 1

        for ii in range(R):
            if ii == 0:
                print("+" + "--" * (C * 2 - 1) + "-" + "+")
            for jj in range(C):
                if jj == 0:
                    print("|", end="")
                if MAP[ii][jj] == 0:
                    print("   ", end=" ")
                else:
                    print(f"{format(MAP[ii][jj], '03')}", end=" ")
                if jj == C - 1:
                    print("\b|", end="")
            if ii == R - 1:
                print("\n+" + "--" * (C * 2 - 1) + "-" + "+")
            print()

        print(f'Rotation: {["북", "동", "남", "서"][d]}')

        final_score = x + 2

        # bfs
        q = deque()
        q.append((x, y))
        visited = [[False] * C for _ in range(R)]
        visited[x][y] = True

        print("BFS Start.. Final Score:", final_score)
        while q:
            x, y = q.popleft()
            print(x, y)
            if final_score < x + 1:
                print("Score Updated to", x + 1)
                final_score = x + 1

            for i, (dx, dy) in enumerate(zip(dxs, dys)):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < R and 0 <= ny < C):
                    continue
                if visited[nx][ny] or MAP[nx][ny] == 0:
                    continue
                if MAP[nx][ny] == MAP[x][y]:
                    q.append((nx, ny))
                    visited[nx][ny] = True
                else:
                    if GOLEMS[MAP[x][y] - 1][1] == i:
                        q.append((nx, ny))
                        visited[nx][ny] = True

        SCORE[i] = final_score
        answer += final_score

        print(f"Answer added by {final_score} = {answer}")
        print()

    return answer


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, "w")


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


# sys.stdin = open("input33.txt")

R, C, K = map(int, input().split())
GOLEMS = [list(map(int, input().split())) for _ in range(K)]

blockPrint()
result = solution(R, C, K, GOLEMS)
enablePrint()
print(result)