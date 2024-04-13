# Utility functions for reading files

class ReadFile:
    def __init__(self):
        pass
    def load_data(self,graph, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():
                    src, dest, weight = line.strip().split()
                    graph.add_edge(src, dest, weight=int(weight))
        return graph