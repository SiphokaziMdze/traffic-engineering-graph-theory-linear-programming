import networkx as nx


# Each link contains:
# node 1, node 2, distance (km), capacity (Mbps)

NSFNET_LINKS = [
    (0, 1, 1100, 100),
    (0, 2, 1600, 100),
    (0, 7, 2800, 100),
    (1, 2, 600, 100),
    (1, 3, 1000, 100),
    (2, 5, 2000, 100),
    (3, 4, 600, 100),
    (3, 10, 2400, 100),
    (4, 5, 1100, 100),
    (4, 6, 800, 100),
    (5, 9, 2000, 100),
    (5, 13, 1900, 100),
    (6, 7, 700, 100),
    (7, 8, 700, 100),
    (8, 9, 900, 100),
    (8, 11, 500, 100),
    (9, 10, 1500, 100),
    (9, 12, 1200, 100),
    (10, 11, 800, 100),
    (11, 12, 300, 100),
    (11, 13, 500, 100),
    (12, 13, 300, 100)
]


# Names of the NSFNET nodes

NODE_NAMES = {
    0: "Seattle",
    1: "Palo Alto",
    2: "San Diego",
    3: "Salt Lake City",
    4: "Boulder",
    5: "Houston",
    6: "Lincoln",
    7: "Champaign",
    8: "Ann Arbor",
    9: "Ithaca",
    10: "Pittsburgh",
    11: "Princeton",
    12: "College Park",
    13: "Atlanta"
}


def build_graph():

    # Create an empty network
    graph = nx.Graph()

    # Add the 14 nodes
    for node, name in NODE_NAMES.items():
        graph.add_node(node, name=name)

    # Add the links
    for node1, node2, distance, capacity in NSFNET_LINKS:
        graph.add_edge(
            node1,
            node2,
            distance=distance,
            capacity=capacity
        )

    return graph


if __name__ == "__main__":

    graph = build_graph()

    print("Number of nodes:", graph.number_of_nodes())
    print("Number of links:", graph.number_of_edges())