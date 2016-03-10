# coding utf-8
"""
NetworkX graph creation from RDF graph

"""
from rdflib import BNode
import networkx as nx

from grontocrawler.graph import create_edges
from grontocrawler.utils import utils


def extract_subgraph(start_queue, g, locality="top", max_to_crawl=100, max_depth=10):
    """
    ([rdflib.URIRef], rdflib.Graph) -> networkx.Graph

    Extracts a subgraph by iteratively visiting breadth-first the graph, the
    traversal starts from the initial queue

    """
    nx_graph = nx.Graph()
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
            successor_objs = get_successors(next_node, g, locality=locality)

            # add more nodes only if we can allow crawling
            for successor_obj in successor_objs:
                if len(to_crawl) <= max_to_crawl:
                    to_crawl = to_crawl + successor_obj["uris"]
                    nx_graph.add_edges_from(successor_obj["edges"])

    return nx_graph


def get_successors(resource, g, locality="top"):
    """
    (rdflib.URIRef, rdflib.Graph) -> [sucessor_obj]

        sucessor_obj = {
            "short_names": short_names,
            "uris": uris,
            "triples": triples,
            "edges": edges,
            "edge_type": "r-predecessor"
        }

    Get successor objects for the resource and available edge production rules

    """
    # list of functions
    edge_production_rules = locality_rules(locality)

    # see the docstring
    sucessor_objs = [edge_production_rule(resource, g)
                     for edge_production_rule in edge_production_rules]

    return sucessor_objs


@utils.memo
def locality_rules(locality):
    """Select the list of rules for a given locality"""
    LOCALITY_RULES = {
        "top": [create_edges.get_direct_subclasses, create_edges.get_r_successors],
        "bottom": [create_edges.get_direct_superclasses, create_edges.get_r_predecessors]
    }
    return LOCALITY_RULES[locality]