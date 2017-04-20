#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: Asan Agibetov

"""
   Copyright 2015-2017 Asan Agibetov <asan.agibetov@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

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
            'label': node_label,
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
