import random, math
from _functools import reduce
from copy import copy
from builtins import isinstance
#from resource import setrlimit, RLIMIT_AS, RLIMIT_DATA

from GLDS import *
from BLDS import *
from astar import *
from heuristics import *
from beam_search import *
from timeit import default_timer as timer



import sys
limit = 2147483647
sys.setrecursionlimit(limit)
#sys.settrace()



def read_problems(file_number):

    side_size = int(file_number[0])

    if side_size == 4:
        limit = 100000
    elif side_size == 5:
        limit = 500000
    elif side_size == 6:
        limit = 1000000

    file_name = "files/problems" + file_number + ".txt"

    print(file_name)

    # f = open("files/problems4-easy.txt", "r")
    f = open(file_name, "r")

    input = f.readlines()
    f.close()
    problems = [NPuzzle.read_from_line(line) for line in input]
    return limit, problems



class NPuzzle:
    """
    Reprezentarea unei stări a problemei și a istoriei mutărilor care au adus starea aici.

    Conține funcționalitate pentru
    - afișare
    - citirea unei stări dintr-o intrare pe o linie de text
    - obținerea sau ștergerea istoriei de mutări
    - obținerea variantei rezolvate a acestei probleme
    - verificarea dacă o listă de mutări fac ca această stare să devină rezolvată.
    """

    NMOVES = 4
    UP, DOWN, LEFT, RIGHT = range(NMOVES)
    ACTIONS = [UP, DOWN, LEFT, RIGHT]
    names = "UP, DOWN, LEFT, RIGHT".split(", ")
    BLANK = ' '
    delta = dict(zip(ACTIONS, [(-1, 0), (1, 0), (0, -1), (0, 1)]))

    PAD = 2

    def __init__(self, puzzle : list[int | str], movesList : list[int] = []):
        """
        Creează o stare nouă pe baza unei liste liniare de piese, care se copiază.

        Opțional, se poate copia și lista de mutări dată.
        """
        self.N = len(puzzle)
        self.side = int(math.sqrt(self.N))
        self.r = copy(puzzle)
        self.moves = copy(movesList)

    def display(self, show = True) -> str:
        l = "-" * ((NPuzzle.PAD + 1) * self.side + 1)
        aslist = self.r

        slices = [aslist[ slice * self.side : (slice+1) * self.side ]  for slice in range(self.side)]
        s = ' |\n| '.join([' '.join([str(e).rjust(NPuzzle.PAD, ' ') for e in line]) for line in slices])

        s = ' ' + l + '\n| ' + s + ' |\n ' + l
        if show: print(s)
        return s
    def display_moves(self):
        print([names[a] if a is not None else None for a in moves])

    def print_line(self):
        return str(self.r)

    @staticmethod
    def read_from_line(line : str):
        list = line.strip('\n][').split(', ')
        numeric = [NPuzzle.BLANK if e == "' '" else int(e) for e in list]
        return NPuzzle(numeric)

    def clear_moves(self):
        """Șterge istoria mutărilor pentru această stare."""
        self.moves.clear()

    def apply_move_inplace(self, move : int):
        """Aplică o mutare, modificând această stare."""
        blankpos = self.r.index(NPuzzle.BLANK)
        y, x = blankpos // self.side, blankpos % self.side
        ny, nx = y + NPuzzle.delta[move][0], x + NPuzzle.delta[move][1]
        if ny < 0 or ny >= self.side or nx < 0 or nx >= self.side: return None
        newpos = ny * self.side + nx
        piece = self.r[newpos]
        self.r[blankpos] = piece
        self.r[newpos] = NPuzzle.BLANK
        #self.moves.append(move)
        return self

    def apply_move(self, move : int):
        """Construiește o nouă stare, rezultată în urma aplicării mutării date."""
        return self.clone().apply_move_inplace(move)

    def solved(self):
        """Întoarce varianta rezolvată a unei probleme de aceeași dimensiune."""
        return NPuzzle(list(range(self.N))[1:] + [NPuzzle.BLANK])

    def verify_solved(self, moves : list[int]) -> bool:
        """"Verifică dacă aplicarea mutărilor date pe starea curentă duce la soluție"""
        return reduce(lambda s, m: s.apply_move_inplace(m), moves, self.clone()) == self.solved()

    def clone(self):
        return NPuzzle(self.r, self.moves)
    def __str__(self) -> str:
        return str(self.N-1) + "-puzzle:" + str(self.r)
    def __repr__(self) -> str: return str(self)
    def __eq__(self, other):
        return self.r == other.r
    def __lt__(self, other):
        return True
    def __hash__(self):
        return hash(tuple(self.r))

    def get_next_states(self):
        next_states = []
        for action in self.ACTIONS:
            next_state = self.apply_move(action)
            if next_state is not None:
                next_states.append(next_state)
        return next_states


def average(list):
    if len(list) == 0:
        return 0

    average = sum(list) / len(list)
    return average

import statistics

def variance(list):
    if len(list) < 2:
        return 0

    mean = average(list)
    res = sum((i - mean) ** 2 for i in list) / (len(list) - 1)
    return res

