# coding utf-8
"""
Tests edge creation from RDF graph to a graph

"""
from rdflib import RDFS

from grontocrawler.entity_mapper import entity_mapper
from grontocrawler.graph import create_edges


def test_direct_superclasses(get_test_graph):
	"""Should return correct direct superclasses"""
	g = get_test_graph
	femur = entity_mapper.match_entity("Femur", g)
	long_bone = entity_mapper.match_entity("Long_bone", g)
	triple = (femur, RDFS.subClassOf, long_bone)

	superclasses = create_edges.get_direct_superclasses(femur, g)

	assert long_bone in superclasses["uris"]
	assert triple in superclasses["triples"]
	assert "Long bone" in superclasses["short_names"]