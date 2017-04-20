#!/usr/bin/env python
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

import argparse
from rdflib import Graph

from grontocrawler.ontomodule import extract_module
from grontocrawler.entity_mapper import entity_mapper
from grontocrawler import config_test


def main():
    """
    CLI to extract ontology modules

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-ontology',
                        default=config_test.config["msh_test_onto"])
    parser.add_argument('-s', '--signature')
    parser.add_argument('-f', '--format-name', default=None)
    parser.add_argument('-o', '--output-file', default="ontology/output.owl")
    parser.add_argument('-d', '--max-depth', default=10)
    parser.add_argument('-l', '--locality', default='top')

    args = parser.parse_args()

    g = Graph().parse(args.input_ontology, format=args.format_name)
    resource = entity_mapper.match_entity(args.signature, g)
    ontomodule = extract_module.extract_module(
        [resource], g, locality=args.locality, max_depth=args.max_depth)

    with open(args.output_file, "w") as f:
        ontomodule.serialize(f)


if __name__ == '__main__':
    main()
