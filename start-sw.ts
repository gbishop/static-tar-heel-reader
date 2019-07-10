// Registers service worker.

export function registerServiceWorker() {
  if ("serviceWorker" in navigator) {
    if (location.host === "localhost:8081") {
      console.log("skipping service worker");
      return;
    }
    navigator.serviceWorker
      .register("worker.js")
      .then(function() {
        console.log("Service worker registered!");
      })
      .catch(err => {
        console.log("Service worker registration failed: " + err);
      });
  }
}

