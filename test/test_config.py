# coding utf-8
"""
Sanity checks for the config of Grontocrawler

"""
import pytest


def test_msh_onto(get_test_graph):
    """Read in test ontology, graph should not be empty"""
    g = get_test_graph

    assert len(g) > 0


@pytest.mark.fma
def test_fma_onto(get_fma_graph):
    """Read in fma in ntriples, the graph should not be empty"""
    g = get_fma_graph

    assert len(g) > 0
