#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Convert graph structure to `dot` graphviz format
#
# A set of IO scripts to convert from one data structure to another. For
# instance to go from a digraph to a dot file, or a graph structure suitable
# for `vis.js`.
import sys

from grontocrawler.graph import produce_graph

# Creat `dot` from digraph representation
#
def to_dot(g, stream=sys.stdout, options=None):
    """
    Args:
        - g (rdflib.graph): RDF graph to transform into `dot` representation
        - stream (default: sys.stdout | file): Where to write the output
    Returns:
        - (graph): `dot` representation of the graph

    """
    digraph = produce_graph.produce_graph(g, options=options)

    stream.write('digraph g {\n')

    # draw nodes, i.e.
    for (node, node_data) in digraph.nodes_iter(data=True):
        node_str = '"%s" [label="%s"] ;\n'
        stream.write(node_str % (node, node_data['node_label']))

    for (source, target, edge_data) in digraph.edges_iter(data=True):
        edge_str = '"%s" -> "%s" [label="%s"] ;\n'
        stream.write(edge_str % (source, target, edge_data['arc_label']))

    stream.write('}\n')

    return g
