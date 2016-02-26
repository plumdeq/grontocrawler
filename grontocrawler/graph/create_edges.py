# coding utf-8
"""
Creates edges out of the RDF graph

:author: Asan Agibetov

"""
from rdflib import RDF, RDFS, OWL

from grontocrawler.utils import utils


def get_direct_superclasses(resource, g):
    """
    (rdflib.URI, rdflib.Graph) -> {
    short_names: [label or short_name],
    uris: [rdflib.URI],
    triples: [(resource, RDFS.subClassOf, superclass)]
    }

    resource (rdflib.URI): resource for which we compute superclasses
    g (rdflib.Graph): RDF graph

    """
    short_names = []
    uris = []
    triples = []

    for superclass in g.objects(resource, RDFS.subClassOf):
        if (superclass, RDF.type, OWL.Class) in g:
            uris.append(superclass)
            triples.append((resource, RDFS.subClassOf, superclass))
            short_names.append(utils.compute_short_name(superclass, g))

    return {
        "short_names": short_names,
        "uris": uris,
        "triples": triples
    }
