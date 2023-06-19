from heapq import heappop, heappush

def beam_search(start, B, h, limit):
    beam = set()
    beam.add(start)
    saved_nodes = 0
    visited = set()
    visited.add(start)

    solved = start.solved()

    while beam and len(visited) < limit:
        # succ priority queue de perechi state, h_value resulted from applying h function
        succ = []

        for state in beam:
            for next_state in state.get_next_states():
                saved_nodes += 1

                if next_state == solved:
                    print("Beam search completed.")
                    return_tuple = (True, len(visited), saved_nodes)
                    return return_tuple

                if next_state not in visited:
                    h_value = h(next_state)
                    h_state_pair = h_value, next_state
                    heappush(succ, h_state_pair)

        selected = set()
        for i in range(B):
            if len(succ) == 0:
                break
            h_state_pair = heappop(succ)

            state = h_state_pair[1]
            selected.add(state)

            visited.add(state)


        beam = selected

    print("Beam start didn't complete.")

    return_tuple = (False, len(visited), saved_nodes)
    return return_tuple