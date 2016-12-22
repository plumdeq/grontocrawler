#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# # Produce graph from nodes and arcs
#
# Convert ontology to a graph, according to the given rules
import networkx as nx
import itertools as it
from grontocrawler.graph import (produce_arcs, produce_nodes)


# Constant options for the graph creation algorithm
OPTIONS = ['is-a-arcs', 'existential-arcs']
# Mapping from 'options' to 'generators'
RULES = {
    'is-a-arcs': produce_arcs.is_a_arcs,
    'existential-arcs': produce_arcs.existential_arcs
}


# We control the created graph via the options which correspond to the edge
# production rules: ['is-a-arcs', 'existential-arcs'] etc.
def produce_graph(g, options=OPTIONS):
    """
    Convert owl classes to nodes, and extract arcs from restrictions

    """
    # apparently `default` parameter in the `def` does not capture the case
    # when `options == None -> True`
    options = options or OPTIONS

    nodes = produce_nodes.produce_nodes(g)
    arcs = produce_all_arcs(g, options=options)

    digraph = nx.DiGraph()
    digraph.add_nodes_from(nodes)
    digraph.add_edges_from(arcs)

    return digraph


# We put this part from `produce_graph` because of the testing issues
#
def produce_all_arcs(g, options=OPTIONS):
    # () - empty generator
    arcs = ()
    for option in options:
        arcs = it.chain(arcs, RULES[option](g))

    return arcs
