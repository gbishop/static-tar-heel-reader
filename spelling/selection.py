import gzip
import json
import re
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
import numpy
import matplotlib.pyplot as plt


reviewed = json.load(gzip.open("reviewed.json.gz", 'rt', encoding='utf-8'))
unreviewed = json.load(gzip.open("unreviewed.json.gz", 'rt', encoding='utf-8'))
books = reviewed + unreviewed
#books = json.load(gzip.open("books.json.gz", 'rt', encoding='utf-8'))



# Generate scores
for book in reviewed: # Let's use only reviewed books for now
    book['score'] = 0
#---------------------------------------------------------------
'''
이거삭제???
# Score 1) deduction on inclusion of website link (spelcial case)
def link_detect(book):
    wordRe = re.compile(r"www[.][a-zA-Z]+")
    wordRe2 = re.compile(r"WWW[.][a-zA-Z]+")
    pages = book['pages']
    for page in pages:
        text = page['text']
        if len(wordRe.findall(text)) >= 1 or len(wordRe2.findall(text)) >= 1:
            return True
    return False
#books = [book for book in books if link_remove(book)]
#print(len(books))

for book in reviewed:
    if link_detect(book):
        book['score'] -= 100
    else:
        continue
'''




# Score 2) Categorized (5%)
# Score 3) Audience (5%)
# Score 4.1) Page_number (30%) <----- 20% ???
# Score 4.2) Sentence_number (5%)  <------ 넣어말아?
# Score 4.3) Word_number (5%) <------ 넣어말아?
# Score 5) Misspelling (30%)
# Score 6) Rating (15%)
# Score 7) Author_credit (15%)


#---------------------------------------------------------------

# Score 2) Categorized (5%)
for book in reviewed:
    if len(book["categories"]) > 0 or len(book["tags"]) > 0:
        book['score'] += 5
    else:
        book['score'] += 0
#---------------------------------------------------------------

# Score 3) Audience (5%)
for book in reviewed:
    if book["audience"] == "E":
        book['score'] += 5
    elif book["audience"] == "C":
        book['score'] += 3
    else:
        book['score'] += 0
#---------------------------------------------------------------

# Score 4) Page_number (30%)
for book in reviewed:
    pages = book['pages']
    page_num = len(pages)
    if page_num >= 11 and page_num <= 17:
        book['score'] += 30
    elif page_num >= 8 and page_num <= 20:
        book['score'] += 20
    elif page_num >= 5 and page_num <= 23:
        book['score'] += 10
    else:
        book['score'] -= 100


#---------------------------------------------------------------
# Score 4.2) Sentence_number (5%)  <------ 넣어말아?

for book in reviewed:
    pages = book['pages']
    page_num = len(pages)
    sentence_num = 0
    for page in pages:
        sentences = sent_tokenize(page['text'])
        sentence_num += len(sentences)
    avg_sentence_num = page_num/sentence_num
    if avg_sentence_num <= 3:
        book['score'] += 몇점?
    elif avg_sentence_num <= 4:
        book['score'] += 몇점?
    else:
        book['score'] -= 100


# Score 4.3) Word_number (5%) <------ 넣어말아?

wordRe = re.compile(r"[a-zA-Z]+\'[a-zA-Z]+|[a-zA-Z]+")
for book in reviewed:
    pages = book['pages']
    page_num = len(pages)
    word_num = 0
    for page in pages:
        words = wordRe.findall(page['text'])
        word_num += len(words)
    avg_word_num = page_num/word_num
    # 7 +- 3
    if avg_word_num >= 4 and avg_word_num <= 10:
        book['score'] += 몇점?
    elif avg_word_num >= 1 and avg_word_num <= 13:
        book['score'] += 몇점?
    elif avg_word_num <= 16:
        book['score'] += 몇점?
    else:
        book['score'] -= 100




#---------------------------------------------------------------
# Score 5) Misspelling (30%)
for book in reviewed:
    if book['misspelled'] == 0:
        book['score'] += 30
    elif book['misspelled'] > 0 and book['misspelled'] <= 2:
        book['score'] += 20
    elif book['misspelled'] > 2 and book['misspelled'] <= 5:
        book['score'] += 10
    elif book['misspelled'] > 5:
        book['score'] -= 100

