import os
import sys

sys.path.insert(0, os.path.abspath(".."))   # чтобы Sphinx видел lab1.py

project = "CI-CD-testing"
author = "Your Name"
release = "1.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

html_theme = "sphinx_rtd_theme"
html_static_path = []
templates_path = []
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]