importScripts(
  "https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js"
);

declare const workbox: typeof import("workbox-sw");

workbox.loadModule("workbox-strategies");
workbox.loadModule("workbox-precaching");

workbox.routing.registerRoute(
  /.jpg|.png/,
  new workbox.strategies.CacheFirst({
    cacheName: "img-cache",
    plugins: [
      new workbox.expiration.Plugin({
        maxAgeSeconds: 30 * 24 * 60 * 60
      })
    ]
  })
);

workbox.routing.registerRoute(
  /.html|.css|.js|.json/,
  new workbox.strategies.CacheFirst({
    cacheName: "html-cache",
    plugins: [
      new workbox.expiration.Plugin({
        maxAgeSeconds: 30 * 24 * 60 * 60
      })
    ]
  })
);

workbox.precaching.precacheAndRoute([
    '/find.html',
    '/find.css',
    '/index.html',
    '/choose.html',
    '/images/favorite.png',
    '/images/reviewed.png',
    '/images/BackArrow.png',
    '/images/NextArrow.png',
    '/book.js',
    '/site.css',

]);

workbox.routing.registerRoute(/.\/content\/index\/AllAvailable$/, async () => {
  let ids = getAllAvailableIDs();
  return new Response(await ids);
});

workbox.routing.registerRoute(
  /.\/content\/index/,
  new workbox.strategies.CacheFirst({
    cacheName: "index-cache",
    plugins: [
      new workbox.expiration.Plugin({
        maxAgeSeconds: 30 * 24 * 60 * 60
      })
    ]
  })
);

// Fetches the available IDs.
async function getAllAvailableIDs(): Promise<string> {
  if (navigator.onLine) {
    let id_req = await fetch("./content/index/AllAvailable");
    if (id_req.ok) {
      return id_req.text();
    }
  }

  // Offline case.
  let ids: string = "";

  let cache = await caches.open("html-cache");
  let keys = await cache.keys();

  if (keys.length == 0) {
    return "";
  }

  keys.forEach((request, index, array) => {
    let url = request.url;
    if (!url.includes("content")) {
      return;
    }

    let tokens = url
        .substring(url.search("content") + "content".length)
        .split("/");

    if (!tokens[tokens.length -1].match(/\d.html/)){
      return;
    }

    let id = tokens.join("");
    id = id.substring(0, id.length - 5);
    ids += id;
  });

  return ids;
}
