#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:author: Asan Agibetov

Axiom decomposer scans axioms (primarily of type subclassof and equivalence)
and creates a hash with a key as the *left_hand_side* of an axiom. We only
treat axioms of OWL-EL, therefore we only accepts atomic classes on the left
hand side of an axiom.

This module contains functionalities needed for

* filter axioms that have a given signature (uri) in the lhs, or rhs (depends on the locality)
* maintain a hash based on a (signature, locality) -> triples
* compute a recursive signature of a hand side (i.e., extract uri of atomic concepts inside a complex definition)

"""
from rdflib import URIRef, BNode

from grontocrawler.axioms import extract_axioms


def filter_axioms_lhs(signature, axioms):
    """
    Filters subclassof or equivalence ``axioms`` that contain ``signature`` in the left hand side

    Args:
        axioms (dict): { 'subclass': [triple, ...], 'equivalent': [triple, ...]

    Returns:
        dict: filtered axioms the same structure as input

    """
    # one axiom is actually a triple (s, p, o)
    subclass_axioms = [(s, p, o)
                       for s, p, o in axioms['subclass']
                       if s == signature]

    equivalent_axioms = [(s, p, o)
                         for s, p, o in axioms['equivalent']
                         if s == signature]

    return {
        'subclass': subclass_axioms,
        'equivalent': equivalent_axioms
    }


def filter_atomic_complex(axioms):
    """
    Filters subclass and equivalent axioms in atomic (atomic concept in rhs)
    and complex (complex concept in rhs)

    Args:
        axioms (list): [triple, ...]

    Returns:
        list: atomic axioms
        list: complex axioms
    """
    # one axiom is actually a triple (s, p, o)
    atomic_axioms = [(s, p, o) for s, p, o in axioms if isinstance(o, URIRef)]
    complex_axioms = [(s, p, o) for s, p, o in axioms if isinstance(o, BNode)]

    return {
        'atomic': atomic_axioms,
        'complex': complex_axioms
    }


def extract_complex_rhs(axiom, g):
    """
    Extracts complex right hand side's triples. We assume it is simply an
    existential restriction.

    Args:
        axiom (tuple): (s, p, o), such that o is BNode
        g (:py:class:`rdflib.Graph`): RDF graph of our ontology

    Returns:
        list: list of triples

    """
    _, _, rhs_bnode = axiom

    if not isinstance(rhs_bnode, BNode):
        raise Exception('RHS should be complex, no BNode found in {}'.format(rhs))

    triples = [(s, p, o)
               for (s, p, o) in g.triples((rhs_bnode, None, None))]

    return triples + [axiom]


def extract_signature(axiom, g):
    """
    Extracts all URIRefs in the axiom. First we extract a possibly complex
    rhs of the axiom, and then extract only URIRefs

    Args:
        axiom (tuple): (s, p, o)
        g (:py:class:`rdflib.Graph`): RDF graph of our ontology
        classes:

    Returns:
        list: list of URIRefs

    """
    triples = []
    s, p, o = axiom
    # cached call for all owl_classes
    owl_classes = extract_axioms.owl_classes(g)

    # if rhs is complex
    if isinstance(o, BNode):
        triples = extract_complex_rhs(axiom, g)

    signature = set([])

    for (s, p, o) in triples:
        if s in owl_classes: signature.add(s)
        if o in owl_classes: signature.add(o)
        # in case we have recursively complex axioms
        if isinstance(s, BNode) or isinstance(o, BNode):
            print('attention recursively complex axiom {}'.format(axiom))

    return list(signature)
