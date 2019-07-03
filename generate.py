"""Generate core of static thr

Experiment with allowing variable base
"""

import gzip
import json
import pystache
import os
import os.path as osp
import itertools
import shutil
import re
from stemming.porter2 import stem
import aspell
from spellchecker import SpellChecker
import contractions
import pandas as pd
import myArgs
import math
from sqlitedict import SqliteDict

args = myArgs.Parse(base=16, Nselect=100, minPages=6, maxPages=20, out=str)

# get all the books
books = json.load(gzip.open("data/books.json.gz", "rt", encoding="utf-8"))

# get the English books that qualify
books = [
    book
    for book in books
    # is English
    if book["language"] == "en"
    # is categorized
    and len(book["categories"]) > 0
    # has an audience
    and book["audience"] in "EC"
    # has enough pages or is reviewed
    and (args.minPages < len(book["pages"]) < args.maxPages or book["reviewed"])
]

# break into reviewed and unreviewed
reviewed = [book for book in books if book["reviewed"]][: args.Nselect]
unreviewed = [book for book in books if not book["reviewed"]][: args.Nselect]
# reviewed books come first
selected = reviewed + unreviewed

# activate the spell checkers
spell = aspell.Speller("lang", "en")
spell2 = SpellChecker()


def getWords(book):
    """Return words from the book

    replace contractions
    check spelling
    stem
    """
    words = []
    for page in book["pages"]:
        text = contractions.fix(page["text"])
        text = text.replace("'", "")
        words += [
            stem(word).lower()
            for word in re.findall(r"[a-z]+", text, re.I)
            if spell.check(word) or spell2.known([word])
        ]
    return set(words)


index = []
for book in selected:
    slug = book["slug"]
    words = getWords(book)
    for word in words:
        index.append((word, slug))
    for category in book["categories"]:
        index.append((category.upper(), slug))
    if book["audience"] == "C":
        index.append(("CAUTION", slug))


index = pd.DataFrame(index)
index.columns = ["word", "slug"]


# repeat because dropping some might change inclusion of others
for i in range(4):
    # drop the words that only occur a few times
    booksPerWord = index.groupby("word").slug.count()
    index = index[index.word.isin(booksPerWord[booksPerWord > 2].index)]

    # drop the books that have too few or too many words
    wordsPerBook = index.groupby("slug").word.count()
    rightSize = (wordsPerBook >= 8) & (wordsPerBook < 100)
    index = index[index.slug.isin(wordsPerBook[rightSize].index)]


# make the index from words to slugs
wordToSlugs = index.groupby("word").slug.apply(list)


slugs = index.slug.unique()


# only keep the selected books for the rest of the processing
books = [book for book in books if book["slug"] in slugs]
Nbooks = len(books)
Dbooks = int(math.ceil(math.log(Nbooks, args.base)))

# count the pictures
pictures = set()
for book in books:
    for page in book["pages"]:
        pictures.add(page["url"])
Npictures = len(pictures)
Dpictures = int(math.ceil(math.log(Npictures, args.base)))

OUT = args.out
CONTENT = osp.join(OUT, "content")


def make_pageid(i):
    """return the fragment for the page"""
    return f"p{i}"


# these must be in collation order
encoding = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def encode(value, digits):
    """Encode an integer into a string"""
    r = []
    base = args.base
    for _ in range(digits):
        r.append(encoding[value % base])
        value //= base
    return "".join(r[::-1])


# map slugs to ids
bookmap = {}


def make_bookid(slug):
    """get unique id for a book"""
    if slug not in bookmap:
        i = len(bookmap)
        r = encode(i, Dbooks)
        path = osp.join(CONTENT, *list(r)) + ".html"
        bookmap[slug] = r, path
    return bookmap[slug]


# map image URL to new name
os.makedirs(OUT, exist_ok=True)
imagemap = SqliteDict(osp.join(OUT, "imagemap.sd"), autocommit=True)


def imgurl(url, bid, bpath):
    """localize and return full image url for a picture"""
    if url in imagemap:
        path = imagemap[url]
    else:
        i = len(imagemap)
        r = encode(i, Dpictures)
        path = osp.join(CONTENT, *r) + ".jpg"
        os.makedirs(osp.dirname(path), exist_ok=True)
        shutil.copyfile("/archives/tarheelreader/production" + url, path)
        imagemap[url] = path
    return osp.relpath(path, osp.dirname(bpath))


