/* Collect state together and allow it to persist */

class State {
  public search = '';
  public reviewed = true;
  public category = '';
  public audience = 'E';
  /* the page of results we are currently displaying */
  public page = 0;
  /* displayedIds is a list of the ids we have shown to the user. We
   * can't backup in the BookSets so we remember all the ones we have
   * seen for this query so that we can allow paging backward in results.
   */
  public displayedIds: string[] = [];
  public booksPerPage = 9;
  public pageColor = '#fff';
  public textColor = '#000';
  public buttonSize = 'small';

  constructor() {
    const s = localStorage.getItem('state');
    const o = (s && JSON.parse(s)) || {};
    console.log('o', o);
    if ('search' in o && typeof o.search === 'string') {
      this.search = o.search;
    }
    if ('reviewed' in o && typeof o.reviewed === 'boolean') {
      this.reviewed = o.reviewed;
    }
    if ('category' in o && typeof o.search === 'string') {
      this.category = o.category;
    }
    if ('audience' in o && typeof o.search === 'string') {
      this.audience = o.audience;
    }
    if ('page' in o && typeof o.page === 'number') {
      this.page = o.page;
    }
    if ('displayedIds' in o && typeof o.pages === 'object') {
      this.displayedIds = o.pages;
    }
    if ('booksPerPage' in o && typeof o.page === 'number') {
      this.booksPerPage = o.booksPerPage;
    }
    if ('pageColor' in o && typeof o.search === 'string') {
      this.pageColor = o.pageColor;
    }
    if ('textColor' in o && typeof o.textColor === 'string') {
      this.textColor = o.textColor;
    }
    if ('buttonSize' in o && typeof o.buttonSize === 'string') {
      this.buttonSize = o.buttonSize;
    }
  }

  public persist() {
    const s = JSON.stringify(this);
    localStorage.setItem('state', s);
  }
}

const state = new State();
export default state;
