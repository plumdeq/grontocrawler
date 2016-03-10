# coding utf-8
"""
Entity mapper which essentially gives the resource for a given keyword, it uses
fuzzy string match on labels (if available), otherwise on URIs, and returns the
best match

"""
from rdflib import Namespace, RDF, OWL, URIRef
from fuzzywuzzy import fuzz, process

from grontocrawler.utils import utils


@utils.memo
def match_entity(query, g):
    """
    (string, rdflib.Graph) -> URI

    query (string): Keyword search term
    g (rdflib.Graph): Input graph

    URI (rdflib.URI): URI of the resource

    Matches URI resource for given keyword

    """
    # keyword = keyword.replace(" ", "_")
    # # g.namespaces return (short_form, URL) tuples
    # namespaces = (Namespace(namespace) for _, namespace in g.namespaces())

    # for namespace in namespaces:
    #     if namespace[keyword] in g.subjects():
    #         return namespace[keyword]

    # return None
    # build a dictionary of entities { uri: label (if any, otherwise uri) }

    # "Long bone" -> "Long_bone": otherwise fuzzy matches "Long bone" to "Bone"
    query = query.replace(" ", "_")

    entities = {}

    for resource in g.subjects(RDF.type, OWL.Class):
        try:
            label = str(g.label(resource))
            if not label:
                _, _, label = g.compute_qname(resource)

        except Exception:
            label = str(resource)

        entities[str(resource)] = label

    label, score, uri = process.extractOne(query, entities)

    # Notify if match score is too low
    if score < 50:
        print("Very low match score {}".format(score))

    return URIRef(uri)
