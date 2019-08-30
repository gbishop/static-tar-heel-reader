import { registerServiceWorker } from "./start-sw.js";

async function init() {
  document.body.classList.add("has-js");
  registerServiceWorker();
}

window.addEventListener("load", init);
