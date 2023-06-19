from heapq import heappop, heappush

def iteration_blds(level, discrepancies, B, h, visited, limit, end, total_nodes):
    succ = []

    for state in level:
        for s in state.get_next_states():
            total_nodes[0] += 1
            if s == end:
                return True

            if s not in visited:
                succ.append((h(s), s))

    if not succ:
        return False

    if (len(visited) + min(B, len(succ))) > limit:
        return False

    succ.sort()

    if discrepancies == 0:
        next_level = set()
        for i in range(B):
            if i == len(succ):
                break

            next_level.add(succ[i][1])

        visited.update(next_level)
        return iteration_blds(next_level, 0, B, h, visited, limit, end, total_nodes)

    else:
        already_explored = B
        while already_explored < len(succ):
            n = min(len(succ) - already_explored, B)

            next_level = set()

            for i in range(already_explored, n + already_explored):
                next_level.add(succ[i][1])

            visited.update(next_level)
            val = iteration_blds(next_level, discrepancies - 1, B, h, visited, limit, end, total_nodes)
            if val == True:
                return val

            already_explored += len(next_level)

        next_level = set()
        for i in range(B):
            if i < len(succ):
                next_level.add(succ[i][1])
        visited.update(next_level)

        return iteration_blds(next_level, discrepancies, B, h, visited, limit, end, total_nodes)



def BLDS(start, h, B, limit):

    end = start.solved()
    discrepancies = 0
    total_nodes = []
    total_nodes.append(0)
    while True:
        visited = set()
        visited.add(start)
        check = iteration_blds({start}, discrepancies, B, h, visited, limit, end, total_nodes)
        if check == True:
            print("BLDS solved the problem.")
            return True, len(visited), total_nodes[0]

        discrepancies += 1
        print(discrepancies)
        if discrepancies == 5:
            return False, len(visited), total_nodes[0]