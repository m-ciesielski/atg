from typing import Tuple


def int_value_from_cli(label: str) -> int:
    while True:
        try:
            value = int(input('Podaj {}: '.format(label)))
        except ValueError:
            print('Podana wartość jest niepoprawna.')
            continue
        else:
            return value


def weighted_edges_from_cli() -> Tuple[list, list]:
    edges = []
    weights = []
    while True:
        try:
            edge_input = input('Dodaj krawędź (w formacie v1,v2,waga) [wpisz S by zakończyć dodawanie krawędzi]: ')
            if edge_input == "S":
                return edges, weights
            edge_input = edge_input.split(',')
            edge = int(edge_input[0]), int(edge_input[1])
            edges.append(edge)
            weights.append(int(edge_input[2]))
        except (ValueError, IndexError):
            print('Podana krawędź ma niepoprawny format.')
