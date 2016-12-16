#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)
mypath = os.path.join(dirname, '..')
mypath = os.path.abspath(mypath)
sys.path.insert(0, mypath)

from rdflib import RDF, RDFS, OWL
from rdflib.extras.infixowl import CastClass

# please note, that in our environment, after importing `sample_ontology`, we
# will have many variables such as mapped OWL classes and `g, ns` - rdflib
# graph, and the namespace
from grontocrawler.sample_ontology.hypo_ontology import *
from grontocrawler.graph import produce_arcs
from grontocrawler.entity_mapper import entity_mapper
from grontocrawler.utils import graph_utils


# # Tests graph creation rules
#
# Graphs are created by iterating through axiom triples and connecting nodes,
# corresponding to classes via restricted properties, please note that we do
# not make any difference between the type of the restriction (some, all, max)
#

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
def test_connect_existential():
    existential_arcs = produce_arcs.existential_arcs

    label    = entity_mapper.compute_short_name(positively_regulates.identifier, g)
    arc_type = str(OWL.someValuesFrom)
    arc_uri  = str(positively_regulates.identifier)
    source   = entity_mapper.compute_short_name(chondro_anabolism.identifier, g)
    targets  = [
        entity_mapper.compute_short_name(collagen_production.identifier, g),
        entity_mapper.compute_short_name(protoaeglycan_production.identifier, g)
        ]

    arc_data = {
        'label': label,
        'arc_type': arc_type,
        'arc_uri': arc_uri
    }

    for target in targets:
        arc = (source, target, arc_data)
        assert graph_utils.is_edge_in_edges(arc, existential_arcs(g))
