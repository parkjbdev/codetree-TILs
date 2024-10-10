from heapq import heappush, heappop, heapify
from math import inf

def solution(CMDS):
    def dijkstra(N, START_VERTEX, EDGES):
        # Distance
        min_distance = [inf for _ in range(N)]
        min_distance[START_VERTEX] = 0

        # Priority Heap: 거리순으로 정렬
        pq = []
        heappush(pq, (min_distance[START_VERTEX], START_VERTEX))

        while pq:
            # 노드 방문
            cost_mid_v, mid_v = heappop(pq)
            if min_distance[mid_v] < cost_mid_v:
                continue

            # 가장 작은 weight 가진 곳으로..
            for next_v, next_c in EDGES[mid_v]:
                cmp_distance = min_distance[mid_v] + next_c
                if cmp_distance < min_distance[next_v]:
                    min_distance[next_v] = cmp_distance
                    heappush(pq, (cmp_distance, next_v))

        return min_distance

    def update_pq(products, costs):
        ret = []
        for id, product in products.items():
            if costs[product["dest"]] < product["revenue"]:
                heappush(ret, (costs[product["dest"]]-  product["revenue"], id))

        return ret

    START_VERTEX = 0
    N = None
    EDGES = None

    min_costs = []
    products = {}
    productq = []

    # For Lazy Calculation
    need_cost_calc = False

    for cmd in CMDS:
        # 코드트리 랜드 건설
        if cmd[0] == 100:
            N, m = cmd[1:3]
            EDGES = [[] for _ in range(N)]
            for i in range(0, m * 3, 3):
                u, v, w = cmd[3 + i:6 + i]
                if u == v: continue
                EDGES[u].append((v, w))
                EDGES[v].append((u, w))
            need_cost_calc = True

        # 여행 상품 생성
        elif cmd[0] == 200:
            id, revenue, dest = cmd[1:]
            products[id] = {"revenue": revenue, "dest": dest}

            if need_cost_calc:
                min_costs = dijkstra(N, START_VERTEX, EDGES)
                productq = update_pq(products, min_costs)
                need_cost_calc = False

            if min_costs[dest] <= revenue:
                heappush(productq, (min_costs[dest] - revenue, id))

        # 여행 상품 취소
        elif cmd[0] == 300:
            id = cmd[1]
            if id in products:
                del products[id]

        # 최적의 여행 상품 판매
        elif cmd[0] == 400:
            if need_cost_calc:
                min_costs = dijkstra(N, START_VERTEX, EDGES)
                productq = update_pq(products, min_costs)
                need_cost_calc = False

            while productq:
                profit, id = heappop(productq)
                if id not in products: continue
                del products[id]
                print(id if profit != inf else -1)
                break
            else: print(-1)

        # 여행 상품의 출발지 변경
        elif cmd[0] == 500:
            START_VERTEX = cmd[1]
            need_cost_calc = True

Q = int(input())  # 명령의 수
CMDS = [list(map(int, input().split())) for _ in range(Q)]
solution(CMDS)