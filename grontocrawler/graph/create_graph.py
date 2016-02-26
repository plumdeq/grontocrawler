# coding utf-8
"""
NetworkX graph creation from RDF graph

"""
import networkx as nx
from grontocrawler.graph import create_edges


def extract_subgraph(start_queue, g):
    """
    ([rdflib.URIRef], rdflib.Graph) -> networkx.Graph

    Extracts a subgraph by iteratively visiting breadth-first the graph, the
    traversal starts from the initial queue

    """
    nx_graph = nx.Graph()
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
                nx_graph.add_edges_from(successor_obj["edges"])

    return nx_graph


def get_successors(resource, g):
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
    edge_production_rules = [create_edges.get_direct_superclasses,
                             create_edges.get_r_predecessors]

    # see the docstring
    sucessor_objs = [edge_production_rule(resource, g)
                     for edge_production_rule in edge_production_rules]

    return sucessor_objs
