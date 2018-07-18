from conda_forge_tick.path_lengths import get_levels, nx


def test_get_levels():
    g = nx.DiGraph(
        [
            ("a", "d"),
            ("a", "f"),
            ("b", "d"),
            ("b", "e"),
            ("b", "g"),
            ("c", "e"),
            ("c", "h"),
            ("d", "f"),
            ("d", "g"),
            ("d", "h"),
            ("e", "g"),
        ]
    )
    levels = {0: {"a", "b", "c"}, 1: {"d", "e"}, 2: {"f", "g", "h"}}
    assert get_levels(g, ["a", "b", "c"]) == levels

    g.add_edges_from([("a", "b"), ("e", "a"), ("c", "g")])
    levels = {0: {"a", "c"}, 1: {"b"}, 2: {"d", "e"}, 3: {"f", "g", "h"}}
    assert get_levels(g, ["a", "c"]) == levels

    g.add_edges_from([("d", "c"), ("a", "c"), ("a", "e"), ("a", "g"), ("a", "h")])
    levels = {0: {"a"}, 1: {"b"}, 2: {"d"}, 3: {"c", "f"}, 4: {"e", "h"}, 5: {"g"}}
    assert get_levels(g, "a") == levels