#---------------------------------------------------------------
# Score 6) Rating (15%)

def help_value(book):
    value = 0
    if book['rating_value'] >= 2.5: # for 2.5 and 3 rating values
        value += 5
    elif book['rating_value'] < 2.5 and book['rating_value'] >= 1.5: # for 1.5 and 2 rating values
        value += 3
    elif book['rating_value'] < 1.5: # for 0, 0.5 and 1 rating values
        value += -100
    return value

def help_count(book):
    count = 0
    if book['rating_count'] <= 5:
        count += 0
    elif book['rating_count'] > 5 and book['rating_count'] <= 20:
        count += 1
    elif book['rating_count'] > 20 and book['rating_count'] <= 100:
        count += 2
    elif book['rating_count'] > 100:
        count += 3
    return count

for book in reviewed:
    value = help_value(book)
    count = help_count(book)
    book['score'] += (value*count)

#---------------------------------------------------------------
# Score 7) Author_credit (15%)


author_score = {}
for book in reviewed:
    author_score[book['author']] = 0
# authors = {author: score, author: score, ...}


# 각 author가 책을 몇권 썻는지 ################
author_book = {}
for book in reviewed:
    if book['author'] not in author_booknum:
        author_book[book['author']] = [book]
        #author_booknum[book['author']] = 1
    else:
        author_book[book['author']].append(book)
        #author_booknum[book['author']] += 1

#1 - beginner
#2~5 - apprentice
#6~15 - competent
#16~ - expert


def help_booknum(author):
    booknum = len(author_book[author])
    score = 0
    if booknum == 1: # beginner
        score += 1
    elif booknum > 1 and booknum <= 5: # apprentice
        score += 2
    elif booknum > 5 and booknum <= 15: # competent
        score += 3
    elif booknum > 15: # expert
        score += 4
    return score

def help_misspelling(author):
    books = author_book[author]
    num = len(books)
    score = 0
    misspelled = 0
    for book in books:
        misspelled += book['misspelled']
    avg_misspelled = misspelled/num
    if avg_misspelled == 0:
        score += 3
    elif avg_misspelled > 0 and avg_misspelled <= 2:
        score += 2
    elif avg_misspelled > 2 and avg_misspelled <= 5:
        score += 1
    elif avg_misspelled > 5:
        score -= 100
    return score

def help_pages(author):
    books = author_book[author]
    num = len(books)
    score = 0
    pages = 0
    for book in books:
        pages += len(book['pages'])
    avg_pages = pages/num
    if avg_pages >= 11 and avg_pages <= 17:
        score += 3
    elif avg_pages >= 8 and avg_pages <= 20:
        score += 2
    elif avg_pages >= 5 and avg_pages <= 23:
        score += 1
    else:
        score -= 100
    return score

for author in author_score.keys():
    weight = help_booknum(author)
    misspelling = help_misspelling(author)
    pages = help_pages(author)
    author_score[author] += weight*((misspelling+pages)/2)


for book in reviewed:
    book['score'] += author_score[book['author']]






'''
# rating_count 통계
# rating_value 통계
num = {}
num2 = []
for book in reviewed:
    num2.append(book['rating_value'])
    if not book['rating_value'] in num:
        num[book['rating_value']] = 1
    else:
        num[book['rating_value']] += 1
num3 = {}
#for i in sorted(num, key=lambda k : num[k], reverse=True):
for i in sorted(num):
    num3[i] = num[i]
print(num3)
print("\n")
print("Mean: {0}".format(numpy.mean(num2)))
print("Median: {0}".format(numpy.median(num2)))
print("Standard deviation: {0}".format(numpy.std(num2)))
'''






## misspelled 통계
'''
num = {}
num2 = []
for book in reviewed:
    num2.append(book['misspelled'])
    if not book['misspelled'] in num:
        num[book['misspelled']] = 1
    else:
        num[book['misspelled']] += 1

num3 = {}
for i in sorted(num, key=lambda k : num[k], reverse=True):
    num3[i] = num[i]

print(num3) # {0: 8205, 1: 993, 2: 221, 3: 85, 4: 29, 5: 16, 6: 6, 14: 3, 7: 2, 17: 2, 10: 2, 18: 2, 8: 2, 9: 1, 35: 1, 12: 1, 21: 1, 13: 1}

print("\n")
print("Mean: {0}".format(numpy.mean(num2)))
print("Median: {0}".format(numpy.median(num2)))
print("Standard deviation: {0}".format(numpy.std(num2)))
Mean: 0.22709704376893347
Median: 0.0
Standard deviation: 0.8867969083116339
'''











