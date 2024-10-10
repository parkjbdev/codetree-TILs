DXS = [-1, 0, 1, 0]
DYS = [0, 1, 0, -1]


class Knight:
    def __init__(self, id, x, y, h, w, k):
        self.id = id
        self.x, self.endx = x - 1, x - 1 + h - 1
        self.y, self.endy = y - 1, y - 1 + w - 1
        self.hp = k
        self.damage = 0

    def __str__(self):
        return f"{self.id} ({self.x}, {self.y})~({self.endx}, {self.endy})"

    def move(self, d):
        self.x += DXS[d]
        self.y += DYS[d]
        self.endx += DXS[d]
        self.endy += DYS[d]
        return (self.x, self.y), (self.endx, self.endy)

    def check_movable(self, d, CHESS_MAP, KNIGHT_MAP):
        sx, sy = self.x + DXS[d], self.y + DYS[d]
        ex, ey = self.endx + DXS[d], self.endy + DYS[d]
        L = len(CHESS_MAP)
        # Check in range
        if not (0 <= sx < L and 0 <= sy < L and 0 <= ex < L and 0 <= ey < L): return False

        # Check for wall
        for i in range(sx, ex + 1):
            for j in range(sy, ey + 1):
                if KNIGHT_MAP[i][j] != self and CHESS_MAP[i][j] == 2: return False

        # Check for other knight
        for i in range(sx, ex + 1):
            for j in range(sy, ey + 1):
                if KNIGHT_MAP[i][j] != None and KNIGHT_MAP[i][j] != self:
                    return KNIGHT_MAP[i][j].check_movable(d, CHESS_MAP, KNIGHT_MAP)

        return True

    def count_current_damage(self, CHESS_MAP):
        cnt = 0
        for i in range(self.x, self.endx + 1):
            for j in range(self.y, self.endy + 1):
                if CHESS_MAP[i][j] == 1: cnt += 1
        return cnt

    def lose_damage(self, CHESS_MAP):
        current_damage = self.count_current_damage(CHESS_MAP)
        self.hp -= current_damage
        self.damage += current_damage

        return self.hp


def solution(L, CHESS_MAP, N, KNIGHTS, Q, CMDS):
    # Knight Initialization
    KNIGHT_MAP = [[None] * L for _ in range(L)]
    knights = []

    for id, (r, c, h, w, k) in enumerate(KNIGHTS):
        knight = Knight(id + 1, r, c, h, w, k)
        knights.append(knight)
        for x in range(knight.x, knight.endx + 1):
            for y in range(knight.y, knight.endy + 1):
                KNIGHT_MAP[x][y] = knight

    # Commands
    for cmd in CMDS:
        knight_idx, direction = cmd[0] - 1, cmd[1]
        attacker_knight = knights[knight_idx]
        if attacker_knight is None: continue

        # attacker_knight를 direction 방향으로 1칸 미루기 가능한지 check
        available_to_be_pushed = attacker_knight.check_movable(direction, CHESS_MAP, KNIGHT_MAP)
        if not available_to_be_pushed: continue

        knights_to_be_attacked = set()

        dx, dy = DXS[direction], DYS[direction]
        sx, ex = attacker_knight.x + dx, attacker_knight.endx + dx
        sy, ey = attacker_knight.y + dy, attacker_knight.endy + dy

        while 0 <= sx <= ex < L and 0 <= sy <= ey < L:
            for i in range(sx, ex + 1):
                for j in range(sy, ey + 1):
                    if KNIGHT_MAP[i][j] != attacker_knight and KNIGHT_MAP[i][j] is not None and KNIGHT_MAP[i][j].check_movable(direction, CHESS_MAP, KNIGHT_MAP):
                        knights_to_be_attacked.add(KNIGHT_MAP[i][j])

            sx += dx
            sy += dy
            ex += dx
            ey += dy

        attacker_knight.move(direction)
        for knight_to_be_attacked in knights_to_be_attacked:
            knight_to_be_attacked.move(direction)
            if knight_to_be_attacked.lose_damage(CHESS_MAP) <= 0:
                # killing attacked knight with no hp
                knights[knight_to_be_attacked.id - 1] = None

    return sum(list(map(lambda x: x.damage if x is not None else 0, knights)))


L, N, Q = map(int, input().split())
CHESS_MAP = [list(map(int, input().split())) for _ in range(L)]
KNIGHTS = [list(map(int, input().split())) for _ in range(N)]
CMDS = [list(map(int, input().split())) for _ in range(Q)]

print(solution(L, CHESS_MAP, N, KNIGHTS, Q, CMDS))