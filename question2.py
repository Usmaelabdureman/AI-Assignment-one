import random
import time
import heapq

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = {}

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
def benchmark(graph, algorithm, start_node, end_node, num_trials=10):
    total_time = 0
    for _ in range(num_trials):
        start_time = time.time()
        algorithm(graph, start_node, end_node)
        end_time = time.time()
        total_time += end_time - start_time
    return total_time / num_trials

# Read graph data from file
def read_graph_from_file(filename):
    graph = Graph()
    with open(filename, 'r') as file:
        for line in file:
            src, dest, weight = line.split()
            weight = int(weight)
            graph.add_edge(src, dest, weight)
    return graph

# Load graph from file
graph = read_graph_from_file("cities_weight_data.txt")

# Randomly picking 10 cities
cities = list(graph.adj_list.keys())
random_cities = random.sample(cities, 10)

# Running benchmarks for each algorithm
print("BFS Benchmark:")
bfs_times = []
for start_city in random_cities:
    for end_city in random_cities:
        if start_city != end_city:
            bfs_time = benchmark(graph, bfs, start_city, end_city)
            bfs_times.append(bfs_time)
print("Average Time:", sum(bfs_times) / len(bfs_times))

print("\nDFS Benchmark:")
dfs_times = []
for start_city in random_cities:
    for end_city in random_cities:
        if start_city != end_city:
            dfs_time = benchmark(graph, dfs, start_city, end_city)
            dfs_times.append(dfs_time)
print("Average Time:", sum(dfs_times) / len(dfs_times))

print("\nUCS Benchmark:")
ucs_times = []
for start_city in random_cities:
    for end_city in random_cities:
        if start_city != end_city:
            ucs_time = benchmark(graph, ucs, start_city, end_city)
            ucs_times.append(ucs_time)
print("Average Time:", sum(ucs_times) / len(ucs_times))
