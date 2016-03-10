# coding utf-8
"""
Extract ontology modules, i.e. set of triples

"""
from rdflib import Graph, BNode

from grontocrawler.graph.create_graph import get_successors


def extract_module(start_queue, g, max_to_crawl=100, max_depth=10):
    """
    ([rdflib.URI], rdflib.Graph) -> rdflib.Graph

    resource (rdflib.URI): resource for which we extract module
    g (rdflib.Graph): RDF graph

    """
    ontomodule = Graph()
    ontomodule.namespace_manager = g.namespace_manager

    visited = []
    to_crawl = start_queue
    depth = 0

    # crawl until the queue is not empty
    while to_crawl:
        print("size of to_crawl: {}, size of visited: {}, depth: {}".format(
            len(to_crawl), len(visited), depth))
        next_node = to_crawl.pop()

        # control the depth
        depth = depth + 1
        if depth > max_depth:
            break

        assert not any(isinstance(x, BNode) for x in to_crawl), "Caught BNodes"

        if next_node not in visited:
            # mark nodes which we have already visited
            visited = visited + [next_node]
            successor_objs = get_successors(next_node, g)

            for successor_obj in successor_objs:
                if len(to_crawl) <= max_to_crawl:
                    to_crawl = to_crawl + successor_obj["uris"]
                    # add all triples
                    for triple in successor_obj["triples"]:
                        ontomodule.add(triple)

    return ontomodule
