import gzip
import json
import pandas as pd
import numpy as np
import helper
import bingspell

def put_books(books):
    for book in books:
        if book['language'] == 'en':
            book['misspelled'] = len(helper.getMisspelled(book))
        else:
            book['misspelled'] = -1
    corrector = bingspell.Bingspell()
    for book in books:
        if book['language'] != 'en':
            continue
        elif book['misspelled'] == 0:
            continue
        elif helper.link_detect(book):
            continue
        elif helper.repetition_detect(book):
            continue
        else:
            book = corrector.put_book(book)
    corrector.close()
    for book in books:
        del book['misspelled']
    return books
