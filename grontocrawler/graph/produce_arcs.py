#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# # Produce arcs of the graph of the ontology
#
# We go through different rules and produce arcs from the axioms
from rdflib import RDF, RDFS, OWL, BNode

from grontocrawler.axioms import axiom_iterators
from grontocrawler.entity_mapper import entity_mapper
from grontocrawler.utils import utils


# ## Existential arcs
#
# We divide into the `iteration`, and `arc creation`, the latter can be
# `memoized`
#
# ```python
#    # Extract R-predecessors of a, i.e.,
#        (a, subof, bnode),
#        (bnode, is-a, OWL.restriction),
#        (bnode, OWL.onProperty, r),
#        (bnode, OWL.someValuesFrom, c)
#
#    Should extract "c"
# ```

@utils.memo
def produce_existential_arc(restriction_bnode, g):
    """
    Memoized on `restriction` of type `BNode` production of existential arcs
    """
    # there can only be one restriction_bnode on one property
    # here we collect, source, label of the arc, and the target
    source_cls   = next(g.subjects(RDFS.subClassOf, restriction_bnode))
    obj_property = next(g.objects(restriction_bnode, OWL.onProperty))
    r_successor  = next(g.objects(restriction_bnode, OWL.someValuesFrom))

    # we assume only atomic concepts in the filler of the restriction
    if not isinstance(r_successor, BNode):
        source_label = entity_mapper.compute_short_name(source_cls, g)
        arc_label    = entity_mapper.compute_short_name(obj_property, g)
        target_label = entity_mapper.compute_short_name(r_successor, g)
        arc_uri      = str(obj_property)
        arc_type     = str(OWL.someValuesFrom)

        arc_data = {
            'label': arc_label,
            'arc_uri': arc_uri,
            'arc_type': arc_type
        }

        arc = (source_label, target_label, arc_data)

        return arc

    return None


def existential_arcs(g):
    """
    Go through triples of restrictions and look for a suitable pattern
    """
    for restriction_bnode in axiom_iterators.restriction_bnodes(g):
        arc = produce_existential_arc(restriction_bnode, g)

        yield arc
