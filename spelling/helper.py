import re
import aspell
import spellchecker
#from nltk.corpus import stopwords
import contractions
import bingspell
import pandas as pd
import numpy as np

spell = aspell.Speller("lang", "en")
spell2 = spellchecker.SpellChecker()
wordRe = re.compile(r"[a-zA-Z]+\'[a-zA-Z]+|[a-zA-Z]+")
#stop_words = set(stopwords.words('english')) ## Stop_words

# Take a book as input, detect if the book contains a link to a website,
# and return True if it does, or False otherwise.
def link_detect(book):
    wordRe1 = re.compile(r"www[.][0-9a-zA-Z]+|WWW[.][0-9a-zA-Z]+")
    wordRe2 = re.compile(r"http|HTTP")
    wordRe3 = re.compile(r"[0-9a-zA-Z]+[.]com|[0-9a-zA-Z]+[.]COM")
    pages = book['pages']
    for page in pages:
        text = page['text']
        if len(wordRe1.findall(text)) >= 1 or \
        len(wordRe2.findall(text)) >= 1 or \
        len(wordRe3.findall(text)) >= 1:
            return True
    return False

# Take a book as input, detect if the book contains
# consecutively repeated characters (e.g., zzzzzz, ahhhhhh, Awwwwww),
# and return True if it does, or False otherwise.
def repetition_detect(book):
    wordRe = re.compile(r'(([a-zA-Z])\2{6,})') ## Threshold: 6; e.g., zzzzzz, ahhhhhh, Awwwwww, etc
    pages = book['pages']
    for page in pages:
        text = page['text']
        temp = wordRe.findall(text)
        temp = [word[0] for word in temp]
        if len(temp) >= 1:
            return True
    return False

# Take books as input, and filter them out by link_detect() and repetition_detect()
def filter(books):
    books = [book for book in books if not link_detect(book)]
    books = [book for book in books if not repetition_detect(book)]
    return books

# Get the dicitonary
word_dictionary = set()
with open('dictionary.txt', 'r') as fp:
    lines = fp.readlines()
    word_dictionary.update([line.replace("\n", "") for line in lines if line[0] != "#"])

# Take a book as input, and find misspelled words in the book, and return them as a list
def getMisspelled(book):
    misspelled = [] # Allow duplicates
    for page in book["pages"]:
        text = contractions.fix(page['text']) # Replace contractions; e.g., can't --> cannot // won't --> will not
        text = text.replace("'s", "") # Remove 's (apostrophe and s)
        words = wordRe.findall(text) # Tokenize a sentence into words
        # words = [w for w in words if not w in stop_words] ## Remove stop words
        words = [w for w in words if not w in word_dictionary] ## Remove correctly spelled words
        for word in words:
            if not spell.check(word) and not spell2.known([word]):
                misspelled.append(word)
    return misspelled

# Take books that have spelling/grammar errors as input,
# correct them in a sentence level, and return the corrected books
def correct(books):
    corrector = bingspell.Bingspell()
    for book in books:
        if book['misspelled'] == 0:
            continue
        else:
            for page in book["pages"]:
                page_copy = page['text'].replace("\n", " ")
                text = contractions.fix(page['text']) # Replace contractions; e.g., can't --> cannot // won't --> will not
                text = text.replace("'s", "") # Remove 's (apostrophe and s)
                words = wordRe.findall(text) # Tokenize a sentence into words
                # words = [w for w in words if not w in stop_words] ## Remove stop words
                words = [w for w in words if not w in word_dictionary] ## Remove correctly spelled words
                for word in words:
                    if not spell.check(word) and not spell2.known([word]):
                        page['text'] = corrector.put_sentence(page_copy)
                        break
    corrector.close()
    return books

# This class does the same job as correct() function does above
# However, while correcting, it records the misspelled words,
# sentences that contained the misspelled words, the corrected sentences,
# and urls. Then, it turns them into a pd.DataFrame file
# so that it can make an excel file later
class Correction:
    def __init__(self):
        self.books = []
        self.index = {}

    # 1. Take books that have spelling/grammar errors as input,
    # correct them in a sentence level, and return the corrected books
    # 2. Record misspelled words, sentences that contained misspelled words,
    # corrected sentences, and urls in self.index.
    def correct(self, books):
        self.books = books
        self.index["word"] = []
        self.index["sentence_changed"] = []
        self.index["sentence"] = []
        self.index["bingspell"] = []
        self.index["url"] = []
        corrector = bingspell.Bingspell()
        for book in self.books:
            if book['misspelled'] == 0:
                continue
            else:
                link = "https://tarheelreader.org{0}".format(book['link'])
                page_number = 1
                for page in book['pages']:
                    url = link + "{0}/".format(page_number)
                    page_copy = page['text'].replace("\n", " ")
                    text = contractions.fix(page['text']) ## Replace contractions; e.g., can't --> cannot // won't --> will not
                    text = text.replace("'s", "") ## remove 's (apostrophe and s)
                    words = wordRe.findall(text)
                    # words = [w for w in words if not w in stop_words] ## Remove stop words
                    words = [w for w in words if not w in word_dictionary] ## Remove proper nouns / person's name / onomatopoeia
                    for word in words:
                        if not spell.check(word) and len(spell2.unknown([word])) >= 1:
                            self.index["word"].append(word)
                            self.index["sentence"].append(page_copy)
                            page['text'] = corrector.put_sentence(page_copy)
                            self.index["bingspell"].append(page['text'])
                            self.index["url"].append(url)
                    page_number += 1
        corrector.close()
        min = 0
        max = len(self.index["sentence"])
        for i in range(min, max):
            if self.index["sentence"][i] == self.index["bingspell"][i]:
                self.index["sentence_changed"].append(False)
            else:
                self.index["sentence_changed"].append(True)
        return self.books

    # Turn self.index into a pd.DataFrame file.
    def frame(self):
        df = pd.DataFrame(self.index, columns = ["word", "sentence_changed", "sentence", "bingspell", "url"])
        df = df.sort_values(by=["word"], inplace=False, ascending=True)
        df = df.set_index(np.arange(len(self.index["word"])))
        df.index.name = "index"
        return df
