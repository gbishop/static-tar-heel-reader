#!/usr/bin/python3
"""Assemble a web page"""

from mako.template import Template
from mako import exceptions
import os
import os.path as osp
import shutil
from html5print import HTMLBeautifier
import myArgs


class CopyPage:
    """Construct a page from a template"""

    def __init__(self, src="src", dst="dist", root="."):
        self.src = src
        self.dst = dst
        self.root = root

    def include(self, name, **kwargs):
        """Render a template with traceback"""
        with open(osp.join(self.src, name), "rt") as fp:
            template = fp.read()
        try:
            html = Template(template).render(
                **kwargs, include=self.include, copy=self.copy, link=self.link
            )
        except Exception:
            print(exceptions.text_error_template().render())
            raise
        return html

    def copy(self, fname):
        """Copy a file and return its name"""
        _, ext = osp.splitext(fname)
        spath = osp.join(self.src, fname)
        oname = fname
        path = osp.join(self.dst, oname)
        os.makedirs(osp.dirname(path), exist_ok=True)
        if ext in [".css"]:
            content = self.include(fname)
            with open(path, "wt") as fp:
                fp.write(content)
        else:
            shutil.copyfile(spath, path)
        return osp.relpath(oname, self.root)

    def link(self, fname):
        """Link a file that is expected"""
        return fname

    def assemble(self, page):
        """Assemble a web page"""
        html = self.include(page)
        html = HTMLBeautifier.beautify(html, 4)
        path = osp.join(self.dst, page)
        with open(path, "wt") as fp:
            fp.write(html)


if __name__ == "__main__":
    args = myArgs.Parse()

    cp = CopyPage()

    try:
        cp.assemble(osp.basename(args.extra_[0]))
    except Exception as e:
        print(e)
