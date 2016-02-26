# coding utf-8
"""
Tests edge creation from RDF graph to a graph

"""
from rdflib import RDFS

from grontocrawler.entity_mapper import entity_mapper
from grontocrawler.graph import create_edges
from grontocrawler.utils import utils


def test_direct_superclasses(get_test_graph):
    """Should return correct direct superclasses"""
    g = get_test_graph

    femur = entity_mapper.match_entity("Femur", g)
    long_bone = entity_mapper.match_entity("Long_bone", g)

    # axioms for OWL
    triples = [(femur, RDFS.subClassOf, long_bone)]

    # edges for Graph
    edges = [("Femur", "Long bone", {'relation': 'subClassOf'})]
    edge_type = "is-a"

    superclasses = create_edges.get_direct_superclasses(femur, g)

    assert long_bone in superclasses["uris"]
    assert set(triples) == set(superclasses["triples"])
    assert "Long bone" in superclasses["short_names"]
    assert utils.same_edge_lists(edges, superclasses["edges"])
    assert edge_type == superclasses["edge_type"]


def test_r_predecessors(get_test_graph):
    """Should return correct r_predecessors"""
    g = get_test_graph

    femur = entity_mapper.match_entity("Femur", g)
    lower_limb = entity_mapper.match_entity("Lower limb", g)
    edges = [("Femur", "Lower limb", {'relation': 'partOf'})]
    edge_type = "r-predecessor"

    r_predecessors = create_edges.get_r_predecessors(femur, g)

    assert lower_limb in r_predecessors["uris"]
    assert "Lower limb" in r_predecessors["short_names"]
    assert utils.same_edge_lists(edges, r_predecessors["edges"])
    assert edge_type == r_predecessors["edge_type"]
