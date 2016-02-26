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


def test_same_edges():
    """Should correctly compare lists of edges with dictionaries as
    attributes"""
    edge_list_1 = [('a', 'b', {'relation': 'r-predecessor'}),
                   ('b', 'c', {'relation': 'is-a'})]

    edge_list_2 = [('a', 'b', {'relation': 'r-predecessor'}),
                   ('b', 'c', {'relation': 'is-a'})]

    edge_list_3 = [('a', 'b', {'relation': 'is-a'}),
                   ('b', 'c', {'relation': 'is-a'})]

    assert utils.same_edge_lists(edge_list_1, edge_list_2)
    assert not utils.same_edge_lists(edge_list_1, edge_list_3)


def test_same_dictionaries():
    """Two not nested dictionaries are equal if they have the same keys and the
    corresponding values are the same"""

    dict_1 = {'relation': 'r-predecessor'}
    dict_2 = {'relation': 'is-a'}
    dict_3 = {'relation': 'r-predecessor'}

    assert not utils.same_dictionaries(dict_1, dict_2)
    assert utils.same_dictionaries(dict_1, dict_3)
