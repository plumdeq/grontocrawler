# coding utf-8
"""
Utils module, i.e., transformations of strings, urls etc.

:author: Asan Agibetov

"""
from rdflib import RDF, RDFS, OWL
from functools import wraps


def memo(f):
    """Memoization for function $f$"""
    cache = {}

    @wraps(f)
    def wrap(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]

    return wrap


@memo
def compute_short_name(resource, g):
    """
    (rdflib.URI, rdflib.Graph) -> string

    resource (rdflib.URI): resource for which we compute superclasses
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


@memo
def triples_for_class(resource, g):
    """
    (rdflib.URI) -> [(s, p, o)]

    Extracts the necessary triples for a given class (label, comment etc)

    """
    triples = []

    if not (resource, RDF.type, OWL.Class) in g:
        return triples

    # if label is available add it too
    label = g.label(resource)
    comment = g.comment(resource)

    if label:
        triples.append((resource, RDFS.label, label))

    if comment:
        triples.append((resource, RDFS.comment, comment))

    triples.append((resource, RDF.type, OWL.Class))

    return triples


def same_edge_lists(edge_list_1, edge_list_2):
    """
    ([(source, target, dict(attributes)],
     [(source, target, dict(attributes)]) -> Bool

    Compares edge lists for NetworkX, especially the values of attribute
    dictionaries

    ASSUMPTION:
        edge lists are ordered

    """
    for (edge_1, edge_2) in zip(edge_list_1, edge_list_2):
        if not same_dictionaries(edge_1[2], edge_2[2]):
            return False

    return True


def same_dictionaries(dict_1, dict_2):
    """
    ({ 'key': 'value', ...},
     { 'key': 'value', ...}) -> Bool

    Compares simple objects (not nested), goes into keys and compares their
    values

    """
    diffkeys = [k for k in dict_1 if dict_1[k] != dict_2[k]]

    return len(diffkeys) == 0
