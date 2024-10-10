N = int(input())
tri = [[] * N for _ in range(N)]

alphabet = 0

for i in range(N):
    for j in range(i, N):
        tri[j].append(chr(65+alphabet))
        alphabet += 1
        alphabet %= 26

for i in range(N):
    res = '  ' * (N - 1 - i)
    if len(res) == 0: print(*tri[i])
    else: print(res, ' '.join(tri[i]), sep='')