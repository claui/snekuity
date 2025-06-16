# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# pylint: skip-file
# type: ignore

project = 'snekuity'
executable = 'snekuity'
author = 'Claudia Pellegrino <clau@tiqua.de>'
description = 'Pythonic API for GnuCash'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'autoapi.extension',
    'myst_parser',
    'sphinx.ext.autodoc',
]

autoapi_dirs = ['../../snekuity']
autoapi_keep_files = True
autoapi_ignore = ['**/stubs/**']
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',
    'special-members',
    'imported-members',
]
autoapi_type = 'python'
autodoc_typehints = 'description'

html_theme = 'sphinx_rtd_theme'

myst_enable_extensions = [
    'deflist',
]


def skip_module(app, what, name, obj, skip, options):
    if what != 'module':
        return skip
    if name in [
        'snekuity.config',
        'snekuity.settings',
        'snekuity.version',
    ]:
        return True
    return skip


def setup(sphinx):
    sphinx.connect('autoapi-skip-member', skip_module)


templates_path = []
exclude_patterns = [
    '**/snekuity/config/**',
    '**/snekuity/settings/**',
    '**/snekuity/version/**',
]

# Man page output

man_pages = [
    (
        'usage',
        'snekuity',
        description,
        [author],
        3,
    )
]

man_show_urls = True
