# coding utf-8
"""
Test NetworkX graph creation from RDF graph

"""
import networkx as nx

from grontocrawler.entity_mapper import entity_mapper
from grontocrawler.graph import create_graph


def test_graph_bottom_locality(get_test_graph):
    """Should contain Lower limb when extracting Femur in the graph"""
    g = get_test_graph

    femur = entity_mapper.match_entity("Femur", g)
    locality = "bottom"

    nx_graph = create_graph.extract_subgraph([femur], g, locality=locality)

    assert nx_graph.has_edge('Femur', 'Lower limb')


def test_graph_iterative_bfs_bottom_locality(get_test_graph):
    """Should return full subgraph, extracted iteratively"""
    g = get_test_graph

    femur = entity_mapper.match_entity("Femur", g)
    locality = "bottom"

    nx_graph = create_graph.extract_subgraph([femur], g, locality=locality)

    print(nx_graph.nodes())

    assert nx.algorithms.shortest_paths.generic.has_path(
        nx_graph, 'Femur', 'Anatomical entity')
