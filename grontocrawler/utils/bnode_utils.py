#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rdflib import BNode, RDF, RDFS, OWL
from rdflib.extras.infixowl import CastClass

from grontocrawler.axioms import axiom_iterators


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

# # Utils functions working with BNodes
#
# These functions help in the manipulation of the blank nodes. In particular,
# removal of duplicate restrictions, or removal of orphan restrictions

def are_same_restrictions(g, r1, r2):
    """
    Restrictions are the same, if they are applied to the same property, and restrict the same concept

    ## Note

    We assume input is correct, i.e., restrictions are indeed restrictions

    Restriction.restrictionType -> URI of the restriction (OWL.someValuesFrom)
    Restriction.restrictionRange -> URI of the restricted class (either URI a OWL:Class, or a BNode)
    """
    r1_cls = CastClass(r1, g)
    r2_cls = CastClass(r2, g)

    # There is an issue, some of the BNodes couldn't be casted
    for (iden, cls) in ((r1, r1_cls), (r2, r2_cls)):
        if cls is None:
            print("Couldn't cast {}".format(iden))
            return False

    # easy to check equalities:
    # * same identifier
    # * not the same restriction type (some | all)
    # * not the same restricted property
    if r1_cls.identifier == r2_cls.identifier: return True
    if r1_cls.restrictionType != r2_cls.restrictionType: return False
    if r1_cls.onProperty != r2_cls.onProperty: return False

    # we do not go in depth and check whether two range BNodes are different
    if r1_cls.restrictionRange == r2_cls.restrictionRange: return True


def orphan_restrictions(g):
    """
    Orphan restrictions are the ones that don't have any subclass

    if no pattern `class1 a [a OWL.Restriction1]`, then delete `OWL.Restriction1`
    """
    for restr_bnode in axiom_iterators.restriction_bnodes(g):
        if not (None, RDFS.subClassOf, restr_bnode) in g:
            yield restr_bnode


def remove_duplicate_restrictions(g):
    """
    Duplicate restrictions are defined on the same property and restrict the same concept
    """
    # we need to keep a list of already removed bnodes
    removed_bnodes = []
    # pairwise comparison of bnodes casted into classes
    bnodes_to_check = (bnode_id
                       for bnode_id in axiom_iterators.restriction_bnodes(g)
                       if bnode_id not in removed_bnodes)
    for bnode_id in bnodes_to_check:
        others = (other
                  for other in axiom_iterators.restriction_bnodes(g)
                  if other != bnode_id)

        sames = (similar
                for similar in others
                if are_same_restrictions(g, similar, bnode_id))

        # delete same restrictions
        for same_restriction in sames:
            cls = CastClass(same_restriction, g)
            cls.delete()
            removed_bnodes.append(same_restriction)

def remove_orphan_restrictions(g):
    """
    Go through orphan restrictions and delete them
    """
    orphans = (CastClass(orphan, g)
               for orphan in orphan_restrictions(g))

    for orphan in orphans:
        orphan.delete()
