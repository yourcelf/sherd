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

class Generator(object):
    def __init__(self, source_dir, output_dir, mirrors):
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.mirrors = mirrors

    def write_sherdified_html(self, source_path):
        with open(source_path) as fh:
            html = fh.read()

        html = html.replace('"', r'\"')
        html = html.replace('\n', '\\n')
        template = read_template("sherdified_html.js")
        html_system_path = os.path.join(
            os.path.relpath(os.path.dirname(source_path), self.source_dir),
            os.path.basename(source_path)
        )
        html_url_path = os.path.join("/", html_system_path.lstrip("."))
        js_system_path = html_system_path + ".js"
        out_path = os.path.join(self.output_dir, "sherd", js_system_path)
        write_file(out_path, template.format(filename=html_url_path, html=html))

    def write_gateway(self):
        gateway_html = read_template("gateway.html").format(
            comma_separated_mirrors=",\n                ".join(
                    '"%s"' % m for m in self.mirrors
                ),
            mirror_li_links="\n".join(
                "<li><a href='{0}/sherd/'>{0}/sherd/</a>".format(mirror) 
                for mirror in self.mirrors),
        )
        write_file(os.path.join(self.output_dir, "index.html"), gateway_html)

    def generate_site(self):
        # Copy over all files; create javascript proxies
        for root, dirs, files in os.walk(self.source_dir):
            for name in files:
                path = os.path.join(root, name)
                ext = os.path.splitext(name)[1]
                if ext == ".html":
                    self.write_sherdified_html(path)
                rel_path = os.path.relpath(path, self.source_dir)
                html_path = os.path.join(self.output_dir, "sherd", rel_path)
                maybe_add_dir_and_copy_file(path, html_path)

        # Write sherd.js file
        maybe_add_dir_and_copy_file(
                os.path.join(SHERD_SOURCE_DIR, "templates", "sherd.js"),
                os.path.join(self.output_dir)
        )
        # Write gateway
        self.write_gateway()
