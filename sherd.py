#!/usr/bin/env python
import os
import sys
import shutil

SHERD_SOURCE_DIR = os.path.dirname(__file__)

def write_file(path, contents):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass
    with open(path, 'w') as fh:
        fh.write(contents)

def maybe_add_dir_and_copy_file(source, dest):
    try:
        os.makedirs(os.path.dirname(dest))
    except OSError:
        pass
    shutil.copy(source, dest)

def read_template(name):
    with open(os.path.join(SHERD_SOURCE_DIR, "templates", name)) as fh:
        contents = fh.read() 
    return contents

def write_gateway():
    gateway_html = read_template("gateway.html").format(
        comma_separated_mirrors=",\n                ".join('"%s"' % m for m in settings.mirrors),
        mirror_li_links="\n".join("<li><a href='{0}/sherd/'>{0}/sherd/</a>".format(
                mirror
            ) for mirror in settings.mirrors),
    )
    write_file(os.path.join(settings.output_dir, "index.html"), gateway_html)

def write_sherdified_html(source_path):
    with open(source_path) as fh:
        html = fh.read()

    html.replace('"', r'\"')
    template = read_template("sherdified_html.js")
    filename = os.path.join(
        os.path.relpath(os.path.dirname(source_path), settings.source_dir),
        "{0}.js".format(os.path.splitext(os.path.basename(source_path))[0])
    )
    out_path = os.path.join(settings.output_dir, settings.data_dir, filename)
    write_file(out_path, template.format(filename=filename, html=html))

def generate_site():
    for root, dirs, files in os.walk(settings.source_dir):
        for name in files:
            path = os.path.join(root, name)
            ext = os.path.splitext(name)[1]
            if ext == ".html":
                write_sherdified_html(path)
            rel_path = os.path.relpath(path, settings.source_dir)
            html_path = os.path.join(settings.output_dir, settings.data_dir, rel_path)
            maybe_add_dir_and_copy_file(path, html_path)

    for root, dirs, files in os.walk(os.path.join(SHERD_SOURCE_DIR, "static")):
        for name in files:
            path = os.path.join(root, name)
            rel_path = os.path.relpath(path, SHERD_SOURCE_DIR)
            dest_path = os.path.join(settings.output_dir, settings.data_dir, rel_path, name)
            maybe_add_dir_and_copy_file(path, dest_path)

    write_gateway()

if __name__ == "__main__":
    try:
        import settings
    except ImportError:
        import imp
        settings_file = sys.argv[0]
        try:
            imp.load_module("settings", settings_file)
        except ImportError:
            print """Cannot find settings module.  Usage:

sherd.py <full path to settings file>
"""
            sys.exit(1)
    generate_site()
