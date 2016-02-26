# coding utf-8
"""
Tests utils module, i.e., transformations of strings, urls etc.

:author: Asan Agibetov

"""
from grontocrawler.utils import utils
from grontocrawler.entity_mapper import entity_mapper


def test_get_shortname(get_test_graph):
    """Should compute qname and transform it to a readable short name"""
    g = get_test_graph

    # get resource's URL
    long_bone = entity_mapper.match_entity("Long bone", g)
    short_name = utils.compute_short_name(long_bone, g)

    assert short_name == "Long bone"
