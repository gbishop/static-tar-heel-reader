import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import aspell
import spellchecker
#from nltk.corpus import stopwords
import contractions


spell = aspell.Speller("lang", "en")
spell2 = spellchecker.SpellChecker()
wordRe = re.compile(r"[a-zA-Z]+\'[a-zA-Z]+|[a-zA-Z]+")


# Get the dicitonary
word_dictionary = set()
with open('dictionary.txt', 'r') as fp:
    lines = fp.readlines()
    word_dictionary.update([line.replace("\n", "") for line in lines if line[0] != "#"])


# Take a sentence as input, access an autocorrect website,
# correct spelling/grammar errors in the sentecne,
# and return the corrected sentence.
def put_sentence(sentence):
    driver = webdriver.Chrome('/Users/chansun/Downloads/chromedriver-2')
    driver.get('https://azure.microsoft.com/en-us/services/cognitive-services/spell-check/')
    search_box = driver.find_element_by_name("Query")
    search_box.clear()
    search_box.send_keys(sentence)
    button = driver.find_element_by_xpath("//input[@type='submit']")
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2.0) # Sleep for 2.0 sec
    correction = driver.find_element_by_id("spell-check-preview").text
    driver.close()
    return correction

# Take a list of sentences as input, access an autocorrect website,
# read through every sentence and correct spelling/grammar errors in it,
# and return the list of corrected sentences.
def put_sentences(sentences):
    driver = webdriver.Chrome('/Users/chansun/Downloads/chromedriver-2')
    driver.get('https://azure.microsoft.com/en-us/services/cognitive-services/spell-check/')
    search_box = driver.find_element_by_name("Query")
    corrections = []
    for sentence in sentences:
        search_box.clear()
        search_box.send_keys(sentence)
        button = driver.find_element_by_xpath("//input[@type='submit']")
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2.0) # Sleep for 2.0 sec
        correction = driver.find_element_by_id("spell-check-preview").text
        corrections.append(correction)
    driver.close()
    return corrections

# Access an autocorrect website (initializer),
# and take a sentence and correct spelling/grammar errors in the sentence (put_sentence method),
# and close the autocorrect website (close mthod).
class Bingspell():
    def __init__(self):
        self.driver = webdriver.Chrome('/Users/chansun/Downloads/chromedriver-2')
        self.driver.get('https://azure.microsoft.com/en-us/services/cognitive-services/spell-check/')
        self.search_box = self.driver.find_element_by_name("Query")

    def put_sentence(self, sentence):
        self.search_box.clear()
        self.search_box.send_keys(sentence)
        button = self.driver.find_element_by_xpath("//input[@type='submit']")
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(2.0) # Sleep for 2.0 sec
        correction = self.driver.find_element_by_id("spell-check-preview").text
        return correction

    def put_book(self, book):
        for page in book['pages']:
            page_copy = page['text'].replace("\n", " ")
            text = contractions.fix(page['text']) ## Replace contractions; e.g., can't --> cannot // won't --> will not
            text = text.replace("'s", "") ## remove 's (apostrophe and s)
            words = wordRe.findall(text)
            # words = [w for w in words if not w in stop_words] ## Remove stop words
            words = [w for w in words if not w in word_dictionary] ## Remove proper nouns / person's name / onomatopoeia
            for word in words:
                if not spell.check(word) and len(spell2.unknown([word])) >= 1:
                    try:
                        page['text'] = self.put_sentence(page_copy)
                        break
                    except:
                        print("Exception occured in {0}".format(book['title']))
                        print("page:\n{0}\n".format(page_copy))
                        break
        return book

    def close(self):
        self.driver.close()
