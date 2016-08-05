#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:author: Asan Agibetov

Creates a semantic graph, primarily for visualization, but perhaps we could
also build similarity matrices out of it. Essentially, it extracts all axioms,
splits into atomic and complex, and based on definitions interconnects concepts
with relationships

"""
import networkx as nx
from rdflib import OWL, RDF, RDFS, BNode, URIRef

from grontocrawler.axioms import (axiom_decomposer, extract_axioms)


def graph_viz(g):
    """
    Create a networkX undirected graph from an RDF graph, by using axiom decomposition

    Args:
        g (:py:class:`rdflib.Graph`): Input RDF graph

    Returns:
        (:py:class:`networkx.DiGraph`): directed graph representation of the ontology

    """
    digraph = nx.Graph()
    all_axioms = extract_axioms.extract_axioms(g)
    ac_axioms = extract_axioms.filter_atomic_complex(
        {
            'subclass': all_axioms['subclass'],
            'equivalent': all_axioms['equivalent']
        })

    return edges_complex(ac_axioms['complex'])


def edges_complex(complex_axioms, g):
    """
    Creates undirected edges from complex axioms

    Args:
        complex_axioms (list): [(s, p, o), ...] such that ``o`` is BNode
        g (:py:class:`rdflib.Graph`): Input RDF graph

    Returns:
        (list): [(from, to, {}), ...]

    """
    for complex_axiom in complex_axioms:
        triples = axiom_decomposer.extract_complex_rhs(complex_axiom, g)


def edges_from_complex_axiom(axiom, g):
    """
    Extracts possible edges from one complex axiom

    Args:
        axiom (tuple): (lhs, subclass | equivalent, bnode)
        g (:py:class:`rdflib.Graph`): Input RDF graph

    Essentially axiom should have the following triples

    .. code-block:: python

        [(source_class, subof, bnode),
         (bnode, is-a, OWL.restriction),
         (bnode, OWL.onProperty, r),
         (bnode, OWL.someValuesFrom, c)]

    """
    source_class, _, bnode = axiom
    on_property = next(g.objects(OWL.onProperty, bnode))
    target_class = next(g.objects(bnode, OWL.someValuesFrom))

    return (source_class, target_class,
            { 'relation_name': on_property })
