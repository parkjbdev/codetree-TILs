REST = int(input())
CUST = list(map(int, input().split()))
LDR, MBR = map(int, input().split())

answer = 0
for cust in CUST:
    left = max(0, cust - LDR)
    count = left // MBR + 1
    if left % MBR != 0: count += 1
    answer += count

print(answer)
