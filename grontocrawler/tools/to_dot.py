#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# put on path `grontocrawler` package
#
import os
import sys


gronto_folder = os.path.dirname(os.path.abspath(__file__))
gronto_folder = os.path.join(gronto_folder, '../..')
sys.path.insert(0, gronto_folder)

from rdflib import Graph

import argparse
from grontocrawler.io import to_dot
# CL tool to convert OWL ontologies into `dot` graph format
#
def main():
    parser = argparse.ArgumentParser()

    def_input = os.path.join(gronto_folder, './shared/ontology/hypo_onto.owl')
    def_output = os.path.join(gronto_folder, './shared/dot/digraph.dot')

    parser.add_argument('-i', '--input-ontology', default=def_input)
    parser.add_argument('-f', '--ontology-format', default='turtle')
    parser.add_argument('-o', '--output-dot', default=def_output)
    # rules for graph edge production
    parser.add_argument('--options', nargs='+', default=None)

    args = parser.parse_args()

    g = Graph().parse(args.input_ontology, format=args.ontology_format)

    with open(args.output_dot, 'w') as f:
        to_dot.to_dot(g, stream=f, options=args.options)


if __name__ == '__main__':
    main()
