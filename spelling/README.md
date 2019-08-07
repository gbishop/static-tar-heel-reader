1. selection.py is the main program. It reads books.json.gz, scores each book in it, orders them by their scores, corrects any spelling/grammar errors, and outputs selection.json.gz and df_misspelled.xlsx. In selection.json.gz, there are 15,000 selected books in total, of which 9,534 are from reviewed books and 5466 are from unreviewed books. df_misspelled.xlsx is an excel file for you to see how many misspelled words there are in the selected books and how the misspelled words were corrected in a sentence level. Most of them were corrected well. However, a very few of them were not corrected because either the words do not exist, the autocorrection program did not recognize them, or they are actually correct words but are not included in dictionary.txt. You might want to toss the selection.json.gz file into your program.

2. dictionary.txt, helper.py, bingspell.py, and score.py are secondary programs that help selection.py.

3. dictionary.txt contains exceptional words that aspell and spellchecker libraries do not have; these are
proper nouns, onomatopoeias, people's names, etc.

4. The threshold numbers used in score.py are based on the average numbers of DLM books.
