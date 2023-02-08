import matplotlib.pyplot as plt
import numpy as np
result_path = ["D:\\Github\\optimization_picking_in_warehouse\\src\\csv\\CSP_(actually_TSP_CPSAT_reference).csv","D:\\Github\\optimization_picking_in_warehouse\\src\\csv\\GA_10_100.csv","D:\\Github\\optimization_picking_in_warehouse\\src\\csv\\Heuristic_10_100_inkali.csv","D:\\Github\\optimization_picking_in_warehouse\\src\\csv\\Nearest_neighbor_10_100.csv"]
#result_path = ["D:\\Github\\optimization_picking_in_warehouse\\src\\csv\\Heuristic_10_100_inkali.csv"]
n_types_of_goods = []
m_shelves = []
success_tests = []
fail_tests = []
run_time = []
minimum_distance = []
N_M = ["N=20,M=10","N=100,M=50","N=200,M=100","N=400,M=200","N=1000,M=500","N=2000,M=1000","N=4000,M=2000"]
#get data
for path in result_path:
    with open(path,"r") as f:
        _n_types_of_goods = []
        _m_shelves = []
        _run_time = []
        _minimum_distance = []
        _number_of_nodes = []
        remove_fails = []
        data = f.readlines()
        data.pop(0)
        for line in data:
            if "No solution" not in line:
                remove_fails.append(line)
        #print(remove_fails)
        for line in remove_fails:
            if "CAN'T" not in line:
                values = line.strip().split(",")
                #print(values)
                _n_types_of_goods.append(int(values[0]))
                _m_shelves.append(int(values[1]))
                _run_time.append(float(values[5]))
                _minimum_distance.append(int(values[4]))
                _number_of_nodes.append(int(values[6]))
            else:
                _n_types_of_goods.append(None)
                _m_shelves.append(None) 
                _run_time.append(None)
                _minimum_distance.append(None)
                _number_of_nodes.append(None)
        n_types_of_goods.append(_n_types_of_goods)
        m_shelves.append(_m_shelves)
        run_time.append(_run_time)
        success_tests.append(len(remove_fails))
        fail_tests.append(len(data) - len(remove_fails))
        minimum_distance.append(_minimum_distance)
minimum_distance[2].append(None)
print(minimum_distance)
#print(n_types_of_goods)
#print(m_shelves)
#N_M_20_10,N_M_100_50,N_M_200_100,N_M_400_200,N_M_1000_500,N_M_2000_1000,N_M_4000_2000 = [],[],[],[],[],[],[]
#for i in range(len(minimum_distance)):
#    N_M_20_10.append(minimum_distance[i][0])
#    N_M_100_50.append(minimum_distance[i][1])
#    N_M_200_100.append(minimum_distance[i][2])
#   N_M_1000_500.append(minimum_distance[i][4])
#    N_M_2000_1000.append(minimum_distance[i][5])
#   N_M_4000_2000.append(minimum_distance[i][6])
CSP,GA,Heuristic,Nea_Neig = minimum_distance[0],minimum_distance[1],minimum_distance[2],minimum_distance[3]

for i in range(CSP.count(None)):
    CSP.remove(None)
    CSP.append(0)
#print(CSP)
for i in range(GA.count(None)):
    GA.remove(None)
    GA.append(0)
for i in range(Nea_Neig.count(None)):
    Nea_Neig.remove(None)
    Nea_Neig.append(0)
for i in range(Heuristic.count(None)):
    Heuristic.remove(None)
    Heuristic.append(0)
#Compare
fig, ax = plt.subplots(figsize = (16,9))
#ax.plot(minimum_distance[0],'-',label = "CSP")
#ax.plot(minimum_distance[1],'-',label = 'GA')
#ax.plot(minimum_distance[2],'-',label = 'Heuristic')
#ax.plot(minimum_distance[3],'-',label = 'Nearest Neighbors')
x = np.arange(len(N_M))
width = 0.2 #The with of the bar
bar1 = ax.bar(x - width/2,CSP,width,label = "CSP",edgecolor = "black")
bar2 = ax.bar(x - width/2 + width,GA,width,label = "GA",edgecolor = "black")
bar3 = ax.bar(x - width/2 + 2*width,Heuristic,width,label = "Heuristic",edgecolor = "black")
bar4 = ax.bar(x - width/2 + 3*width,Nea_Neig,width,label = "Nearest Neighbors",edgecolor = "black")

ax.set_xticks(x + width/2, N_M)
ax.set_xticklabels(N_M)
ax.set_ylabel("p_min")
#ax.set_xlabel("Run Time")
plt.title("Comparing distance between 4 methods")

ax.bar_label(bar1,padding=3)
ax.bar_label(bar2,padding=3)
ax.bar_label(bar3,padding=3)
ax.bar_label(bar4,padding=3)

plt.text(0,2000,"Can't find feasible solution => p_min = 0",fontdict={'color': 'black','size':'15'},bbox = {'edgecolor' : 'red','facecolor':'none'})
plt.legend(loc = "upper left")  
fig.tight_layout()
plt.show()
#plt.savefig("D:/Github/optimization_picking_in_warehouse/src/figures/Comparing_distance_between_4_methods.png")  

    