import { RangeSet } from './BookSet';

importScripts('https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js');

declare var workbox: any;

workbox.loadModule('workbox-strategies');
workbox.loadModule('workbox-precaching');

workbox.routing.registerRoute(
    /.jpg/,
    new workbox.strategies.CacheFirst({
        cacheName: "img-cache",
        plugins: [
            new workbox.expiration.Plugin({
                maxAgeSeconds: 30*24*60*60
            })
        ],
    })
);


workbox.routing.registerRoute(
    /.html|.css|.js|.json/,
    new workbox.strategies.CacheFirst({
        cacheName: "html-cache",
        plugins: [
            new workbox.expiration.Plugin({
                maxAgeSeconds: 30*24*60*60
            })
        ],
    })
);

workbox.routing.registerRoute(
    /\/content\/index\/AllAvailable$/,
    async () => {
        let ids = getAllAvailableIDs();
        return new Response(await ids);
    }
);

workbox.routing.registerRoute(
    /\/content\/index/,
    new workbox.strategies.CacheFirst({
        cacheName: "index-cache",
        plugins: [
            new workbox.expiration.Plugin({
                maxAgeSeconds: 30*24*60*60
            })
        ],
    })
);

interface Config {
  base: number; // base of the encoding used for ids
  digits: number; // number of digits in each id
  lastReviewed: string; // id of last reviewed book
  first: string; // id of first book
  last: string; // id of last book
}

// Fetches the available IDs. For offline case, can just generate a RangeSet.
async function getAllAvailableIDs(): Promise<string>{
    if (navigator.onLine){
        let config: Config = await (await fetch("content/config.json")).json();
        let range = new RangeSet(config.first, config.last, config.digits, config.base);
        let ids = "";
        while (true){
            let curr = range.next();
            if(!curr) { break; }
            ids += curr;
        }
        return ids;
    }

    // Offline case.
    let ids: string = "";
    return new Promise((resolve, reject) => {
        caches.open('html-cache').then((cache) => {
            cache.keys().then((keys) => {
                if (keys.length == 0){
                    resolve("");
                }

                keys.forEach((request, index, array) => {
                    let url = request.url;
                    if (!url.includes('content')){
                        return;
                    }
                    let tokens = url.substring(url.search('content') + 'content'.length).split('/');
                    if (!tokens[tokens.length-1].match(/\d.html/)){
                        return;
                    }
                    let id = tokens.join('');
                    id = id.substring(0, id.length-5);
                    ids += id;
                });
                resolve(ids);
            })
        });
    });
}
