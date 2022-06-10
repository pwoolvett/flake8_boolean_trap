#!/usr/bin/env python3
from datetime import date

from flake8_boolean_trap import Plugin

default_role = "py:obj"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
]

source_suffix = [".rst", ".md"]
root_doc = "index"

project = "flake8_boolean_trap"
year = date.today().year
author = "Pablo Woolvett <github@devx.pw>"
copyright = f"{year}, {author}"

version = Plugin.version
release = version

language = "en"


# -- autodoc config ---------------------------------------------------
autoclass_content = "both"

# -- napoleon config ---------------------------------------------------
# See https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#getting-started
napoleon_google_docstring = True
# napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
# napoleon_include_special_with_doc = True
# napoleon_use_admonition_for_examples = False
# napoleon_use_admonition_for_notes = False
# napoleon_use_admonition_for_references = False
napoleon_preprocess_types = True
# napoleon_use_ivar = False
# napoleon_use_param = True
# napoleon_use_rtype = True
# napoleon_type_aliases = None
napoleon_attr_annotations = True

# -- sphinx-theme options ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"
html_theme_options = {
    "sidebar_hide_name": True,
}
html_show_copyright = False

# -- Options for HTML output -------------------------------------------------


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
# html_logo = "_static/logo.png"
# html_favicon = "_static/logo.png"
html_css_files = [
    "css/site.css",
]
# hide sphinx footer
html_show_sphinx = False

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "flake8_boolean_trapdoc"
