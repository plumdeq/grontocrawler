#!/usr/bin/env python

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

    args = parser.parse_args()

    g = Graph().parse(args.input_ontology, format=args.format_name)
    resource = entity_mapper.match_entity(args.signature, g)
    ontomodule = extract_module.extract_module([resource], g)

    with open(args.output_file, "w") as f:
        ontomodule.serialize(f)


if __name__ == '__main__':
    main()
