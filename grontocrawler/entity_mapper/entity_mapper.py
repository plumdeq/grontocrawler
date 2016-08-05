#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:author: Asan Agibetov

Entity mapper which essentially gives the resource for a given keyword, it uses
fuzzy string match on labels (if available), otherwise on URIs, and returns the
best match

"""
from rdflib import RDF, OWL, URIRef
from fuzzywuzzy import process

from grontocrawler.utils import utils
from grontocrawler.axioms import extract_axioms


@utils.memo
def match_entity(query, g):
    """
    (string, rdflib.Graph) -> URI

    Args:
        query (string): Keyword search term
        g (rdflib.Graph): Input graph

    Returns:
        URI (rdflib.URI): URI of the resource

    Matches URI resource for given keyword

    """
    # "Long bone" -> "Long_bone": otherwise fuzzy matches "Long bone" to "Bone"
    query = query.replace(" ", "_")

    # cached call
    all_entities = entities(g)

    label, score, uri = process.extractOne(query, all_entities)

    # Notify if match score is too low
    if score < 50:
        print("Very low match score {}".format(score))

    return URIRef(uri)


@utils.memo
def entities(g):
    """
    entities(rdflib.Graph) -> { uri: label | uri }

    constructs a cached dictionary of uris to labels

    """
    entities = {}
    owl_classes = extract_axioms.owl_classes(g)

    for owl_class in owl_classes:
        try:
            label = str(g.label(owl_class))
            if not label:
                _, _, label = g.compute_qname(owl_class)

        except Exception:
            label = str(owl_class)

        entities[str(owl_class)] = label

    return entities
