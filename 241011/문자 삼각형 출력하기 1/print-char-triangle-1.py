N = int(input())
tri = [[] * N for _ in range(N)]

alphabet = 0

for i in range(N):
    for j in range(i, N):
        tri[j].append(chr(65+alphabet))
        alphabet += 1
        alphabet %= 26

for i in range(N):
    print('  ' * (N - 1 - i), ' '.join(tri[i]), sep='')