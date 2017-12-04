from graph import Graph


class Digraph(Graph):
    def __init__(self, vertices: set, edges: list):
        super(Digraph, self).__init__(vertices=vertices, edges=edges)

    def transpose(self):
        transposed_edges = [(edge[1], edge[0]) for edge in self.edges]
        return Digraph(vertices=set(self.vertices), edges=transposed_edges)

    def _create_n_matrix(self):
        matrix = [[0 for _ in range(len(self.vertices))] for _ in range(len(self.vertices))]
        for edge in self.edges:
            matrix[edge[0]][edge[1]] += 1

        return matrix
