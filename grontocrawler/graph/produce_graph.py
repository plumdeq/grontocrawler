#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# # Produce graph from nodes and arcs
#
# Convert ontology to a graph, according to the given rules
import networkx as nx
from grontocrawler.graph import (produce_arcs, produce_nodes)

def produce_graph(g):
    """
    Convert owl classes to nodes, and extract arcs from restrictions

    """
    nodes = produce_nodes.produce_nodes(g)
    arcs = produce_arcs.existential_arcs(g)

    digraph = nx.DiGraph()
    digraph.add_nodes_from(nodes)
    digraph.add_edges_from(arcs)

    return digraph
