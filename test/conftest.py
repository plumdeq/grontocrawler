# coding utf-8
"""
Initit KB fixture for tests of Grontocrawler

"""
import pytest
from rdflib import Graph

from grontocrawler import config_test


@pytest.fixture(scope="module")
def get_test_graph():
    """Parse the test MSH ontology"""
    # Get dictionary object with all configs
    test_config = config_test.config
    g = Graph().parse(test_config["msh_test_onto"])

    return g


@pytest.fixture(scope="module")
def get_fma_graph():
    """Parse FMA-EL in turtle syntax and return an rdflib Graph"""
    test_config = config_test.config
    g = Graph().parse(test_config["fma_el_turtle"], format="turtle")

    return g
