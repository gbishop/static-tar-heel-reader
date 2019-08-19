/* code used in each book */

import state from "./state";
import swipe from "./swipe";
import speak from "./speech";

window.addEventListener("load", () => {
  /* restore page and text color */
  document.documentElement.style.setProperty("--page-color", state.pageColor);
  document.documentElement.style.setProperty("--text-color", state.textColor);
  document.body.setAttribute("data-buttonsize", state.buttonSize);

  /* fix the links back to point to the find page.
   * should this be conditional on coming from there?
   */
  const bid = document.body.id;
  const backTo =
    (state.mode == "find" ? "../../find.html" : "../../choose.html") +
    "#" +
    bid;
  document
    .querySelectorAll("a[href^='./']")
    .forEach((link: HTMLAnchorElement) => (link.href = backTo));

  /* make sure we have a page number so it isn't just blank */
  if (!location.hash) {
    location.hash = "#p1";
  }

  /* allow switch (keyboard) selection of links */
  function moveToNext() {
    // get the currently selected if any
    const selected = document.querySelector(".selected");
    // get all the items we can select
    const selectable = document.querySelectorAll("section:target a");
    // assume the first
    let next = 0;
    // if was selected, unselect it and compute the index of the next one
    if (selected) {
      selected.classList.remove("selected");
      next = ([].indexOf.call(selectable, selected) + 1) % selectable.length;
    }
    // mark the new one selected
    selectable[next].classList.add("selected");
  }

  /* click the currently selected link */
  function activateCurrent() {
    const selected = document.querySelector("a.selected");
    if (selected) {
      (selected as HTMLAnchorElement).click();
    }
  }

  /* Allow reading the book with switches */
  window.addEventListener("keydown", e => {
    if (e.key == "ArrowRight" || e.key == "Space") {
      // next page or next menu item
      e.preventDefault();
      const next = document.querySelector("section:target a.next");
      if (next) {
        (next as HTMLAnchorElement).click();
      } else {
        moveToNext();
      }
    } else if (e.key == "ArrowLeft" || e.key == "Enter") {
      // back one page or activate menu
      e.preventDefault();
      const back = document.querySelector("section:target a.back");
      if (back) {
        (back as HTMLAnchorElement).click();
      } else {
        activateCurrent();
      }
    }
  });

  /* allow paging through with swipes */
  swipe(direction => {
    const selector =
      direction == "right" ? "section:target a.back" : "section:target a.next";
    const link: HTMLAnchorElement = document.querySelector(selector);
    if (link) link.click();
  });

  /* speak the text on the page */
  function read() {
    const node = document.querySelector(
      "section:target h1, section:target p"
    ) as HTMLElement;
    console.log("node", node);
    if (node) {
      const text = node.innerText;
      console.log("text", text);
      speak(text);
    }
  }

  /* speak the text when the hash changes */
  window.addEventListener("hashchange", read);
  read();
});
