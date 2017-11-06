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

        vertex_degree_map = {vertex_index: degree for vertex_index, degree in enumerate(sequence)}
        vertices = {i for i, _ in enumerate(sequence)}
        edges = cls.create_edges_from_vertex_degree_map(vertex_degree_map)

        return cls(vertices=vertices, edges=edges)

    @classmethod
    def create_from_user_input(cls):
        while True:
            while True:
                try:
                    vertex_count = int(input('Podaj liczbę wierzchołków: '))
                except ValueError:
                    print('Podana wartość jest niepoprawna.')
                    continue
                else:
                    break

            edges = []
            while True:
                try:
                    edge_input = input('Dodaj krawędź (w formacie v1,v2) [wpisz S by zakończyć dodawanie krawędzi]: ')
                    if edge_input == "S":
                        break
                    edge_input = edge_input.split(',')
                    edge = int(edge_input[0]), int(edge_input[1])
                    edges.append(edge)
                except ValueError:
                    print('Podana krawędź ma niepoprawny format.')
                    continue

            vertices = {v for v in range(vertex_count)}

            return cls(vertices=vertices, edges=edges)

    def __str__(self):
        return pformat(self.n_matrix)

    @staticmethod
    def _create_edges_from_vertex_degree_map(vertex_degree_map: dict, edges: list):
        max_vertex = max(vertex_degree_map, key=vertex_degree_map.get)
        max_vertex_degree = vertex_degree_map[max_vertex]
        if max_vertex_degree == 0:
            return

        vertices_sorted_by_degree = [(vertex, degree) for vertex, degree in
                                     reversed(sorted(vertex_degree_map.items(), key=operator.itemgetter(1)))]
        vertices_to_connect = [vertex for vertex, degree in
                               vertices_sorted_by_degree
                               if degree > 0 and vertex != max_vertex]
        for vertex in vertices_to_connect[:max_vertex_degree]:
            edges.append((max_vertex, vertex))
            vertex_degree_map[vertex] -= 1

        vertex_degree_map[max_vertex] = 0

        Graph._create_edges_from_vertex_degree_map(vertex_degree_map, edges)

    @staticmethod
    def create_edges_from_vertex_degree_map(vertex_degree_map: dict) -> list:
        edges = []
        Graph._create_edges_from_vertex_degree_map(vertex_degree_map, edges)
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
        # self.n_matrix.append([0 for _ in range(len(vertices))])
        # for neighbours_list in self.n_matrix:
        #     neighbours_list.append(0)
        self.n_matrix = self._create_n_matrix()
        return new_vertex_index

    def add_edge(self, edge: tuple):
        if edge[0] not in self.vertices or edge[1] not in self.vertices:
            raise ValueError('Wierzcholki {} nie naleza do grafu.'.format(edge))
        self.edges.append(edge)
        self.n_matrix[edge[0]][edge[1]] += 1
        self.n_matrix[edge[1]][edge[0]] += 1

    def remove_vertex(self, vertex: int):
        if vertex not in self.vertices:
            raise ValueError('Wierzchołek {} nie należy do grafu.'.format(vertex))

        corrected_edges = []

        for edge in self.edges:
            if vertex in edge:
                self.edges.remove(edge)
            elif edge[0] > vertex or edge[1] > vertex:
                corrected_edge = (edge[0], edge[1])
                if edge[0] > vertex:
                    corrected_edge = (corrected_edge[0] - 1, corrected_edge[1])
                if edge[1] > vertex:
                    corrected_edge = (corrected_edge[0], corrected_edge[1] - 1)
                corrected_edges.append(corrected_edge)
                self.edges.remove(edge)

        self.edges += corrected_edges

        self.vertices = {i for i in range(len(self.vertices) - 1)}
        self.n_matrix = self._create_n_matrix()

    def remove_edge(self, edge: tuple):
        if edge not in self.edges:
            raise ValueError('Krawędź {} nie należy do grafu.'.format(edge))

        self.edges.remove(edge)
        self.n_matrix[edge[0]][edge[1]] -= 1
        self.n_matrix[edge[1]][edge[0]] -= 1

    def get_vertex_neighbours(self, vertex: int) -> set:
        if vertex not in self.vertices:
            raise ValueError('Wierzcholek {} nie nalezy do grafu.'.format(vertex))
        neighbours = set()
        for v, edge_count in enumerate(self.n_matrix[vertex]):
            if edge_count > 0:
                neighbours.add(v)
        return neighbours

    def get_vertex_degree(self, vertex: int):
        if vertex not in self.vertices:
            raise ValueError('Wierzcholek {} nie nalezy do grafu.'.format(vertex))
        return sum(edge_count for edge_count in self.n_matrix[vertex])

    def get_min_vertex_degree(self):
        return min(self.get_vertex_degree(vertex) for vertex in self.vertices)

    def get_max_vertex_degree(self):
        return max(self.get_vertex_degree(vertex) for vertex in self.vertices)

    def get_odd_vertices_count(self):
        return sum(1 for vertex in self.vertices if self.get_vertex_degree(vertex) % 2 != 0)

    def get_even_vertices_count(self):
        return sum(1 for vertex in self.vertices if self.get_vertex_degree(vertex) % 2 == 0)

    def get_sorted_vertex_degree_list(self):
        vertex_degrees = [self.get_vertex_degree(vertex) for vertex in self.vertices]
        sorted_vertex_degrees = list(reversed(sorted(vertex_degrees)))
        return sorted_vertex_degrees


