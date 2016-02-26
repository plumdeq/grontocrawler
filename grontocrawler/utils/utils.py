# coding utf-8
"""
Utils module, i.e., transformations of strings, urls etc.

:author: Asan Agibetov

"""


def compute_short_name(resource, g):
    """
    (rdflib.URI, rdflib.Graph) -> string

    resource (rdflib.URI): resource for which we compute superclasses
    g (rdflib.Graph): RDF graph

    """
    ns, uri, qname = g.compute_qname(resource)

    return qname.replace("_", " ")


def same_edge_lists(edge_list_1, edge_list_2):
    """
    ([(source, target, dict(attributes)],
     [(source, target, dict(attributes)]) -> Bool

    Compares edge lists for NetworkX, especially the values of attribute
    dictionaries

    ASSUMPTION:
        edge lists are ordered

    """
    for (edge_1, edge_2) in zip(edge_list_1, edge_list_2):
        if not same_dictionaries(edge_1[2], edge_2[2]):
            return False

    return True


def same_dictionaries(dict_1, dict_2):
    """
    ({ 'key': 'value', ...},
     { 'key': 'value', ...}) -> Bool

    Compares simple objects (not nested), goes into keys and compares their
    values

    """
    diffkeys = [k for k in dict_1 if dict_1[k] != dict_2[k]]

    return len(diffkeys) == 0
