# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import glob
import importlib
import inspect
import os
import subprocess
import time

import darglint2

# -- Dynamic fields ----------------------------------------------------------

branch = subprocess.check_output(
    ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=os.path.dirname(__file__)
).decode()
year = time.strftime("%Y")
version = darglint2.__version__

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "darglint2"
copyright = f"2023-{year} the Darglint2 developers"
author = "Terrence Reilly"
release = version
repository = "https://github.com/akaihola/darglint2/"
url = "https://akaihola.github.io/darglint2"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# some extensions are bundled with sphinx,
# the others can be found in the `docs` dependencies group
extensions = [
    # nice read the docs theme
    "sphinx_rtd_theme",
    # custom 404 not found page
    "notfound.extension",
    # copy code button
    "sphinx_copybutton",
    # include markdown files in docs
    "myst_parser",
    # tabs, badgets and more html widgets
    "sphinx_design",
    # automatically generated api docs
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    # link references to source code
    "sphinx.ext.linkcode",
    # link shortcuts
    "sphinx.ext.extlinks",
    # automatically generated argparse commandline docs
    "sphinxarg.ext",
    # show previews on external websites
    "sphinxext.opengraph",
    # No ideas whether its needed
    "sphinx.ext.githubpages",
]

exclude_patterns = []

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    # "linkify", # needs additional dep
    "replacements",
    "smartquotes",
    "strikethrough",
    "tasklist",
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]

# the html title is used for contructing the title show for the browser tab
html_title = f"{project} {release}"


html_css_files = [
    # add markers to external links
    # "css/ext-links.css",
    #
    # load the open source bootstrap icon set
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css",
    #
    # style the version selector
    "css/version-selector.css",
]

templates_path = [
    "_templates",
]


# override sidebar contents to add `versioning.html`
# The template uses data exposed by `sphinx-multiversion` to generate
# a version selector that is show in the sidebar
html_sidebars = {
    "**": [
        "sidebar/brand.html",  # override `furo/sidebar/brand.html`
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "sidebar/scroll-end.html",
        "versioning.html",
    ],
}

# configure theme options exposed by the furo theme
html_theme_options = {
    # configure 'edit source' button
    "source_repository": repository,
    "source_branch": branch,
    "source_directory": "docs/",
    # Add link to repository
    "footer_icons": [
        {
            "name": "GitHub",
            "url": repository,
            "class": "bi bi-github bi-2x",
        },
    ],
}

# disable localization
locale_dirs = []

# -- Extension Options -------------------------------------------------------

# sphinx_copybutton
copybutton_exclude = ".linenos, .gp"  # exclude these elements from being copied


# mock building docs with sphinx-multiversion
mock_version = os.getenv("MOCK_VERSION")
if mock_version:
    html_context = {
        "current_version": {"name": mock_version},
        "latest_version": {"name": "v1.8.3"},
        "versions": {
            "tags": [{"name": "v1.8.3"}, {"name": "v1.5"}],
            "branches": [{"name": "docs"}, {"name": "main"}],
        },
    }

# sphinx-opengraph
ogp_site_url = url


# sphinx.ext.extlinks
extlinks_detect_hardcoded_links = True
extlinks = {"issue": (f"{repository}/issues/%s", "issue %s")}


# sphinx.ext.linkcode
def linkcode_resolve(domain, info):
    """
    Provides an URL for a given python source object.

    The function should return None if no link is to be added.
    The argument domain specifies the language domain the object is in.
    `info` is a dictionary with the following keys
    guaranteed to be present (in the case of `py` domain):

    - module (name of the module)
    - fullname (name of the object)

    Args:
        domain (str): directive domain
        info (dict): The objects data.

    Returns:
        str: The github URL of the corresponding source

    .. seealso::

        https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html#confval-linkcode_resolve
    """

    if domain != "py":
        return None
    if not info["module"]:
        return None

    filename = info["module"].replace(".", "/")

    # import module to determine lineno
    module_str = info["module"]
    object_str = info["fullname"]
    module = importlib.import_module(module_str)

    members = {n: v for n, v in inspect.getmembers(module)}
    if object_str not in members:
        return None
    lines, lineno = inspect.getsourcelines(members[object_str])

    return (
        f"https://github.com/akaihola/darglint2/blob/{branch}/{filename}.py#L{lineno}"
    )


# ---- Remove link to blog of the furo creator --------------------------
# the furo sphinx theme contains attribution to sphinx and furo in the page footer.
# However this attribution includes a link to the blog of the creator of furo.
# The following hook runs over the build directory after sphinx has finished building.


def edit_html(app, exception):
    """
    Modify generated html after building.

    Removes the link to the blog of the furo creator.
    """
    if exception:
        raise exception

    for file in glob.glob(f"{app.outdir}/**/*.html", recursive=True):
        with open(file, "r") as f:
            text = f.read()

        text = text.replace(
            '<a class="muted-link" href="https://pradyunsg.me">@pradyunsg</a>\'s', ""
        )
        with open(file, "w") as f:
            f.write(text)


def setup(app):
    app.connect("build-finished", edit_html)
