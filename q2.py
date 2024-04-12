import random
import time
import heapq
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.adj_list = {}
        self.coordinates = {}

    def add_node(self, node, x, y):
        if node not in self.adj_list:
            self.adj_list[node] = {}
            self.coordinates[node] = (x, y)

    def add_edge(self, src, dest, weight):
        if src not in self.adj_list:
            self.adj_list[src] = {}
        if dest not in self.adj_list:
            self.adj_list[dest] = {}
        self.adj_list[src][dest] = weight
        self.adj_list[dest][src] = weight

def bfs(graph, start_node, end_node):
    visited = set()
    queue = [(start_node, [start_node])]

    while queue:
        node, path = queue.pop(0)
        if node not in visited:
            visited.add(node)
            if node == end_node:
                return path
            for neighbor in graph.adj_list[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

def dfs(graph, start_node, end_node):
    visited = set()

    def dfs_recursive(node, path):
        visited.add(node)
        if node == end_node:
            return path
        for neighbor in graph.adj_list[node]:
            if neighbor not in visited:
                result = dfs_recursive(neighbor, path + [neighbor])
                if result:
                    return result

    return dfs_recursive(start_node, [start_node])

def ucs(graph, start_node, end_node):
    visited = set()
    priority_queue = [(0, start_node, [start_node])]  # (cost, node, path)

    while priority_queue:
        cost, node, path = heapq.heappop(priority_queue)
        if node not in visited:
            visited.add(node)
            if node == end_node:
                return path
            for neighbor, edge_cost in graph.adj_list[node].items():
                if neighbor not in visited:
                    heapq.heappush(priority_queue, (cost + edge_cost, neighbor, path + [neighbor]))

# Benchmark function
def benchmark(graph, algorithm, start_node, end_node, num_trials=5):
    total_time = 0
    for _ in range(num_trials):
        start_time = time.time()
        algorithm(graph, start_node, end_node)
        end_time = time.time()
        total_time += end_time - start_time
    return total_time / num_trials

# Generate random graphs
def generate_random_graph(n, p):
    graph = Graph()
    nodes = [str(i) for i in range(n)]

    for i in range(n):
        x, y = random.uniform(0, 100), random.uniform(0, 100)
        graph.add_node(nodes[i], x, y)

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                weight = random.randint(1, 100)
                graph.add_edge(nodes[i], nodes[j], weight)

    return graph

# Randomly select 10 nodes
def select_random_nodes(graph):
    return random.sample(list(graph.adj_list.keys()), 10)

# Run experiments
graph_sizes = [10, 20, 30, 40]
edge_probs = [0.2, 0.4, 0.6, 0.8]
algorithms = {'BFS': bfs, 'DFS': dfs, 'UCS': ucs}
results = {size: {prob: {algorithm: {'times': [], 'lengths': []} for algorithm in algorithms} for prob in edge_probs} for size in graph_sizes}

for size in graph_sizes:
    for prob in edge_probs:
        print(f"Running experiments for graph size {size} with edge probability {prob}")
        for _ in range(5):
            graph = generate_random_graph(size, prob)
            nodes = select_random_nodes(graph)
            for algorithm in algorithms:
                for i in range(len(nodes)):
                    for j in range(i + 1, len(nodes)):
                        start_node, end_node = nodes[i], nodes[j]
                        time_taken = benchmark(graph, algorithms[algorithm], start_node, end_node)
                        path = algorithms[algorithm](graph, start_node, end_node)
                        if path:
                            length = sum(graph.adj_list[path[k]][path[k+1]] for k in range(len(path) - 1))
                            results[size][prob][algorithm]['times'].append(time_taken)
                            results[size][prob][algorithm]['lengths'].append(length)

# # Plotting
# plt.figure(figsize=(16, 10))

# for i, size in enumerate(graph_sizes, 1):
#     for j, prob in enumerate(edge_probs, 1):
#         for k, algorithm in enumerate(algorithms, 1):
#             plt.subplot(4, 4, (i - 1) * 4 + j)
#             avg_time = sum(results[size][prob][algorithm]['times']) / len(results[size][prob][algorithm]['times'])
#             avg_length = sum(results[size][prob][algorithm]['lengths']) / len(results[size][prob][algorithm]['lengths'])
#             plt.bar(algorithm, avg_time, label=f"Time: {avg_time:.2f}\nLength: {avg_length:.2f}", color='blue')
#             plt.title(f"Graph Size: {size}, Edge Probability: {prob}")
#             plt.ylabel("Average Time")
#             plt.xticks(rotation=45)

# plt.tight_layout()
# plt.show()

for size in graph_sizes:
    for prob in edge_probs:
        plt.figure(figsize=(8, 6))
        for k, algorithm in enumerate(algorithms, 1):
            avg_times = [sum(results[size][prob][algorithm]['times']) / len(results[size][prob][algorithm]['times'])] * len(nodes)
            avg_lengths = [sum(results[size][prob][algorithm]['lengths']) / len(results[size][prob][algorithm]['lengths'])] * len(nodes)
            plt.bar(algorithm, avg_times[0], label=f"Time: {avg_times[0]:.2f}\nLength: {avg_lengths[0]:.2f}", color='blue')
            plt.title(f"Graph Size: {size}, Edge Probability: {prob}")
            plt.ylabel("Average Time")
            plt.xticks(rotation=45)
            plt.tight_layout()
        plt.show()
