# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os


sys.path.insert(0, os.path.abspath("../../src"))


project = "AI assistant parsers core"
copyright = "2024, AI Assistant"
author = "AI Assistant"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "autoapi.extension",
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.coverage",
    "sphinx.ext.ifconfig",
    "sphinx.ext.todo",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "ru"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

napoleon_google_docstring = True

add_module_names = False
autoapi_add_toctree_entry = True
autoapi_dirs = ['../../src']
