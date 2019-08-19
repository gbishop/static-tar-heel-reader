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
import state from "./state";
// porter2 stemmer
import { stem } from "stemr";

import swipe from "./swipe";

import { registerServiceWorker } from "./start-sw";

import {
  BookSet,
  Intersection,
  Difference,
  Limit,
  RangeSet,
  StringSet,
  ArraySet
} from "./BookSet";

import speak from "./speech";

function getQueryTerms(): string[] {
  const searchBox = document.querySelector("#search") as HTMLInputElement;
  const query = searchBox.value;
  if (query.length) {
    const pattern = /[a-z]{3,}/gi;
    return query.match(pattern).map(stem);
  } else {
    return [];
  }
}

async function getIndexForTerm(term: string): Promise<BookSet | null> {
  const resp = await fetch("content/index/" + term);
  let result;
  if (resp.ok) {
    const text = await resp.text();
    if (text.indexOf("-") > 0) {
      const parts = text.split("-");
      result = new RangeSet(parts[0], parts[1], config.digits, config.base);
    } else {
      result = new StringSet(text, config.digits);
    }
  }
  return result;
}

async function getBookCover(bid: string): Promise<HTMLElement | null> {
  // get the prefix of the path for this index
  const prefix =
    "content/" +
    bid
      .split("")
      .slice(0, -1)
      .join("/") +
    "/";
  // fetch the index
  const resp = await fetch(prefix + "index.html");
  // get the html
  const html = await resp.text();
  // parse it
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, "text/html");
  // get the entry for this book
  const item = doc.getElementById(bid);
  if (item) {
    // fix the image URL
    const img: HTMLImageElement = item.querySelector("img");
    img.setAttribute("src", prefix + img.getAttribute("src"));
    // fix the link URL
    const link: HTMLAnchorElement = item.querySelector("a");
    link.setAttribute("href", prefix + link.getAttribute("href"));
    // add the favorites indicator
    if (state.fav.bookIds.indexOf(bid) >= 0) {
      item.classList.add("F");
    }
  }
  return item;
}

let ids: BookSet;
// keep track of the ids we have shown
const displayedIds = <string[]>[];
let page = 0;

async function find() {
  if (state.mode === "choose" || state.mode === "edit") {
    ids = new ArraySet(state.fav.bookIds);
  } else {
    const terms = getQueryTerms();
    terms.push("AllAvailable");
    if (state.category) {
      terms.push(state.category);
    }
    if (state.audience == "C") {
      terms.push("CAUTION");
    }

    let tsets = await Promise.all(terms.map(getIndexForTerm));
    ids = tsets.reduce((p, c) => {
      if (!p) {
        return c;
      } else if (!c) {
        return p;
      }
      return new Intersection(p, c);
    });
    if (state.reviewed) {
      ids = new Limit(ids, config.lastReviewed);
    }
    if (state.audience == "E") {
      const caution = await getIndexForTerm("CAUTION");
      ids = new Difference(ids, caution);
    }
  }
  displayedIds.length = 0;
  if (location.hash) {
    const backFrom = location.hash.slice(1);
    console.log("skipping to", backFrom);
    // configure things so we're on the page with the current book
    while (1) {
      let id = "";
      for (let i = 0; i < state.booksPerPage; i++) {
        id = ids.next();
        if (!id) {
          break;
        }
        displayedIds.push(id);
      }
      console.log("page", displayedIds[displayedIds.length - 1]);
      if (displayedIds[displayedIds.length - 1] >= backFrom) break;
    }
    page = Math.max(
      0,
      Math.floor(displayedIds.length / state.booksPerPage) - 1
    );
    console.log("page", page);
  }
  return render();
}

async function render() {
  // clear the old ones from the page
  const list = document.querySelector("ul");
  let last;
  while ((last = list.lastChild)) list.removeChild(last);

  // determine where to start
  let offset = page * state.booksPerPage;
  for (let i = 0; i < state.booksPerPage + 1; i++) {
    const o = i + offset;
    const bid = displayedIds[o] || ids.next();
    if (!bid) {
      break;
    }
    displayedIds[o] = bid;
    if (i >= state.booksPerPage) {
      break;
    }
    const book = await getBookCover(bid);
    list.appendChild(book);
  }
  state.persist();

  // visibility of back and next buttons
  document.querySelector("#back").classList.toggle("hidden", page <= 0);
  document
    .querySelector("#next")
    .classList.toggle("hidden", !displayedIds[(page + 1) * state.booksPerPage]);
}

