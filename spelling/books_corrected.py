import gzip
import json
import pandas as pd
import numpy as np
import os
import time
import each_books


# Get all books
books = json.load(gzip.open("books.json.gz", 'rt', encoding='utf-8')) # Number of books: 68078

# Divide books
books1 = books[:10000] # 10000
books2 = books[10000:20000] # 10000

books3_1 = books[20000:22500] # 2500
books3_2 = books[22500:25000] # 2500
books3_3 = books[25000:27500] # 2500
books3_4 = books[27500:30000] # 2500

books4_1 = books[30000:32500] # 2500
books4_2 = books[32500:35000] # 2500
books4_3 = books[35000:37500] # 2500
books4_4 = books[37500:40000] # 2500

books5_1 = books[40000:42500] # 2500
books5_2 = books[42500:45000] # 2500
books5_3 = books[45000:47500] # 2500
books5_4 = books[47500:50000] # 2500

books6_1 = books[50000:52500] # 2500
books6_2 = books[52500:55000] # 2500
books6_3 = books[55000:57500] # 2500
books6_4 = books[57500:60000] # 2500

books7_1 = books[60000:64000] # 4000
books7_2 = books[64000:] # 4078


# Correct books1
start = time.time()  # Save start time
books1 = each_books.put_books(books1)
with open('books1.json', 'w', encoding='utf-8') as fp:
    json.dump(books1, fp)
