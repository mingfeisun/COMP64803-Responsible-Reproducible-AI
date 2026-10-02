# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Hackathon Project'
copyright = '0, Michael Dodds, Oscar Hill, Stan Xio, Alex Higginbottom'
author = 'Michael Dodds, Oscar Hill, Stan Xio, Alex Higginbottom'
release = '0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
import os
import sys

sys.path.insert(0, os.path.abspath('../../main/'))


extensions = [
    'sphinx.ext.autodoc',      # Core Sphinx autodoc extension
    'sphinx.ext.napoleon',     # For NumPy & Google style docstrings
    'sphinx.ext.viewcode',     # Add "view code" links to doc pages
    'sphinx.ext.autosummary', # Optional: generate summary docs
    'sphinx.ext.mathjax',
    'myst_parser'
]
autosummary_generate = True 
# Napoleon settings (optional, defaults are generally good)
napoleon_google_docstring = False  # For Google-style
napoleon_numpy_docstring = True    # For NumPy-style
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
