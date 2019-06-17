/* code used in each book */

window.addEventListener('load', () => {
  /* fix the links back to point to the find page.
   * should this be conditional on coming from there?
   */
  document
    .querySelectorAll("a[href^='./']")
    .forEach((link: HTMLAnchorElement) => (link.href = '../../find.html'));
});