def run_astar(problems, limit, heuristic):
    succes_time_list = []
    succes_number_of_nodes = []
    succes_path_length = []
    total_solved = 0
    total = 0
    for problem in problems:
        total += 1
        start = timer()
        tuple = astar(problem, heuristic, limit)
        end = timer()

        (check, len_visited, saved_nodes) = tuple
        if check:
            total_solved += 1
            time_function = end - start
            succes_time_list.append(time_function)
            succes_number_of_nodes.append(saved_nodes)
            succes_path_length.append(len_visited)

    print(succes_number_of_nodes)
    print("\n")
    print("Mean time to run algorithm for solved problems:" + str(average(succes_time_list)))
    print("Variance time to run algorithm for solved problems:" + str(variance(succes_time_list)))


    print("\n")
    print("Mean length paths for solved problems: " + str(average(succes_path_length)))
    print("Variance length paths for solved problems: " + str(variance(succes_path_length)))
    print("\n")
    print("Mean saved nodes for solved problems: " + str(average(succes_number_of_nodes)))
    print("Variance saved nodes for solved problems: " + str(variance(succes_number_of_nodes)))
    print("\n")

    print("Percentage of succesful games: " + str(((total_solved / total) * 100)) + ".")


def run_beam_search(problems, limit, B, heuristic):
    succes_time_list = []
    succes_number_of_nodes = []
    succes_path_length = []
    total_solved = 0
    total = 0

    for problem in problems:
        total += 1
        start = timer()
        tuple_beam = beam_search(problem, B, heuristic, limit)
        end = timer()

        (check, len_visited, saved_nodes) = tuple_beam
        if check:
            total_solved += 1
            time_function = end - start
            succes_time_list.append(time_function)
            succes_number_of_nodes.append(saved_nodes)
            succes_path_length.append(len_visited)

    print(succes_number_of_nodes)
    print("\n")
    print("Mean time to run algorithm for solved problems:" + str(average(succes_time_list)))
    print("Variance time to run algorithm for solved problems:" + str(variance(succes_time_list)))


    print("\n")
    print("Mean length paths for solved problems: " + str(average(succes_path_length)))
    print("Variance length paths for solved problems: " + str(variance(succes_path_length)))
    print("\n")
    print("Mean saved nodes for solved problems: " + str(average(succes_number_of_nodes)))
    print("Variance saved nodes for solved problems: " + str(variance(succes_number_of_nodes)))
    print("\n")

    print("Percentage of succesful games: " + str(((total_solved / total) * 100)) + ".")


def run_glds(problems, limit, heuristic):
    succes_time_list = []
    succes_number_of_nodes = []
    succes_path_length = []
    total_solved = 0
    total = 0

    for problem in problems:
        total += 1

        start = timer()
        tuple_glds = GLDS(problem, heuristic, limit)
        end = timer()

        (check, len_visited, saved_nodes) = tuple_glds
        if check:
            total_solved += 1
            time_function = end - start
            succes_time_list.append(time_function)
            succes_number_of_nodes.append(saved_nodes)
            succes_path_length.append(len_visited)

    print(succes_number_of_nodes)
    print("\n")
    print("Mean time to run algorithm for solved problems:" + str(average(succes_time_list)))
    print("Variance time to run algorithm for solved problems:" + str(variance(succes_time_list)))

    print("\n")
    print("Mean length paths for solved problems: " + str(average(succes_path_length)))
    print("Variance length paths for solved problems: " + str(variance(succes_path_length)))
    print("\n")
    print("Mean saved nodes for solved problems: " + str(average(succes_number_of_nodes)))
    print("Variance saved nodes for solved problems: " + str(variance(succes_number_of_nodes)))
    print("\n")

    print("Percentage of succesful games: " + str(((total_solved / total) * 100)) + ".")



def run_blds(problems, limit, B, heuristic):
    succes_time_list = []
    succes_number_of_nodes = []
    succes_path_length = []
    total_solved = 0
    total = 0

    for problem in problems:
        total += 1
        start = timer()
        tuple_blds = BLDS(problem, heuristic, B, limit)
        end = timer()

        (check, len_visited, saved_nodes) = tuple_blds
        if check:
            total_solved += 1
            time_function = end - start
            succes_time_list.append(time_function)
            succes_number_of_nodes.append(saved_nodes)
            succes_path_length.append(len_visited)

    print(succes_number_of_nodes)
    print("\n")
    print("Mean time to run algorithm for solved problems:" + str(average(succes_time_list)))
    print("Variance time to run algorithm for solved problems:" + str(variance(succes_time_list)))


    print("\n")
    print("Mean length paths for solved problems: " + str(average(succes_path_length)))
    print("Variance length paths for solved problems: " + str(variance(succes_path_length)))
    print("\n")
    print("Mean saved nodes for solved problems: " + str(average(succes_number_of_nodes)))
    print("Variance saved nodes for solved problems: " + str(variance(succes_number_of_nodes)))
    print("\n")

    print("Percentage of succesful games: " + str(((total_solved / total) * 100)) + ".")


MLIMIT = 3 * 10 ** 9 # 2 GB RAM limit
#setrlimit(RLIMIT_DATA, (MLIMIT, MLIMIT))



algorithms = ["astar", "beam_search", "glds", "blds"]


# 1 - astar, 2 - beam_search, 3 - glds, 4 - blds
# se seteaza tipul de problema in file_number : "4", "4-easy", "5", "5-easy", etc.
# se alege euristica
# se alege b-ul de la beam search sau bdls

algorithm_number = 4
file_number = "4-easy"
heuristic = out_of_place
B = 50


limit, problems = read_problems(file_number)

if algorithms[algorithm_number - 1] == "blds":
    run_blds(problems, limit, B, heuristic)

if algorithms[algorithm_number - 1] == "astar":
    run_astar(problems, limit, heuristic)

if algorithms[algorithm_number - 1] == "beam_search":
    run_beam_search(problems, limit, B, heuristic)

if algorithms[algorithm_number - 1] == "glds":
    run_glds(problems, limit, heuristic)


