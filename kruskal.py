import disjoint_set
from tree import Tree
from weighted_graph import WeightedGraph


def kruskal(graph: WeightedGraph):
    min_spanning_tree_edges = set()
    vertices_disjoint_sets = {vertex: disjoint_set.make_set(vertex) for vertex in graph.vertices}

    for edge in sorted(graph.edges, key=lambda e: graph.weight_map[e]):
        v0_disjoint_set, v1_disjoint_set = vertices_disjoint_sets[edge[0]], vertices_disjoint_sets[edge[1]]
        if disjoint_set.find(v0_disjoint_set) != disjoint_set.find(v1_disjoint_set):
            min_spanning_tree_edges.add(edge)
            disjoint_set.union(v0_disjoint_set, v1_disjoint_set)

    min_spanning_tree_vertices = set()
    for spanning_edge in min_spanning_tree_edges:
        min_spanning_tree_vertices.add(spanning_edge[0])
        min_spanning_tree_vertices.add(spanning_edge[1])

    min_spanning_tree = Tree(edges=list(min_spanning_tree_edges),
                             vertices=min_spanning_tree_vertices)
    return min_spanning_tree


if __name__ == '__main__':
    g = WeightedGraph.create_from_user_input()
    kruskal_min_spanning_tree = kruskal(g)
    print('Minimalne drzewo spinające: {} '
          '\nKrawędzie drzewa: {}'.format(kruskal_min_spanning_tree,
                                          kruskal_min_spanning_tree.edges))
