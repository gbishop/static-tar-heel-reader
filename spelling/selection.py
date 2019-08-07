import gzip
import json
import pandas as pd
import numpy as np
import score
import helper
from operator import itemgetter
import os


# Get all books
books = json.load(gzip.open("books.json.gz", 'rt', encoding='utf-8'))
# Get books that are in English
books = [book for book in books if book["language"] == "en"]


# Get reviewed books (Number of reviewed book: 9582)
reviewed = [book for book in books if book["reviewed"]]
# Get unreviewed books (Number of unreviewed book: 53990)
unreviewed = [book for book in books if not book["reviewed"]]


# Remove books that contain a link to a website
# or consecutively repeated characters such as ahhhhhh, zzzzzz, or Awwwwww.
reviewed = helper.filter(reviewed) # Number of reviewed book: 9534
unreviewed = helper.filter(unreviewed) # Number of unreviewed book: 53347


# Add 'misspelled' dictionary in the books
for book in reviewed:
    book['misspelled'] = len(helper.getMisspelled(book))
for book in unreviewed:
    book['misspelled'] = len(helper.getMisspelled(book))


# Score reviewed books (Score ranges from -100.0 to +100.0)
reviewed = score.put_books(reviewed)
# Score unreviewed books (Score ranges from -100.0 to +100.0)
unreviewed = score.put_books(unreviewed)


# Create selected books
selection = reviewed
# Order the unreviewed books by their score (from highest to lowest)
unreviewed = sorted(unreviewed, key=itemgetter('score'), reverse=True)
# Get the best 5466 books from unreviewed and add them to the selected books
selection += unreviewed[:5466]
# Number of selected books: 15,000; 9534 from reviewed books plus 5466 from unreviewed books


# Create Correction object
use_me = helper.Correction()
# Correct spelling/grammar errors in the selected books
selection = use_me.correct(selection)
# Order the selected books by their score (from highest to lowest)
selection = sorted(selection, key=itemgetter('score'), reverse=True)


# Save the selected books as json files
with open('selection.json', 'w', encoding='utf-8') as fp:
    json.dump(selection, fp)
with open("selection.json", "rb") as fp:
    with gzip.open("selection.json.gz", "wb") as fp2:
        fp2.writelines(fp)
os.remove('selection.json')


# Make the misspelled words and corrected sentences into an excel file
use_me.frame().to_excel('df_misspelled.xlsx')
