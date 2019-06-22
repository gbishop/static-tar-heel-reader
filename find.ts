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

// persistant state
import state from './state';
// porter2 stemmer
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
  if (state.category) {
    terms.push(state.category);
  }
  if (state.audience == 'C') {
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
    if (state.reviewed) {
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
    if (state.reviewed) {
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
  if (state.audience == 'E') {
    const caution = await getIndexForTerm('CAUTION');
    ids = new Difference(ids, caution);
  }
  const start = state.pages[state.pages.length - 1];
  if (start) {
    ids.skipTo(start);
  }
  return render();
}

function empty(node: HTMLElement) {
  let last;
  while ((last = node.lastChild)) node.removeChild(last);
}

async function render() {
  // clear the old ones from the page
  empty(document.querySelector('ul'));
  const SS = state;

  let offset = SS.page * state.booksPerPage;
  let bid;
  let i;
  for (i = 0; i < state.booksPerPage + 1; i++) {
    const o = i + offset;
    bid = SS.pages[o] || ids.next();
    if (!bid) {
      break;
    }
    SS.pages[o] = bid;
    if (i >= state.booksPerPage) {
      break;
    }
    const book = await getBookCover(bid);
    addBookToPage(book);
  }
  state.persist();

  // visibility of back and next buttons
  pagingVisibility();
}

function pagingVisibility() {
  // visibility of back and next buttons
  const SS = state;
  document.querySelector('#back').classList.toggle('hidden', SS.page <= 0);
  document
    .querySelector('#next')
    .classList.toggle('hidden', !SS.pages[(SS.page + 1) * state.booksPerPage]);
}

function updateState(): void {
  const form: HTMLFormElement = document.querySelector('form');
  state.search = form.search.value;
  state.reviewed = form.reviewed.value == 'R';
  state.category = form.category.value;
  state.audience = form.audience.value;
}

function updateAndChange(selector: string, value: string, c = true) {
  const e = document.querySelector(selector) as HTMLInputElement;
  e.value = value;
  if (c) e.dispatchEvent(new Event('change'));
}

function updateControls(form: HTMLFormElement): void {}

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
function activateCurrent(e: KeyboardEvent) {
  const selected = document.querySelector('.selected a, a.selected');
  if (selected) {
    e.preventDefault();
    (selected as HTMLAnchorElement).click();
  }
}

async function init() {
  /* fetch configuration for the content */
  config = await (await fetch('content/config.json')).json();

  const form = document.querySelector('form');
  if (form) {
    /* handle searches */
    form.addEventListener('submit', e => {
      e.preventDefault();
      updateState();
      state.pages = [];
      state.page = 0;
      state.persist();
      find();
    });

    /* enable stepping through pages of results */
    document.querySelector('#next').addEventListener('click', e => {
      e.preventDefault();
      (e.target as HTMLElement).classList.remove('selected');
      state.page += 1;
      render();
    });
    document.querySelector('#back').addEventListener('click', e => {
      e.preventDefault();
      (e.target as HTMLElement).classList.remove('selected');
      state.page -= 1;
      render();
    });

    /* switch control based on keys */
    window.addEventListener('keydown', e => {
      if (e.code == 'ArrowRight' || e.code == 'Space') {
        e.preventDefault();
        moveToNext();
      } else if (e.code == 'ArrowLeft' || e.code == 'Enter') {
        activateCurrent(e);
      }
    });

    /* handle changes to page color */
    document
      .querySelector('select[name=page]')
      .addEventListener('change', e => {
        state.pageColor = (e.target as HTMLInputElement).value;
        document.documentElement.style.setProperty(
          '--page-color',
          state.pageColor,
        );
      });

    /* handle changes to text color */
    document
      .querySelector('select[name=text]')
      .addEventListener('change', e => {
        state.textColor = (e.target as HTMLInputElement).value;
        document.documentElement.style.setProperty(
          '--text-color',
          state.textColor,
        );
      });

    /* handle changes to the number of books per page */
    document.querySelector('input[name=bpp]').addEventListener('change', e => {
      let newbpp = parseInt((e.target as HTMLInputElement).value);
      state.page = Math.floor((state.page * state.booksPerPage) / newbpp);
      state.booksPerPage = newbpp;
      state.persist();
      render();
    });

    /* update the dom from the button size control */
    document
      .querySelector('select[name=buttons]')
      .addEventListener('change', e => {
        state.buttonSize = (e.target as HTMLInputElement).value;
        const bs = state.buttonSize == 'none' ? 'small' : state.buttonSize;
        document.body.setAttribute('data-buttonSize', bs);
      });

    /* persist the state when the menu is closed */
    const menu = document.querySelector('details');
    menu.addEventListener('toggle', e => {
      if (!menu.open) {
        state.persist();
      }
    });

    /* Add a close button because some might not realized how to dismiss it */
    menu
      .querySelector('#close')
      .addEventListener('click', e => menu.removeAttribute('open'));

    /* now that the handlers are registered update the controls to restore
     * their saved values */
    form.search.value = state.search;
    form.reviewed.value = state.reviewed ? 'R' : '';
    form.category.value = state.category;
    form.audience.value = state.audience;
    updateAndChange('input[name=bpp]', '' + state.booksPerPage, false);
    updateAndChange('select[name=page]', state.pageColor);
    updateAndChange('select[name=text]', state.textColor);
    updateAndChange('select[name=buttons]', state.buttonSize);

    find();
  }
}

window.addEventListener('load', init);