print("books1 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books2
start = time.time()  # Save start time
books2 = each_books.put_books(books2)
with open('books2.json', 'w', encoding='utf-8') as fp:
    json.dump(books2, fp)
print("books2 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books3_1
start = time.time()  # Save start time
books3_1 = each_books.put_books(books3_1)
with open('books3_1.json', 'w', encoding='utf-8') as fp:
    json.dump(books3_1, fp)
print("books3_1 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books3_2
start = time.time()  # Save start time
books3_2 = each_books.put_books(books3_2)
with open('books3_2.json', 'w', encoding='utf-8') as fp:
    json.dump(books3_2, fp)
print("books3_2 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books3_3
start = time.time()  # Save start time
books3_3 = each_books.put_books(books3_3)
with open('books3_3.json', 'w', encoding='utf-8') as fp:
    json.dump(books3_3, fp)
print("books3_3 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books3_4
start = time.time()  # Save start time
books3_4 = each_books.put_books(books3_4)
with open('books3_4.json', 'w', encoding='utf-8') as fp:
    json.dump(books3_4, fp)
print("books3_4 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books4_1
start = time.time()  # Save start time
books4_1 = each_books.put_books(books4_1)
with open('books4_1.json', 'w', encoding='utf-8') as fp:
    json.dump(books4_1, fp)
print("books4_1 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books4_2
start = time.time()  # Save start time
books4_2 = each_books.put_books(books4_2)
with open('books4_2.json', 'w', encoding='utf-8') as fp:
    json.dump(books4_2, fp)
print("books4_2 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books4_3
start = time.time()  # Save start time
books4_3 = each_books.put_books(books4_3)
with open('books4_3.json', 'w', encoding='utf-8') as fp:
    json.dump(books4_3, fp)
print("books4_3 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books4_4
start = time.time()  # Save start time
books4_4 = each_books.put_books(books4_4)
with open('books4_4.json', 'w', encoding='utf-8') as fp:
    json.dump(books4_4, fp)
print("books4_4 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books5_1
start = time.time()  # Save start time
books5_1 = each_books.put_books(books5_1)
with open('books5_1.json', 'w', encoding='utf-8') as fp:
    json.dump(books5_1, fp)
print("books5_1 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books5_2
start = time.time()  # Save start time
books5_2 = each_books.put_books(books5_2)
with open('books5_2.json', 'w', encoding='utf-8') as fp:
    json.dump(books5_2, fp)
print("books5_2 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books5_3
start = time.time()  # Save start time
books5_3 = each_books.put_books(books5_3)
with open('books5_3.json', 'w', encoding='utf-8') as fp:
    json.dump(books5_3, fp)
print("books5_3 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books5_4
start = time.time()  # Save start time
books5_4 = each_books.put_books(books5_4)
with open('books5_4.json', 'w', encoding='utf-8') as fp:
    json.dump(books5_4, fp)
print("books5_4 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books6_1
start = time.time()  # Save start time
books6_1 = each_books.put_books(books6_1)
with open('books6_1.json', 'w', encoding='utf-8') as fp:
    json.dump(books6_1, fp)
print("books6_1 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books6_2
start = time.time()  # Save start time
books6_2 = each_books.put_books(books6_2)
with open('books6_2.json', 'w', encoding='utf-8') as fp:
    json.dump(books6_2, fp)
print("books6_2 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books6_3
start = time.time()  # Save start time
books6_3 = each_books.put_books(books6_3)
with open('books6_3.json', 'w', encoding='utf-8') as fp:
    json.dump(books6_3, fp)
print("books6_3 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books6_4
start = time.time()  # Save start time
books6_4 = each_books.put_books(books6_4)
with open('books6_4.json', 'w', encoding='utf-8') as fp:
    json.dump(books6_4, fp)
print("books6_4 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books7_1
start = time.time()  # Save start time
books7_1 = each_books.put_books(books7_1)
with open('books7_1.json', 'w', encoding='utf-8') as fp:
    json.dump(books7_1, fp)
print("books7_1 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time

# Correct books7_2
start = time.time()  # Save start time
books7_2 = each_books.put_books(books7_2)
with open('books7_2.json', 'w', encoding='utf-8') as fp:
    json.dump(books7_2, fp)
print("books7_2 complete!")
print("time :", time.time() - start)  # Current time - start time = operation time


# Combine books
books_corrected = []
books_corrected += json.loads(open("books1.json").read())
books_corrected += json.loads(open("books2.json").read())

books_corrected += json.loads(open("books3_1.json").read())
books_corrected += json.loads(open("books3_2.json").read())
books_corrected += json.loads(open("books3_3.json").read())
books_corrected += json.loads(open("books3_4.json").read())

books_corrected += json.loads(open("books4_1.json").read())
books_corrected += json.loads(open("books4_2.json").read())
books_corrected += json.loads(open("books4_3.json").read())
books_corrected += json.loads(open("books4_4.json").read())

books_corrected += json.loads(open("books5_1.json").read())
books_corrected += json.loads(open("books5_2.json").read())
books_corrected += json.loads(open("books5_3.json").read())
books_corrected += json.loads(open("books5_4.json").read())

books_corrected += json.loads(open("books6_1.json").read())
books_corrected += json.loads(open("books6_2.json").read())
books_corrected += json.loads(open("books6_3.json").read())
books_corrected += json.loads(open("books6_4.json").read())

books_corrected += json.loads(open("books7_1.json").read())
books_corrected += json.loads(open("books7_2.json").read())
print("len(books_corrected): {0}".format(len(books_corrected)))


# Save the corrected books as a json file
with open('books_corrected.json', 'w', encoding='utf-8') as fp:
    json.dump(books_corrected, fp)
# Save the corrected books as a json.gz file
with open("books_corrected.json", "rb") as fp:
    with gzip.open("books_corrected.json.gz", "wb") as fp2:
        fp2.writelines(fp)
print("books_corrected complete!")


# Remove unnecessary books
os.remove('books1.json')
os.remove('books2.json')

os.remove('books3_1.json')
os.remove('books3_2.json')
os.remove('books3_3.json')
os.remove('books3_4.json')

os.remove('books4_1.json')
os.remove('books4_2.json')
os.remove('books4_3.json')
os.remove('books4_4.json')

os.remove('books5_1.json')
os.remove('books5_2.json')
os.remove('books5_3.json')
os.remove('books5_4.json')

os.remove('books6_1.json')
os.remove('books6_2.json')
os.remove('books6_3.json')
os.remove('books6_4.json')

os.remove('books7_1.json')
os.remove('books7_2.json')


print("\n")
print("Task complete!")
