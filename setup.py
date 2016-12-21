from setuptools import setup

setup(name='grontocrawler',
      version='0.3.3',
      description='transformation of OWL ontologies into graphs',
      author='Asan Agibetov',
      author_email='asan.agibetov@gmail.com',
      url='grontocrawler.plumdeq.xyz',
      install_requires=[
          'networkx',
          'rdflib',
          'fuzzywuzzy',
          'python-Levenshtein'
        ]
     )
