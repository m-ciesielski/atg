from graph import Graph


class WeightedGraph(Graph):
    def __init__(self, vertices: set, edges: list, weights: list):
        self.weight_map = {e: w for e, w in zip(edges, weights)}
        super(WeightedGraph, self).__init__(vertices=vertices, edges=edges)

    @classmethod
    def create_from_user_input(cls):
        while True:
            try:
                vertex_count = int(input('Podaj liczbę wierzchołków: '))
            except ValueError:
                print('Podana wartość jest niepoprawna.')
                continue
            else:
                break
        edges = []
        weights = []
        while True:
            try:
                edge_input = input('Dodaj krawędź (w formacie v1,v2,waga) [wpisz S by zakończyć dodawanie krawędzi]: ')
                if edge_input == "S":
                    break
                edge_input = edge_input.split(',')
                edge = int(edge_input[0]), int(edge_input[1])
                edges.append(edge)
                weights.append(int(edge_input[2]))
            except (ValueError, IndexError):
                print('Podana krawędź ma niepoprawny format.')
                continue
        vertices = {v for v in range(vertex_count)}
        return cls(vertices=vertices, edges=edges, weights=weights)

