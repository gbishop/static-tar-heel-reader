# Notes on Static THR 5 September 2019

## Key idea

I'm trying to implement full-text search with static hosting, reasonable file
sizes, and limited computation. I chose to give each book a unique ID encoded in
(say) base 36 (0-9 and A-Z). The ids are sorted in some order (currently date)
with _reviewed_ books first because we want to feature those.

The index for a word simply lists the book ids as a string. For example, the
index for the word "did" is `3C5475ACAF` with 2-digit book ids encoded in
base 16. "did" occurs in 6 books in that tiny 100-book collection.

### Issues

1. I currently store the words in files with the word as their name. The above
   index for "did" is in the file index/did. This will, no doubt, cause problems
   when we try to include languages with unicode characters. Perhaps we should
   hash the word and use that for the filename?
2. I store categories as 4-letter "words" in uppercase. This has to change.
3. This coding is inefficient with lots of leading zeros wasting space. Can we
   easily do better?
4. Should we consider using a higher base for the ids and then translating when
   we go to the URL?
5. Is there some better approach? This is the first thing I thought of that
   allowed incremental results.
6. What order should they be in? Popularity?
7. Which words should not be indexed?

## BookSet.ts

Implements sort-merge algorithms for selecting subsets of books. Assumes the
sort has already by done. I chose this approach because I wanted to produce
search outputs incrementally.

### Issues

1. Should we change the encoding? This is the only place that would have to
   change.
2. Encoding the first unreviewed in config.json is a hack.

## BookSet.test.ts

Simple tests for BookSet.ts.

## book.mako book-index.mako

The generated books and indexes down in the content folder are generated from
these templates.

## book.css book.ts

Supporting styles and code for books.

## choose.html

Choose a book to read from a _favorites_ page. Identical to the _find_ page
except for the absence of search controls.

## favorites.css favorites.html favorites.ts

Manage favorites page and supporting styles and code.

## find.css find.html find.ts

Book search page and supporting files.

### Issues

1. We should signal the user when a word is not indexed; it currently ignores
   such words silently.
2. We should signal when we are working. Would help with testing as well.

## head.mako

Template for html page headers.

## images/

Icons uses on the site.

## index.css index.html index.ts

Home page for the site.

## manifest.json start-sw.ts worker.ts

Service worker prototype.

### Issues

1. How to update?
2. How much to precache?
3. Cache management strategy?
4. How to search offline?

## menu.mako

Template for the menu.

### Issues

1. I'm using the html5 disclosure element `details` to implement the menu. It
   seems accessible to me. Is it?

## settings.css settings.html settings.ts

Settings page.

### Issues

1. Ugly. Needs help.

## site.css

Site wide styles.

### Issues

1. Shouldn't this just be included in the page css?
2. Should we even have different css per page?

## speech.ts

Module for managing speech.

### Issues

1. Any way to manage the list of voices? For English books shouldn't it only
   display EN voices?

## state.ts

Module for persistent state.

### Issues

1. We're using local storage and indexedDB. These are domain specific. How to
   manage multiple editions on the same domain?

## swipe.ts

Handle swipe events.
