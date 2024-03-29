import os, sys
sys.path.insert(0, os.path.abspath('../')) #documentation is detected
sys.path.insert(0, os.path.abspath('../tractor_beam'))
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'tractor_beam'
copyright = '2023, Prismadic, LLC'
author = 'Prismadic, LLC.'
version = "v0.0.2"
release = "latest"
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.todo'
    , 'sphinx.ext.viewcode'
    , 'sphinx.ext.autodoc'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_show_sphinx = False
html_show_copyright = True
html_context = {
    "display_github": True, # Integrate GitHub
    "github_user": "Prismadic", # Username
    "github_repo": "tractor-beam", # Repo name
    "github_version": "main", # Version
    "conf_py_path": "/docs/", # Path in the checkout to the docs root
}

github_url = "https://github.com/Prismadic/tractor-beam"
display_github = True
html_logo = "../tractor_beam.png"
pygments_style = 'dracula'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    "collapse_navigation" : False
    , 'prev_next_buttons_location': 'None'
    , 'logo_only': True
    , 'navigation_depth': 5
}