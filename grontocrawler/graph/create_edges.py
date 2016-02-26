# coding utf-8
"""
Creates edges out of the RDF graph

:author: Asan Agibetov

"""
from rdflib import RDF, RDFS, OWL, BNode

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
    edges = []

    for superclass in g.objects(resource, RDFS.subClassOf):
        if (superclass, RDF.type, OWL.Class) in g:
            uris.append(superclass)
            triples.append((resource, RDFS.subClassOf, superclass))

            # compute short names for edges ids
            short_name_resource = utils.compute_short_name(resource, g)
            short_name_superclass = utils.compute_short_name(superclass, g)

            short_names.append(short_name_superclass)

            edges.append((short_name_resource, short_name_superclass,
                         {'relation': 'subClassOf'}))

    return {
        "short_names": short_names,
        "uris": uris,
        "triples": triples,
        "edges": edges,
        "edge_type": "is-a"

    }


def get_r_predecessors(resource, g):
    """
    (rdflib.URI, rdflib.Graph) -> {
        short_names: [label or short_name],
        uris: [rdflib.URI],
        triples: [(resource, RDFS.subClassOf, superclass)]
    }

    resource (rdflib.URI): resource for which we compute superclasses
    g (rdflib.Graph): RDF graph

    Extract R-predecessors, i.e.,
        (a, subof, bnode),
        (bnode, is-a, OWL.restriction),
        (bnode, OWL.onProperty, r),
        (bnode, OWL.someValuesFrom, c)

    Should extract "c"

    """
    short_names = []
    uris = []
    triples = []
    edges = []

    # first get all the bnodes, i.e., restrictions
    restrictions = (restriction
                    for restriction in g.objects(resource, RDFS.subClassOf)
                    if isinstance(restriction, BNode) and
                    (restriction, RDF.type, OWL.Restriction) in g)

    # Now get all the R-predecessors as well as the object properties
    for restriction in restrictions:
        # there can only be one restriction on one property
        obj_property = next(g.objects(restriction, OWL.onProperty))

        # we assume only atomic concepts in the filler of the restriction
        r_predecessor = next(g.objects(restriction, OWL.someValuesFrom))
        uris.append(r_predecessor)

        # add r-predecessor axiom
        triples.extend([
            (resource, RDFS.subClassOf, restriction),
            (restriction, RDF.type, OWL.Restriction),
            (restriction, OWL.onProperty, obj_property),
            (restriction, OWL.someValuesFrom, r_predecessor)
        ])

        # get short names (aka sn)
        sn_r_predecessor = utils.compute_short_name(r_predecessor, g)
        sn_obj_property = utils.compute_short_name(obj_property, g)
        sn_resource = utils.compute_short_name(resource, g)

        short_names.append(sn_r_predecessor)

        edges.append((sn_resource, sn_r_predecessor,
                     {'relation': sn_obj_property}))

    return {
        "short_names": short_names,
        "uris": uris,
        "triples": triples,
        "edges": edges,
        "edge_type": "r-predecessor"
    }
