/* Camino 規劃手冊 — 離線快取 Service Worker
   v3 策略：頁面「網路優先」（連線永遠拿最新版，離線才退回快取）；
   其他同源資源維持快取優先＋背景更新。 */
const CACHE = 'camino-v6';
const ASSETS = ['.', 'index.html', 'manifest.json', 'icon.svg'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      // cache:'reload' 繞過瀏覽器 HTTP 快取，預存一定是 origin 最新版
      .then(c => c.addAll(ASSETS.map(u => new Request(u, { cache: 'reload' }))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;

  // 頁面本體：網路優先（no-store 繞過 GitHub Pages max-age=600），離線退快取
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(new Request(e.request.url, { cache: 'no-store' })).then(res => {
        if (res && res.status === 200) {
          const c1 = res.clone(), c2 = res.clone();
          caches.open(CACHE).then(c => { c.put('index.html', c1); c.put('.', c2); });
        }
        return res;
      }).catch(() =>
        caches.match(e.request)
          .then(r => r || caches.match('index.html'))
          .then(r => r || caches.match('.'))
      )
    );
    return;
  }

  // 其他同源資源：快取優先、背景更新
  e.respondWith(
    caches.match(e.request).then(cached => {
      const live = fetch(e.request).then(res => {
        if (res && res.status === 200) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy));
        }
        return res;
      }).catch(() => cached);
      return cached || live;
    })
  );
});
