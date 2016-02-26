# coding utf-8
"""
Tests for entity mapper which essentially gives the resource for a given keyword

"""
from grontocrawler.entity_mapper import entity_mapper


def test_entity_mapper(get_test_graph):
    """'Femur' keyword should resolve to the correct resource"""
    g = get_test_graph

    matched_resource_1 = entity_mapper.match_entity("Femur", g)
    matched_resource_2 = entity_mapper.match_entity("Long bone", g)

    assert matched_resource_1
    assert matched_resource_2
