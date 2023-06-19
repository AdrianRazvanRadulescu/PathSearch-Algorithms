from heapq import heappop, heappush
from heuristics import *

def astar(start, h, limit):
    frontier = []

    end = start.solved()

    heappush(frontier, (0 + h(start), start))

    visited = {start: (None, 0)}
    saved_nodes = 1

    while frontier:
        current_cost, curr_state = heappop(frontier)
        current_depth = visited[curr_state][1]

        if curr_state == end:
            print("A star search completed.")
            return_tuple = (True, len(visited), saved_nodes)
            return return_tuple

        for next_state in curr_state.get_next_states():
            next_state_depth = current_depth + 1
            saved_nodes += 1

            if next_state not in visited:
                visited[next_state] = (curr_state, next_state_depth)
                if len(visited) > limit:
                    print("Limit of " + str(limit) + " has been reached.")
                    return_tuple = (False, len(visited), saved_nodes)
                    return return_tuple
                heappush(frontier, (next_state_depth + h(next_state), next_state))

    return_tuple = (False, len(visited), saved_nodes)
    return return_tuple
