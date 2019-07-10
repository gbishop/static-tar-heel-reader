## This file takes "books.json.gz" file as an input
## Python version 3.7.0 was used.
import gzip
import json
import re
import pickle
import aspell
import spellchecker
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import contractions
import time
import difflib
import requests
import pickle
from bs4 import BeautifulSoup
import threading
import datetime

def startTimer():
    s = datetime.datetime.now()
    print(s)
    timer = threading.Timer(5, startTimer)
    timer.start()

spell= aspell.Speller('lang', 'en')
spell2 = spellchecker.SpellChecker()
wordRe = re.compile(r"[a-zA-Z]+\'[a-zA-Z]+|[a-zA-Z]+")
stop_words = set(stopwords.words('english')) ## Stop_words

books = json.loads(open("books.json").read())
books = [book for book in books if book['language'] == 'en' and book['reviewed']]

misspelled = set()

for book in books:
    for page in book['pages']:
        text = contractions.fix(page['text']) ## Replace contractions; e.g., can't --> cannot // won't --> will not
        text = text.replace("'s", "") ## remove 's (apostrophe and s)
        words = wordRe.findall(text)
        words = list(set(words))
        words = [w for w in words if not w in stop_words] ## Remove stop words
        for word in words:
            if not spell.check(word) and not spell2.known([word]):
                misspelled.add(word)


with open('misspelled_words.txt', 'w') as fp:
    for word in sorted(misspelled):
        fp.write("{0}\n".format(word))


class Wikipedia:
    def __init__(self, words):
        self.words = words
        self.words2 = [] ## words2 is a list of words not found on Wikipedia (misspelled)
        self.words3 = [] ## words3 is a list of words found on Wikipedia (new_aspell_dictionary)

    def helper(self):
        for word in self.words:
            url = "https://en.wikipedia.org/wiki/{0}".format(word)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html5lib")
            ## check if the word is found on Wikipedia
            rows = soup.findAll('div', {'class':'noarticletext mw-content-ltr'})
            if (len(rows) != 0):
                self.words2.append(word)
            else:
                ## check if the page is redirected
                rows2 = soup.findAll('span', {'class':'mw-redirectedfrom'})
                if (len(rows2) != 0):
                    self.words2.append(word)
                else:
                    self.words3.append(word)

startTimer() ## timer
wikipedia = Wikipedia(misspelled)
wikipedia.helper()

#with open('new_misspelled_wikipedia.txt', 'w') as fp:
#    for word in sorted(wikipedia.words2):
#        fp.write("{0}\n".format(word))

#with open('new_aspell_dictionary_wikipedia.txt', 'w') as fp:
#    for word in sorted(wikipedia.words3):
#        fp.write("{0}\n".format(word))

with open('wikipedia.txt', 'w') as fp:
    for word in sorted(wikipedia.words3):
        fp.write("{0}\n".format(word))

print("job done\n\n\n")
