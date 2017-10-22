from pprint import pformat
import operator


class Graph:
    def __init__(self, vertices: set, edges: list):
        self.vertices = vertices
        self.edges = edges
        self.n_matrix = self._create_n_matrix()

    @classmethod
    def create_from_graph_sequence(cls, sequence: list):
        if not is_graph_sequence(sequence):
            raise ValueError('Ciąg: {} nie jest ciągem grafowym.'.format(sequence))

        vertex_level_map = {vertex_index: level for vertex_index, level in enumerate(sequence)}
        vertices = {i for i, _ in enumerate(sequence)}
        edges = cls.create_edges_from_vertex_level_map(vertex_level_map)

        return cls(vertices=vertices, edges=edges)

    def __str__(self):
        return pformat(self.n_matrix)

    @staticmethod
    def _create_edges_from_vertex_level_map(vertex_level_map: dict, edges: list):
        max_vertex = max(vertex_level_map, key=vertex_level_map.get)
        max_vertex_level = vertex_level_map[max_vertex]
        if max_vertex_level == 0:
            return

        vertices_sorted_by_level = [(vertex, level) for vertex, level in
                                    reversed(sorted(vertex_level_map.items(), key=operator.itemgetter(1)))]
        vertices_to_connect = [vertex for vertex, level in
                               vertices_sorted_by_level
                               if level > 0 and vertex != max_vertex]
        for vertex in vertices_to_connect[:max_vertex_level]:
            edges.append((max_vertex, vertex))
            vertex_level_map[vertex] -= 1

        vertex_level_map[max_vertex] = 0

        Graph._create_edges_from_vertex_level_map(vertex_level_map, edges)

    @staticmethod
    def create_edges_from_vertex_level_map(vertex_level_map: dict) -> list:
        edges = []
        Graph._create_edges_from_vertex_level_map(vertex_level_map, edges)
        return edges

    def _create_n_matrix(self):
        matrix = [[0 for _ in range(len(self.vertices))] for _ in range(len(self.vertices))]
        for edge in self.edges:
            matrix[edge[0]][edge[1]] += 1
            matrix[edge[1]][edge[0]] += 1

        return matrix

    def add_vertex(self) -> int:
        new_vertex_index = len(self.vertices)
        self.vertices.add(new_vertex_index)
        # TODO: opt
        self.n_matrix = self._create_n_matrix()
        return new_vertex_index

    def add_edge(self, edge: tuple):
        self.edges.append(edge)
        self.n_matrix[edge[0]][edge[1]] += 1
        self.n_matrix[edge[1]][edge[0]] += 1

    def remove_vertex(self, vertex: int):
        self.vertices.remove(vertex)
        self.n_matrix = self._create_n_matrix()

    def remove_edge(self, edge: tuple):
        self.edges.remove(edge)
        self.n_matrix[edge[0]][edge[1]] -= 1
        self.n_matrix[edge[1]][edge[0]] -= 1

    def get_vertex_neighbours(self, vertex: int) -> set:
        neighbours = set()
        for v, edge_count in enumerate(self.n_matrix[vertex]):
            if edge_count > 0:
                neighbours.add(v)
        return neighbours

    def get_vertex_level(self, vertex: int):
        if vertex not in self.vertices:
            raise ValueError('Wierzcholek {} nie nalezy do grafu.'.format(vertex))
        return sum(edge_count for edge_count in self.n_matrix[vertex])

    def get_min_vertex_level(self):
        return min(self.get_vertex_level(vertex) for vertex in self.vertices)

    def get_max_vertex_level(self):
        return max(self.get_vertex_level(vertex) for vertex in self.vertices)

    def get_odd_vertices_count(self):
        return sum(1 for vertex in self.vertices if self.get_vertex_level(vertex) % 2 != 0)

    def get_even_vertices_count(self):
        return sum(1 for vertex in self.vertices if self.get_vertex_level(vertex) % 2 == 0)

    def get_sorted_vertex_level_list(self):
        vertex_levels = [self.get_vertex_level(vertex) for vertex in self.vertices]
        sorted_vertex_levels = list(reversed(sorted(vertex_levels)))
        return sorted_vertex_levels


# 1.2
# Podgraf izomorficzny do cyklu C3
def is_graph_c3_free(graph: Graph) -> bool:
    if len(graph.vertices) < 3:
        return True

    for vertex in graph.vertices:
        if graph.get_vertex_level(vertex) == 2:
            for neighbour_vertex in graph.get_vertex_neighbours(vertex):
                if graph.get_vertex_level(neighbour_vertex) == 2:
                    if graph.get_vertex_neighbours(vertex).intersection(graph.get_vertex_neighbours(neighbour_vertex)):
                        # Jeśli oba wierzchołki stopnia 2 mają tego samego sąsiada
                        # (zbiór wspólny sąsiadów jest niepusty), to
                        # graf zawiera podgraf izomorficzny do cyklu C3
                        return False

    return True


# 1.3
# Sprawdzenie, czy ciąg liczb naturalnych jest ciągem grafowym
def is_graph_sequence(sequence: list) -> bool:

    # sortowanie ciągu nierosnąco
    sequence = list(reversed((sorted(sequence))))

    if sequence[0] == 0:
        return True

    levels_to_reduce = [l for l in sequence[1:] if l > 0]
    if len(levels_to_reduce) < sequence[0]:
        # Ciąg nie jest graficzny, jeśli liczba stopni w ciągu
        # nie wystarcza do połączenia z wierzchołkiem o najwyższym stopniu
        return False

    # Wywołanie procedury rekurencyjnie ze zredukowaną listą stopni
    reduced_sequence = [0] + [level - 1 for level in levels_to_reduce]
    return is_graph_sequence(reduced_sequence)


def test_graph():
    g = Graph({0, 1, 2}, [(0, 1), (1, 2)])
    print('Graf testowy: {}'.format(g))
    g.add_vertex()
    print('Graf po dodaniu nowego wierzchołka: {}'.format(g))
    g.add_edge((3, 1))
    print('Graf po dodaniu krawędzi 3-1: {}'.format(g))
    
    print("Max stopien: {}".format(g.get_max_vertex_level()))
    print("Min stopien: {}".format(g.get_min_vertex_level()))
    print("Wierzcholki parzystego stopnia: {}".format(g.get_odd_vertices_count()))
    print("Wierzcholki nieparzystego stopnia: {}".format(g.get_even_vertices_count()))
    print("Posortowana lista stopni: {}".format(g.get_sorted_vertex_level_list()))


def test_c3_graph():
    g = Graph({0, 1, 2, 3}, [(0, 1), (0, 2), (1, 2), (2, 3)])
    assert not is_graph_c3_free(g)
    c3_free_g = Graph({0, 1, 2, 3}, [(0, 1), (1, 2), (2, 3)])
    assert is_graph_c3_free(c3_free_g)


def test_is_graph_sequence():
    assert is_graph_sequence([2, 3, 2, 3, 2])
    assert not is_graph_sequence([1, 4, 2, 3, 1])


def test_create_graph():
    seq = [2, 3, 2, 3, 2]
    g = Graph.create_from_graph_sequence(seq)
    print('Graf utworzony z ciągu {}: \n {}'.format(seq, g))
    assert g is not None

if __name__ == '__main__':
    test_graph()
    test_c3_graph()
    test_is_graph_sequence()
    test_create_graph()
