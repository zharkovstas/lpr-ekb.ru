self.addEventListener('fetch', event => {
    const requestUrl = new URL(event.request.url);
    if (event.request.mode === 'navigate' && requestUrl.pathname.endsWith('/')) {
        event.respondWith(async function () {
            const fetchResponseP = fetch(event.request);
            const fetchResponseCloneP = fetchResponseP.then(r => r.clone());

            event.waitUntil(async function () {
                const cache = await caches.open('my-cache-name');
                await cache.put(requestUrl, await fetchResponseCloneP);
            }());

            return (await caches.match(requestUrl)) || fetchResponseP;
        }());
    }
});
