#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: Asan Agibetov
#
# # Produce nodes of the graph of the ontology
#
# We go through all atomic classes and produce nodes
from rdflib import RDF, RDFS, OWL, BNode

from grontocrawler.axioms import axiom_iterators
from grontocrawler.entity_mapper import entity_mapper
from grontocrawler.utils import utils


# Memoized creation of a node from a URI
@utils.memo
def produce_node(owl_class_uri, g):
    if isinstance(owl_class_uri, BNode):
        return None

    node_id = str(owl_class_uri)
    node_label = entity_mapper.compute_short_name(owl_class_uri, g)
    node_uri = node_id

    node_data = {
            'node_label': node_label,
            'node_uri': node_uri
        }

    return (node_id, node_data)


def produce_nodes(g):
    """
    Go through all axioms corresponding to atomic owl classes and convert them
    into nodes

    """
    nodes = (produce_node(owl_class_uri, g)
             for owl_class_uri in axiom_iterators.owl_class_uris(g))

    for node in nodes:
        yield node
