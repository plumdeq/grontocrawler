# coding utf-8
"""
Extract ontology modules, i.e. set of triples

"""
from rdflib import Graph

from grontocrawler.graph.create_graph import get_successors


def extract_module(start_queue, g):
    """
    ([rdflib.URI], rdflib.Graph) -> rdflib.Graph

    resource (rdflib.URI): resource for which we extract module
    g (rdflib.Graph): RDF graph

    """
    ontomodule = Graph()
    ontomodule.namespace_manager = g.namespace_manager

    visited = []
    to_crawl = start_queue

    # crawl until the queue is not empty
    while to_crawl:
        next_node = to_crawl.pop()
        if next_node not in visited:
            # mark nodes which we have already visited
            visited = visited + [next_node]
            successor_objs = get_successors(next_node, g)

            for successor_obj in successor_objs:
                to_crawl = to_crawl + successor_obj["uris"]
                # add all triples
                for triple in successor_obj["triples"]:
                    ontomodule.add(triple)

    return ontomodule
