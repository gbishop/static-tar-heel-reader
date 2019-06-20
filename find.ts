/*
 * get the string from the search box
 * split it into words
 * stem them and toss any we should ignore
 * for each word
 *   fetch the index and split it into ids
 * intersect the arrays of ids
 * for each id in the intersection
 *   get the index entry
 *   add it to the page
 *   quit and remember where we are if we have enough
 */

interface Config {
  base: number; // base of the encoding used for ids
  digits: number; // number of digits in each id
  lastReviewed: string; // id of last reviewed book
  first: string; // id of first book
  last: string; // id of last book
}

// load this down below in init
let config: Config;

import {stem} from 'stemr';

import {
  BookSet,
  Intersection,
  Difference,
  RangeSet,
  StringSet,
} from './BookSet';

function getQueryTerms(): string[] {
  const searchBox = document.querySelector('#search') as HTMLInputElement;
  const query = searchBox.value;
  if (query.length) {
    const pattern = /[a-z]{3,}/gi;
    return query.match(pattern).map(stem);
  } else {
    return [];
  }
}

async function getIndexForTerm(term: string): Promise<BookSet | null> {
  const resp = await fetch('content/index/' + term);
  let result;
  if (resp.ok) {
    const text = await resp.text();
    result = new StringSet(text, config.digits);
  }
  return result;
}

function intersect(x: string[], y: string[]): string[] {
  let i = 0,
    j = 0,
    r = [];
  while (i < x.length && j < y.length) {
    if (x[i] < y[j]) {
      i++;
    } else if (y[j] < x[i]) {
      j++;
    } else {
      r.push(x[i]);
      i++;
      j++;
    }
  }
  return r;
}

function intersectIndexes(indexes: string[][]) {
  // get the shortest one first
  indexes.sort((a, b) => a.length - b.length);
  return indexes.reduce(intersect);
}

async function getBookCover(bid: string): Promise<HTMLElement | null> {
  // get the prefix of the path for this index
  const prefix =
    'content/' +
    bid
      .split('')
      .slice(0, -1)
      .join('/') +
    '/';
  // fetch the index
  const resp = await fetch(prefix + 'index.html');
  // get the html
  const html = await resp.text();
  // parse it
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');
  // get the entry for this book
  const item = doc.getElementById(bid);
  if (item) {
    // fix the image URL
    const img: HTMLImageElement = item.querySelector('img');
    img.setAttribute('src', prefix + img.getAttribute('src'));
    // fix the link URL
    const link: HTMLAnchorElement = item.querySelector('a');
    link.setAttribute('href', prefix + link.getAttribute('href'));
  }
  return item;
}

function addBookToPage(book: HTMLElement) {
  const list = document.querySelector('ul');
  if (list) {
    list.appendChild(book);
  }
}

let ids: BookSet;

async function find() {
  const terms = getQueryTerms();
  if (searchState.category) {
    terms.push(searchState.category);
  }
  if (searchState.audience == 'C') {
    terms.push('CAUTION');
  }
  if (terms.length) {
    let tsets = await Promise.all(terms.map(getIndexForTerm));
    ids = tsets.reduce((p, c) => {
      if (!p) {
        return c;
      } else if (!c) {
        return p;
      }
      return new Intersection(p, c);
    });
    if (!ids) {
      // these numbers should come from a file
      ids = new RangeSet(config.first, config.last, config.digits, config.base);
    }
    if (searchState.reviewed) {
      // these numbers should come from a file
      ids = new Intersection(
        new RangeSet(
          config.first,
          config.lastReviewed,
          config.digits,
          config.base,
        ),
        ids,
      );
    }
  } else {
    if (searchState.reviewed) {
      // these numbers should come from a file
      ids = new RangeSet(
        config.first,
        config.lastReviewed,
        config.digits,
        config.base,
      );
    } else {
      // these numbers should come from a file
      ids = new RangeSet(config.first, config.last, config.digits, config.base);
    }
  }
  if (searchState.audience == 'E') {
    const caution = await getIndexForTerm('CAUTION');
    ids = new Difference(ids, caution);
  }
  const start = searchState.pages[searchState.pages.length - 1];
  if (start) {
    ids.skipTo(start);
  }
  return render();
}

