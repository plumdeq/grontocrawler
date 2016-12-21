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

# # Testing axiom iterators
from rdflib import RDF, RDFS, OWL, BNode, URIRef

# please note, that in our environment, after importing `sample_ontology`, we
# will have many variables such as mapped OWL classes and `g, ns` - rdflib
# graph, and the namespace
from grontocrawler.sample_ontology.hypo_ontology import *
from grontocrawler.axioms import axiom_iterators

# Check that subclass axioms are correctly iterated
# Note: that axioms in this case are triples (None, RDFS.subClassOf, None)
def test_atomic_subclass_axioms():
    subclass_axioms = axiom_iterators.subclass_axioms

    # all triples contain RDFS.subClassesOf
    for (s, p, o) in subclass_axioms(g):
        assert p == RDFS.subClassOf

    # known subclassof assertions between atomic classes can be found
    assert (tnf_alpha.identifier, RDFS.subClassOf, con.identifier) in subclass_axioms(g)
    assert (chondro_anabolism.identifier, RDFS.subClassOf, occ.identifier) in subclass_axioms(g)


# No bnodes should be among owl classes
def test_owl_classes_uris():
    owl_class_uris = axiom_iterators.owl_class_uris

    for owl_class_uri in owl_class_uris(g):
        assert not isinstance(owl_class_uri, BNode)
        assert (owl_class_uri, RDF.type, OWL.Class) in g


# Only bnodes should be among anonymous classes
def test_anonymous_class_bnodes():
    anonymous_class_bnodes = axiom_iterators.anonymous_class_bnodes

    for anonymous_class_bnode in anonymous_class_bnodes(g):
        assert isinstance(anonymous_class_bnode, BNode)


# Only bnodes should be among restrictions
def test_anonymous_class_bnodes():
    restriction_bnodes = axiom_iterators.restriction_bnodes

    for restriction_bnode in restriction_bnodes(g):
        assert isinstance(restriction_bnode, BNode)
        assert (restriction_bnode, RDF.type, OWL.Restriction) in g

# No bnodes as subject or object
def test_is_axioms():
    is_a_axioms = axiom_iterators.is_a_axioms

    for triple in is_a_axioms(g):
        s, p, o = triple
        assert not isinstance(s, BNode)
        assert not isinstance(o, BNode)
        assert p == RDFS.subClassOf
