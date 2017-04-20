#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:author: Asan Agibetov

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

Statistics on OWL axioms in the ontology. Essentially we compute and measure
timing for the following statistics

* subclassof, equivalentClass number of axioms
* domain, range number of axioms
* number of classes
* time needed to build entity mapper dictionary (uri -> label or uri)

"""
from rdflib import Graph

from grontocrawler.utils import utils
from grontocrawler.config_test import benchmark_ontologies
from grontocrawler.entity_mapper import entity_mapper
from grontocrawler.axioms import extract_axioms


def count_axioms(g):
    """
    Counts number of axioms in graph ``g``.

    Args:
        g (:py:class:`rdflib.Graph`): RDF graph on which we operate

    Returns:
        dict: dict with number of axioms per axiom in RDF graph ``g``

    """
    counts = {}

    axioms = extract_axioms.extract_axioms(g)

    for axiom, triples in axioms.items():
        counts[axiom] = len(triples)

    return counts


def stats_onto(onto_path, onto_format='nt', log=True):
    """
    Computes statistics for the ontology in the path ``onto_path``, encoded
    with the format ``onto_format``

    Args:
        onto_path (string): path to the ontology
        onto_format (string): encoding format of the ontology
        log (bool): level of logging

    Returns:
        dict: statistics of time executions and results of executions

    Number of axioms, classes, time needed to parse ontology, time needed to
    build entity dictionary, time needed to match a keyword to a resource

    """
    g = Graph()
    timeit = utils.timeit

    times = {}

    if log:
        print('\nExecution time for {}'.format(onto_path))

    # parse
    if log:
        print('\nParsing ontology\n=============')
    times['parsing'] = timeit(g.parse, log=log)(onto_path, format=onto_format)

    # axioms
    if log:
        print('\nCounting axioms\n=============')

    times['axioms'] = timeit(count_axioms, log=log)(g)

    # classes
    if log:
        print('\nCounting OWL classes\n=============')

    times['classes'] = timeit(extract_axioms.owl_classes, log=log)(g)

    # build entity mapper
    if log:
        print('\nBuilding entity mapper dicitonary\n====================')

    times['entity_mapper'] = timeit(entity_mapper.entities, log=log)(g)

    # match entity
    if log:
        print('\nMatching keyword to OWL class\n====================\n')

    keyword = 'Semitendinosis'
    times['match'] = timeit(entity_mapper.match_entity, log=log)(keyword, g)

    # print short summary
    print('==========={}=============\n'.format(onto_path))
    for criterion, stats in times.items():
        # first item in ``stats`` is the result of execution
        print('%s: exec time %2.4f secs' % (criterion, stats[1]))

    print('\n')

    return times


def stats_benchmark_ontos(log=True):
    """
    Calls ` :py:func:`stats_onto` for all benchmark ontologies

    Returns:
        dict: stats dict per ontology

    """
    stats = {}
    for onto_path in benchmark_ontologies:
        stats[onto_path] = stats_onto(onto_path, log=log)

    return stats
