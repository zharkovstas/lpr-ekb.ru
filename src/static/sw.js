self.addEventListener('fetch', event => {
    if (event.request.mode === 'navigate') {
        event.respondWith(async function () {
            const normalizedUrl = new URL(event.request.url);
            normalizedUrl.search = '';

            const fetchResponseP = fetch(normalizedUrl);
            const fetchResponseCloneP = fetchResponseP.then(r => r.clone());

            event.waitUntil(async function () {
                const cache = await caches.open('my-cache-name');
                await cache.put(normalizedUrl, await fetchResponseCloneP.then(cleanResponse));
            }());

            return (await caches.match(normalizedUrl)) || fetchResponseP;
        }());
    }
});

function cleanResponse(response) {
    const clonedResponse = response.clone();

    const bodyPromise = 'body' in clonedResponse ?
        Promise.resolve(clonedResponse.body) :
        clonedResponse.blob();

    return bodyPromise.then((body) => {
        return new Response(body, {
            headers: clonedResponse.headers,
            status: clonedResponse.status,
            statusText: clonedResponse.statusText,
        });
    });
}
