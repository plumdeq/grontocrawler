#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ## I/O conversion from/to different formats
#
# We have many classes of conversion of `networkx` graphs:
#
#   * `nx -> dot`, for dot graphs visualization
#   * `nx -> vis.js` for frontend javascript visualization
#
# same old trick to put this directory into the path
import os
import sys

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)
mypath = os.path.join(dirname, '..')
mypath = os.path.abspath(mypath)
sys.path.insert(0, mypath)

import pytest
import networkx as nx

from grontocrawler.io import to_visjs

# ## Fixtures
#
# Preparing the `nx` graph. Note that since the real `hypo nx graph` is posing
# issues, we only check on a very simple networkx graph
@pytest.fixture
def nx_graph():
    digraph = nx.DiGraph()
    nodes = range(5)
    edges = [
            ( 1, 2, { 'some_key': 'some_value' } ),
            ( 2, 3, { 'anyg_key': 'some_value' } ),
            ( 1, 4, { 'anyg_field': 'some_value' } ),
            ( 4, 2, { 'anyf_field': 'some_value' } ),
            ( 4, 3, { 'anye_field': 'some_value' } ),
        ]

    digraph.add_nodes_from(nodes)
    digraph.add_edges_from(edges)

    return digraph

#
# ## Test nx -> vis.js
#
def test_nodes_visjs(nx_graph):
    digraph = nx_graph

    visjs_nodes = list(to_visjs.convert_nodes(digraph))
    # since the format of nx nodes and visjs nodes stays the same, we only
    # check the length of the nodes list
    assert len(visjs_nodes) == len(digraph.nodes())


def test_edges_visjs(nx_graph):
    digraph = nx_graph

    visjs_arcs = list(to_visjs.convert_arcs(digraph))
    # should be same number of arcs, and each arc should have same from and
    # same to
    assert len(visjs_arcs) == len(digraph.edges())
