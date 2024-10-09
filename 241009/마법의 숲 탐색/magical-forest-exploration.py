# R, C: 숲의 크기
# K: 정령의 수
# c_i: 골렘이 출발하는 열
# d_i: 골렘의 출구방향 정보

# 탐색 우선순위
# 1) 남쪽으로 한칸
# 2) 서쪽으로 회전 (서쪽으로 한칸, 남쪽으로 한칸, 출구 반시계방향 회전)
# 3) 동쪽으로 회전 (동쪽으로 한칸, 남쪽으로 한칸, 출구 시계방향 회전)
# 4) 가장 남쪽에 도달하여 더이상 이동할수 없을경우, 상하좌우 인접칸 이동..
# 단, 현재 골렘의 출구가 다른 골렘과 인접 시, 해당 출구를 통해 다른 골렘으로 이동가능

# 정령이 이동할 수 있는 가장 남쪽칸의 총합

# 만약 골렘이 최대한 남쪽으로 이동했지만 골렘의 몸 일부가 여전히 숲을 벗어난 상태라면,
# 해당 골렘을 포함해 숲에 위치한 모든 골렘들은 숲을 빠져나간 뒤
# 다음 골렘부터 새롭게 숲의 탐색을 시작합니다.
# 단, 이 경우에는 정령이 도달하는 최종 위치를 답에 포함시키지 않습니다.

# 북, 동, 남, 서
# 0, 1, 2, 3
import sys
import os


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

    answer = 0
    MAP = [[0] * C for _ in range(R)]
    SCORE = [0 for _ in range(K)]

    for i, golem in enumerate(GOLEMS):
        x, y = -2, golem[0] - 1
        d = golem[1]

        movable = is_movable(x, y)

        print(f"Golem #{i} Start: {x}, {y}, {d}")
        print(f"First Movability Test: {movable}")

        if not movable:
            MAP = [[0] * C for _ in range(R)]

        # 내려갈수 있는지 판단
        print("***** Start of while loop *****")
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
            print("  *** loop ***   ")
        print("***** End of while loop *****")

        GOLEMS[i][1] = d

        MAP[x][y] = i + 1
        MAP[x][y - 1] = i + 1
        MAP[x][y + 1] = i + 1
        MAP[x - 1][y] = i + 1
        MAP[x + 1][y] = i + 1

        print(*MAP, sep="\n")

        print(f'Rotation: {["북", "동", "남", "서"][d]}')

        final_score = x + 2
        if d == 0:
            x -= 1
            if MAP[x][y - 1] != 0:
                final_score = max(final_score, SCORE[MAP[x][y - 1] - 1])
            if MAP[x - 1][y] != 0:
                final_score = max(final_score, SCORE[MAP[x - 1][y] - 1])
            if MAP[x][y + 1] != 0:
                final_score = max(final_score, SCORE[MAP[x][y + 1] - 1])
        elif d == 1:
            y += 1
            if MAP[x - 1][y] != 0:
                final_score = max(final_score, SCORE[MAP[x - 1][y] - 1])
            if y + 1 < C and MAP[x][y + 1] != 0:
                final_score = max(final_score, SCORE[MAP[x][y + 1] - 1])
            if MAP[x + 1][y] != 0:
                final_score = max(final_score, SCORE[MAP[x + 1][y] - 1])
        elif d == 2:
            x += 1
            if MAP[x][y - 1] != 0:
                final_score = max(final_score, SCORE[MAP[x][y - 1] - 1])
            if x + 1 < R and MAP[x + 1][y] != 0:
                final_score = max(final_score, SCORE[MAP[x + 1][y] - 1])
            if MAP[x][y + 1] != 0:
                final_score = max(final_score, SCORE[MAP[x][y + 1] - 1])
        elif d == 3:
            y -= 1
            if MAP[x - 1][y] != 0:
                final_score = max(final_score, SCORE[MAP[x - 1][y] - 1])
            if y - 1 >= 0 and MAP[x][y - 1] != 0:
                final_score = max(final_score, SCORE[MAP[x][y - 1] - 1])
            if MAP[x + 1][y] != 0:
                final_score = max(final_score, SCORE[MAP[x + 1][y] - 1])

        SCORE[i] = final_score
        if movable:
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


# TestCase 1
# blockPrint()
# test1 = solution(6, 5, 6, [[2, 3], [2, 0], [4, 2], [2, 0], [2, 0], [2, 2]])
# print(test1)

# TestCase 2
# blockPrint()
# test2 = solution(7, 9, 6, [[4, 1], [5, 1], [2, 1], [8, 1], [2, 2], [6, 0]])
# enablePrint()
# print(test2)

R, C, K = map(int, input().split())
GOLEMS = [list(map(int, input().split())) for _ in range(K)]
blockPrint()
result = solution(R, C, K, GOLEMS)
enablePrint()
print(result)