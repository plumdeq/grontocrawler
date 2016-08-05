#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:author: Asan Agibetov

Extracts OWL EL axioms in the given ontology. In particular it allows us to
decompose ontology into axioms:

* subclassof
* equivalentclass
* domain
* range

Based on the extracted axioms we could then create

* graphs for visualization
* extract subontologies (i.e., triples)
* compute similarity among the concepts

"""
from rdflib import RDF, RDFS, OWL, URIRef, BNode
from grontocrawler.utils import utils


# axioms taken into account
axioms_map = {
    'subclass': RDFS.subClassOf,
    'equivalent': OWL.equivalentClass,
    'domain': RDFS.domain,
    'range': RDFS.range
}


@utils.memo
def extract_axioms(g):
    """
    Extract triples for all axioms, one triple per axiom

    Args:
        g (:py:class:`rdflib.Graph`): RDF graph on which we operate

    Returns:
        dict: one triple per axiom in RDF graph ``g``

    """
    axioms = {}

    for axiom, uri in axioms_map.items():
        triples = [triple
                   for triple in g.triples((None, uri, None))]
        axioms[axiom] = triples

    return axioms


@utils.memo
def owl_classes(g):
    """
    Extracts uris of all OWL classes

    Args:
        g (:py:class:`rdflib.Graph`): RDF graph on which we operate

    Returns:
        list: list of URIs of OWL.classes

    """
    return [cls for cls in g.subjects(RDF.type, OWL.Class)
                if isinstance(cls, URIRef)]

@utils.memo
def anonymous_classes(g):
    """
    Extracts BNodes of all OWL classes

    Args:
        g (:py:class:`rdflib.Graph`): RDF graph on which we operate

    Returns:
        list: list of BNodes of OWL.classes

    """
    return [cls for cls in g.subjects(RDF.type, OWL.Class)
                if isinstance(cls, BNode)]
