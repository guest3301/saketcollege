// sw.js
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('todo-cache-v1').then(cache => {
            return cache.addAll([
                '/',
                '/index.html',
                '/icon.png'
            ]);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});

self.addEventListener('push', event => {
    const options = {
        body: event.data.text(),
        icon: '/icon.png',
        vibrate: [200, 100, 200]
    };
    
    event.waitUntil(
        self.registration.showNotification('Todo Reminder', options)
    );
});