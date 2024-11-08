# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'BRAILS++'
copyright = '2024, fmk'
author = 'fmk'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'nbsphinx',
              'sphinx_copybutton',
              'sphinx.ext.autosummary',
              'sphinx.ext.imgconverter']

autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['sphynx/templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['setup.py', 'conf.py', '**/*.ipynb', '**/*groundingdino*', '**/lib']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['sphynx/static']

rst_prolog = f"""
.. |fmk| replace:: **fmk**
.. |app| replace:: BrailsPlusPlus
.. |SimCenter| replace:: `SimCenter`_
.. _SimCenter: https://simcenter.designsafe-ci.org/
.. |DesignSafe| replace:: `DesignSafe`_
.. _DesignSafe: https://designsafe-ci.org
.. |br| raw:: html

    <br>

"""