# write the books copying the images
ndx = []
template = open("book.mustache").read()
lastReviewed = None
for progress, book in enumerate(books):
    if progress % 100 == 0:
        print(progress)
    bid, bpath = make_bookid(book["slug"])
    icons = []
    if book["audience"] == "C":
        icons.append("C")
    if book["reviewed"]:
        icons.append("R")
        lastReviewed = bid
    last = bid
    ipath = osp.join(osp.dirname(bpath), "index.html")
    ndx.append(
        dict(
            title=book["title"],
            author=book["author"],
            pages=len(book["pages"]),
            image=imgurl(book["pages"][0]["url"], bid, bpath),
            icons=" ".join(icons),
            id=bid,
            link=bid[-1],
            path=ipath,
        )
    )
    view = dict(start="#" + make_pageid(1), title=book["title"], index=f"./#{bid}")
    pages = [
        dict(
            title=book["title"],
            author=book["author"],
            image=imgurl(book["pages"][1]["url"], bid, bpath),
            id=make_pageid(1),
            back=view["index"],
            next="#" + make_pageid(2),
        )
    ]
    for i, page in enumerate(book["pages"][1:]):
        pageno = i + 2
        pages.append(
            dict(
                pageno=pageno,
                id=make_pageid(pageno),
                image=imgurl(page["url"], bid, bpath),
                text=page["text"],
                back="#" + make_pageid(pageno - 1),
                next="#" + make_pageid(pageno + 1),
            )
        )
    pages[-1]["next"] = "#done"
    view["pages"] = pages
    html = pystache.render(template, view)
    os.makedirs(osp.dirname(bpath), exist_ok=True)
    with open(bpath, "wt", encoding="utf-8") as fp:
        fp.write(html)

print("last reviewed", lastReviewed)

# write the index.htmls
itemplate = open("index.mustache").read()
ipaths = sorted(set(b["path"] for b in ndx))
start = osp.join(CONTENT, "index.html")
back = start
i = 1
for path, group in itertools.groupby(ndx, lambda v: v["path"]):
    view = dict(
        name="index",
        books=group,
        back=osp.relpath(back, osp.dirname(path)),
        next=osp.relpath(ipaths[i] if i < len(ipaths) else start, osp.dirname(path)),
    )
    with open(path, "wt", encoding="utf-8") as fp:
        fp.write(pystache.render(itemplate, view))
    back = path
    i += 1

# write the front page
with open(osp.join(OUT, "index.html"), "wt", encoding="utf-8") as fp:
    wtemplate = open("welcome.mustache", "rt").read()
    view = dict(start=osp.relpath(ipaths[0], OUT))
    html = pystache.render(wtemplate, view)
    fp.write(html)

# write the word indexes
WOUT = osp.join(CONTENT, "index")
os.makedirs(WOUT, exist_ok=True)

for word in wordToSlugs.keys():
    if len(word) < 3:
        continue
    ids = sorted([bookmap[slug][0] for slug in wordToSlugs[word]])
    with open(osp.join(WOUT, word), "wt", encoding="utf-8") as fp:
        fp.write("".join(ids))

# write the AllAvailable file
with open(osp.join(WOUT, 'AllAvailable'), "wt", encoding='utf-8') as fp:
    fp.write('%s-%s' % ("0" * Dbooks, last))

# record parameters needed by the js
config = {
    "base": args.base,
    "digits": Dbooks,
    "first": "0" * Dbooks,
    "lastReviewed": lastReviewed,
    "last": last,
}
with open(osp.join(CONTENT, "config.json"), "wt") as fp:
    json.dump(config, fp)

# copy the extras
for fname in [
        "site.css",
        "index.css",
        "book.css",
        "book.js",
        "find.html",
        "find.js",
        "find.css",
        "images/BackArrow.png",
        "images/NextArrow.png",
        "images/favorite.png",
        "images/caution.png",
        "images/reviewed.png",
        "images/settings.png",
]:
    if osp.exists(fname):
        opath = osp.join(OUT, fname)
        os.makedirs(osp.dirname(opath), exist_ok=True)
        shutil.copyfile(fname, opath)