'''
pages = []
for book in books1:
    pages.append(len(book['pages'])-1)
print("Number of books: {0}".format(len(pages)))
print("Mean: {0}".format(numpy.mean(pages)))
print("Median: {0}".format(numpy.median(pages)))
print("Standard deviation: {0}".format(numpy.std(pages)))
Number of books: 9573
Mean: 10.197012430794944
Median: 9.0
Standard deviation: 5.394946338912095
'''





'''
pages = []
for book in books1:
    if authors[book['author']] == 1:
        pages.append(len(book['pages']) - 1)
print("Number of books: {0}".format(len(pages)))
print("Mean: {0}".format(numpy.mean(pages)))
print("Median: {0}".format(numpy.median(pages)))
print("Standard deviation: {0}".format(numpy.std(pages)))
Number of books: 3397
Mean: 9.674124227259346
Median: 9.0
Standard deviation: 4.973591001832657
'''




'''
pages = []
for book in books:
    if book['author'] == "DLM":
        pages.append(len(book['pages'])-1)
print("Number of books: {0}".format(len(pages)))
print("Mean: {0}".format(numpy.mean(pages)))
print("Median: {0}".format(numpy.median(pages)))
print("Standard deviation: {0}".format(numpy.std(pages)))
Number of books: 369
Mean: 14.363143631436314
Median: 14.0
Standard deviation: 3.008271682987659
'''



## Sentence는 4개 이상이면 감점하고
'''
sentence_num = []
for book in books:
    if book['author'] == "DLM":
        for page in book["pages"]:
            sentences = sent_tokenize(page['text'])
            sentence_num.append(len(sentences))
            if len(sentences) > 3:
                print(book['title'])
print("Mean: {0}".format(numpy.mean(sentence_num)))
print("Median: {0}".format(numpy.median(sentence_num)))
print("Standard deviation: {0}".format(numpy.std(sentence_num)))
Mean: 1.1097628240485384
Median: 1.0
Standard deviation: 0.3416784743298523
'''

'''
sentence_num = []
titles = set()
for book in reviewed:
    for page in book["pages"]:
        sentences = sent_tokenize(page['text'])
        sentence_num.append(len(sentences))
        if len(sentences) > 3:
            titles.add(book['title'])
print("Mean: {0}".format(numpy.mean(sentence_num)))
print("Median: {0}".format(numpy.median(sentence_num)))
print("Standard deviation: {0}".format(numpy.std(sentence_num)))
print("\n\n")
print(len(titles))
for title in titles:
    print(title)
'''


# Words는 30자 보다 많거나, 3자 보다 적으면 감점
'''
wordRe = re.compile(r"[a-zA-Z]+\'[a-zA-Z]+|[a-zA-Z]+")
word_num = []
titles = set()
for book in reviewed:
    if book['author'] == "DLM":
        for page in book["pages"]:
            words = wordRe.findall(page['text'])
            word_num.append(len(words))
            if len(words) < 3 and len(words) > 15:
                titles.add(book['title'])
print("Mean: {0}".format(numpy.mean(word_num)))
print("Median: {0}".format(numpy.median(word_num)))
print("Standard deviation: {0}".format(numpy.std(word_num)))
print("\n\n")
print(len(titles))
for title in titles:
    print(title)
Mean: 7.299347327571001
Median: 7.0
Standard deviation: 3.2998823347237782
'''












# Codes for producing/saving the file
'''
selection = books
for book in selection:
    del book['misspelled']
    del book['score']

with open('selection.json', 'w', encoding='utf-8') as fp:
    json.dump(selection, fp)

with open("selection.json", "rb") as fp:
    with gzip.open("selection.json.gz", "wb") as fp2:
        fp2.writelines(fp)

os.remove('correction.json')
'''
