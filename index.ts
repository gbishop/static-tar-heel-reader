import { registerServiceWorker } from "./start-sw";

async function init(){
    registerServiceWorker();
}

window.addEventListener('load', init);