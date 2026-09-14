import random


def generate_traffic_matrix(
    graph,
    seed=42,
    min_demand=2,
    max_demand=8,
    density=0.3
):
    # Make the random results repeatable
    random.seed(seed)

    nodes = list(graph.nodes())
    traffic_matrix = {}

    # Check every possible source and destination
    for source in nodes:

        for destination in nodes:

            # A node cannot send traffic to itself
            if source == destination:
                continue

            # Decide whether this pair should have traffic
            if random.random() < density:

                demand = random.randint(
                    min_demand,
                    max_demand
                )

                traffic_matrix[
                    (source, destination)
                ] = demand

    return traffic_matrix


if __name__ == "__main__":

    from topology import build_graph

    graph = build_graph()

    traffic = generate_traffic_matrix(graph)

    print(
        "Number of demands:",
        len(traffic)
    )

    print(
        "Total traffic:",
        sum(traffic.values()),
        "Mbps"
    )