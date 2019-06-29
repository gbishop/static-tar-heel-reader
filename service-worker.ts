import { QueryObject, QueryObjectI, QueryType } from './QueryObject';

console.log("Hello from service worker!");

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
    /.html|.css|.js/,
    new workbox.strategies.CacheFirst({
        cacheName: "html-cache",
        plugins: [
            new workbox.expiration.Plugin({
                maxAgeSeconds: 30*24*60*60
            })
        ],
    })
);

let x = this;

/**
 * Example of communicating with the Service Worker like any other worker: messages.
 * Uses QueryObject interface to receive a query and act appropriately.
 * 
 * Alternative would be to communicate by intercepting fetches.
 */
self.addEventListener('message', function(event){
    // There MUST be a better type guard. Expecting QueryObject.
    if ('query_param' in event.data &&
        'query_type' in event.data){
        if (event.data.query_type === QueryType.GET_CACHEDIDS){

            let ids: string[] = [];

            caches.open('html-cache').then((cache) => {
                cache.keys().then((keys) => {
                    keys.forEach((request, index, array) => {
                        let url = request.url;
                        if (url.search('content') == -1){
                            return;
                        }
                        let tokens = url.substring(url.search('content') + 'content'.length).split('/');
                        if (!tokens[tokens.length-1].match(/\d.html/)){
                            return;
                        }
                        let id = tokens.join('');
                        id = id.substring(0, id.length-5);
                        ids.push(id);
                    });
                    event.ports[0].postMessage(ids);
                });
            });

        }
    } else {
        console.warn("Something not quite working. QueryObject not received.");
    }
});