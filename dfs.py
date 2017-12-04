from graph import Graph
from tree import Tree


def dfs_visit_vertex(graph: Graph, vertex, visited_vertex_map: dict,
                     visited_edges: list or None,
                     visited_vertices: list or set or None):
    visited_vertex_map[vertex] = True
    if visited_vertices is not None:
        if isinstance(visited_vertices, list):
            visited_vertices.append(vertex)
        else:
            visited_vertices.add(vertex)
    for neighbour_vertex in graph.get_vertex_neighbours(vertex):
        visited = visited_vertex_map[neighbour_vertex]
        if not visited:
            if visited_edges is not None:
                visited_edges.append((vertex, neighbour_vertex))
            dfs_visit_vertex(graph, neighbour_vertex, visited_vertex_map,
                             visited_edges, visited_vertices)


def dfs_spanning_tree(graph: Graph, root_vertex) -> Tree:
    if root_vertex not in graph.vertices:
        raise ValueError('Wierzchołek startowy nie należy do grafu.')

    spanning_tree_edges = []
    spanning_tree = None
    visited_vertex_map = {v: False for v in graph.vertices}
    dfs_visit_vertex(graph, root_vertex, visited_vertex_map,
                     visited_edges=spanning_tree_edges,
                     visited_vertices=None)

    spanning_tree_vertices = set()
    for spanning_edge in spanning_tree_edges:
        spanning_tree_vertices.add(spanning_edge[0])
        spanning_tree_vertices.add(spanning_edge[1])

    if spanning_tree_vertices == graph.vertices:
        spanning_tree = Tree(edges=spanning_tree_edges,
                             vertices=spanning_tree_vertices)

    return spanning_tree


def dfs_connected_components(graph: Graph) -> set:
    connected_components = set()
    connected_component_vertices = set()
    visited_vertex_map = {v: False for v in graph.vertices}
    for vertex in visited_vertex_map:
        visited = visited_vertex_map[vertex]
        if not visited:
            dfs_visit_vertex(graph, vertex, visited_vertex_map,
                             visited_edges=None,
                             visited_vertices=connected_component_vertices)
            if not connected_component_vertices:
                connected_component_vertices.add(vertex)
            connected_components.add(frozenset(connected_component_vertices))
            connected_component_vertices = set()

    return connected_components


def is_graph_connected(graph: Graph):
    connected_components = dfs_connected_components(graph)
    return len(connected_components) == 1


if __name__ == '__main__':
    g = Graph.create_from_user_input()
    spanning_tree = dfs_spanning_tree(g, list(g.vertices)[0])
    print('Drzewo spinające: {}'.format(spanning_tree))
    print('Składowe spójności: {}'.format(dfs_connected_components(g)))
    print('Graf spójny: {}'.format(is_graph_connected(g)))
