from math import inf
from typing import Tuple

from console_input_utils import int_value_from_cli, weighted_edges_from_cli
from weighted_graph import WeightedGraph
from digraph import Digraph


class DirectedNetwork(WeightedGraph, Digraph):
    def __init__(self, vertices: set, edges: list, weights: list, start_vertex: int, end_vertex: int):
        if start_vertex not in vertices or end_vertex not in vertices:
            raise ValueError('Podane punkty startowe i końcowe nie należą do sieci.')

        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.weights = weights

        super().__init__(vertices=vertices, edges=edges, weights=weights)

        if not self.get_vertex_neighbours(self.start_vertex):
            raise ValueError('Podany punkt startowy nie jest źródłem.')
        if self.get_vertex_neighbours(self.end_vertex):
            raise ValueError('Podany punkt końcowy nie jest ujściem.')

    @classmethod
    def create_from_user_input(cls):
        vertex_count = int_value_from_cli(label='liczbę wierzchołków')
        edges, weights = weighted_edges_from_cli()
        start_vertex = int_value_from_cli(label='wierzchołek startowy')
        end_vertex = int_value_from_cli(label='wierzchołek końcowy')
        vertices = {v for v in range(vertex_count)}
        return cls(vertices=vertices, edges=edges, weights=weights,
                   start_vertex=start_vertex, end_vertex=end_vertex)

    def get_vertex_predecessors(self, vertex: int) -> set:
        if vertex not in self.vertices:
            raise ValueError('Wierzcholek {} nie nalezy do grafu.'.format(vertex))
        predecessors = set()
        for edge in self.edges:
            if edge[1] == vertex:
                predecessors.add(edge[0])
        return predecessors

    def get_shortest_path_map(self, start: int) -> dict:
        if start not in self.vertices:
            raise ValueError('Podane punkt startowy nie należy do sieci.')
        topological_sort = dfs_topological_sort(self)
        shortest_paths_map = {vertex: inf for vertex in self.vertices if vertex != start}
        shortest_paths_map[start] = 0

        while topological_sort:
            vertex = topological_sort.pop()
            if vertex == start:
                continue
            predecessors = self.get_vertex_predecessors(vertex)
            if predecessors:
                shortest_paths_map[vertex] = min(shortest_paths_map[predecessor] + self.weight_map[(predecessor, vertex)]
                                                 for predecessor in predecessors)
        return shortest_paths_map

    def get_longest_path_map(self, start: int) -> dict:
        if start not in self.vertices:
            raise ValueError('Podany punkt startowy nie należy do sieci.')

        weights_changed_signs = [-w for w in self.weights]
        helper_network = DirectedNetwork(edges=self.edges, vertices=self.vertices,
                                         weights=weights_changed_signs,
                                         start_vertex=self.start_vertex, end_vertex=self.end_vertex)
        longest_paths_map_in_helper_network = helper_network.get_shortest_path_map(start)
        longest_paths_map = {vertex: -length for vertex, length in longest_paths_map_in_helper_network.items()}
        return longest_paths_map

    def get_longest_path(self, start: int, end: int):
        if start not in self.vertices or end not in self.vertices:
            raise ValueError('Podany punkt startowy/końcowy nie należy do sieci.')

        return self.get_longest_path_map(start=start)[end]

    def get_process_minimal_finish_time(self) -> int:
        return self.get_longest_path(start=self.start_vertex, end=self.end_vertex)

    def get_task_minimal_start_time(self, task: Tuple[int, int]) -> int:
        return self.get_longest_path(start=self.start_vertex, end=task[0])

    def get_task_maximal_start_time(self, task: Tuple[int, int]) -> int:
        return self.get_process_minimal_finish_time() - self.get_longest_path(start=task[1], end=self.end_vertex)\
               - self.weight_map[task]


def dfs_visit_vertex_topological_sort(network: DirectedNetwork,
                                      vertex, visited_vertex_map: dict,
                                      visited_vertices: list):
    visited_vertex_map[vertex] = True
    for neighbour_vertex in network.get_vertex_neighbours(vertex):
        visited = visited_vertex_map[neighbour_vertex]
        if not visited:
            dfs_visit_vertex_topological_sort(network, neighbour_vertex, visited_vertex_map,
                                              visited_vertices)

    visited_vertices.append(vertex)


def dfs_topological_sort(network: DirectedNetwork) -> list:
    visited_vertex_map = {vertex: False for vertex in network.vertices}
    topological_sort = []
    for vertex in network.vertices:
        if not visited_vertex_map[vertex]:
            dfs_visit_vertex_topological_sort(network, vertex, visited_vertex_map,
                                              visited_vertices=topological_sort)

    return topological_sort


if __name__ == '__main__':
    # test_network = DirectedNetwork(edges=[(0, 1), (0, 3),
    #                                       (3, 1), (3, 4),
    #                                       (1, 2), (2, 4),
    #                                       (2, 5), (4, 5)
    #                                       ],
    #                                weights=[1, 2, -4, 3, 6, 1, -2, 1],
    #                                vertices=set([i for i in range(0, 6)]),
    #                                start_vertex=0,
    #                                end_vertex=5
    #                                )
    test_network_2 = DirectedNetwork(edges=[(0, 1), (0, 3),
                                            (3, 1), (3, 4),
                                            (1, 2), (2, 4),
                                            (2, 5), (4, 5)
                                            ],
                                     weights=[1, 2, 4, 3, 6, 1, 4, 1],
                                     vertices=set([i for i in range(0, 6)]),
                                     start_vertex=0,
                                     end_vertex=5
                                     )
    # network = DirectedNetwork.create_from_user_input()

    network = test_network_2

    print('Minimalny czas realizacji: {}'.format(network.get_process_minimal_finish_time()))
    print('Porządek topologiczny: {}'.format(dfs_topological_sort(network)))
    for task in network.edges:
        print('Minimalny czas rozpoczęcia zadania {}: {}'.format(task, network.get_task_minimal_start_time(task)))
        print('Maksymalny czas rozpoczęcia zadania {}: {}\n'.format(task, network.get_task_maximal_start_time(task)))

