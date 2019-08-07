import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

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

    def close(self):
        self.driver.close()
