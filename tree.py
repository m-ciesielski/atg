from collections import deque

from graph import Graph


class Tree(Graph):
    def __init__(self, vertices: set, edges: list):
        if Tree._validate_tree(vertices, edges):
            super().__init__(vertices=vertices, edges=edges)
        else:
            raise ValueError('Podany graf nie jest drzewem.')

    @staticmethod
    def _validate_tree(vertices: set, edges: list):
        # TODO: sprawdzenie czy drzewo zawiera cykl
        if len(edges) != (len(vertices) - 1):
            return False
        else:
            return True

    def get_leaf_vertices(self) -> set:
        return {v for v in self.vertices if self.get_vertex_degree(v) == 1}

    def remove_vertex(self, vertex: int):
        if vertex not in self.vertices:
            raise ValueError('Wierzchołek {} nie należy do grafu.'.format(vertex))

        for edge in self.edges:
            if vertex in edge:
                self.edges.remove(edge)

        self.vertices.remove(vertex)

        for i in range(len(self.n_matrix)):
            self.n_matrix[i][vertex] = 0
            self.n_matrix[vertex][i] = 0

    def find_center(self) -> set:
        temp_tree = Tree(vertices=set(self.vertices), edges=list(self.edges))

        leaf_queue = deque(temp_tree.get_leaf_vertices())
        parent_queue = deque()
        while len(temp_tree.vertices) > 2 or len(leaf_queue) > 0:
            if len(leaf_queue) == 0:
                leaf_queue = parent_queue
                parent_queue = deque()

            leaf = leaf_queue.popleft()
            neighbours = temp_tree.get_vertex_neighbours(leaf)
            if not neighbours:
                break
            parent = neighbours.pop()

            temp_tree.remove_vertex(leaf)

            if temp_tree.get_vertex_degree(parent) <= 1:
                    parent_queue.append(parent)

        return temp_tree.vertices


def test():
    test_tree = Tree({0, 1, 2, 3, 4, 5, 6},
                     [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (5, 6)])
    print(test_tree.find_center())
    test_tree_2 = Tree({0, 1, 2, 3, 4, 5, 6, 7, 8},
                       [(0, 1), (0, 2), (1, 3), (1, 4), (4, 7), (7, 6), (7, 8), (2, 5)])
    print(test_tree_2.find_center())
    test_tree_3 = Tree({0, 1, 2, 3, 4},
                       [(0, 1), (0, 2), (0, 3), (0, 4)])
    print(test_tree_3.find_center())
    test_tree_4 = Tree({0, 1, 2, 3, 4, 5},
                       [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5)])
    print(test_tree_4.find_center())

if __name__ == '__main__':
    g = Tree.create_from_user_input()
    print(g.find_center())

