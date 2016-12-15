#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:author: Asan Agibetov

Utils module, i.e., transformations of strings, urls etc.

"""
from rdflib import RDF, RDFS, OWL
from functools import wraps
import time


def memo(f):
    """
    Memoization for function ``f``, if recompute is True, then we force
    recomputation

    Args:
        f (func): function to memoize

    """
    cache = {}

    @wraps(f)
    def wrap(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]

    return wrap


def timeit(f, log=True):
    """
    Times the execution of the function ``f``

    Returns:
        *: result of applying ``f`` to ``args`` and ``kw``
        float: time needed to execute ``f``

    Usage
    -----

    Either use it as

    .. code-block:: python

        @timeit
        def new_fn():
            ...

    Or re-alias the function

    .. code-block:: python

        new_fn = timeit(new_fn)

    """
    def timed(*args, **kw):
        tstart = time.time()
        result = f(*args, **kw)
        tend = time.time()

        if log:
            print('func:%r args: [%r, %r] took: %2.4f sec' % \
                    (f.__name__, args, kw, tend-tstart))

        return (result, tend-tstart)

    return timed


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
