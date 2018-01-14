from enum import Enum
from typing import Set, Tuple

from graph import Graph
from directed_network import DirectedNetwork
from edmonds_karp import edmonds_karp


class VertexColour(Enum):
    RED = 0
    BLUE = 1

    def opposite_colour(self):
        if self == VertexColour.RED:
            return VertexColour.BLUE
        elif self == VertexColour.BLUE:
            return VertexColour.RED


def dfs_bipart_visit_vertex(graph: Graph, vertex,
                            vertex_colours: dict,
                            color_to_use: VertexColour):
    if not vertex_colours[vertex]:
        vertex_colours[vertex] = color_to_use
    for neighbour_vertex in graph.get_vertex_neighbours(vertex):
        if vertex_colours[neighbour_vertex] == vertex_colours[vertex]:
            raise ValueError('Podany graf nie jest dwudzielny.')
        if not vertex_colours[neighbour_vertex]:
            dfs_bipart_visit_vertex(graph, neighbour_vertex, vertex_colours,
                                    color_to_use.opposite_colour())


def dfs_bipart(graph: Graph) -> dict or None:
    vertex_colours = {v: None for v in graph.vertices}
    start_vertex = list(graph.vertices)[0]
    dfs_bipart_visit_vertex(graph=graph, vertex=start_vertex,
                            vertex_colours=vertex_colours, color_to_use=VertexColour.RED)

    return vertex_colours


def bipart_graph(graph: Graph) -> Tuple[set, set]:
    vertex_colours = dfs_bipart(graph=graph)
    red_part = {v for v, colour in vertex_colours.items() if colour == VertexColour.RED}
    blue_part = {v for v, colour in vertex_colours.items() if colour == VertexColour.BLUE}

    return blue_part, red_part


def biparted_graph_to_flow_network(graph: Graph, biparted_vertices: Tuple[set, set]):
    red_vertices, blue_vertices = biparted_vertices
    # Upewnienie się, że wszystkie łuki mają zwrot od niebieskich do czerwonych
    for edge in list(graph.edges):
        if edge[0] not in blue_vertices:
            graph.remove_edge(edge)
            graph.add_edge((edge[1], edge[0]))

    start_vertex = graph.add_vertex()
    end_vertex = graph.add_vertex()

    for blue_vertex in blue_vertices:
        graph.add_edge((start_vertex, blue_vertex))

    for red_vertex in red_vertices:
        graph.add_edge((red_vertex, end_vertex))

    flow_network = DirectedNetwork(vertices=graph.vertices,
                                   edges=graph.edges,
                                   weights=[1 for _ in range(len(graph.edges))],
                                   start_vertex=start_vertex,
                                   end_vertex=end_vertex)

    return flow_network


def maximal_matching(graph: Graph):
    biparted_vertices = bipart_graph(graph)
    flow_network = biparted_graph_to_flow_network(graph, biparted_vertices)
    _, _, flows = edmonds_karp(flow_network)
    max_match = [e for e, flow_value in flows.items() if flow_value == 1
                 and e[0] != flow_network.start_vertex and e[1] != flow_network.end_vertex]
    return max_match


if __name__ == '__main__':
    test_graph = Graph(edges=[(0, 5), (0, 7), (0, 9),
                              (1, 6), (1, 8),
                              (2, 5), (2, 6), (2, 7), (2, 8), (2, 9),
                              (3, 7), (3, 8),
                              (4, 6), (4, 8)
                              ],
                       vertices=set([i for i in range(0, 10)]),
                       )
    print('Maksymalne skojarzenie: {}'.format(maximal_matching(test_graph)))