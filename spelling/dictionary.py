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

aspell_check = aspell.Speller('lang', 'en')
spell_check = spellchecker.SpellChecker()
wordRe = re.compile(r"[a-zA-Z]+\'[a-zA-Z]+|[a-zA-Z]+")
stop_words = set(stopwords.words('english')) ## Stop_words

word_dictionary = set()
with open('dictionary.txt', 'r') as fp:
    lines = fp.readlines()
    word_dictionary.update([line.replace("\n", "") for line in lines if line[0] != "#"])

onomatopoeia = set()
with open('onomatopoeia.txt', 'r') as fp:
    lines = fp.readlines()
    onomatopoeia.update([line.replace("\n", "") for line in lines])
wikipedia = set()
with open('wikipedia.txt', 'r') as fp:
    lines = fp.readlines()
    wikipedia.update([line.replace("\n", "") for line in lines])

class Spelling:
    def __init__(self, books):
        self.books = json.loads(open(books).read())
        #self.books = json.load(gzip.open(books, 'rt', encoding='utf-8'))
        self.books = [book for book in self.books if book['language'] == 'en' and book['reviewed']]
        self.index1 = {} # misspelled words that do not end with -s
        self.index2 = {} # misspelled words that end with -s
        self.index3 = set() # correct_words to be added to the dictionary
        self.index4 = {} # all misspelled words with suggested words

    def helper0(self):
        self.index1["word"] = []
        self.index1["sentence"] = []
        self.index1["url"] = []

        self.index2["word"] = []
        self.index2["sentence"] = []
        self.index2["url"] = []

        for book in self.books:
            link = "https://tarheelreader.org{0}".format(book['link'])
            page_number = 1
            for page in book['pages']:
                url = link + "{0}/".format(page_number)
                page_copy = page['text'].replace("\n", " ")
                text = contractions.fix(page['text']) ## Replace contractions; e.g., can't --> cannot // won't --> will not
                text = text.replace("'s", "") ## remove 's (apostrophe and s)
                words = wordRe.findall(text)
                words = list(set(words))
                words = [w for w in words if not w in stop_words] ## Remove stop words
                words = [w for w in words if not w in word_dictionary] ## Remove proper nouns / person's name / onomatopoeia
                for word in words:
                    ## If the word is not found from aspell libary and spellchecker libary,
                    ## add the word to the index object
                    if not aspell_check.check(word) and len(spell_check.unknown([word])) >= 1 :
                        ## Prevent duplicates
                        if not word in self.index1["word"] and not word in self.index2["word"]:
                            ## Check plural case
                            if word[-1] == "s":
                                # misspelled words that end with -s
                                self.index2["word"].append(word)
                                self.index2["sentence"].append(page_copy)
                                self.index2["url"].append(url)

                                temp = set()
                                temp.update(aspell_check.suggest(word))
                                temp.update(onomatopoeia)
                                temp.update(wikipedia)
                                self.index4[word] = difflib.get_close_matches(word, temp, n=2, cutoff = 0.6)
                            else:
                                # misspelled words that do not end with -s
                                self.index1["word"].append(word)
                                self.index1["sentence"].append(page_copy)
                                self.index1["url"].append(url)

                                temp = set()
                                temp.update(aspell_check.suggest(word))
                                temp.update(onomatopoeia)
                                temp.update(wikipedia)
                                self.index4[word] = difflib.get_close_matches(word, temp, n=2, cutoff = 0.6)
                    else:
                        self.index3.add(word)
                        word_dictionary.add(word)
                page_number += 1
        return True

    def helper1(self):
        df1 = pd.DataFrame(self.index1, columns = ["word", "sentence", "url"])
        df1 = df1.sort_values(by=["word"], inplace=False, ascending=True)
        df1 = df1.set_index(np.arange(len(self.index1["word"])))
        df1.index.name = "index"
        return df1

    def helper2(self):
        df2 = pd.DataFrame(self.index2, columns = ["word", "sentence", "url"])
        df2 = df2.sort_values(by=["word"], inplace=False, ascending=True)
        df2 = df2.set_index(np.arange(len(self.index2["word"])))
        df2.index.name = "index"
        return df2

if __name__ == "__main__":
    start = time.time()

    #books = Spelling('books.json.gz')
    books = Spelling('books.json')
    books.helper0()

    #df1 = books.helper1()
    #df1.to_csv('misspelled1.csv')
    #df1.to_excel('misspelled1.xlsx')

    #df2 = books.helper2()
    #df2.to_csv('misspelled2.csv')
    #df2.to_excel('misspelled2.xlsx')

    '''
    with open('dictionary.txt', 'r') as fp:
        lines = fp.readlines()
        with open('dictionary.txt', 'w') as fp:
            for line in lines:
                fp.write(line)
            if len(books.index3) != 0:
                fp.write("#new_words\n")
                for word in sorted(books.index3):
                    fp.write("{0}\n".format(word))
    '''

    with open('suggestions.txt', 'w') as fp:
        fp.write("word: suggested words\n")
        for word in sorted(books.index4.keys()):
            fp.write("{0}: {1}\n".format(word, books.index4[word]))

    # Check how long it takes to run a program (in sec)
    print("time(sec) :", time.time() - start)
