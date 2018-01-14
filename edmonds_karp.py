from collections import deque

from directed_network import DirectedNetwork


class VertexTrait:
    def __init__(self, sign: str, predecessor: int or None, flow_value: float):
        if sign not in {'+', '-'}:
            raise ValueError('Znak musi mieć wartość + lub -.')
        self.sign = sign
        self.predecessor = predecessor
        self.flow_value = flow_value

    def __repr__(self):
        return f'({self.predecessor}{self.sign}, {self.flow_value})'


def edmonds_karp(network: DirectedNetwork):
    flows = {edge: 0 for edge in network.edges}
    flows.update({tuple(reversed(edge)): 0 for edge in network.edges})
    traits = {vertex: None for vertex in network.vertices}
    capacity = {edge: weight for edge, weight in zip(network.edges, network.weights)}
    max_flow = 0
    max_path = []

    vertex_queue = deque([network.start_vertex])
    traits[network.start_vertex] = VertexTrait(sign='-', predecessor=None, flow_value=float('inf'))
    while vertex_queue:
        vertex = vertex_queue.popleft()
        for neighbour in network.get_vertex_neighbours(vertex):
            edge = (vertex, neighbour)
            reversed_edge = tuple(reversed(edge))
            if capacity[edge] <= 0 or traits[neighbour]:
                continue
            if flows[edge] < capacity[edge]:
                flow_value = min(capacity[edge] - flows[edge], traits[vertex].flow_value)
                traits[neighbour] = VertexTrait(sign='+', predecessor=vertex, flow_value=flow_value)
                vertex_queue.append(neighbour)
            elif reversed_edge in capacity and flows[reversed_edge] < capacity[reversed_edge]:
                flow_value = min(capacity[reversed_edge] - flows[reversed_edge], traits[vertex].flow_value)
                traits[neighbour] = VertexTrait(sign='-', predecessor=vertex, flow_value=flow_value)
                vertex_queue.append(neighbour)

            if network.end_vertex in vertex_queue:
                max_path = []
                augmenting_path_vertex = network.end_vertex
                flow_to_increase = traits[augmenting_path_vertex].flow_value
                max_flow = max_flow + flow_to_increase
                while augmenting_path_vertex != network.start_vertex:
                    max_path.append(augmenting_path_vertex)
                    predecessor = traits[augmenting_path_vertex].predecessor
                    sign = traits[augmenting_path_vertex].sign
                    if sign == '+':
                        flows[predecessor, augmenting_path_vertex] += flow_to_increase
                    else:
                        flows[augmenting_path_vertex, predecessor] += flow_to_increase
                    augmenting_path_vertex = predecessor

                max_path.append(network.start_vertex)
                max_path = list(reversed(max_path))
                print(f'Ścieżka powiększająca: {max_path}')
                traits = {vertex: None for vertex in network.vertices}
                traits[network.start_vertex] = VertexTrait(sign='-', predecessor=None, flow_value=float('inf'))
                vertex_queue = deque([network.start_vertex])

    vertices_with_traits = set([v for v, trait in traits.items() if trait is not None])
    minimal_cut_vertices = network.vertices - vertices_with_traits
    minimal_cut = [(u, v) for u, v in network.edges if u in vertices_with_traits and v in minimal_cut_vertices]
    return max_flow, minimal_cut, {edge: flow for edge, flow in flows.items() if flow > 0}


if __name__ == '__main__':
    test_network = DirectedNetwork(edges=[(0, 1), (1, 3),
                                          (0, 2), (2, 3),
                                          ],
                                   weights=[4, 5, 7, 6],
                                   vertices=set([i for i in range(0, 4)]),
                                   start_vertex=0,
                                   end_vertex=3
                                   )
    test_network_2 = DirectedNetwork(edges=[(0, 1), (0, 2),
                                            (1, 2), (1, 3),
                                            (2, 1), (2, 4),
                                            (3, 2), (3, 5),
                                            (4, 3), (4, 5)],
                                     weights=[16, 13,
                                              10, 12,
                                              4, 14,
                                              9, 20,
                                              7, 4],
                                     vertices=set([i for i in range(0, 6)]),
                                     start_vertex=0,
                                     end_vertex=5)
    test_network_3 = DirectedNetwork(edges=[(0, 1), (0, 2),
                                            (1, 2), (1, 3),
                                            (2, 1), (2, 4),
                                            (3, 2)],
                                     weights=[16, 13,
                                              10, 12,
                                              4, 14,
                                              9],
                                     vertices=set([i for i in range(0, 6)]),
                                     start_vertex=0,
                                     end_vertex=5)
    # network = DirectedNetwork.create_from_user_input()

    max_flow, minimal_cut, flows = edmonds_karp(test_network)
    print(f'Maksymalny przepływ {max_flow}, minimalny przekrój: {minimal_cut}, Przepływy: {flows}')
    print()
    max_flow, minimal_cut, flows = edmonds_karp(test_network_2)
    print(f'Maksymalny przepływ {max_flow}, minimalny przekrój: {minimal_cut}, Przepływy: {flows}')
    print()
    max_flow, minimal_cut, flows = edmonds_karp(test_network_3)
    print(f'Maksymalny przepływ {max_flow}, minimalny przekrój: {minimal_cut}, Przepływy: {flows}')
