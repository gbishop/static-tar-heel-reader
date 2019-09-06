#!/usr/bin/python3

"""Make a subset of our books for the team"""

import gzip
import json
import os.path as osp
import os
import shutil

indir = "/archives/tarheelreader/production"
outdir = "/var/tmp/subset"

books = json.load(gzip.open("books.json.gz", "rt", encoding="utf-8"))

N = 100

subset = books[:N]

# reproduce the production images structure for the subset

for book in subset:
    for page in book["pages"]:
        url = page["url"]
        opath = outdir + url
        if not osp.exists(opath):
            os.makedirs(osp.dirname(opath), exist_ok=True)
            ipath = indir + url
            shutil.copyfile(ipath, opath)

json.dump(subset, gzip.open(osp.join(outdir, "books.json.gz"), "wt", encoding="utf-8"))