# 1.2
# Podgraf izomorficzny do cyklu C3
def is_graph_c3_free(graph: Graph) -> bool:
    if len(graph.vertices) < 3:
        return True

    for vertex in graph.vertices:

        if graph.get_vertex_degree(vertex) >= 2:
            for neighbour_vertex in graph.get_vertex_neighbours(vertex):
                if graph.get_vertex_degree(neighbour_vertex) >= 2:
                    if graph.get_vertex_neighbours(vertex).intersection(graph.get_vertex_neighbours(neighbour_vertex)):
                        # Jeśli oba wierzchołki stopnia co najmniej 2 mają tego samego sąsiada
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

    degrees_to_reduce = [l for l in sequence[1:] if l > 0]
    if len(degrees_to_reduce) < sequence[0]:
        # Ciąg nie jest graficzny, jeśli liczba stopni w ciągu
        # nie wystarcza do połączenia z wierzchołkiem o najwyższym stopniu
        return False

    # Wywołanie procedury rekurencyjnie ze zredukowaną listą stopni
    reduced_sequence = [0] + [degree - 1 for degree in degrees_to_reduce]
    return is_graph_sequence(reduced_sequence)


def test_graph():
    g = Graph({0, 1, 2}, [(0, 1), (1, 2)])
    print('Graf testowy: \n{}'.format(g))
    g.add_vertex()
    g.add_vertex()
    print('Graf po dodaniu nowego wierzchołka: \n{}'.format(g))
    #g.add_edge((3, 1))
    g.add_edge((3, 4))
    print('Graf po dodaniu krawędzi 3-4: \n{}'.format(g))
    
    print("Max stopien: {}".format(g.get_max_vertex_degree()))
    print("Min stopien: {}".format(g.get_min_vertex_degree()))
    print("Wierzcholki parzystego stopnia: {}".format(g.get_odd_vertices_count()))
    print("Wierzcholki nieparzystego stopnia: {}".format(g.get_even_vertices_count()))
    print("Posortowana lista stopni: {}".format(g.get_sorted_vertex_degree_list()))

    # g.remove_edge((3, 1))
    # print('Graf po usunięciu krawędzi 3-1: \n{}'.format(g))
    #
    g.remove_vertex(2)
    print('Graf po usunięciu wierzchołka 2: \n{}'.format(g))

    #g.remove_vertex(2)
    print('Stopien  wierzchołka 2: \n{}'.format(g.get_vertex_degree(2)))


def test_c3_graph():
    g = Graph({0, 1, 2, 3}, [(0, 1), (0, 2), (0, 3), (1, 2)])
    print('Graf nie zawiera cyklu c3: {}'.format(is_graph_c3_free(g)))
    assert not is_graph_c3_free(g)
    # c3_free_g = Graph({0, 1, 2, 3}, [(0, 1), (1, 2), (2, 3)])
    # assert is_graph_c3_free(c3_free_g)


def test_is_graph_sequence():
    #assert is_graph_sequence([2, 3, 2, 3, 2])
    seq = [3, 2, 2, 2, 1]
    print('Ciag {} jest ciagem grafowym: {}'.format(seq, is_graph_sequence(seq)))
    #assert not is_graph_sequence([1, 4, 2, 3, 1])


def test_create_graph():
    seq = [3, 2, 2, 2, 1]
    g = Graph.create_from_graph_sequence(seq)
    print('Graf utworzony z ciągu {}: \n {}'.format(seq, g))
    assert g is not None

    non_graph_seq = [1, 4, 2, 3, 1]
    ng = None
    try:
        ng = Graph.create_from_graph_sequence(non_graph_seq)
    except ValueError:
        pass
    assert ng is None

if __name__ == '__main__':
    test_graph()
    test_c3_graph()
    test_is_graph_sequence()
    test_create_graph()
