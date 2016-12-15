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
from grontocrawler.axioms import axiom_iterators


# # Tests graph creation rules
#
# Graphs are created by iterating through axiom triples and connecting nodes,
# corresponding to classes via restricted properties, please note that we do
# not make any difference between the type of the restriction (some, all, max)
#

# Connect nodes via simple existential restriction
def test_connect_existential():
    subclass_axioms = axiom_iterators.subclass_axioms

    for (s, _, o) in subclass_axioms(g):
        pass
