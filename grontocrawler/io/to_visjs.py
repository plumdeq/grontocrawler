#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Convert nx graph to visjs format
#
# Vis.js requires separate `nodes` and `edges` JSON objects
#
# Nodes should have `{ id: unique_id, other key:value parirs }`
# Edges should have `{ from: node_id, to: node_id, other key:value pairs }`
#
def convert_nodes(digraph):
    for node in digraph.nodes_iter(data=True):
        yield node


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


def convert_arcs(digraph):
    for arc in digraph.edges_iter(data=True):
        yield convert_arc(arc)
