# coding utf-8
"""
Tests for entity mapper which essentially gives the resource for a given keyword

""" 
from rdflib import Namespace


def match_entity(keyword, g):
	"""
	(string, rdflib.Graph) -> URI

	keyword (string): Keyword search term
	g (rdflib.Graph): Input graph

	URI (rdflib.URI): URI of the resource

	Matches URI resource for given keyword

	"""
	# g.namespaces return (short_form, URL) tuples
	namespaces = (Namespace(namespace) for _, namespace in g.namespaces())

	for namespace in namespaces:
		if namespace[keyword] in g.subjects():
			return namespace[keyword]

	return None