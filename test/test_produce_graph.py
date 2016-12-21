#!/usr/bin/env python
# -*- coding: utf-8 -*-
# same old trick to put this directory into the path
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
from grontocrawler.graph import produce_graph
from grontocrawler.entity_mapper import entity_mapper
from grontocrawler.utils import graph_utils

# # Test produce graph code
#
# Here we test that all the options for edge production are propagated properly
#
# ## Fixtures
#
def make_is_a_arc():
    source    = str(tnf_alpha.identifier)
    target    = str(con.identifier)
    arc_label = entity_mapper.compute_short_name(RDFS.subClassOf, g)
    arc_uri   = str(RDFS.subClassOf)
    arc_type  = str(RDFS.subClassOf)

    arc_data = {
        'arc_label': arc_label,
        'arc_type': arc_type,
        'arc_uri': arc_uri
    }

    arc = (source, target, arc_data)

    return arc


def make_existential_arc():
    source    = str(chondro_anabolism.identifier)
    target    = str(collagen_production.identifier)
    arc_label = entity_mapper.compute_short_name(
            positively_regulates.identifier, g)
    arc_uri   = str(positively_regulates.identifier)
    arc_type  = str(OWL.someValuesFrom)

    arc_data = {
        'arc_label': arc_label,
        'arc_type': arc_type,
        'arc_uri': arc_uri
    }

    arc = (source, target, arc_data)

    return arc

#
# ## Test is-a arcs
# * `is-a` arcs should be present
# * `existential` arcs should NOT be present
def test_is_a_arcs():
    options = ['is-a-arcs']
    digraph = produce_graph.produce_graph(g, options = options)

    # is-a arc should be in the digraph
    is_a_arc = make_is_a_arc()
    assert graph_utils.is_edge_in_edges(is_a_arc, digraph.edges_iter(data=True))

    # existential arc should not be in digraph
    existential_arc = make_existential_arc()
    assert not graph_utils.is_edge_in_edges(existential_arc, digraph.edges_iter(data=True))


# ## Test existential arcs
# * `is-a` arcs should NOT be present
# * `existential` arcs should be present
def test_existential_arcs():
    options = ['existential-arcs']
    digraph = produce_graph.produce_graph(g, options = options)

    # Is-a arc should not be in the digraph
    is_a_arc = make_is_a_arc()
    assert not graph_utils.is_edge_in_edges(is_a_arc, digraph.edges_iter(data=True))

    # existential arc should not be in digraph
    existential_arc = make_existential_arc()
    assert graph_utils.is_edge_in_edges(existential_arc, digraph.edges_iter(data=True))


# ## Test full graph
# * `is-a` arcs should be present
# * `existential` arcs should be present
def test_full_arcs():
    options = ['is-a-arcs', 'existential-arcs']
    digraph = produce_graph.produce_graph(g, options = options)

    # Is-a arc should not be in the digraph
    is_a_arc = make_is_a_arc()
    assert graph_utils.is_edge_in_edges(is_a_arc, digraph.edges_iter(data=True))

    # existential arc should not be in digraph
    existential_arc = make_existential_arc()
    assert graph_utils.is_edge_in_edges(existential_arc, digraph.edges_iter(data=True))
