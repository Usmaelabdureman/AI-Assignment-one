
from collections import deque
from heapq import heappush, heappop
class Search:
    def __init__(self) -> None:
        pass

    def dfs(self, graph, start, end):
        stack = [start]
        visited = set([start])
        path = {start: None}

        while stack:
            curr = stack.pop()
            if curr == end:
                break

            for neighbor in graph.get_neighbors(curr):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
                    path[neighbor] = curr

        return self.reconstruct_path(path, start, end)
#  dfs with recursion
    def dfs_recur(self, graph, start, end, visited=set(), path=None):
        if start == end:
            return self.reconstruct_path(path, start, end)
        for neighbor in graph.get_neighbors(start):
            if neighbor not in visited:
                visited.add(neighbor)
                path[neighbor] = start
                route = self.dfs_recur(graph, neighbor, end, visited, path)
                if route:
                    return route
        return None

    def reconstruct_path(self, path, start, end):

        if end not in path:
            return None
        step = end
        route = []
        while step is not None:
            route.append(step)
            step = path[step]
        route.reverse()
        return route if route[0] == start else None
    
    def bfs(self,graph, start, end):
  
        queue = deque([start])
        visited = set([start])
        path = {start: None}

        while queue:
            curr = queue.popleft()
            if curr == end:
                break

            for neighbor in graph.get_neighbors(curr):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    path[neighbor] = curr
        return self.reconstruct_path(path, start, end)
    
    # def ucs(self,graph, start, goal):
    #     priority_queue = []
    #     heappush(priority_queue, (0, start, [start]))  # (current_cost, current_node, path)
    #     visited = set()

    #     while priority_queue:
    #         current_cost, current_node, path = heappop(priority_queue)

    #         if current_node in visited:
    #             continue
    #         visited.add(current_node)

    #         if current_node == goal:
    #             return path, current_cost

    #         for neighbor, cost in graph.get_neighbors(current_node).items():
    #             if neighbor not in visited:
    #                 heappush(priority_queue, (current_cost + cost, neighbor, path + [neighbor]))

    #     return None, None  
