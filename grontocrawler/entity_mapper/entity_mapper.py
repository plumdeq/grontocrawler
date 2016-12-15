#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# Entity mapper which essentially gives the resource for a given keyword, it uses
# fuzzy string match on labels (if available), otherwise on URIs, and returns the
# best match
#
#
from rdflib import RDF, RDFS, OWL, URIRef
from fuzzywuzzy import process

from grontocrawler.utils import utils
from grontocrawler.axioms import axiom_iterators


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
    Constructs a cached dictionary of uris to labels

    Args:
        g (rdflib.Graph): Input graph

    Returns:
        (dict): ``{ uri: label | uri }``

    """
    entities = {}

    for owl_class in axiom_iterators.owl_class_uris(g):
        try:
            label = str(g.label(owl_class))
            if not label:
                _, _, label = g.compute_qname(owl_class)

        except Exception:
            label = str(owl_class)

        entities[str(owl_class)] = label

    return entities


@utils.memo
def compute_short_name(resource, g):
    """
    (rdflib.URI, rdflib.Graph) -> string

    resource (rdflib.URI): resource for which we compute short name
    g (rdflib.Graph): RDF graph

    Tries to extract label, if the label does not exist, then tries to divide
    the URI, otherwise simply return the string with the full URI

    """
    try:
        label = g.label(resource)

        if not label:
            ns, uri, qname = g.compute_qname(resource)
            return qname.replace("_", " ")

        return str(label)
    except Exception:
        return str(resource)


@utils.memo
def annotations(resource, g):
    """
    (rdflib.URI) -> [(s, p, o)]

    Extracts available annotation triples for a given class (label, comment
    etc)

    """
    triples = []

    if not ((resource, RDF.type, OWL.Class) in g) and \
            not ((resource, RDF.type, OWL.ObjectProperty)):
        return triples

    # if label is available add it too
    label = g.label(resource)
    comment = g.comment(resource)

    if label:
        triples.append((resource, RDFS.label, label))

    if comment:
        triples.append((resource, RDFS.comment, comment))

    if (resource, RDF.type, OWL.Class) in g:
        triples.append((resource, RDF.type, OWL.Class))

    elif (resource, RDF.type, OWL.ObjectProperty) in g:
        triples.append((resource, RDF.type, OWL.ObjectProperty))

    return triples
