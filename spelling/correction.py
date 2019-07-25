import gzip
import json
import re
import os
import pickle
import aspell
import spellchecker
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import contractions
import time
import difflib
import bingspell
import helper

spell = aspell.Speller("lang", "en")
spell2 = spellchecker.SpellChecker()
wordRe = re.compile(r"[a-zA-Z]+\'[a-zA-Z]+|[a-zA-Z]+")
##stop_words = set(stopwords.words('english')) ## Stop_words
##----------------------------------------------------
##----------------------------------------------------
# Get the dicitonary
word_dictionary = set()
with open('dictionary.txt', 'r') as fp:
    lines = fp.readlines()
    word_dictionary.update([line.replace("\n", "") for line in lines if line[0] != "#"])
##----------------------------------------------------
##----------------------------------------------------
books = json.load(gzip.open("books.json.gz", 'rt', encoding='utf-8'))
books = [book for book in books if book["language"] == "en"]
reviewed = [book for book in books if book["reviewed"]]
unreviewed = [book for book in books if not book["reviewed"]]
##----------------------------------------------------
##----------------------------------------------------
for book in reviewed:
    book['misspelled'] = len(helper.getMisspelled(book))
for book in unreviewed:
    book['misspelled'] = len(helper.getMisspelled(book))
print("No modifiction:")
print(len(reviewed))
print(len(unreviewed))

reviewed = helper.filter(reviewed)
unreviewed = helper.filter(unreviewed)
print("\nAfter deletion of repeations:")
print(len(reviewed))
print(len(unreviewed))
##----------------------------------------------------
##----------------------------------------------------






class Spelling:
    def __init__(self, books):
        self.books = books
        self.index1 = {} # misspelled words that do not end with -s
        self.index2 = {} # misspelled words that end with -s

    def helper0(self):
        self.index1["word"] = []
        #self.index1["correction"] = []
        self.index1["sentence"] = []
        self.index1["url"] = []
        self.index1["bingspell"] = []

        for book in self.books:
            link = "https://tarheelreader.org{0}".format(book['link'])
            page_number = 1
            for page in book['pages']:
                url = link + "{0}/".format(page_number)
                page_copy = page['text'].replace("\n", " ")
                text = contractions.fix(page['text']) ## Replace contractions; e.g., can't --> cannot // won't --> will not
                #text = text.replace("'s", "") ## remove 's (apostrophe and s)
                words = wordRe.findall(text)
                words = [w for w in words if not w in word_dictionary] ## Remove proper nouns / person's name / onomatopoeia
                for word in words:
                    if not spell.check(word) and len(spell2.unknown([word])) >= 1:
                        if not word in self.index1["word"]:
                            self.index1["word"].append(word)
                            self.index1["sentence"].append(page_copy)
                            self.index1["url"].append(url)
                            #self.index1["correction"].append(getSuggestion(word))
                page_number += 1
        return True

    def helper00(self):
        self.index1["bingspell"] = bingspell.put_sentences(self.index1["sentence"])

    def helper1(self):
        df1 = pd.DataFrame(self.index1, columns = ["word", "sentence", "bingspell", "url"])
        #df1 = pd.DataFrame(self.index1, columns = ["word", "correction", "sentence", "bingspell", "url"])
        df1 = df1.sort_values(by=["word"], inplace=False, ascending=True)
        df1 = df1.set_index(np.arange(len(self.index1["word"])))
        df1.index.name = "index"
        return df1

    def helper2(self):
        df2 = pd.DataFrame(self.index2, columns = ["word", "sentence", "bingspell", "url"])
        #df2 = pd.DataFrame(self.index2, columns = ["word", "correction","sentence", "bingspell", "url"])
        df2 = df2.sort_values(by=["word"], inplace=False, ascending=True)
        df2 = df2.set_index(np.arange(len(self.index2["word"])))
        df2.index.name = "index"
        return df2



test00 = Spelling(reviewed)
test00.helper0()
test00.helper00()

df1 = test00.helper1()
df1.to_excel('test0111.xlsx')

#df2 = test00.helper2()
#df2.to_excel('test0222.xlsx')








#----------------------------------------------------

'''
#for book in reviewed:
#    book['misspelled'] = len(getMisspelled(book))
with open('reviewed.json', 'w', encoding='utf-8') as fp:
    json.dump(reviewed, fp)
with open("reviewed.json", "rb") as fp:
    with gzip.open("reviewed.json.gz", "wb") as fp2:
        fp2.writelines(fp)
os.remove('reviewed.json')


#for book in unreviewed:
#    book['misspelled'] = len(getMisspelled(book))
with open('unreviewed.json', 'w', encoding='utf-8') as fp:
    json.dump(unreviewed, fp)
with open("unreviewed.json", "rb") as fp:
    with gzip.open("unreviewed.json.gz", "wb") as fp2:
        fp2.writelines(fp)
os.remove('unreviewed.json')
'''
