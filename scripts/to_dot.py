#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
author: Asan Agibetov

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
# put on path `grontocrawler` package
#
import os
import sys


gronto_folder = os.path.dirname(os.path.abspath(__file__))
gronto_folder = os.path.join(gronto_folder, '..')
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
