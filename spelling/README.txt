{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww23560\viewh12120\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 a) selection.py is the main program. It reads books.json.gz, scores each book in it, orders them by their scores, corrects any spelling/grammar errors, and outputs selection.json.gz and df_misspelled.xlsx. In selection.json.gz, there are 15,000 selected books in total, of which 9,534 are from reviewed books and 5466 are from unreviewed books. df_misspelled.xlsx is an excel file for you to see how many misspelled words there are in the selected books and how the misspelled words were corrected in a sentence level. Most of them were corrected well. However, a very few of them were not corrected because either the words do not exist, the autocorrection program did not recognize them, or they are actually correct words but are not included in dictionary.txt. You might want to toss the selection.json.gz file into your program.\
\
b) dictionary.txt, helper.py, bingspell.py, and score.py are secondary programs that help selection.py. \
\
c) dictionary.txt contains exceptional words that aspell and spellchecker libraries do not have; these are\
proper nouns, onomatopoeias, people's names, etc.\
\
d) The threshold numbers used in score.py are based on the average numbers of DLM books.}