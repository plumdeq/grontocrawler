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
#
# We write from `g` graph, the sample hypothesis ontology
#
from grontocrawler.sample_ontology.hypo_ontology import g
# CL tool to convert OWL ontologies into `dot` graph format
#
def main():
    parser     = argparse.ArgumentParser()

    def_output  = os.path.join(gronto_folder, './shared/ontology/hypo_onto.owl')

    parser.add_argument('-o', '--output-ontology', default=def_output)
    parser.add_argument('-f', '--ontology-format', default='turtle')

    args = parser.parse_args()

    with open(args.output_ontology, 'w') as f:
        f.write(g.serialize(format=args.ontology_format))


if __name__ == '__main__':
    main()
