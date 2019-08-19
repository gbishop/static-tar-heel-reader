#!/usr/bin/python3
"""Assemble a web page"""

import sys
from mako.template import Template
from mako import exceptions
import os
import os.path as osp
import shutil
from htmlmin import minify
from html5print import HTMLBeautifier
import hashlib
from glob import glob
import myArgs


class CopyPage:
    """Construct a page from a template"""

    def __init__(self, src="src", dst="dist", root=".", dev=1, use_sw=0):
        self.src = src
        self.dst = dst
        self.root = root
        self.dev = dev
        self.use_sw = use_sw

    def include(self, name, **kwargs):
        """Render a template with traceback"""
        with open(osp.join(self.src, name), "rt") as fp:
            template = fp.read()
        try:
            html = Template(template).render(
                **kwargs,
                include=self.include,
                copy=self.copy,
                link=self.link,
                dev=self.dev,
                use_sw=self.use_sw,
            )
        except Exception:
            print(exceptions.text_error_template().render())
            raise
        return html

    def copy(self, fname):
        """Copy a file and return its name"""
        _, ext = osp.splitext(fname)
        spath = osp.join(self.src, fname)
        if not self.dev:
            base, ext = osp.splitext(fname)
            with open(spath, "rb") as fp:
                content = fp.read()
            bust = hashlib.md5(content).hexdigest()[:6]
            oname = f"{base}.{bust}{ext}"
        else:
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
        if self.dev:
            return fname
        # determine the hashed name
        base, ext = osp.splitext(fname)
        pat = osp.join(self.dst, f"{base}.*{ext}")
        names = glob(pat)
        name = osp.basename(names[0])
        return osp.relpath(name, self.root)

    def assemble(self, page):
        """Assemble a web page"""
        html = self.include(page)
        if self.dev:
            html = HTMLBeautifier.beautify(html, 4)
        else:
            html = minify(html)
        path = osp.join(self.dst, page)
        with open(path, "wt") as fp:
            fp.write(html)


if __name__ == "__main__":
    args = myArgs.Parse(dev=1, sw=0)

    cp = CopyPage(dev=args.dev, use_sw=args.sw)

    try:
        cp.assemble(osp.basename(args.extra_[0]))
    except Exception as e:
        print(e)
