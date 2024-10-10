max1, w1 = map(int, input().split())
max2, w2 = map(int, input().split())
max3, w3 = map(int, input().split())

maxs = [max1, max2, max3]
ws = [w1, w2, w3]

for i in range(100):
    s = i % 3
    n = (s + 1) % 3

    togo = min(ws[s], maxs[n] - ws[n])
    ws[s] -= togo
    ws[n] += togo

print(*ws, sep='\n')