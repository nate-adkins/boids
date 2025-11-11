import csv
import matplotlib.pyplot as plt

file = "data.csv"
flag = "-1"

with open(file, newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)

columns = list(zip(*rows))
columns = columns[1:]

numpy_agents = []
numpy_k = []
numpy_avg = []

lists_agents = []
lists_k = []
lists_avg = []

for column in columns:
    method = column[0]
    agents = column[1]
    k = column[2]

    if agents == flag or k == flag:
        continue

    agents = int(agents)
    k = int(k)
    values = [float(val) for val in column[3:] if val != flag]
    avg = sum(values) / len(values) if values else 0

    if method == "numpy":
        numpy_agents.append(agents)
        numpy_k.append(k)
        numpy_avg.append(avg)
    elif method == "lists":
        lists_agents.append(agents)
        lists_k.append(k)
        lists_avg.append(avg)

numpy_filtered_agents = []
numpy_filtered_avg = []

for a, k, avg in zip(numpy_agents, numpy_k, numpy_avg):
    if a / k == 10:
        numpy_filtered_agents.append(a)
        numpy_filtered_avg.append(avg)

lists_filtered_agents = []
lists_filtered_avg = []

for a, k, avg in zip(lists_agents, lists_k, lists_avg):
    if a / k == 10:
        lists_filtered_agents.append(a)
        lists_filtered_avg.append(avg)

plt.figure(figsize=(10,6))
plt.plot(numpy_filtered_agents, numpy_filtered_avg, marker='o', label='Numpy')
plt.plot(lists_filtered_agents, lists_filtered_avg, marker='s', label='Lists')

plt.xlabel('Number of agents')
plt.ylabel('Average runtime (ms)')
plt.title('Python Lists vs Numpy Vectorization: Boids Iteration Time')
plt.legend()
plt.grid(True)
# plt.yscale('log')
plt.show()
