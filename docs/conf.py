# Configuration file for the Sphinx documentation builder.

project = 'Causal Resonance Unification (CRU) Thesis'
copyright = '2025, The Cleary Group LLC'
author = 'Shaun Cleary'
release = '1.0.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']
