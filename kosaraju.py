from random import choice

from digraph import Digraph
from dfs import dfs_visit_vertex


def dfs_visit_vertex_kosaraju(graph: Digraph, vertex, visited_vertex_map: dict,
                              visited_edges: list or None,
                              visited_vertices: list):
    for neighbour_vertex in graph.get_vertex_neighbours(vertex):
        visited = visited_vertex_map[neighbour_vertex]
        if not visited:
            visited_vertex_map[neighbour_vertex] = True
            dfs_visit_vertex_kosaraju(graph, neighbour_vertex, visited_vertex_map,
                                      visited_edges, visited_vertices)
    if vertex not in visited_vertices:
        visited_vertices.append(vertex)


def dfs_kosaraju(graph: Digraph, root_vertex, vertex_stack: list, visited_vertex_map: dict):
    if root_vertex not in graph.vertices:
        raise ValueError('Wierzchołek startowy nie należy do grafu.')

    dfs_visit_vertex_kosaraju(graph, root_vertex, visited_vertex_map,
                              visited_edges=None,
                              visited_vertices=vertex_stack)


def kosaraju(graph: Digraph) -> list:
    connected_components = []
    vertex_stack = []  # S
    visited_vertex_map = {v: False for v in graph.vertices}

    while len(vertex_stack) < len(graph.vertices):
        # dfs_vertex = 3
        # dfs_vertex = 0
        dfs_vertex = choice(list(graph.vertices - set(vertex_stack)))
        dfs_kosaraju(graph, dfs_vertex, vertex_stack=vertex_stack,
                     visited_vertex_map=visited_vertex_map)

    #vertex_stack = list(reversed(vertex_stack))
    transposed_graph = graph.transpose()
    visited_vertex_map_t = {v: False for v in transposed_graph.vertices}

    while vertex_stack:
        top_stack_vertex = vertex_stack.pop()
        connected_component = list()
        dfs_kosaraju(transposed_graph, top_stack_vertex, connected_component,
                     visited_vertex_map_t)
        connected_component = set(connected_component)
        connected_components.append(connected_component)

        remaining_edges = [edge for edge in transposed_graph.edges
                           if edge[0] and edge[1] not in connected_component]
        transposed_graph = Digraph(edges=remaining_edges,
                                   vertices=transposed_graph.vertices)
        for component_vertex in connected_component:
            try:
                vertex_stack.remove(component_vertex)
            except ValueError:
                continue

    return connected_components


if __name__ == '__main__':
    test_digraph = Digraph(vertices=set([i for i in range(0, 9)]),
                           edges=[(0, 1), (0, 2), (0, 3),
                                  (3, 4),
                                  (4, 5),
                                  (5, 6), (5, 7), (5, 2),
                                  (6, 3),
                                  (7, 8),
                                  (8, 7)])
    # g = Digraph.create_from_user_input()
    print('Składowe spójności: {}'.format(kosaraju(test_digraph)))
