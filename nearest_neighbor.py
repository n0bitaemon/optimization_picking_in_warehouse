INT_MAX = 2147483647
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

# Check to see if we have enough products
def end(q, N):
    for i in range(N):
        if(q[i] != 0): return False
    return True

def cal_nearest_shelf(c, D, M, r):
    min_d = INT_MAX
    nearest = -1
    for i in range(M + 1):
        if i not in r and D[c][i] != 0 and min_d > D[c][i]: # condition for nearest shelf
            nearest = i
            min_d = D[c][i]
    return nearest, D[c][nearest]

def nearest_neighbor():
    N, M, Q, D, q = getInput()
    s = 0 # Starting location
    c = s # Current location
    r = [] # Result array
    total = 0 # Total distance moved

    r.append(s) # Append starting location
    print("Start from shelf %d" % s)
    print("Matrix q:", q)

    while end(q, N) == False:
        c, distance = cal_nearest_shelf(c, D, M, r) # Find next shelf to go
        r.append(c)
        print("Go to shelf %d" % c)
        total += distance # Increase distance moved 
        for i in range(N):
            if(q[i] != 0):
                taken = Q[i][c-1] if Q[i][c-1] < q[i] else q[i] # The number of products of type i we will take from the shelf c
                q[i] -= taken
        print("Matrix q:", q)

    r.append(s) # Append ending location
    print("Return to shelf %d" % s)
    total += D[c][s]

    print(r)
    print("Total distance =", total)

nearest_neighbor()
