#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: Asan Agibetov
#
# # Axiom iterators
#
# These iterators go through triples in a graph, which serve as *entry-points*
# to the encoding of the OWL axioms. For instance, subclass axioms will iterate
# through triples of the form
#
# ```turtle
# (None, RDFS.subClassOf, None)
# ```
from rdflib import RDF, RDFS, OWL, URIRef, BNode

def subclass_axioms(g):
    """
    Extract triples of the form `(None, RDFS.subClassOf, None)`, one triple per axiom

    Args:
        g (:py:class:`rdflib.Graph`): RDF graph on which we operate

    Returns:
        iterator: one triple per axiom in RDF graph ``g``

    """
    for triple in g.triples((None, RDFS.subClassOf, None)):
        yield triple
