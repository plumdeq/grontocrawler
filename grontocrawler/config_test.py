#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:author: Asan Agibetov

Config values for Grontocrawler during test phase

In particular it contains filenames of the benchmark ontologies

"""
import os

config = {
    "msh_test_onto": "ontology/msh_onto_test.owl",
    "fma_el_turtle": "ontology/fma-el.nt"
}

benchmark_ontologies_path = "/Users/asan/.ontologies/external/ntriples"
benchmark_ontologies = []
for root, dirs, files in os.walk(benchmark_ontologies_path):
    benchmark_ontologies = [os.path.join(root, f)
                            for f in files]
