// Registers service worker and begins work on detecting online status, changing visual state to reflect that.

import { QueryObject, QueryType } from './QueryObject';
import { rejects } from 'assert';

if ('serviceWorker' in navigator){
    window.addEventListener('load', ()=> {
        navigator.serviceWorker.register('../../worker.js')
            .then(function(){
                console.log("Service worker registered!");
            });
    })
}

// Query object left in global scope for testing communication with worker.
let qm = new QueryObject(QueryType.GET_CACHEDIDS, [0xdeadbeef]);

/**
 * Sends a message, and returns promise of a list containing IDs of cached books.
 */
function sendMessage(){
    return new Promise((resolve, reject) => {
        console.log("New message channel...");
        let msg_chan = new MessageChannel();
        msg_chan.port1.onmessage = function(event){
            if (event.data.error){
                reject(event.data.error);
            } else {
                console.log(event.data);
                resolve(event.data);
            }
        }

        navigator.serviceWorker.controller.postMessage(qm, [msg_chan.port2]);
    })
}

(window as any).sendMessage = sendMessage;


/**
 * Uses a heuristic in fetching to mark books that have been cached.
 * Moving now to directly querying the cache in the service worker.
 */
function markAvailableBooks(){
    let book_entries: HTMLCollection = document.getElementsByClassName("R");
    for(let i = 0; i < book_entries.length; i++){
        let entry = book_entries[i];
        console.warn("Checking for entry:" + entry);
        if (entry instanceof HTMLElement){
            let href = entry.getAttribute("href");
            if (href !== undefined){
                let f = fetch(href)
                    .then(() => {
                        (entry as HTMLElement).style.backgroundColor = "green";
                        console.log(`Changed color to indicate ${href} has already been cached.`);
                    })
                    .catch(() => {
                        console.log(`Failed to fetch ${href} from cache.`);
                    });
            }
        }
        
    }
}

function onlineHook (){
    console.info("We're online! Here can load new contents.");
}

function offlineHook (){
    markAvailableBooks();
}

window.addEventListener('load', ()=> {

    if (!navigator.onLine){
        alert("Offline mode! Highlighting cached entries.");
        offlineHook();
    } else {
        console.log("Already online.");
    }

    window.addEventListener('online', onlineHook);
});