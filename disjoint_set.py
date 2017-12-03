"""
MakeSet(x) initializes disjoint set for object x
Find(x) returns representative object of the set containing x
Union(x,y) makes two sets containing x and y respectively into one set

Some Applications:
- Kruskal's algorithm for finding minimal spanning trees
- Finding connected components in graphs
- Finding connected components in images (binary)
"""


class DisjointSet:
    def __init__(self, v):
        self.v = v
        self.parent = self
        self.rank = 0


def make_set(x) -> DisjointSet:
    return DisjointSet(x)


def union(x: DisjointSet, y: DisjointSet):
    x_root = find(x)
    y_root = find(y)
    if x_root.rank > y_root.rank:
        y_root.parent = x_root
    elif x_root.rank < y_root.rank:
        x_root.parent = y_root
    elif x_root != y_root: # Unless x and y are already in same set, merge them
        y_root.parent = x_root
        x_root.rank += 1


def find(x: DisjointSet):
    if x.parent == x:
        return x
    else:
        x.parent = find(x.parent)
        return x.parent
