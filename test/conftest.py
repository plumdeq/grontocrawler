# coding utf-8
"""
Initit KB fixture for tests of Grontocrawler

"""
import pytest
from rdflib import Graph

from grontocrawler import config_test


@pytest.fixture(scope="module")
def get_test_onto():
	"""File path to the test ontology"""
	# Get dictionary object with all configs
	test_config = config_test.config
	g = Graph().parse(test_config["test_onto"])	

	return g