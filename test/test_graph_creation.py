#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)
mypath = os.path.join(dirname, '..')
mypath = os.path.abspath(mypath)
sys.path.insert(0, mypath)

from rdflib import RDF, RDFS, OWL, BNode
from rdflib.extras.infixowl import CastClass

# please note, that in our environment, after importing `sample_ontology`, we
# will have many variables such as mapped OWL classes and `g, ns` - rdflib
# graph, and the namespace
from grontocrawler.sample_ontology.hypo_ontology import *
from grontocrawler.graph import produce_arcs, produce_nodes
from grontocrawler.entity_mapper import entity_mapper
from grontocrawler.utils import graph_utils
from grontocrawler.axioms import axiom_iterators


# # Tests graph creation rules
#
# Graphs are created by iterating through axiom triples and connecting nodes,
# corresponding to classes via restricted properties, please note that we do
# not make any difference between the type of the restriction (some, all, max)
#
# ## Warning
#
# Apparently there are these issues with context managers in `rdflib`, we
# should probably only test smaller portions of code. Like a simple production
# of an arc, for a given `restriction bnode`, instead of going through whole
# `graph`.

# Connect nodes via simple existential restriction
# known restrictions should be treated correctly
#
# ```python
# chondro_anabolism.subClassOf = [
#         (positively_regulates | some | collagen_production),
#         (positively_regulates | some | protoaeglycan_production)
#     ]
# ```
#
def test_existential_arcs():
    arc_label = entity_mapper.compute_short_name(positively_regulates.identifier, g)
    arc_type  = str(OWL.someValuesFrom)
    arc_uri   = str(positively_regulates.identifier)
    source    = str(chondro_anabolism.identifier)
    targets   = [
        str(collagen_production.identifier),
        str(protoaeglycan_production.identifier)
        ]

    arc_data = {
        'arc_label': arc_label,
        'arc_type': arc_type,
        'arc_uri': arc_uri
    }

    # find bnodes of the restrictions
    restriction_bnodes = [o for o in g.objects(chondro_anabolism.identifier, RDFS.subClassOf)
                            if isinstance(o, BNode) and (o, RDF.type, OWL.Restriction)]

    arcs = [produce_arcs.produce_existential_arc(restriction_bnode, g)
            for restriction_bnode in restriction_bnodes]

    for target in targets:
        arc = (source, target, arc_data)
        assert graph_utils.is_edge_in_edges(arc, arcs)


# All is-a relations should be propagated among atomic classes only
#
def test_is_a_arcs():
    arc_label = entity_mapper.compute_short_name(RDFS.subClassOf, g)
    arc_uri   = str(RDFS.subClassOf)
    arc_type  = str(RDFS.subClassOf)

    source    = str(tnf_alpha.identifier)
    targets   = [str(con.identifier)]

    arc_data = {
        'arc_label': arc_label,
        'arc_type': arc_type,
        'arc_uri': arc_uri
    }

    # find is-a axioms
    is_a_axioms = list(axiom_iterators.is_a_axioms(g))

    arcs = [produce_arcs.produce_is_a_arc(is_a_axiom, g)
            for is_a_axiom in is_a_axioms]

    for target in targets:
        arc = (source, target, arc_data)
        assert graph_utils.is_edge_in_edges(arc, arcs)


# All nodes correspond to atomic classes in the ontology
#
def test_number_nodes():
    num_classes = len(list(axiom_iterators.owl_class_uris(g)))

    assert num_classes == len(list(produce_nodes.produce_nodes(g)))

# Test some specific nodes which should correspond to existing classes
def test_produce_nodes():
    node_id = str(con.identifier)
    node_label = entity_mapper.compute_short_name(con.identifier, g)
    node_uri = node_id

    node_data = {
        'node_label': node_label,
        'node_uri': node_uri
    }

    node = (node_id, node_data)
    produced_node = produce_nodes.produce_node(con.identifier, g)

    assert graph_utils.are_same_nodes(node, produced_node)
