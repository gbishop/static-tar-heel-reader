/* implement choosing favorites */

import { openDB, DBSchema } from "./web_modules/idb.js";
import state from "./state.js";
import { registerServiceWorker } from "./start-sw.js";

interface IFavorites {
  id?: number;
  name: string;
  bookIds: string[];
}

interface FavoritesDB extends DBSchema {
  favorites: {
    key: number;
    value: IFavorites;
    indexes: { "by-name": string };
  };
}

/* a helper for generating html */
function html(
  tagName: string,
  attributes: { [attr: string]: any },
  ...children: (HTMLElement | string)[]
): HTMLElement {
  // create the element
  const r = document.createElement(tagName);
  // add the attributes
  for (const key in attributes) {
    // special case for booleans
    if (typeof attributes[key] === "boolean") {
      if (attributes[key]) {
        r.setAttribute(key, "");
      }
    } else {
      r.setAttribute(key, attributes[key]);
    }
  }
  // add the children
  children.forEach(child => {
    // special case for strings
    if (typeof child === "string") {
      r.appendChild(document.createTextNode(child));
    } else {
      r.appendChild(child);
    }
  });
  return r;
}

/* encapsulate opening the db */
async function openFavorites() {
  return openDB<FavoritesDB>("Favorites", 2, {
    upgrade(db) {
      console.log("upgrade");
      const store = db.createObjectStore("favorites", {
        keyPath: "id",
        autoIncrement: true
      });
      store.createIndex("by-name", "name");
    }
  });
}

/* add a favorite to the UL */
function addToList(fav: IFavorites) {
  const list = document.querySelector("#list");
  const checked = fav.id == state.fav.id;
  const node = html(
    "li",
    {},
    // radio button
    html("input", {
      type: "radio",
      name: "active",
      value: fav.id,
      id: fav.id,
      checked
    }),
    // list name
    html("label", { for: fav.id }, fav.name),
    // hidden until renaming
    html("input", {
      type: "text",
      name: "name",
      value: fav.name
    }),
    // number of books in the set
    ` (${fav.bookIds.length} books)`
  );
  // move the tools to the active set
  if (checked) {
    node.appendChild(document.querySelector("#tools"));
  }
  list.appendChild(node);
}

/* persist values into the state */
function updateState(fav: IFavorites) {
  state.fav.id = fav.id;
  state.fav.bookIds = fav.bookIds;
  state.fav.name = fav.name;
  state.persist();
}

/* initialize the page */
async function init() {
  registerServiceWorker();

  const db = await openFavorites();
  // update the favorites from the state
  db.put("favorites", state.fav);
  // display the favorites
  let cursor = await db.transaction("favorites").store.openCursor();
  while (cursor) {
    const fav = cursor.value;
    addToList(fav);
    cursor = await cursor.continue();
  }

  // move the tools on select
  document.querySelector("#list").addEventListener("change", async e => {
    // get the target element
    const t = e.target as HTMLInputElement;
    // get its parent
    const li = t.closest("li");
    // move the tools
    li.appendChild(document.querySelector("#tools"));
    // get the id from the button control
    const input: HTMLInputElement = li.querySelector("input[name=active]");
    const id = parseInt(input.value, 10);
    // get the database
    const db = await openFavorites();
    let fav;
    if (t.matches("input[name=name]")) {
      /* changing the name */
      const tx = db.transaction("favorites", "readwrite");
      fav = await tx.store.get(id);
      fav.name = t.value;
      tx.store.put(fav);
      const label = li.querySelector("label");
      label.innerText = fav.name;
    } else {
      /* changing the active set */
      fav = await db.get("favorites", id);
    }
    updateState(fav);
  });

  /* clear renaming if the name input loses focus */
  document.querySelector("#list").addEventListener("focusout", e => {
    const t = e.target as HTMLElement;
    if (t.matches("input[name=name]")) {
      for (const node of [...document.querySelectorAll("li.renaming")]) {
        node.classList.remove("renaming");
      }
    }
  });

  /* trigger change in name field if the user hits enter */
  window.addEventListener("keydown", e => {
    if (e.code != "Enter") {
      return;
    }
    const t = e.target as HTMLElement;
    if (t.matches("input[name=name]")) {
      t.blur();
    }
  });

  /* read button */
  document.querySelector("#read").addEventListener("click", async e => {
    const t = e.target as HTMLElement;
    const li = t.closest("li");
    const input: HTMLInputElement = li.querySelector("input[name=active]");
    const id = parseInt(input.value, 10);
    const db = await openFavorites();
    const fav = await db.get("favorites", id);
    updateState(fav);
    location.href = "choose.html";
  });

  /* edit button allows us to add and remove favorites */
  document.querySelector("#edit").addEventListener("click", async e => {
    const t = e.target as HTMLElement;
    const li = t.closest("li");
    const input: HTMLInputElement = li.querySelector("input[name=active]");
    const id = parseInt(input.value, 10);
    const db = await openFavorites();
    const fav = await db.get("favorites", id);
    updateState(fav);
    state.mode = "edit";
    state.persist();
    location.href = "find.html";
  });

  /* new button */
  document.querySelector("#new").addEventListener("click", async e => {
    const db = await openFavorites();
    const fav: IFavorites = { name: "New Favorites", bookIds: <string[]>[] };
    const t = await db.put("favorites", fav);
    fav.id = t;
    updateState(fav);
    addToList(fav);
  });

  /* rename button */
  document.querySelector("#rename").addEventListener("click", e => {
    const t = e.target as HTMLElement;
    const li = t.closest("li");
    const input: HTMLInputElement = li.querySelector("input[name=active]");
    const id = parseInt(input.value, 10);
    // show the text input for the new name
    li.classList.add("renaming");
    const name = li.querySelector("input[name=name]") as HTMLInputElement;
    // focus it and select the current value
    name.focus();
    name.select();
  });

  /* delete button */
  document.querySelector("#delete").addEventListener("click", async e => {
    const t = e.target as HTMLElement;
    const li = t.closest("li");
    const input: HTMLInputElement = li.querySelector("input[name=active]");
    const id = parseInt(input.value, 10);
    // delete the set from the db
    const db = await openFavorites();
    await db.delete("favorites", id);
    // move the tools to a safe place
    document.body.appendChild(document.querySelector("#tools"));
    // remove the item from the list
    li.remove();
  });
}

window.addEventListener("load", init);
