import networkx as nx
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix


def solve_traffic_engineering_lp(graph, traffic_matrix):

    # Get all traffic demands
    demands = list(traffic_matrix.items())
    num_demands = len(demands)

    # Create both directions for every link
    directed_edges = []

    for u, v in graph.edges():
        directed_edges.append((u, v))
        directed_edges.append((v, u))

    num_edges = len(directed_edges)

    # Give every directed edge a number
    edge_index = {}

    for i, edge in enumerate(directed_edges):
        edge_index[edge] = i

    # Total number of flow variables
    num_flow_variables = num_demands * num_edges

    # Add one extra variable for maximum utilization
    num_variables = num_flow_variables + 1
    utilization_variable = num_flow_variables

    # Find the position of a flow variable
    def get_variable(demand_number, edge):
        return demand_number * num_edges + edge_index[edge]

    # --------------------------------------------------
    # OBJECTIVE
    # Minimize maximum link utilization
    # --------------------------------------------------

    objective = np.zeros(num_variables)
    objective[utilization_variable] = 1

    # --------------------------------------------------
    # FLOW CONSERVATION
    # --------------------------------------------------

    nodes = list(graph.nodes())
    node_index = {}

    for i, node in enumerate(nodes):
        node_index[node] = i

    num_nodes = len(nodes)

    A_eq = lil_matrix(
        (num_demands * num_nodes, num_variables)
    )

    b_eq = np.zeros(num_demands * num_nodes)

    for demand_number, ((source, destination), demand) in enumerate(demands):

        for node in nodes:

            row = demand_number * num_nodes + node_index[node]

            # Outgoing flow
            for neighbour in graph.neighbors(node):
                A_eq[row, get_variable(
                    demand_number, (node, neighbour)
                )] += 1

                # Incoming flow
                A_eq[row, get_variable(
                    demand_number, (neighbour, node)
                )] -= 1

            # Source produces the traffic
            if node == source:
                b_eq[row] = demand

            # Destination receives the traffic
            elif node == destination:
                b_eq[row] = -demand

    # --------------------------------------------------
    # LINK CAPACITY CONSTRAINTS
    # --------------------------------------------------

    physical_edges = list(graph.edges())

    A_ub = lil_matrix(
        (len(physical_edges), num_variables)
    )

    b_ub = np.zeros(len(physical_edges))

    for row, (u, v) in enumerate(physical_edges):

        capacity = graph.edges[u, v]["capacity"]

        for demand_number in range(num_demands):

            # Flow in both directions uses the same physical link
            A_ub[row, get_variable(
                demand_number, (u, v)
            )] += 1

            A_ub[row, get_variable(
                demand_number, (v, u)
            )] += 1

        # Total flow must be less than:
        # capacity × maximum utilization
        A_ub[row, utilization_variable] = -capacity

    # All flow values and utilization must be >= 0
    bounds = [(0, None)] * num_variables

    # --------------------------------------------------
    # SOLVE THE LP
    # --------------------------------------------------

    result = linprog(
        objective,
        A_ub=A_ub.tocsr(),
        b_ub=b_ub,
        A_eq=A_eq.tocsr(),
        b_eq=b_eq,
        bounds=bounds,
        method="highs"
    )

    flows = {}
    utilization = {}

    if result.success:

        solution = result.x

        # Save the flows used by each demand
        for demand_number in range(num_demands):

            flows[demand_number] = {}

            for edge in directed_edges:

                value = solution[
                    get_variable(demand_number, edge)
                ]

                if value > 0.000001:
                    flows[demand_number][edge] = value

        # Calculate utilization for every physical link
        for u, v in physical_edges:

            capacity = graph.edges[u, v]["capacity"]

            total_flow = 0

            for demand_number in range(num_demands):

                total_flow += flows.get(
                    demand_number, {}
                ).get((u, v), 0)

                total_flow += flows.get(
                    demand_number, {}
                ).get((v, u), 0)

            utilization[(u, v)] = total_flow / capacity

    return {
        "max_utilization": (
            result.x[utilization_variable]
            if result.success else None
        ),
        "flows": flows,
        "utilization": utilization,
        "status": result.message,
        "success": result.success
    }