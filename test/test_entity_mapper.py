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
from grontocrawler.sample_ontology.hypo_ontology_with_mistakes import *
from grontocrawler.entity_mapper import entity_mapper

# # Test entity mapper
#
# Entity mapper gives you identifiers of the RDF resources which you can match
# with strings or keywords

def test_simple_entity():
    con_matched = entity_mapper.match_entity('Continuant', g)
    assert con_matched == con.identifier

    occ_matched = entity_mapper.match_entity('Occurrent', g)
    assert occ_matched == occ.identifier


def test_compute_shortname():
    con_matched = entity_mapper.match_entity('continuant', g)
    assert entity_mapper.compute_short_name(con_matched, g) == 'Continuant'

    occ_matched = entity_mapper.match_entity('Occurrent', g)
    assert entity_mapper.compute_short_name(occ_matched, g) == 'Occurent'
