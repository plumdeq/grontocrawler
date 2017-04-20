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
import sys
import json

# # Convert nx graph to visjs format
#
# Vis.js requires separate `nodes` and `edges` JSON objects
#
# Nodes should have `{ id: unique_id, other key:value parirs }`
# Edges should have `{ from: node_id, to: node_id, other key:value pairs }`
#
def to_visjs_nodes(digraph):
    for node in digraph.nodes_iter(data=True):
        yield convert_node(node)


def convert_node(node):
    node_id, node_data = node

    # update dict with ids
    node_dict = {
            'id': node_id
        }
    node_dict.update(node_data)

    return node_dict

# ## Convert arcs
#
# We divide to a *generator* of converted arcs, and a converter function on one
# single arc (which can be memoized on source and target values)
def convert_arc(arc):
    source, target, arc_data = arc

    # update dict, by changing only from and to values
    arc_dict = {
            'from': source,
            'to': target
        }
    arc_dict.update(arc_data)

    return arc_dict


def to_visjs_arcs(digraph):
    for arc in digraph.edges_iter(data=True):
        yield convert_arc(arc)


# ## Write nodes
#
# Convert nodes to visjs format and write them in the JSON file
def write_nodes(digraph, stream=sys.stdout):
    stream.write('[\n')

    for visjs_node in to_visjs_nodes(digraph):
        json.dump(visjs_node, stream)
        stream.write(',\n')

    stream.write(']')

# ## Write arcs
#
# Convert arcs to visjs format and write them in the JSON file
def write_arcs(digraph, stream=sys.stdout):
    stream.write('[\n')

    for visjs_arc in to_visjs_arcs(digraph):
        json.dump(visjs_arc, stream)
        stream.write(',\n')

    stream.write(']')
