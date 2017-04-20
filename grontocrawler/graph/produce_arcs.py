#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   Copyright 2015-2017 Asan Agibetov <asan.agibetov@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

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
    if isinstance(r_successor, BNode):
        return None

    source_id = str(source_cls)
    target_id = str(r_successor)

    arc_label = entity_mapper.compute_short_name(obj_property, g)
    arc_uri   = str(obj_property)
    arc_type  = str(OWL.someValuesFrom)

    arc_data = {
        'label': arc_label,
        'arc_uri': arc_uri,
        'arc_type': arc_type
    }

    arc = (source_id, target_id, arc_data)

    return arc


def existential_arcs(g):
    """
    Go through triples of restrictions and look for a suitable pattern

    """
    arcs_itr = (produce_existential_arc(restriction_bnode, g)
                for restriction_bnode in axiom_iterators.restriction_bnodes(g))

    for arc in arcs_itr:
        yield arc


# ## Is-a arcs
#
# We divide into the `iteration`, and `arc creation`, the latter can be
# `memoized`. Note that we do not check that both: `source` and `target` are
# URIRefs, as it should be already taken care of by `is_a_axioms` generator.
#
# ```python
#    # Extract is-a arcs of a, i.e.,
#        (a, subof, b),
#
#    Should create "(a, b, b_data)"
# ```
@utils.memo
def produce_is_a_arc(triple, g):
    """
    Memoized on `triple` for the production of is-a arcs

    """
    s, p, o = triple
    # here we collect, source, label of the arc, and the target
    source_id = str(s)
    target_id = str(o)

    arc_label = entity_mapper.compute_short_name(p, g)
    arc_uri   = str(p)
    arc_type  = str(p)

    arc_data = {
        'label': arc_label,
        'arc_uri': arc_uri,
        'arc_type': arc_type
    }

    arc = (source_id, target_id, arc_data)

    return arc


def is_a_arcs(g):
    arcs_itr = (produce_is_a_arc(triple, g)
                for triple in axiom_iterators.is_a_axioms(g))

    for arc in arcs_itr:
        yield arc
