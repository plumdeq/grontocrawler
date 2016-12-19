#!/usr/bin/env python
# -*- coding: utf-8 -*-

# # Sample ontology on which we test grontocrawler
from rdflib.extras.infixowl import (
        Class, Property, CastClass, some
    )
from rdflib import Namespace, Graph, OWL
from rdflib.namespace import NamespaceManager

ns = Namespace('http://plumdeq.xyz/ontologies/hypothesis/')
ns_manager = NamespaceManager(Graph())
ns_manager.bind('hypo', ns, override=False)
ns_manager.bind('owl', OWL, override=False)
g = Graph()
g.namespace_manager = ns_manager


# ## Main classes
#
con = Class(ns.Continuant, graph=g)
occ = Class(ns.Occurent, graph=g)

# ##  Properties

# Main properties, such as `capable of`, `negatively regulates`
capable_of               =     Property(ns.capable_of, graph=g, domain=[occ], range=[occ])
negatively_regulates     =     Property(ns.negatively_regulates, graph=g, domain=[occ], range=[occ])
positively_regulates     =     Property(ns.positively_regulates, graph=g, domain=[occ], range=[occ])
reduces_levels_of        =     Property(ns.reduces_levels_of, graph=g, domain=[occ], range=[con])
increases_levels_of      =     Property(ns.increases_levels_of, graph=g, domain=[occ], range=[con])
inhibits                 =     Property(ns.inhibits, graph=g, domain=[occ], range=[occ])
activates                =     Property(ns.activates, graph=g, domain=[occ], range=[occ])

# ## Atomic continuants
#
# We model basic classes in our hypothesis ontology, which represent bio
# macro-molecules, biomolecules and cells in the cartillage
#
# * chondrocytes (cells)
# * cytokines (biomolecules), pro-inflammatory guys
# * tnf-alpha (biomolecule), mmp13 (enzyme), adamt (enzyme) bad guys
# * collagen, protoglyecan (macro-molecules) good guys
chondrocytes = Class(ns.Chondrocytes, graph=g, subClassOf=[con])
collagen = Class(ns.Collagen_type_II, graph=g, subClassOf=[con])
protoaeglycan = Class(ns.Protoaeglycan, graph=g, subClassOf=[con])
tnf_alpha = Class(ns.TNF_alpha, graph=g, subClassOf=[con])
mmp13 = Class(ns.MMP13, graph=g, subClassOf=[con])
adamt = Class(ns.Adamt, graph=g, subClassOf=[con])

# ## Atomic occurrents
#
# Atomic occurrents include anabolic/catabolic activities of continuants,
# production of certain molecules and destruction or disassembly of certain
# molecules

# processes linked with `chondrocytes`
chondro_anabolism = Class(ns.Chondrocytes_anabolism_activity, graph=g, subClassOf=[occ])
chondro_catabolism = Class(ns.Chondrocytes_catabolism_activity, graph=g, subClassOf=[occ])
chondro_apoptosis = Class(ns.Chondrocytes_apoptosis, graph=g, subClassOf=[occ])


# processes linked with production of molecules
collagen_production = Class(ns.Collagen_production, graph=g, subClassOf=[occ])
protoaeglycan_production = Class(ns.Protoaeglycan_production, graph=g, subClassOf=[occ])
tnf_production = Class(ns.TNF_alpha_production, graph=g, subClassOf=[occ])
mmp13_production = Class(ns.MMP13_production, graph=g, subClassOf=[occ])
adamt_production = Class(ns.Adamt_production, graph=g, subClassOf=[occ])

# processes which are hidden, our system should suggest them
tnf_overproduction = Class(ns.TNF_alpha_overproduction, graph=g, subClassOf=[occ])

# ## Causal relations via restrictions
#
# * anabolism of chondrocytes is good for collagen, protoglyecans production
# * catabolism of chondrocytes is good for tnf-alpha, mmp13, adamt production
# * tnf_alpha inihibts collagen/protoglyecan production
# * mmp13 digests available collagen
# * adamt digest available protoglyecan

# assigning new parents only adds them, previous parents are not deleted
chondro_anabolism.subClassOf = [
        (positively_regulates | some | collagen_production),
        (positively_regulates | some | protoaeglycan_production)
    ]

chondro_catabolism.subClassOf = [
        (positively_regulates | some | tnf_production),
        (positively_regulates | some | mmp13_production),
        (positively_regulates | some | adamt_production)
    ]

tnf_overproduction.subClassOf = [
        (inhibits | some | chondro_anabolism),
        (activates | some | chondro_catabolism)
    ]

tnf_production.subClassOf = [
        (increases_levels_of | some | tnf_alpha)
    ]

mmp13_production.subClassOf = [
        (reduces_levels_of | some | collagen)
    ]

adamt_production.subClassOf = [
        (reduces_levels_of | some | protoaeglycan)
    ]
