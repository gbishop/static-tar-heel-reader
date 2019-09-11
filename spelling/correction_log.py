import gzip
import json

books = json.load(gzip.open("books.json.gz", 'rt', encoding='utf-8')) # ORIGINAL BOOKS
books_corrected = json.loads(open("books_corrected.json").read()) # CORRECTED BOOKS
with open('correction_log.txt', 'w', encoding='utf-8') as fp:
    for i in range(0, len(books)):
        temp1 = books[i] # ORIGINAL BOOKS
        temp2 = books_corrected[i] # CORRECTED BOOKS
        link = "https://tarheelreader.org{0}".format(temp1['link'])
        page_number = 1
        for j in range(0, len(temp1['pages'])):
            url = link + "{0}/".format(page_number)
            if temp1['pages'][j]['text'] != temp2['pages'][j]['text']:
                print("Book Title= {0}".format(temp1['title']))
                print("Author= {0}".format(temp1['author']))
                print("Page= {0}".format(j+1))
                print("url= {0}".format(url))
                print("temp1= {0}".format(temp1['pages'][j]['text'])) # ORIGINAL SENTENCE
                print("temp2= {0}".format(temp2['pages'][j]['text'])) # CORRECTED SENTENCE
                print("\n")
                fp.write("Book Title= {0}\n".format(temp1['title']))
                fp.write("Author= {0}\n".format(temp1['author']))
                fp.write("Page= {0}\n".format(j+1))
                fp.write("url= {0}\n".format(url))
                fp.write("temp1= {0}\n".format(temp1['pages'][j]['text'])) # ORIGINAL SENTENCE
                fp.write("temp2= {0}\n".format(temp2['pages'][j]['text'])) # CORRECTED SENTENCE
                fp.write("\n")
            page_number += 1

print("\n")
print("Task complete!")
