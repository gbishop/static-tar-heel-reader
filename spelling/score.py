import re
from nltk.tokenize import sent_tokenize, word_tokenize
#---------------------------------------------------------------
# Score Criteria:
# Criterion 1) Categorized (5%)
# Criterion 2) Audience (5%)
# Criterion 3) Right_form (30%)
#               3.1) Page_number (20%)
#               3.2) Avg. Sentence_number (5%)
#               3.3) Avg. Word_number (5%)
# Criterion 4) Misspelling (30%)
# Criterion 5) Rating (15%)
# Criterion 6) Author's credit (15%)
#---------------------------------------------------------------
# Criterion 1) Categorized (5%)
def categorized(book):
    score = 0
    if len(book['categories']) > 0 or len(book['tags']) > 0:
        score += 5
    else:
        score -= 5
    return score
#---------------------------------------------------------------
# Criterion 2) Audience (5%)
def audience(book):
    score = 0
    if book['audience'] == "E":
        score += 5
    elif book['audience'] == "C":
        score += 3
    else:
        score -= 5
    return score
#---------------------------------------------------------------
# Criterion 3) Right_form (30%)
# Criterion 3.1) Page_number (20%)
def page_number(book):
    score = 0
    pages = book['pages'][1:]
    page_num = len(pages)
    if page_num >= 11 and page_num <= 17:
        score += 20
    elif page_num >= 8 and page_num <= 20:
        score += 15
    elif page_num >= 5 and page_num <= 23:
        score += 10
    else:
        score -= 20
    return score

# Criterion 3.2) Avg. Sentence_number (5%)
def sentence_number(book):
    score = 0
    pages = book['pages'][1:]
    page_num = len(pages)
    sentence_num = 0
    for page in pages:
        sentences = sent_tokenize(page['text'])
        sentence_num += len(sentences)
    avg_sentence_num = sentence_num/page_num
    if avg_sentence_num <= 3:
        score += 5
    elif avg_sentence_num <= 4:
        score += 3
    else:
        score -= 5
    return score

# Criterion 3.3) Avg. Word_number (5%)
wordRe = re.compile(r"[a-zA-Z]+\'[a-zA-Z]+|[a-zA-Z]+")
def word_number(book):
    score = 0
    pages = book['pages'][1:]
    page_num = len(pages)
    word_num = 0
    for page in pages:
        words = wordRe.findall(page['text'])
        word_num += len(words)
    avg_word_num = word_num/page_num
    # avg = 7; std.dev = +-3
    if avg_word_num >= 4 and avg_word_num <= 10:
        score += 5
    elif avg_word_num >= 1 and avg_word_num <= 13:
        score += 3
    elif avg_word_num <= 16:
        score += 1
    else:
        score -= 5
    return score

def right_form(book):
    score = 0
    score += page_number(book)
    score += sentence_number(book)
    score += word_number(book)
    return score
#---------------------------------------------------------------
# Criterion 4) Misspelling (30%)
def misspelling(book):
    score = 0
    if book['misspelled'] == 0:
        score += 30
    elif book['misspelled'] == 1:
        score += 20
    elif book['misspelled'] == 2:
        score += 10
    else:
        score -= 30
    return score
#---------------------------------------------------------------
# Criterion 5) Rating (15%)
def help_value(book):
    value = 0
    if book['rating_value'] >= 2.5: # for 2.5 and 3 ratings
        value += 5
    elif book['rating_value'] < 2.5 and book['rating_value'] >= 1.5: # for 1.5 and 2 ratings
        value += 3
    elif book['rating_value'] < 1.5: # for 0, 0.5 and 1 ratings
        value -= 5
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

def rating(book):
    value = help_value(book)
    weight = help_count(book) # The rating count works as weight
    return value*weight
#---------------------------------------------------------------
# Criterion 6) Author's credit (15%)
class Authors_credit:
    def __init__(self, books):
        self.author_score = self.author_score(books)
        self.author_book = self.author_book(books)
        self.helper()

    def author_score(self, books):
        author_score = {}
        for book in books:
            author_score[book['author']] = 0
        return author_score

    def author_book(self, books):
        author_book = {}
        for book in books:
            if book['author'] not in author_book:
                author_book[book['author']] = [book]
            else:
                author_book[book['author']].append(book)
        return author_book

    def help_booknum(self, author):
        booknum = len(self.author_book[author])
        score = 0
        if booknum == 1: # Beginner
            score += 1
        elif booknum > 1 and booknum <= 5: # Apprentice
            score += 2
        elif booknum > 5 and booknum <= 15: # Competent
            score += 3
        elif booknum > 15 and booknum <= 60: # Expert
            score += 4
        elif booknum > 60: # Institution
            score += 5
        return score

    def help_misspelling(self, author):
        books = self.author_book[author]
        book_num = len(books)
        score = 0
        misspelled = 0
        for book in books:
            misspelled += book['misspelled']
        avg_misspelled = misspelled/book_num
        if avg_misspelled == 0:
            score += 3
        elif avg_misspelled <= 1:
            score += 2
        elif avg_misspelled <= 2:
            score += 1
        else:
            score -= 3
        return score

    def help_pages(self, author):
        books = self.author_book[author]
        book_num = len(books)
        score = 0
        pages = 0
        for book in books:
            pages += len(book['pages'][1:])
        avg_pages = pages/book_num
        if avg_pages >= 11 and avg_pages <= 17:
            score += 3
        elif avg_pages >= 8 and avg_pages <= 20:
            score += 2
        elif avg_pages >= 5 and avg_pages <= 23:
            score += 1
        else:
            score -= 3
        return score

    def helper(self):
        for author in self.author_score.keys():
            weight = self.help_booknum(author) # The number of books works as weight
            misspelling = self.help_misspelling(author)
            pages = self.help_pages(author)
            self.author_score[author] = weight*((misspelling+pages)/2)

    def authors_credit(self, book):
        return self.author_score[book['author']]
#--------------------------------------------------------------
# 1) Take books as input, and score each book by the 6 criteria
# 2) Score ranges from -100.0 to +100.0
def put_books(books):
    # Add 'score' dictionary in the books
    for book in books:
        book['score'] = 0

    # Create an Authors_credit object to use authors_credit() instance method
    authors_credit = Authors_credit(books)
    authors_credit.helper()

    # Score books
    for book in books:
        book['score'] += categorized(book) # Criterion 1) Categorized (5%)
        book['score'] += audience(book) # Criterion 2) Audience (5%)
        book['score'] += right_form(book) # Criterion 3) Right_form (30%)
        book['score'] += misspelling(book) # Criterion 4) Misspelling (30%)
        book['score'] += rating(book) # Criterion 5) Rating (15%)
        book['score'] += authors_credit.authors_credit(book) # Criterion 6) Author's credit (15%)
    return books
