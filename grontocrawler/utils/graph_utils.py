#!/usr/bin/env python
# -*- coding: utf-8 -*-

# # Utils functions for graph manipulation
#
def are_same_edges(edge1, edge2):
    """
    ((source, target, dict), (s2, t2, d2)) -> bool

    """
    s1, t1, d1 = edge1
    s2, t2, d2 = edge2

    # extremities of the edges should be the same
    if not (s1 == s2) or not (t1 == t2):
        return False

    if not are_same_dictionaries(d1, d2):
        return False

    return True


def are_same_edge_lists(edge_list_1, edge_list_2):
    """
    ([(source, target, dict(attributes)],
     [(source, target, dict(attributes)]) -> Bool

    Compares edge lists for NetworkX, especially the values of attribute
    dictionaries

    ASSUMPTION:
        edge lists are ordered

    """
    for (edge_1, edge_2) in zip(edge_list_1, edge_list_2):
        if not are_same_edges(edge_1, edge_2):
            return False

    return True


def are_same_dictionaries(dict_1, dict_2):
    """
    ({ 'key': 'value', ...},
     { 'key': 'value', ...}) -> Bool

    Compares simple objects (not nested), goes into keys and compares their
    values

    """
    # find out if the keys lists are the same
    if not dict_1.keys() == dict_2.keys():
        return False

    # keys are the same, we can simply compare values
    for k in dict_1:
        if dict_1[k] != dict_2[k]:
            return False

    return True


# We check whether a given edge (tuple) can be found in an edge iterator
#
def is_edge_in_edges(edge, edge_itr):
    any_same_edge = (are_same_edges(edge, other) for other in edge_itr)
    return any(any_same_edge)
