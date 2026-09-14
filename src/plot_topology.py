import matplotlib.pyplot as plt
import networkx as nx

from topology import build_graph, NODE_NAMES


def plot_topology():

    # Build the NSFNET network
    graph = build_graph()

    # Choose positions for the nodes
    positions = nx.spring_layout(
        graph,
        seed=7
    )

    # Create the graph
    plt.figure(figsize=(9, 7))

    # Draw the links
    nx.draw_networkx_edges(
        graph,
        positions
    )

    # Draw the nodes
    nx.draw_networkx_nodes(
        graph,
        positions,
        node_size=900
    )

    # Add node labels
    labels = {}

    for node in graph.nodes():
        labels[node] = f"{node}\n{NODE_NAMES[node]}"

    nx.draw_networkx_labels(
        graph,
        positions,
        labels=labels,
        font_size=7
    )

    # Add a title
    plt.title(
        f"NSFNET Topology: "
        f"{graph.number_of_nodes()} nodes, "
        f"{graph.number_of_edges()} links"
    )

    # Hide the axes
    plt.axis("off")

    plt.tight_layout()

    # Save the image
    plt.savefig(
        "../results/nsfnet_topology.png",
        dpi=150
    )

    plt.close()

    print("Topology diagram saved.")


if __name__ == "__main__":
    plot_topology()