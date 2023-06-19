
def out_of_place(puzzle):
    result = 0
    for i in range(puzzle.N - 1):
        if i + 1 != puzzle.r[i]:
            result += 1

    if puzzle.r[puzzle.N - 1] != ' ':
        result += 1

    return result

def manhattan(puzzle):
    sum = 0

    for k in range(puzzle.N):
        i = int(k / puzzle.side)
        j = k % puzzle.side

        if (puzzle.r[k] != ' '):
            solved_i = int((puzzle.r[k] - 1) / puzzle.side)
            solved_j = (puzzle.r[k] - 1) % (puzzle.side)
            distance = abs(solved_i - i) + abs(solved_j - j)
            sum += distance
        else:
            solved_i = puzzle.side - 1
            solved_j = puzzle.side - 1
            distance = abs(solved_i - i) + abs(solved_j - j)
            sum += distance

    return sum