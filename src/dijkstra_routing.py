import networkx as nx
from topology import build_graph


def shortest_path_routing(graph, traffic_matrix):
    link_loads = {}
    paths = {}

    # Start every link with zero traffic
    for u, v in graph.edges():
        link_loads[tuple(sorted((u, v)))] = 0

    # Route each traffic demand using Dijkstra
    for (source, destination), demand in traffic_matrix.items():

        path = nx.dijkstra_path(
            graph,
            source,
            destination,
            weight="distance"
        )

        paths[(source, destination)] = path

        # Add the demand to every link used by the path
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]

            link = tuple(sorted((u, v)))
            link_loads[link] += demand

    # Calculate how much of each link's capacity is being used
    utilization = {}

    for link, load in link_loads.items():
        u, v = link
        capacity = graph.edges[u, v]["capacity"]
        utilization[link] = load / capacity

    # Find the most heavily used link
    if utilization:
        max_utilization = max(utilization.values())
    else:
        max_utilization = 0

    return {
        "link_loads": link_loads,
        "paths": paths,
        "utilization": utilization,
        "max_utilization": max_utilization
    }


if __name__ == "__main__":

    graph = build_graph()

    from traffic_matrix import generate_traffic_matrix

    traffic = generate_traffic_matrix(graph, seed=42)

    result = shortest_path_routing(graph, traffic)

    print("=== Dijkstra Shortest-Path Routing ===")
    print("Total demands:", len(traffic))
    print("Maximum link utilization:",
          f"{result['max_utilization']:.2%}")

    print("\nMost congested links:")

    top_links = sorted(
        result["utilization"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    for link, utilization in top_links:
        print(f"{link}: {utilization:.2%}")