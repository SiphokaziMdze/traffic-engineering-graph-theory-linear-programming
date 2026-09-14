# Traffic Engineering on NSFNET: Dijkstra vs Linear Programming

A Python project that compares two approaches to routing network traffic:

- Dijkstra shortest-path routing
- Linear Programming (LP) traffic engineering

The project uses the 14-node NSFNET topology and compares how each approach affects network link utilisation.

## Overview

In a computer network, traffic needs to be routed between different nodes.

This project compares two approaches:

### 1. Dijkstra Shortest-Path Routing

Each traffic demand is sent along the shortest path based on physical distance.

This approach is simple, but multiple demands can use the same links and cause congestion.

### 2. Linear Programming Traffic Engineering

The LP approach considers all traffic demands together.

Traffic can be split across different paths to reduce congestion and minimise the maximum link utilisation in the network.

## How It Works

```text
NSFNET Topology
       |
       v
Traffic Matrix
       |
       +------------------+
       |                  |
       v                  v
   Dijkstra               LP
Shortest Path        Traffic Optimisation
       |                  |
       v                  v
Link Utilisation    Link Utilisation
       |                  |
       +--------+---------+
                |
                v
          Compare Results