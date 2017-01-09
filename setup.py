from setuptools import setup

setup(name='grontocrawler',
      version='0.3.6',
      description='transformation of OWL ontologies into graphs',
      author='Asan Agibetov',
      author_email='asan.agibetov@gmail.com',
      url='grontocrawler.plumdeq.xyz',
      packages=['grontocrawler'],
      install_requires=[
          'networkx',
          'rdflib',
          'fuzzywuzzy',
          'python-Levenshtein'
        ]
     )
