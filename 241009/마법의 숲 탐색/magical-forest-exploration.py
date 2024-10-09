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

    def move(x, y, d):
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

        return x, y, d


    answer = 0
    MAP = [[0] * C for _ in range(R)]
    SCORE = [0 for _ in range(K)]

    for i, golem in enumerate(GOLEMS):
        x, y = -2, golem[0] - 1
        d = golem[1]

        score_count = True
        print(f"Golem #{i} Start: {x}, {y}, {d}")
        x, y, d = move(x, y, d)

        # 아직 밖일 경우
        if x - 1 < 0:
            print("MAP FULL!!!")
            score_count = False
            MAP = [[0] * C for _ in range(R)]
            x, y, d = -2, golem[0] - 1, golem[1]
            x, y, d = move(x, y, d)


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
        if score_count:
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
# test1 = solution(6, 5, 6, [[2, 3], [2, 0], [4, 2], [2, 0], [2, 0], [2, 2]])
# print(test1)

# # TestCase 2
# blockPrint()
# test2 = solution(7, 9, 6, [[4, 1], [5, 1], [2, 1], [8, 1], [2, 2], [6, 0]])
# enablePrint()
# print(test2)

# R, C, K = 6, 7, 11
# GOLEMS = [
#     [3, 0],
#     [4, 0],
#     [2, 2],
#     [6, 2],
#     [6, 1],
#     [5, 0],
#     [5, 2],
#     [5, 3],
#     [6, 2],
#     [5, 0],
#     [4, 1],
# ]

R, C, K = map(int, input().split())
GOLEMS = [list(map(int, input().split())) for _ in range(K)]

blockPrint()
result = solution(R, C, K, GOLEMS)
enablePrint()
print(result)