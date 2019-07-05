// Registers service worker and begins work on detecting online status, changing visual state to reflect that.

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("worker.js").then(function() {
      console.log("Service worker registered!");
    });
  });
}

/**
 * Uses a heuristic in fetching to mark books that have been cached.
 * Moving now to directly querying the cache in the service worker.
 * TODO: Use AllAvailable instead of heuristic fetches.
 */
async function markAvailableBooks() {
  let book_entries: HTMLCollection = document.getElementsByClassName("R");
  for (let i = 0; i < book_entries.length; i++) {
    let entry = book_entries[i];
    if (entry instanceof HTMLElement) {
      let href = entry.getAttribute("href");
      if (href !== undefined) {
        let f = fetch(href)
          .then(() => {
            (entry as HTMLElement).style.backgroundColor = "green";
            console.log(
              `Changed color to indicate ${href} has already been cached.`
            );
          })
          .catch(() => {
            console.log(`Failed to fetch ${href} from cache.`);
          });
      }
    }
  }
}

function onlineHook() {
  console.info("We're online! Here can load new contents.");
}

function offlineHook() {
  markAvailableBooks();
}

window.addEventListener("load", () => {
  if (!navigator.onLine) {
    alert("Offline mode! Highlighting cached entries.");
    offlineHook();
  } else {
    console.log("Already online.");
  }
  window.addEventListener("online", onlineHook);
});
