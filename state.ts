/* Collect state together and allow it to persist */

const version = 4; /* version of the persistent data */

class State {
  public mode: "find" | "choose" | "edit";
  public search = "";
  public reviewed = true;
  public category = "";
  public audience = "E";
  /* the page of results we are currently displaying */
  public page = 0;
  /* displayedIds is a list of the ids we have shown to the user. We
   * can't backup in the BookSets so we remember all the ones we have
   * seen for this query so that we can allow paging backward in results.
   */
  public displayedIds: string[] = [];
  public booksPerPage = 9;
  public pageColor = "#fff";
  public textColor = "#000";
  public buttonSize = "small";
  /* favorites related values */
  public fav = {
    id: 1,
    name: "Favorites",
    bookIds: <string[]>[]
  };
  /* speech related values */
  public speech = {
    voice: "silent",
    rate: 1, // 0.1 to 10
    pitch: 1, // 0 to 2
    lang: "en-US"
  };

  constructor() {
    const s = localStorage.getItem("state");
    const o = (s && JSON.parse(s)) || {};
    if (o && o.version === version) {
      Object.assign(this, o);
    }
    this.persist();
  }

  public persist() {
    const o = Object.assign({}, this, { version });
    const s = JSON.stringify(o);
    localStorage.setItem("state", s);
  }
}

const state = new State();
export default state;
