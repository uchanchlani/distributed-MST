
import sys
# coding: utf-8

# ## Generate graph
from random import randint


# V = input()
# E = input()
def generate_graph(V,E):
    print(f'generating graph with vertices: {V} and edges: {E}')
    weight_pool = generate_weight_pool(E)
    # print(f'weight pool: {weight_pool}')

    graph = {}
    nodes = [0]
    len_edges = 0

    # Picks a random node from previous nodes and connects to it.
    # Picks up a random index from weight_pool and chooses as the weight of 
    #  edge to previous generated node.
    # Add these <node, edge> pair to graph
    for v in range(1, V):
        pv = randint(0, len(nodes)-1)
        w_ind = randint(0, len(weight_pool)-1)
        nodes.append(v)
        if v not in graph:
            graph[v] = {}
        if pv not in graph:
            graph[pv] = {}
        graph[v][pv] = weight_pool[w_ind]
        graph[pv][v] = weight_pool[w_ind]
        # print(f'{v} -> {pv}: {weight_pool[w_ind]}')
        del weight_pool[w_ind]
        len_edges += 1

    # print('Generate extra edges')
    # restricting number of edges to fully connected graph
    while len_edges < min(E, V*(V-1)/2):
        u_ind = v_ind = 0
        while u_ind == v_ind or nodes[v_ind] in graph[nodes[u_ind]]:
            u_ind = randint(0, len(nodes)-1)
            v_ind = randint(0, len(nodes)-1)
        w_ind = randint(0, len(weight_pool)-1)
        u = nodes[u_ind]
        v = nodes[v_ind]
        graph[u][v] = weight_pool[w_ind]
        graph[v][u] = weight_pool[w_ind]
        # print(f'{v} -> {u}: {weight_pool[w_ind]}')
        del weight_pool[w_ind]
        len_edges += 1

    # print(f'Graph: \n{graph}')
        
    # write graph to file
    grp_file = f'graph_{V}_{E}_input'
    f_writer = open(grp_file, 'w')
    f_writer.write(f'{str(V)}\n')
    for v in range(0,V):
        for u,w in graph[v].items():
            f_writer.write(f'{str(u)} {str(w)} ')
        f_writer.write('\n')
    f_writer.close()

def generate_weight_pool(E):
    start = randint(1, 300)
    end = start + randint(5, 10)*E
    weight_pool = [x for x in range(start, end)]
    return weight_pool

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("V and E missing")
        sys.exit(1)

    V = int(sys.argv[1])
    E = int(sys.argv[2])
    generate_graph(V, E)

