"""fetch all the thr books"""
import requests
from sqlitedict import SqliteDict
import gzip
import json


books = SqliteDict("allbooks.sqlite", autocommit=True)


for page in range(1, 10000):
    if page % 100 == 0:
        print(page)
    url = (
        "http://test.tarheelreader.org/find/"
        "?search=&category=&reviewed=&audience=&language=&"
        f"page={page}&json=1"
    )
    resp = requests.get(url)
    r = resp.json()
    for b in r["books"]:
        if b["slug"] in books:
            continue
        url = "http://test.tarheelreader.org/book-as-json/" f'?slug={b["slug"]}'
        resp = requests.get(url)
        book = resp.json()
        books[b["slug"]] = book
    if not r["more"]:
        break


rows = sorted(books.values(), key=lambda b: b["ID"])
with gzip.open("books.json.gz", "wt", encoding="utf-8") as fp:
    json.dump(rows, fp)
