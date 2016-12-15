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

# # Testing utils functions
#
# ## Testing bnode utils functions
from rdflib import RDF, RDFS, OWL
from rdflib.extras.infixowl import some
# please note, that in our environment, after importing `sample_ontology`, we
# will have many variables such as mapped OWL classes and `g, ns` - rdflib
# graph, and the namespace
from grontocrawler.sample_ontology.hypo_ontology import *
from grontocrawler.utils import bnode_utils


# orphan restrictions do not have subclasses, i.e., nobody uses them, assuming
# we do not allow restrictions on the left hand side of axioms
def test_remove_orphan_restrictions():
    # in the beginning, fresh graph should not contain orphan restrictions
    assert len(list(bnode_utils.orphan_restrictions(g))) == 0

    # add random restrictions
    negatively_regulates | some | tnf_alpha
    negatively_regulates | some | chondro_anabolism
    negatively_regulates | some | chondro_catabolism

    assert len(list(bnode_utils.orphan_restrictions(g))) == 3

    # remove orphan restrictions
    bnode_utils.remove_orphan_restrictions(g)
    # assert are empty
    assert len(list(bnode_utils.orphan_restrictions(g))) == 0

# restrictions applied to the same property, same type of restriction on the
# same concept (atomic) are the same
def test_same_restriction():
    # find existing restriction
    a = negatively_regulates | some | tnf_alpha
    b = negatively_regulates | some | chondro_anabolism
    c = negatively_regulates | some | tnf_alpha

    assert not bnode_utils.are_same_restrictions(g, a, b)
    assert bnode_utils.are_same_restrictions(g, a, a)
    assert bnode_utils.are_same_restrictions(g, a, c)
