# coding utf-8
"""
Tests ontomodule extraction

"""
from rdflib import RDF, RDFS, OWL, BNode

from grontocrawler.ontomodule import extract_module
from grontocrawler.entity_mapper import entity_mapper


def test_ontomodule_extraction(get_test_graph):
    """Check if all triples are extracted"""
    g = get_test_graph

    femur = entity_mapper.match_entity("Femur", g)
    # lower_limb = entity_mapper.match_entity("Lower limb", g)

    # ontomodule is rdflib.Graph
    ontomodule = extract_module.extract_module([femur], g)

    # assert that the r-predecessor axioms are there
    restrictions = (restriction
                    for restriction in ontomodule.objects(femur,
                                                          RDFS.subClassOf)
                    if isinstance(restriction, BNode) and
                    (restriction, RDF.type, OWL.Restriction) in g)

    assert len(list(restrictions)) != 0

    # Now assert all the R-predecessors as well as the object properties
    for restriction in restrictions:
        # there can only be one restriction on one property
        obj_property = next(g.objects(restriction, OWL.onProperty))

        # we assume only atomic concepts in the filler of the restriction
        r_predecessor = next(g.objects(restriction, OWL.someValuesFrom))

        # add r-predecessor axiom
        triples = [
            (femur, RDFS.subClassOf, restriction),
            (restriction, RDF.type, OWL.Restriction),
            (restriction, OWL.onProperty, obj_property),
            (restriction, OWL.someValuesFrom, r_predecessor)
        ]

        for triple in triples:
            assert triple in ontomodule