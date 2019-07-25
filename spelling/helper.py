import re
import os
import aspell
import spellchecker
#from nltk.corpus import stopwords
import contractions

spell = aspell.Speller("lang", "en")
spell2 = spellchecker.SpellChecker()
wordRe = re.compile(r"[a-zA-Z]+\'[a-zA-Z]+|[a-zA-Z]+")
##stop_words = set(stopwords.words('english')) ## Stop_words

# Remove books that contain a link to a website
def link_detect(book):
    wordRe = re.compile(r"www[.][a-zA-Z]+")
    wordRe2 = re.compile(r"WWW[.][a-zA-Z]+")
    wordRe3= re.compile(r"http")
    wordRe4= re.compile(r"HTTP")
    pages = book['pages']
    for page in pages:
        text = page['text']
        if len(wordRe.findall(text)) >= 1 or \
        len(wordRe2.findall(text)) >= 1 or \
        len(wordRe3.findall(text)) >= 1 or \
        len(wordRe4.findall(text)) >= 1:
            #print("link: {0}".format(text))
            return True
    return False

## Remove books that contain consecutively repeated characters (6 or more)
def repetition_detect(book):
    wordRe = re.compile(r'(([a-zA-Z])\2{6,})') ## Threshold: 6; e.g., zzzzzz, ahhhhhhh, Awwwwww, etc
    pages = book['pages']
    for page in pages:
        text = page['text']
        temp = wordRe.findall(text)
        temp = [word[0] for word in temp]
        if len(temp) >= 1:
            #print("repetition: {0}".format(text))
            return True
    return False

## Filter books by link_detect() and repetition_detect()
def filter(books):
    books = [book for book in books if not link_detect(book)]
    books = [book for book in books if not repetition_detect(book)]
    return books


# Get the dicitonary
word_dictionary = set()
with open('dictionary.txt', 'r') as fp:
    lines = fp.readlines()
    word_dictionary.update([line.replace("\n", "") for line in lines if line[0] != "#"])

# Get misspelled words
# Input: a book
# Output: a set of Misspelled words
def getMisspelled(book):
    misspelled = set()
    for page in book["pages"]:
        text = contractions.fix(page['text']) # Replace contractions; e.g., can't --> cannot // won't --> will not
        text = text.replace("'s", "") # Remove 's (apostrophe and s)
        words = wordRe.findall(text) # Tokenize a sentence into words
        words = list(set(words)) # Remove duplicates
        ## words = [w for w in words if not w in stop_words] ## Remove stop words
        words = [w for w in words if not w in word_dictionary] ## Remove correctly spelled words
        for word in words:
            if not spell.check(word) and not spell2.known([word]):
                misspelled.add(word)
    return misspelled
