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


# Only among atomic OWL classes
def is_a_axioms(g):
    for triple in g.triples((None, RDFS.subClassOf, None)):
        s, p, o  = triple
        if not isinstance(s, BNode) and not isinstance(o, BNode):
            yield triple


def owl_class_uris(g):
    """
    Extracts uris of all OWL classes, which are not BNodes

    Args:
        g (:py:class:`rdflib.Graph`): RDF graph on which we operate

    Returns:
        list: list of URIs of OWL.classes

    """
    for cls in g.subjects(RDF.type, OWL.Class):
        if isinstance(cls, URIRef):
            yield cls


def anonymous_class_bnodes(g):
    """
    Extracts BNodes of all OWL classes

    Args:
        g (:py:class:`rdflib.Graph`): RDF graph on which we operate

    Returns:
        list: list of BNodes of OWL.classes

    """
    for anonymous_cls in g.subjects(RDF.type, OWL.Class):
        if isinstance(anonymous_cls, BNode):
            yield anonymous_cls


def restriction_bnodes(g):
    """
    Generator which gives all BNodes (identifiers) which are restrictions from a graph `g`
    """
    for restriction_bnode in g.subjects(RDF.type, OWL.Restriction):
        if isinstance(restriction_bnode, BNode):
            yield restriction_bnode
