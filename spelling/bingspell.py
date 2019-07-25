import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def put_sentence(sentence):
    driver = webdriver.Chrome('/Users/chansun/Downloads/chromedriver-2')
    driver.get('https://azure.microsoft.com/en-us/services/cognitive-services/spell-check/')
    search_box = driver.find_element_by_name("Query")
    search_box.clear()
    search_box.send_keys(sentence)
    button = driver.find_element_by_xpath("//input[@type='submit']")
    #driver.implicitly_wait(5)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2) # 2 초 대기
    correction = driver.find_element_by_id("spell-check-preview").text
    #print(correction)
    #req = driver.page_source
    #soup=BeautifulSoup(req, 'html.parser')
    #rows = soup.findAll('div', {'class':'cs-demo-json'})
    #json = rows[0].text.strip()
    #myDict = eval(json)
    #print(type(json))
    #print(type(myDict))
    #for row in rows:
    #    print(row.text.strip())
    driver.close()
    return correction

def put_sentences(sentences):
    driver = webdriver.Chrome('/Users/chansun/Downloads/chromedriver-2')
    driver.get('https://azure.microsoft.com/en-us/services/cognitive-services/spell-check/')
    search_box = driver.find_element_by_name("Query")
    corrections = []
    for sentence in sentences:
        search_box.clear()
        search_box.send_keys(sentence)
        button = driver.find_element_by_xpath("//input[@type='submit']")
        #driver.implicitly_wait(5)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2) # 2 초 대기
        correction = driver.find_element_by_id("spell-check-preview").text
        corrections.append(correction)
        #print(correction)
        #req = driver.page_source
        #soup=BeautifulSoup(req, 'html.parser')
        #rows = soup.findAll('div', {'class':'cs-demo-json'})
        #json = rows[0].text.strip()
        #myDict = eval(json)
        #print(type(json))
        #print(type(myDict))
    driver.close()
    return corrections

#sentence = "People abandonded fireworks but some people keep fire-works in their homes."
#print(sentence)
#print("\n")
#print(put_sentence(sentence))

#sentences = ["People abandonded fireworks but some people keep fire-works in their homes.", "Sometimes a small boat makes a good afteroon snack.", "He lectured agaist slavery in the U.S and in Great Britain. He also held government jobs."]
#for sentence in sentences:
#    print(sentence)
#print("\n")
#print(put_sentences(sentences))
