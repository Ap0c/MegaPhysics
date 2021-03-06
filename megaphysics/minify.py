# Handles asset minification and compression.

# -------- Standard Libraries -------- #

import os
import re


# -------- Third Party Libraries -------- #

from cssmin import cssmin
from slimit import minify as jsmin

# -------- Globals -------- #

BUILD_PATH = "build/assets/"

# -------- Functions -------- #


def import_file(filename, PATH):
    if os.path.isfile(PATH+filename):
        with open(PATH+filename, "r") as f:
            if not re.search("\.min\.", filename):
                if filename.endswith(".css"):
                    return cssmin(f.read())
                else:
                    return jsmin(f.read(), mangle=True, mangle_toplevel=True)
            return f.read()
    return filename


def compile(ASSETS_LOCATION, dir, ext, build_filename):
    PATH = ASSETS_LOCATION+dir
    res = ""
    with open(PATH+"imports"+ext) as f:
        imports = f.read()
        a = re.split("import (.+)", imports)
        for substr in a:
            res = res + import_file(substr, PATH)
    open(BUILD_PATH+build_filename, "w").write(res)


def compile_css(ASSETS_LOCATION):
    print "Compiling css..."
    compile(ASSETS_LOCATION, "/css/", ".css", "styles.min.css")


def compile_js(ASSETS_LOCATION):
    print "Compiling js..."
    compile(ASSETS_LOCATION, "/js/", ".js", "scripts.min.js")