function updateState(): void {
  const form: HTMLFormElement = document.querySelector("form");
  state.search = form.search.value;
  state.reviewed = form.reviewed.value == "R";
  state.category = form.category.value;
  state.audience = form.audience.value;
}

function updateControls(form: HTMLFormElement): void {}

/* allow switch (keyboard) selection of books */
function moveToNext() {
  // get the currently selected if any
  let selected = document.querySelector(".selected");
  // get all the items we can select
  const selectable = document.querySelectorAll(
    "li, a#back:not(.hidden), a#next:not(.hidden)"
  );
  // assume the first
  let next = 0;
  // if was selected, unselect it and compute the index of the next one
  if (selected) {
    selected.classList.remove("selected");
    next = ([].indexOf.call(selectable, selected) + 1) % selectable.length;
  }
  selected = selectable[next];
  // mark the new one selected
  selected.classList.add("selected");
  // make sure it is visible
  selected.scrollIntoView({
    behavior: "smooth",
    block: "nearest",
    inline: "nearest"
  });
  const h1 = selected.querySelector("h1");
  if (h1) {
    speak(h1.innerText);
  } else {
    speak((selected as HTMLElement).innerText);
  }
}

/* click the currently selected link */
function activateCurrent(e: KeyboardEvent) {
  const selected: HTMLAnchorElement = document.querySelector(
    ".selected a, a.selected"
  );
  if (selected) {
    e.preventDefault();
    selected.click();
  }
}

/* toggle favorite on currently selected book */
function toggleFavorite(selected: HTMLElement) {
  if (selected) {
    const bid = selected.id;
    const ndx = state.fav.bookIds.indexOf(bid);
    if (ndx >= 0) {
      state.fav.bookIds.splice(ndx, 1);
      selected.classList.remove("F");
    } else {
      state.fav.bookIds.push(bid);
      state.fav.bookIds.sort();
      selected.classList.add("F");
    }
    state.persist();
  }
}

async function init() {
  /* restore page and text color */
  document.documentElement.style.setProperty("--page-color", state.pageColor);
  document.documentElement.style.setProperty("--text-color", state.textColor);
  document.body.setAttribute("data-buttonsize", state.buttonSize);

  /* fetch configuration for the content */
  config = await (await fetch("content/config.json")).json();

  /* register service worker. */
  registerServiceWorker();

  const form = document.querySelector("form");
  if (form) {
    if (state.mode !== "edit") state.mode = "find";

    /* handle searches */
    form.addEventListener("submit", e => {
      e.preventDefault();
      updateState();
      state.mode = "find";
      state.persist();
      find();
    });

    /* restore the search form values */
    form.search.value = state.search;
    form.reviewed.value = state.reviewed ? "R" : "";
    form.category.value = state.category;
    form.audience.value = state.audience;
  } else {
    state.mode = "choose";
    document.querySelector("h1.title").innerHTML = state.fav.name;
  }

  /* enable stepping through pages of results */
  document.querySelector("#next").addEventListener("click", e => {
    e.preventDefault();
    (e.target as HTMLElement).classList.remove("selected");
    page += 1;
    render();
  });
  document.querySelector("#back").addEventListener("click", e => {
    e.preventDefault();
    (e.target as HTMLElement).classList.remove("selected");
    page -= 1;
    render();
  });

  /* enable swiping through results */
  swipe(direction => {
    const selector =
      direction == "right" ? "a.back:not(.hidden)" : "a.next:not(.hidden)";
    const link: HTMLAnchorElement = document.querySelector(selector);
    if (link) link.click();
  });

  /* switch control based on keys */
  window.addEventListener("keydown", e => {
    const t = e.target as HTMLElement;
    if (t.matches("input,select,button")) {
      return;
    }
    if (e.key == "ArrowRight" || e.key == "Space") {
      e.preventDefault();
      moveToNext();
    } else if (e.key == "ArrowLeft" || e.key == "Enter") {
      activateCurrent(e);
    } else if (e.key == "f" && state.mode == "find") {
      const selected: HTMLAnchorElement = document.querySelector("li.selected");
      toggleFavorite(selected);
    }
  });

  /* toggle favorite using the mouse in favorite selection mode */
  document.querySelector("#list").addEventListener("click", e => {
    const t = e.target as HTMLElement;
    if (t.matches("#list li")) {
      toggleFavorite(t);
    }
  });

  /* toggle favorite selection mode */
  const heart = document.querySelector("#heart");
  if (heart) {
    heart.addEventListener("click", e => {
      document.body.classList.toggle("hearts");
    });
  }

  find();
}

window.addEventListener("load", init);
