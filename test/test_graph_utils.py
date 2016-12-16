#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Asan Agibetov

# same old trick to put this directory into the path
import os
import sys

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)
mypath = os.path.join(dirname, '..')
mypath = os.path.abspath(mypath)
sys.path.insert(0, mypath)


# # Tests utils functions
# Tests utils module, i.e., transformations of strings, urls etc.

from grontocrawler.utils import graph_utils
# from grontocrawler.entity_mapper import entity_mapper


# def test_get_shortname(get_test_graph):
#     """Should compute qname and transform it to a readable short name"""
#     g = get_test_graph
#
#     # get resource's URL
#     long_bone = entity_mapper.match_entity("Long bone", g)
#     short_name = utils.compute_short_name(long_bone, g)
#
#     assert short_name == "Long bone"


# Should correctly compare lists of edges with dictionaries as attributes
def test_same_edge_lists():
    edge_list_1 = [('a', 'b', {'relation': 'r-predecessor'}),
                   ('b', 'c', {'relation': 'is-a'})]

    edge_list_2 = [('a', 'b', {'relation': 'r-predecessor'}),
                   ('b', 'c', {'relation': 'is-a'})]

    edge_list_3 = [('a', 'b', {'relation': 'is-a'}),
                   ('b', 'c', {'relation': 'is-a'})]

    edge_list_4 = [('b', 'b', {'relation': 'is-a'}),
                   ('b', 'c', {'relation': 'is-a'})]

    assert graph_utils.are_same_edge_lists(edge_list_1, edge_list_2)
    assert not graph_utils.are_same_edge_lists(edge_list_1, edge_list_3)
    assert not graph_utils.are_same_edge_lists(edge_list_3, edge_list_4)


# Should correctly compare nodes
def test_same_nodes():
    nodes = [('a',{'relation': 'r-predecessor'}),
             ('b',{'relation': 'is-a'}),
             ('a2',{'relation': 'r-predecessor', 'key': 'value'}),
             ('b2',{'relation': 'is-a', 'another': 'value'}),
             ('a',{'relation': 'r-predecessor'})]

    assert graph_utils.are_same_nodes(nodes[0], nodes[0])
    assert not graph_utils.are_same_nodes(nodes[0], nodes[1])
    assert graph_utils.are_same_nodes(nodes[0], nodes[-1])

# Two not nested dictionaries are equal if they have the same keys and the
# corresponding values are the same
def test_same_dictionaries():
    dict_1 = {'relation': 'r-predecessor'}
    dict_2 = {'relation': 'is-a'}
    dict_3 = {'relation': 'r-predecessor'}

    assert not graph_utils.are_same_dictionaries(dict_1, dict_2)
    assert graph_utils.are_same_dictionaries(dict_1, dict_3)


# All memebers of the edge list should be identified as members of the edge
# list. A different edge should not be identified as the member of the edge
# list
def test_edge_in_edge_itr():
    edge_list = [('a', 'b', {'relation': 'r-predecessor'}),
                 ('b', 'c', {'relation': 'is-a'}),
                 ('b', 'c', {'relation': 'is-a', 'label': 'hello there'}),
                 ('d', 'e', {'relation': 'is-a', 'label': 'hello there', 'some key': 'yet another'})
                 ]

    not_in_edge_list = ('a', 'b', {'relation': 'r-successor'})

    assert not graph_utils.is_edge_in_edges(not_in_edge_list, edge_list)

    for edge_in_list in edge_list:
        assert graph_utils.is_edge_in_edges(edge_in_list, edge_list)


# All members of nodes lists are in the node list, node outside the list is not
# in the list
def test_node_in_nodes_itr():
    node_list = [('a',{'relation': 'r-predecessor'}),
                 ('b',{'relation': 'is-a'}),
                 ('a2',{'relation': 'r-predecessor', 'key': 'value'}),
                 ('b2',{'relation': 'is-a', 'another': 'value'})]

    not_in_node_list = ('a',{'relation': 'r-predecessor', 'something': 'nothing'})

    for node_in_list in node_list:
        assert graph_utils.is_node_in_nodes(node_in_list, node_list)

    assert not graph_utils.is_node_in_nodes(not_in_node_list, node_list)
