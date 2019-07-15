import { registerServiceWorker } from "./start-sw";

async function init() {
  document.body.classList.add("has-js");
  registerServiceWorker();
}

window.addEventListener("load", init);
