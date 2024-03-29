# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or classes to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sphinx_rtd_theme
from datetime import datetime
import os
import sys
from git import Repo
sys.path.insert(0, os.path.abspath('../..'))


with open('../../hydroeval/version.py') as fv:
    exec(fv.read())

# -- Project information -----------------------------------------------------
project = 'hydroeval'
copyright = '{}, Thibault Hallouin.'.format(
    datetime.now().year
)
author = 'Thibault Hallouin'

# The full version, including alpha/beta/rc tags
release = __version__
version = __version__

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.doctest',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.githubpages',
    'nbsphinx',
    'sphinx.ext.mathjax'
]

# Boolean indicating whether to scan all found documents for
# autosummary directives, and to generate stub pages for each
# (http://sphinx-doc.org/latest/ext/autosummary.html)
autosummary_generate = True

# Both the class’ and the __init__ method’s docstring are concatenated
# and inserted.
autoclass_content = 'both'

# This value selects how automatically documented members are sorted
# (http://sphinx-doc.org/latest/ext/autodoc.html)
autodoc_member_order = 'bysource'
autosummary_member_order = 'bysource'

# This value is a list of autodoc directive flags that should be
# automatically applied to all autodoc
# directives. (http://sphinx-doc.org/latest/ext/autodoc.html)
autodoc_default_flags = ['members', 'inherited-members', 'show-inheritance']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['../_doc_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['Thumbs.db', '.DS_Store']

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# If true, the current module name will be prepended to all
# description unit titles (such as .. function::).
add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in
# the output. They are ignored by default.
show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# The default language to highlight source code
highlight_language = 'python'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['../_doc_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'hydroevaldoc'

# Paths (filenames) here must be relative to (under) html_static_path as above:
html_css_files = [
    'theme_overrides.css'
]

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    '**': ['about.html',
           'navigation.html',
           'searchbox.html',
           'versions.html']
}

# https://alabaster.readthedocs.io/en/latest/customization.html
# https://github.com/bitprophet/alabaster/blob/master/alabaster/theme.conf

html_theme_options = {
    'canonical_url': 'https://thibhlln.github.io/hydroeval',
    'prev_next_buttons_location': None,
    'navigation_depth': 3
}

# If not '', a 'Last updated on:' timestamp is inserted at every page
# bottom, using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

# Additional templates that should be rendered to pages, maps page
# names to template names.
# html_additional_pages = {}

# If false, no module index is generated.
html_domain_indices = True

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = False

html_show_sourcelink = False

# info for versioning at bottom of sidebar
repo = Repo(search_parent_directories=True)
remote_url = repo.remotes.origin.url

versions = [
    (tag.name,
     os.sep.join([html_theme_options['canonical_url'],
                  tag.name if tag.name != 'v{}'.format(version) else '']))
    for tag in repo.tags if tag.name >= 'v0.1.0'
]
html_context = {
    'current_version': version,
    'versions': versions,
    'show_versions': True if versions else False,
    'links': [
        ('<span class="fa fa-code"> Source Code', remote_url),
        ('<span class="fa fa-bug"> Issue Tracker',
         os.sep.join([remote_url.replace('.git', ''), 'issues'])),
        ('<span class="fa fa-users"> User Support',
         os.sep.join([remote_url.replace('.git', ''), 'discussions']))
    ]
}

# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'sphinx': ('https://www.sphinx-doc.org/en/master/',  None),
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://docs.scipy.org/doc/numpy', None),
    'cfunits': ('https://ncas-cms.github.io/cfunits', None)
}

intersphinx_cache_limit = 5

# -- Options for intersphinx extension ---------------------------------------

# to get left alignment of equations
mathjax_config = {
    "jax": ["input/TeX", "output/HTML-CSS"],
    "displayAlign": "left"
}
