import random
from collections import deque
from copy import deepcopy

#Undirected graph using an adjacency list
class Graph:

    def __init__(self, n):
        self.adj = {}
        for i in range(n):
            self.adj[i] = []

    def are_connected(self, node1, node2):
        return node2 in self.adj[node1]

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self):
        self.adj[len(self.adj)] = []

    def add_edge(self, node1, node2):
        if node1 not in self.adj[node2]:
            self.adj[node1].append(node2)
            self.adj[node2].append(node1)

    def number_of_nodes():
        return len()


#Breadth First Search
def BFS(G, node1, node2):
    Q = deque([node1])
    marked = {node1 : True}
    for node in G.adj:
        if node != node1:
            marked[node] = False
    while len(Q) != 0:
        current_node = Q.popleft()
        for node in G.adj[current_node]:
            if node == node2:
                return True
            if not marked[node]:
                Q.append(node)
                marked[node] = True
    return False


#Depth First Search
def DFS(G, node1, node2):
    S = [node1]
    marked = {}
    for node in G.adj:
        marked[node] = False
    while len(S) != 0:
        current_node = S.pop()
        if not marked[current_node]:
            marked[current_node] = True
            for node in G.adj[current_node]:
                if node == node2:
                    return True
                S.append(node)
    return False


#Use the methods below to determine minimum Vertex Covers
def add_to_each(sets, element):
    copy = sets.copy()
    for set in copy:
        set.append(element)
    return copy

def power_set(set):
    if set == []:
        return [[]]
    return power_set(set[1:]) + add_to_each(power_set(set[1:]), set[0])

def is_vertex_cover(G, C):
    for start in G.adj:
        for end in G.adj[start]:
            if not(start in C or end in C):
                return False
    return True

def MVC(G):
    nodes = [i for i in range(G.get_size())]
    subsets = power_set(nodes)
    min_cover = nodes
    for subset in subsets:
        if is_vertex_cover(G, subset):
            if len(subset) < len(min_cover):
                min_cover = subset
    return min_cover


# BFS 2
def BFS2(G, node1, node2):
    Q = deque([node1])
    marked = {node1: True}
    predecessor = {node: None for node in G.adj}

    while Q:
        current_node = Q.popleft()
        for neighbor in G.adj[current_node]:
            if not marked.get(neighbor):
                marked[neighbor] = True
                predecessor[neighbor] = current_node
                Q.append(neighbor)
                if neighbor == node2:
                    path = []
                    while node2 is not None:
                        path.append(node2)
                        node2 = predecessor[node2]
                    return path[::-1]

    return []


# DFS 2
def DFS2(G, node1, node2):
    S = [node1]
    marked = {node: False for node in G.adj}
    predecessor = {node: None for node in G.adj}

    while S:
        current_node = S.pop()
        if not marked[current_node]:
            marked[current_node] = True
            for neighbor in G.adj[current_node]:
                if not marked[neighbor]:
                    predecessor[neighbor] = current_node
                    S.append(neighbor)
                    if neighbor == node2:
                        path = []
                        while node2 is not None:
                            path.append(node2)
                            node2 = predecessor[node2]
                        return path[::-1]

    return []


# DFS 3
def DFS3(G, node1):
    S = [node1]
    marked = {node: False for node in G.adj}
    predecessor = {node: None for node in G.adj}

    while S:
        current_node = S.pop()
        if not marked[current_node]:
            marked[current_node] = True
            for neighbor in G.adj[current_node]:
                if not marked[neighbor]:
                    predecessor[neighbor] = current_node
                    S.append(neighbor)

    return predecessor


# BFS 3
def BFS3(G, node1):
    Q = deque([node1])
    marked = {node1: True}
    predecessor = {node: None for node in G.adj}

    while Q:
        current_node = Q.popleft()
        for neighbor in G.adj[current_node]:
            if not marked.get(neighbor):
                marked[neighbor] = True
                predecessor[neighbor] = current_node
                Q.append(neighbor)

    return predecessor


# HAS CYCLE
def has_cycle(G):
    for node in G.adj:
        # Using BFS3 as it gives a predecessor dictionary
        pred = BFS3(G, node)
        visited = {n: False for n in G.adj}

        Q = deque([node])
        while Q:
            current_node = Q.popleft()
            visited[current_node] = True
            for neighbor in G.adj[current_node]:
                if visited[neighbor] and pred[current_node] != neighbor:
                    return True
                if not visited[neighbor]:
                    Q.append(neighbor)
    return False


# IS CONNECTED
def is_connected(G):
    # Arbitrarily choosing a starting node. Let's start with 0
    # BFS3 will give us a predecessor dictionary
    pred = BFS3(G, 0)

    # If any node doesn't have a predecessor and isn't the starting node, the graph isn't connected
    for node, pre in pred.items():
        if pre is None and node != 0:
            return False
    return True


# CREATE RANDOM GRAPH
def create_random_graph(i, j):
    G = Graph(i)

    added_edges = 0
    while added_edges < j:
        # Randomly choose two distinct nodes
        node1, node2 = random.sample(range(i), 2)

        # If the edge doesn't already exist, add it
        if not G.are_connected(node1, node2):
            G.add_edge(node1, node2)
            added_edges += 1

    return G


# VERTEX COVER approx1(G)
def approx1(G):
    C = set()
    G_copy = deepcopy(G)  # Create a copy of the graph so as not to modify the original
    while not is_vertex_cover(G, C):
        v = G_copy.get_highest_degree_vertex()
        C.add(v)
        G_copy.remove_vertex_and_edges(v)
    return C


# VERTEX COVER approx2(G)
def approx2(G):
    C = set()
    G_copy = deepcopy(G)  # Create a copy of the graph so as not to modify the original
    while not is_vertex_cover(G, C):
        v = random.choice(list(G_copy.adj.keys()))
        C.add(v)
    return C


# VERTEX COVER approx3(G)
def approx3(G):
    C = set()
    G_copy = deepcopy(G)  # Create a copy of the graph so as not to modify the original
    while not is_vertex_cover(G, C):
        u, v = G_copy.get_random_edge()
        C.add(u)
        C.add(v)
        G_copy.remove_vertex_and_edges(u)
        G_copy.remove_vertex_and_edges(v)
    return C



# MULTIPLE RUNS
def multiple_runs(n):
    connected_count = 0
    nodes = 100
    edges = 500
    for i in range(n):
        g = create_random_graph(nodes, edges)
        if is_connected(g):
            connected_count += 1

    print("total runs: ", n, "\ntotal connected: ", connected_count, "\npercentage of connected: ", connected_count/n * 100, "%"
          "\nnodes: ", nodes, "edges: ", edges)


multiple_runs(100)