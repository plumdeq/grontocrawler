#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov

"""
   Copyright 2015-2017 Asan Agibetov <asan.agibetov@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

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
        stream.write(node_str % (node, node_data['label']))

    for (source, target, edge_data) in digraph.edges_iter(data=True):
        edge_str = '"%s" -> "%s" [label="%s"] ;\n'
        stream.write(edge_str % (source, target, edge_data['label']))

    stream.write('}\n')

    return g
