# Grontocrawler: graph-based ontology exploration

[Grontcrawler (link)][grontocrawler] transforms OWL-EL ontologies (a restricted
subset, see paper for details) into undirected graphs by following rule-based,
fix-point edge-production procedure. Graph representation of ontologies allows
us to study the axiomatic structure of the underlying OWL-EL ontology (both
TBox and ABox, i.e., definitions and instances) by exploring its graph
representaion using the graph drawing techniques.

Demo:

* [Grontcrawler (link)][grontocrawler]

Related publications:

* Agibetov, Asan, Giuseppe Patanè, and Michela Spagnuolo. 2015.  “Grontocrawler: Graph-Based Ontology Exploration.” In *Smart Tools and Apps for Graphics - Eurographics Italian Chapter Conference*, ed by. Andrea Giachetti, Silvia Biasotti, and Marco Tarini, 67–76. The Eurographics Association.  doi:[10.2312/stag.20151293](https://doi.org/10.2312/stag.20151293).

Online presentations:

* [Eurographics conference on Smart Applications and Tools in Graphics (STAG) 2015 presentation][stag2015]

Applicability to other contexts:

* The framework is very general and will work on any OWL ontology (only OWL-EL axioms will be taken into account for the graph transformation for more expressive OWL profiles)

## LICENSE

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


[grontocrawler]: http://grontocrawler.plumdeq.xyz
[stag2015]: http://asan.agibetov.me/talks/stag2015
