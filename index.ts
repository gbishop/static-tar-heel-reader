import { registerServiceWorker } from "./start-sw";

function init(){
    registerServiceWorker();
}

window.addEventListener('load', init);