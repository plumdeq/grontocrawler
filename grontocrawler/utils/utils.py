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
