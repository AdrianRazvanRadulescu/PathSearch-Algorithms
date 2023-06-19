import sys
from heapq import heappop, heappush
from heuristics import *


import sys
from heapq import heappop, heappush
from heuristics import *

global first_time
def iteration_glds(state, discrepancies, h, visited, limit, end, total_nodes):
    succ = []

    for successor_state in state.get_next_states():
        total_nodes[0] += 1
        if successor_state == end:
            return True

        if successor_state not in visited:
            heappush(succ, (h(successor_state), successor_state))

    if not succ:
        return False

    if len(visited) >= limit:
        return False

    h_best, best = heappop(succ)

    if discrepancies == 0:
        visited.add(best)
        return iteration_glds(best, 0, h, visited, limit, end, total_nodes)
    else:
        while succ:
            h_s, s = heappop(succ)
            visited.add(s)
            check = iteration_glds(s, discrepancies - 1, h, visited, limit, end, total_nodes)
            if check == True:
                return True

        visited.add(best)
        return iteration_glds(best, discrepancies, h, visited, limit, end, total_nodes)

def GLDS(start, h, limit):

    end = start.solved()
    discrepancies = 0
    total_nodes = []
    total_nodes.append(0)

    while True:
        visited = set()
        visited.add(start)
        check = iteration_glds(start, discrepancies, h, visited, limit, end, total_nodes)

        if check:
            print("The algorithm runs as it is supposed to.")
            break

        discrepancies += 1
        print(discrepancies)
        # if discrepancies >= 5:
        #     return (False, 0, 0)

    return check, len(visited), total_nodes[0]