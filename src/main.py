import matplotlib.pyplot as plt

from topology import build_graph
from traffic_matrix import generate_traffic_matrix
from dijkstra_routing import shortest_path_routing
from lp_traffic_engineering import solve_traffic_engineering_lp


def run_comparison(seed=42, density=0.5):

    # Build the NSFNET network
    graph = build_graph()

    # Generate traffic between network nodes
    traffic = generate_traffic_matrix(
        graph,
        seed=seed,
        density=density
    )

    # Run Dijkstra routing
    dijkstra_result = shortest_path_routing(
        graph,
        traffic
    )

    # Run Linear Programming optimisation
    lp_result = solve_traffic_engineering_lp(
        graph,
        traffic
    )

    # Display the results
    print("=" * 50)
    print("NSFNET Traffic Engineering")
    print("=" * 50)

    print("Number of demands:", len(traffic))
    print("Total traffic:", sum(traffic.values()), "Mbps")

    print(
        "Dijkstra maximum utilization:",
        f"{dijkstra_result['max_utilization']:.2%}"
    )

    if lp_result["success"]:

        print(
            "LP maximum utilization:",
            f"{lp_result['max_utilization']:.2%}"
        )

        improvement = (
            dijkstra_result["max_utilization"]
            - lp_result["max_utilization"]
        )

        print(
            "Reduction in maximum utilization:",
            f"{improvement:.2%}"
        )

    else:
        print("LP optimisation failed.")

    # Create comparison chart
    plot_comparison(
        dijkstra_result,
        lp_result
    )

    return dijkstra_result, lp_result


def plot_comparison(dijkstra_result, lp_result):

    dijkstra_value = (
        dijkstra_result["max_utilization"] * 100
    )

    if lp_result["success"]:
        lp_value = lp_result["max_utilization"] * 100
    else:
        lp_value = 0

    labels = ["Dijkstra", "Linear Programming"]
    values = [dijkstra_value, lp_value]

    plt.figure(figsize=(7, 5))

    plt.bar(labels, values)

    plt.ylabel("Maximum Link Utilization (%)")
    plt.title("NSFNET: Dijkstra vs Linear Programming")

    # Display the values above the bars
    for i, value in enumerate(values):
        plt.text(
            i,
            value + 1,
            f"{value:.1f}%",
            ha="center"
        )

    plt.tight_layout()

    plt.savefig(
        "../results/utilization_comparison.png"
    )

    plt.close()

    print("Comparison chart saved.")


if __name__ == "__main__":
    run_comparison()