function empty(node: HTMLElement) {
  let last;
  while ((last = node.lastChild)) node.removeChild(last);
}

const BooksPerPage = 12;

async function render() {
  // clear the old ones from the page
  empty(document.querySelector('ul'));
  const SS = searchState;

  let offset = SS.page * BooksPerPage;
  let bid;
  let i;
  for (i = 0; i < BooksPerPage + 1; i++) {
    const o = i + offset;
    bid = SS.pages[o] || ids.next();
    if (!bid) {
      break;
    }
    SS.pages[o] = bid;
    if (i >= BooksPerPage) {
      break;
    }
    const book = await getBookCover(bid);
    addBookToPage(book);
  }
  persistState();

  // visibility of back and next buttons
  document.querySelector('#back').classList.toggle('hidden', SS.page <= 0);
  document
    .querySelector('#next')
    .classList.toggle('hidden', !SS.pages[(SS.page + 1) * BooksPerPage]);
}

interface SearchState {
  search: string;
  reviewed: boolean;
  category: string;
  audience: string;
  page: number;
  pages: string[];
}

const defaultSearchState: SearchState = {
  search: '',
  reviewed: true,
  category: '',
  audience: 'E',
  page: 0,
  pages: [],
};

let searchState = {...defaultSearchState};

function updateState(): void {
  const form: HTMLFormElement = document.querySelector('form');
  const s = searchState;
  s.search = form.search.value;
  s.reviewed = form.reviewed.value == 'R';
  s.category = form.category.value;
  s.audience = form.audience.value;
}

function updateControls(form: HTMLFormElement): void {
  const s = searchState;
  form.search.value = s.search;
  form.reviewed.value = s.reviewed ? 'R' : '';
  form.category.value = s.category;
  form.audience.value = s.audience;
}

function persistState(): void {
  updateState();
  const s = JSON.stringify(searchState);
  localStorage.setItem('searchState', s);
}

function restoreState(): void {
  const s = localStorage.getItem('searchState');
  if (s) {
    searchState = JSON.parse(s);
  } else {
    searchState = {...defaultSearchState};
  }
}

/* allow switch (keyboard) selection of books */
function moveToNext() {
  // get the currently selected if any
  const selected = document.querySelector('.selected');
  // get all the items we can select
  const selectable = document.querySelectorAll(
    'li, a#back:not(.hidden), a#next:not(.hidden)',
  );
  // assume the first
  let next = 0;
  // if was selected, unselect it and compute the index of the next one
  if (selected) {
    selected.classList.remove('selected');
    next = ([].indexOf.call(selectable, selected) + 1) % selectable.length;
  }
  // mark the new one selected
  selectable[next].classList.add('selected');
  // make sure it is visible
  selectable[next].scrollIntoView({
    behavior: 'smooth',
    block: 'nearest',
    inline: 'nearest',
  });
}

/* click the currently selected link */
function activateCurrent() {
  const selected = document.querySelector('.selected a, a.selected');
  if (selected) {
    (selected as HTMLAnchorElement).click();
  }
}

async function init() {
  config = await (await fetch('content/config.json')).json();

  const form = document.querySelector('form');
  if (form) {
    restoreState();
    updateControls(form);
    form.addEventListener('submit', e => {
      e.preventDefault();
      searchState.pages = [];
      searchState.page = 0;
      persistState();
      find();
    });
    form.addEventListener('change', () => {
      // persistState();
    });
    document.querySelector('#next').addEventListener('click', e => {
      e.preventDefault();
      searchState.page += 1;
      render();
    });
    document.querySelector('#back').addEventListener('click', e => {
      e.preventDefault();
      searchState.page -= 1;
      render();
    });
    window.addEventListener('keydown', e => {
      if (e.code == 'ArrowRight' || e.code == 'Space') {
        e.preventDefault();
        moveToNext();
      } else if (e.code == 'ArrowLeft' || e.code == 'Enter') {
        e.preventDefault();
        activateCurrent();
      }
    });
    find();
  }
}

window.addEventListener('load', init);
