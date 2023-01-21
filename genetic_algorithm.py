import random

def getInput():
    # N: The number of type of product
    # M: The number of shelf
    N, M = [int(i) for i in input().split()]

    # Matrix Q(NxM)
    Q = []
    for i in range(N): # Input N lines (equivalent to N types of product)
        Q.append([int(i) for i in input().split()])

    # Distance matrix
    D = []
    for i in range(M+1): # Input M+1 lines (equivalent to distances between shelf 0,1,2,...,M)
        D.append([int(i) for i in input().split()])

    # Products that need to take
    q = [int(i) for i in input().split()]

    return N, M, Q, D, q

class Individual:
    def __init__(self):
        self.path = []
        self.fitness = 0
    def __lt__(self, other):
        return self.fitness < other.fitness
    def __gt__(self, other):
        return self.fitness > other.fitness

def end(q):
    for p_num in q:
        if p_num != 0:
            return False
    return True

# Return a random number from start and end
def rand_num(start, end):
    return random.randint(start, end - 1)

# Check if a shelf is already traversed
def is_traversed(shelf, path):
    return shelf in path

def create_path(s, Q, q, M, N):
    path = []
    path.append(s) # Append starting location
    q_temp = q.copy()
    while not end(q_temp):
        shelf = rand_num(1, M+1) # Generate random shelf from 1 -> M+1
        if not is_traversed(shelf, path):
            path.append(shelf)
            for i in range(N):
                if q_temp[i] != 0:
                    taken = Q[i][shelf-1] if Q[i][shelf-1] < q_temp[i] else q_temp[i]
                    q_temp[i] -= taken

    path.append(s) # Append ending location
    return path

# Calculate fitness of a path
def cal_fitness(path, D):
    fitness = 0
    for i in range(len(path)):
        fitness += D[path[i-1]][path[i]] # fitness += D[previous_node][current_node]
    return fitness

# Mutated gene: swap two positions
def mutated_swap(ind, D):
    while True:
        r = rand_num(1, len(ind.path) - 1) # First random position (cannot be first or last postion)
        r1 = rand_num(1, len(ind.path) - 1) # Second random position
        if r != r1:
            temp = ind.path[r]
            ind.path[r] = ind.path[r1]
            ind.path[r1] = temp
            break
    ind.fitness = cal_fitness(ind.path, D) # Recalculate fitness value

# Mutated gene: cut from a position and generate a new part
def mutated_add(ind, M, D, q):
    r = rand_num(len(ind.path)//2, len(ind.path) - 1) # Random position to cut (from len//2 -> len-1)
    for s in ind.path[r:]:
        ind.path.remove(s)
     

def traverse_until():
    N, M, Q, D, q = getInput()

    s = 0 # Starting location

    POP_NUM = 3 # The number of individuals
    POPULATION = [] # An array that contains all individuals

    # Create a population of POP_NUM individuals
    for i in range(POP_NUM):
        temp_ind = Individual()
        temp_ind.path = create_path(s, Q, q, M, N)
        temp_ind.fitness = cal_fitness(temp_ind.path, D)
        POPULATION.append(temp_ind)

    POPULATION.sort()

    for i in POPULATION:
        print("------- BREAK -------")
        print(i.path)
        print("FITNESS =", i.fitness)

    mutated_swap(POPULATION[0], D)
    print(POPULATION[0].path)
    print("FITNESS =", POPULATION[0].fitness)

traverse_until()
