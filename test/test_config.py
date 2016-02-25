# coding utf-8
"""
Sanity checks for the config of Grontocrawler

"""

def test_config(get_test_graph):
	"""Read in test ontology, graph should not be empty"""
	g = get_test_graph

	assert len(g) > 0