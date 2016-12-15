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
from rdflib import RDF, RDFS, OWL

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
