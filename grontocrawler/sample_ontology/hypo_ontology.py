#!/usr/bin/env python
# -*- coding: utf-8 -*-

# # Sample ontology on which we test grontocrawler
from rdflib.extras.infixowl import (
        Class, Property, CastClass, some
    )
from rdflib import Namespace, Graph, OWL, Literal
from rdflib.namespace import NamespaceManager

ns = Namespace('http://plumdeq.xyz/ontologies/hypothesis/')
ns_manager = NamespaceManager(Graph())
ns_manager.bind('hypo', ns, override=False)
ns_manager.bind('owl', OWL, override=False)
g = Graph()
g.namespace_manager = ns_manager


# ## Main classes
#
con = Class(ns.Continuant, graph=g, comment=Literal('Material entity. Examples: cells, molecules, joints'))
occ = Class(ns.Occurent, graph=g, comment=Literal('Occuring processes, which start and end at some point'))

# ##  Properties

# Main properties, such as `capable of`, `negatively regulates`
capable_of = Property(ns.capable_of, graph=g, domain=[occ], range=[occ])
negatively_regulates = Property(ns.negatively_regulates, graph=g, domain=[occ], range=[occ])
positively_regulates = Property(ns.positively_regulates, graph=g, domain=[occ], range=[occ])
reduces_levels_of = Property(ns.reduces_levels_of, graph=g, domain=[occ], range=[con])
increases_levels_of = Property(ns.increases_levels_of, graph=g, domain=[occ], range=[con])
inhibits = Property(ns.inhibits, graph=g, domain=[occ], range=[occ])
activates = Property(ns.activates, graph=g, domain=[occ], range=[occ])
results_in = Property(ns.results_in, graph=g, domain=[occ], range=[occ])

# ## Atomic continuants
#
# We model basic classes in our hypothesis ontology, which represent bio
# macro-molecules, biomolecules and cells in the cartillage
#
# * chondrocytes (cells)
# * cytokines (biomolecules), pro-inflammatory guys
# * tnf-alpha (biomolecule), mmp13 (enzyme), adamt (enzyme) bad guys
# * collagen, protoglyecan (macro-molecules) good guys
chondrocytes = Class(
        ns.Chondrocytes,
        graph=g,
        subClassOf=[con],
        comment=Literal('Chondrocytes are the ontly cells in the knee cartilage')
    )
collagen = Class(
        ns.Collagen_type_II,
        graph=g,
        subClassOf=[con],
        comment=Literal('Collagen type II, macromolecule, together with Protoaeglycans, are the main building blocks of the cartilage.')
    )
protoaeglycan = Class(
        ns.Protoaeglycan,
        graph=g,
        subClassOf=[con],
        comment=Literal('A macromolecule, together with Collagen are the main building blocks of the cartilage')
    )
tnf_alpha = Class(
        ns.TNF_alpha,
        graph=g,
        subClassOf=[con],
        comment=Literal('A biomolecule which is capable of inhibiting collagen and protaeglycan production, the latter are necessary for the molecular stability of the cartilage')
    )
mmp13 = Class(
        ns.MMP13,
        graph=g,
        subClassOf=[con],
        comment=Literal('Enzyme which is capable of catalyzing chondrocytes catabolism activity, i.e., break down of collagen and protoaeglycans')
    )
adamt = Class(
        ns.Adamt,
        graph=g,
        subClassOf=[con],
        comment=Literal('Enzyme which is capable of catalyzing chondrocytes catabolism activity, i.e., break down of collagen and protoaeglycans')
    )

# ## Atomic occurrents
#
# Atomic occurrents include anabolic/catabolic activities of continuants,
# production of certain molecules and destruction or disassembly of certain
# molecules

# ## Processes linked with `chondrocytes`
chondro_anabolism = Class(
        ns.Chondrocytes_anabolism_activity,
        graph=g,
        subClassOf=[occ],
        comment=Literal('Chondrocytes anabolism activity is the process of construction of molecules from smaller units')
    )
chondro_catabolism = Class(
        ns.Chondrocytes_catabolism_activity,
        graph=g,
        subClassOf=[occ],
        comment=Literal('Chondrocytes catabolism activity is the process of separation of molecules. Opposite of chondrocytes anabolism')
    )
chondro_apoptosis = Class(
        ns.Chondrocytes_apoptosis,
        graph=g,
        subClassOf=[occ],
        comment=Literal('Chondrocytes apoptosis is the process where the chondrocytes, cells, are dying')
    )
chondro_hyper = Class(
        ns.Chondrocytes_hypertrophy,
        graph=g,
        subClassOf=[occ],
        comment=Literal('Increase in the volume of an organ or tissue due ot the enlargement of its component cells')
    )

# processes linked with production of molecules
collagen_production = Class(ns.Collagen_production, graph=g, subClassOf=[occ])
protoaeglycan_production = Class(ns.Protoaeglycan_production, graph=g, subClassOf=[occ])
tnf_production = Class(ns.TNF_alpha_production, graph=g, subClassOf=[occ])
mmp13_production = Class(ns.MMP13_production, graph=g, subClassOf=[occ])
adamt_production = Class(ns.Adamt_production, graph=g, subClassOf=[occ])

# processes which are hidden, our system should suggest them
tnf_overproduction = Class(ns.TNF_alpha_overproduction, graph=g, subClassOf=[occ])

# ## Processes outside cellular level
mechanical_overloading = Class(
        ns.Mechanical_overloading,
        graph=g,
        subClassOf=[occ],
        comment=Literal('Mechanical overloading of the cartilage, environmental factor')
    )

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

chondro_hyper.subClassOf = [
        (positively_regulates | some | mmp13_production),
        (positively_regulates | some | adamt_production),
        (negatively_regulates | some | chondro_anabolism)
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

# ## Causal relations outside of the cellular level
#
mechanical_overloading.subClassOf = [
        (results_in | some | chondro_catabolism),
        (results_in | some | chondro_apoptosis)
    ]
