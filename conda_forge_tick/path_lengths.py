"""
Functions to find the longest paths between nodes in a graph.

"""
from copy import deepcopy
from collections import defaultdict

import networkx as nx


def cyclic_topological_sort(graph, sources):
    """Return a list of nodes in a graph with cycles in topological order.

    Performs a topological sort of `graph` starting from the node `source`.
    This is not a true topological sort if `graph` contains cycles, but
    any nodes that are not part of a cycle are given in correct topological
    order.

    Parameters
    ----------
    graph : networkx.classes.digraph.DiGraph
        A directed graph.
    source : iterable
        The names of the source nodes

    Returns
    -------
    list
        The nodes of `graph` in topological sort order.

    """

    g2 = deepcopy(graph)
    order = []
    for source in sources:
        _visit(g2, source, order)
    return reversed(order)


def _visit(graph, node, order):
    if graph.node[node].get("visited", False):
        return
    graph.node[node]["visited"] = True
    for n in graph.neighbors(node):
        _visit(graph, n, order)
    order.append(node)


def get_longest_paths(graph, sources):
    """Get the length of the longest path to each node from a set of source
    nodes.

    Parameters
    ----------
    graph : networkx.classes.digraph.DiGraph
        A directed graph.
    sources : list of str
        The names of the source nodes.

    Returns
    -------
    dict
        A dictionary where keys are the names of the nodes in `graph` and
        values are the lengths of the longest path from a node in `sources`.

    """

    dist = {node: -float("inf") for node in graph}
    for source in sources:
        dist[source] = 0
    visited = []
    for u in cyclic_topological_sort(graph, sources):
        visited.append(u)
        for v in graph.neighbors(u):
            if v in visited:
                continue
            if dist[v] < dist[u] + 1:
                dist[v] = dist[u] + 1

    return dist


def get_levels(graph, sources):
    """Get the nodes in each level of a topological sort of a graph starting
    from a set of source nodes.

    Parameters
    ----------
    graph : networkx.classes.digraph.DiGraph
        A directed graph.
    sources : list of str
        The names of the source nodes.

    Returns
    -------
    dict
        A dictionary where keys are integers and values are the names of the
        nodes in `graph` with longest path length to a source node equal to the
        key.

    """

    g2 = deepcopy(graph)
    desc = []
    for source in sources:
        desc += list(graph.successors(source))
    for node in graph.node:
        if node not in desc and node not in sources:
            g2.remove_node(node)

    dist = get_longest_paths(g2, sources)
    levels = defaultdict(set)
    for k, v in dist.items():
        levels[v].add(k)
    return levels
