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

# Check to see if we have taken enough products
def end(q):
    for p_num in q:
        if p_num != 0:
            return False
    return True

# Calculate current q based on current path
def cal_q(path, N,  Q, q):
    for shelf in path: # For each shelf
        if shelf == path[0]: # Skip starting and ending point
            continue
        for i in range(N): # For each type of products
            if q[i] != 0: # If we still need products of type i
                taken = Q[i][shelf-1] if Q[i][shelf-1] < q[i] else q[i]
                q[i] -= taken
    return q


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
    new_ind = Individual()
    new_ind.path = ind.path.copy()
    while True:
        r = rand_num(1, len(new_ind.path) - 1) # First random position (cannot be first or last postion)
        r1 = rand_num(1, len(new_ind.path) - 1) # Second random position
        if r != r1:
            temp = new_ind.path[r]
            new_ind.path[r] = new_ind.path[r1]
            new_ind.path[r1] = temp
            break
    new_ind.fitness = cal_fitness(new_ind.path, D) # Recalculate fitness value
    return new_ind

# Mutated gene: cut from a position and generate a new part
def mutated_cut(ind, M, N, D, Q, q):
    new_ind = Individual()
    new_ind.path = ind.path.copy()

    r = rand_num(len(new_ind.path)//2, len(new_ind.path) - 1) # Random position to cut (from len//2 -> len-1)
    new_ind.path = new_ind.path[:r] # Cut fron position r
    q_temp = q.copy()
    q_temp = cal_q(new_ind.path, N, Q, q_temp) # Recalculate q matrix

    # Generate new path
    while not end(q_temp):
        shelf = rand_num(1, M+1)
        if not is_traversed(shelf, new_ind.path):
            new_ind.path.append(shelf)
            for i in range(N):
                if q_temp[i] != 0:
                    taken = Q[i][shelf-1] if Q[i][shelf-1] < q_temp[i] else q_temp[i]
                    q_temp[i] -= taken

    new_ind.path.append(new_ind.path[0]) # Append ending location
    new_ind.fitness = cal_fitness(new_ind.path, D) # Recalculate fitness value
    return new_ind

# Select the first p_size individuals that have highest fitness value
def select(p, p_size):
    p.sort()
    return p[:p_size]

def print_population(p):
    for i in range(len(p)):
        print("=> INDIVIDUAL %d" % i)
        print(p[i].path)
        print("FITNESS:", p[i].fitness)

def traverse_until():
    N, M, Q, D, q = getInput()

    s = 0 # Starting location
    gen = 1 # Generation number
    gen_thres = 100

    POP_SIZE = 100 # The number of individuals
    population = [] # An array that contains all individuals

    MUTATED_SWAP_PERCENT = 0.5
    MUTATED_ADD_PERCENT = 0.5

    # Create a population of POP_SIZE individuals
    for i in range(POP_SIZE):
        temp_ind = Individual()
        temp_ind.path = create_path(s, Q, q, M, N)
        temp_ind.fitness = cal_fitness(temp_ind.path, D)
        population.append(temp_ind)

    # Loop for gen_thres generations
    while gen <= gen_thres:
        print("-------- GEN %d ---------" % gen)
        # Mutated gene by swapping: 0.5% 
        mutated_swap_num = int(POP_SIZE*MUTATED_SWAP_PERCENT)
        for ind in population[0:mutated_swap_num] :
            new_ind = mutated_swap(ind, D)
            population.append(new_ind)

        # Mutated gene by cutting: 0.5%
        mutated_cut_num = mutated_swap_num + int(POP_SIZE*MUTATED_ADD_PERCENT)
        print("mutated_swap_num=%d, mutated_cut_num=%d" % (mutated_swap_num, mutated_cut_num))
        for ind in population[mutated_swap_num:mutated_cut_num]:
            new_ind = mutated_cut(ind, M, N, D, Q, q)
            population.append(new_ind)
    
        # Crossover gene: x%
        population = select(population, POP_SIZE)
    
        print_population(population)

        gen += 1

    return population[0]

result = traverse_until()
print("--------- RESULT ---------")
print(result.path)
print("FITNESS =", result.fitness)
