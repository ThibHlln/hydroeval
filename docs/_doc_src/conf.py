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
import pydata_sphinx_theme
from datetime import datetime
import os
import sys
from git import Repo
sys.path.insert(0, os.path.abspath('../..'))


with open('../../hydroeval/version.py') as fv:
    exec(fv.read())

# -- Project information -----------------------------------------------------
project = 'hydroeval'
copyright = '2018-{}, Thibault Hallouin'.format(
    datetime.now().year
)
author = 'Thibault Hallouin'

# The full version, including alpha/beta/rc tags
if os.getenv('VERSION_RELEASE'):
    release = 'v{}'.format(__version__)
    version = 'v{}'.format(__version__)
else:
    release = 'latest'
    version = 'latest'

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.doctest',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.githubpages',
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
html_theme = 'pydata_sphinx_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['../_doc_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'hydroevaldoc'

# Paths (filenames) here must be relative to (under) html_static_path as above:
html_css_files = [
    'custom.css'
]

# Custom sidebar templates, maps document names to template names.
html_sidebars = {}

# https://alabaster.readthedocs.io/en/latest/customization.html
# https://github.com/bitprophet/alabaster/blob/master/alabaster/theme.conf

html_baseurl = 'https://thibhlln.github.io/hydroeval'

html_logo = '../_doc_img/hydroeval-logo.svg'

html_favicon = '../_doc_img/hydroeval-favicon.ico'

html_permalinks_icon = '<span class="fa fa-link">'

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/ThibHlln/hydroeval",
            "icon": "fab fa-github",
        }
    ],
    "show_prev_next": False,
    "navbar_align": "left"
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
    (tag.name, '/'.join([html_baseurl, tag.name[1:]]))
    for tag in repo.tags if tag.name >= 'v0.1.0'
]

if version != 'latest':
    if (version, '/'.join([html_baseurl, __version__])) not in versions:
        versions.insert(0, (version, '/'.join([html_baseurl, __version__])))
versions.insert(0, ('latest', html_baseurl))

html_context = {
    'current_version': version if version == 'latest' else __version__,
    'versions': versions,
    'show_versions': True if versions else False,
    'links': [
        ('Source Code', remote_url),
        ('Issue Tracker', '/'.join([remote_url.replace('.git', ''), 'issues'])),
        ('User Support', '/'.join([remote_url.replace('.git', ''), 'discussions']))
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

# -- Options for mathjax extension ---------------------------------------

# to get left alignment of equations
mathjax3_config = {
    "chtml": {
        "displayAlign": "left"
    },
    "options": {
        "ignoreHtmlClass": "tex2jax_ignore",
        "processHtmlClass": "tex2jax_process"
    }
}
