/* code used in each book */

window.addEventListener('load', () => {
  /* fix the links back to point to the find page.
   * should this be conditional on coming from there?
   */
  document
    .querySelectorAll("a[href^='./']")
    .forEach((link: HTMLAnchorElement) => (link.href = '../../find.html'));

  /* make sure we have a page number so it isn't just blank */
  if (!location.hash) {
    location.hash = '#p1';
  }

  /* allow switch (keyboard) selection of links */
  function moveToNext() {
    // get the currently selected if any
    const selected = document.querySelector('.selected');
    // get all the items we can select
    const selectable = document.querySelectorAll('section:target a');
    // assume the first
    let next = 0;
    // if was selected, unselect it and compute the index of the next one
    if (selected) {
      selected.classList.remove('selected');
      next = ([].indexOf.call(selectable, selected) + 1) % selectable.length;
    }
    // mark the new one selected
    selectable[next].classList.add('selected');
  }

  /* click the currently selected link */
  function activateCurrent() {
    const selected = document.querySelector('a.selected');
    if (selected) {
      (selected as HTMLAnchorElement).click();
    }
  }

  /* Allow reading the book with switches */
  window.addEventListener('keydown', e => {
    if (e.code == 'ArrowRight' || e.code == 'Space') {
      // next page or next menu item
      e.preventDefault();
      const next = document.querySelector('section:target a.next');
      if (next) {
        (next as HTMLAnchorElement).click();
      } else {
        moveToNext();
      }
    } else if (e.code == 'ArrowLeft' || e.code == 'Enter') {
      // back one page or activate menu
      e.preventDefault();
      const back = document.querySelector('section:target a.back');
      if (back) {
        (back as HTMLAnchorElement).click();
      } else {
        activateCurrent();
      }
    }
  });
});
