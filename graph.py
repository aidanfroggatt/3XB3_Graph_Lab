import random
from collections import deque
from copy import deepcopy
import matplotlib.pyplot as plt

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

    # Fixed number_of_nodes by adding self parameter and taking length of self adjacency list
    def number_of_nodes(self):
        return len(self.adj)


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
    # Changed G.getSize() to G.number_of_nodes()
    nodes = [i for i in range(G.number_of_nodes())]
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


def approx1(G):
    C = []
    G_copy = deepcopy(G)

    while True:
        # Step 2: Find the vertex with the highest degree in G_copy
        v = max(G_copy.adj, key=lambda k: len(G_copy.adj[k]))

        # Step 3: Add v to C
        C.append(v)

        # Step 4: Remove all edges incident to node v from G_copy
        for neighbor in G_copy.adj[v]:
            G_copy.adj[neighbor].remove(v)
        G_copy.adj[v] = []

        # Step 5: If C is a Vertex Cover return C
        if is_vertex_cover(G, C):
            return C


def approx2(G):
    C = []
    G_copy = deepcopy(G)
    nodes = list(G_copy.adj.keys())

    while True:
        # Step 2: Select a vertex randomly from G_copy which is not already in C
        v = random.choice([node for node in nodes if node not in C])

        # Step 3: Add v to C
        C.append(v)

        # Step 4: If C is a Vertex Cover return C
        if is_vertex_cover(G, C):
            return C


def approx3(G):
    C = []
    G_copy = deepcopy(G)

    while True:
        # Step 2: Select an edge randomly from G_copy
        edges = [(node, neighbor) for node in G_copy.adj for neighbor in G_copy.adj[node]]
        if not edges:
            break
        u, v = random.choice(edges)

        # Step 3: Add u and v to C
        if u not in C:
            C.append(u)
        if v not in C:
            C.append(v)

        # Step 4: Remove all edges incident to u or v from G_copy
        for neighbor in G_copy.adj[u]:
            G_copy.adj[neighbor].remove(u)
        G_copy.adj[u] = []
        for neighbor in G_copy.adj[v]:
            G_copy.adj[neighbor].remove(v)
        G_copy.adj[v] = []

        # Step 5: If C is a Vertex Cover return C
        if is_vertex_cover(G, C):
            return C


def is_independent_set(G, S):
    for v in S:
        for u in S:
            if G.are_connected(v, u):
                return False
    return True


def MIS(G):
    nodes = [i for i in range(G.number_of_nodes())]
    subsets = power_set(nodes)
    max_independent_set = []
    for subset in subsets:
        if is_independent_set(G, subset):
            if len(subset) > len(max_independent_set):
                max_independent_set = subset
    return max_independent_set



# MULTIPLE RUNS
def multiple_runs(n):
    nodes, edges = 8, 15
    mvc_sum, a1_sum, a2_sum, a3_sum = 0, 0, 0, 0
    for i in range(n):
        for i in range(1000):
            g = create_random_graph(nodes, edges)
            mvc_sum += len(MVC(g))
            a1_sum += len(approx1(g))
            a2_sum += len(approx2(g))
            a3_sum += len(approx3(g))
#     display the average size of the minimum vertex cover and the average size of the approximations
    print("Average size of the minimum vertex cover: ", mvc_sum / n)
    print("Average size of the approximation 1: ", a1_sum / n)
    print("Average size of the approximation 2: ", a2_sum / n)
    print("Average size of the approximation 3: ", a3_sum / n)
#     display the number of nodes and edges in the graph
    print("Number of nodes: ", nodes)
    print("Number of edges: ", edges)


multiple_runs(100)
