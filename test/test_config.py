# coding utf-8
"""
Sanity checks for the config of Grontocrawler

"""

def test_config(get_test_onto):
	"""read in test ontology, graph should not be empty"""
	g = get_test_onto

	assert len(g) > 0