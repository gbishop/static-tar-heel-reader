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

import {stem} from 'stemr';

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

async function getIndexForTerm(term: string): Promise<string[]> {
  const resp = await fetch('index/' + term);
  let result;
  if (resp.ok) {
    const text = await resp.text();
    console.log('text', text.length);
    const N = text.length / 3;
    result = new Array(N);
    for (let i = 0; i < N; i++) {
      result[i] = text.slice(i * 3, i * 3 + 3);
    }
  } else {
    result = [];
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

function bidToIndex(bid: string): string {
  return `${bid[0]}/${bid[1]}/index.html`;
}

async function getBookCover(bid: string): Promise<HTMLElement | null> {
  // get the prefix of the path for this index
  const prefix = bid
    .split('')
    .join('/')
    .slice(0, 4);
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

async function find() {
  const terms = getQueryTerms();
  const indexes = [];
  for (const term of terms) {
    const index = await getIndexForTerm(term);
    if (index.length) {
      indexes.push(index);
    }
  }
  let i = 0;
  const node = document.querySelector('ul');
  if (node) {
    let last;
    while ((last = node.lastChild)) node.removeChild(last);
  }
  for (const bid of intersectIndexes(indexes)) {
    const book = await getBookCover(bid);
    if (book) {
      i += 1;
      addBookToPage(book);
    }
    if (i >= 20) {
      // figure out how to continue
      break;
    }
  }
}

interface SearchState {
  search: string,
  reviewed: boolean,
  category: string,
  audience: string,
  page: number,
}

const defaultSearchState: SearchState = {
  search: '',
  reviewed: true,
  category: '',
  audience: 'E',
  page: 1
}

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
  form.reviewed.value = s.reviewed ? 'R' : 'U';
  form.category.value = s.category;
  form.audience.value = s.audience;
}

function persistState(): void {
  updateState();
  const s = JSON.stringify(searchState);
  localStorage.setItem('searchState', s);
  console.log('persist', s);
}

function restoreState(): void {
  const s = localStorage.getItem('searchState');
  console.log('restore', s);
  if (s) {
    searchState = JSON.parse(s);
  } else {
    searchState = {...defaultSearchState};
  }
}

function init() {
  const form = document.querySelector('form');
  if (form) {
    restoreState();
    updateControls(form);
    form.addEventListener('submit', e => {
      e.preventDefault();
      find();
    });
    form.addEventListener('change', persistState);
    find();
  }
}

function play() {
  console.log('play');
  let A = new ArraySet(['000', '001', '010', '100']);
  let B = new ArraySet(['000', '010', '011', '100']);
  let C = new Intersection(A, B);
  let D = new RangeSet('000','099');
  let E = new Intersection(D, C);
  let c = E.next();
  while (c) {
    console.log(c);
    c = E.next();
  }
  find();
  let s = getSearchSettings();
  s.page += 1;
  setSearchSettings(s);
  console.log(getSearchSettings());
}

window.addEventListener('load', init);
