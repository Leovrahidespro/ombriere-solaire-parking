/* Bandeau cookies — Google Analytics et Microsoft Clarity ne sont chargés qu'après acceptation.
   Le choix est conservé 6 mois, puis redemandé. "Gérer les cookies" (pied de page) rouvre le bandeau. */
(function () {
  var GA_ID = '';          // à renseigner (ex. G-XXXXXXX) pour activer Google Analytics
  var CLARITY_ID = '';     // à renseigner pour activer Microsoft Clarity
  var KEY = 'osp_cookie_consent';
  var MAX_AGE = 182 * 24 * 3600 * 1000; // ~6 mois
  var loaded = false;

  function read() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY));
      if (v && (v.c === 'granted' || v.c === 'denied') && Date.now() - v.t < MAX_AGE) return v.c;
    } catch (e) {}
    return null;
  }
  function save(c) {
    try { localStorage.setItem(KEY, JSON.stringify({ c: c, t: Date.now() })); } catch (e) {}
  }

  function loadTrackers() {
    if (loaded) return;
    loaded = true;
    if (GA_ID) {
    var s = document.createElement('script');
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    s.async = true;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
    }
    if (CLARITY_ID)
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', CLARITY_ID);
  }

  function clearTrackerCookies() {
    var host = location.hostname.replace(/^www\./, '');
    document.cookie.split(';').forEach(function (c) {
      var name = c.split('=')[0].trim();
      if (/^(_ga|_gid|_gat|_clck|_clsk|CLID|MUID)/.test(name)) {
        ['', '; domain=' + host, '; domain=.' + host].forEach(function (d) {
          document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + d;
        });
      }
    });
  }

  var css =
    '#sa-cookie{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;max-width:560px;margin:0 auto;' +
    'background:#fff;color:#1a1a1a;border:1px solid #d4d4d8;border-radius:12px;box-shadow:0 10px 40px rgba(0,0,0,.18);' +
    'padding:1.1rem 1.25rem;font:400 .875rem/1.5 Inter,system-ui,sans-serif}' +
    '#sa-cookie p{margin:0 0 .9rem}#sa-cookie a{color:#b45309;text-decoration:underline}' +
    '#sa-cookie .sa-btns{display:flex;gap:.6rem}' +
    '#sa-cookie button{flex:1;height:42px;border-radius:8px;font:600 .875rem Inter,system-ui,sans-serif;cursor:pointer}' +
    '#sa-cookie .sa-no{background:#fff;color:#1a1a1a;border:1.5px solid #1a1a1a}' +
    '#sa-cookie .sa-yes{background:#f59e0b;color:#0c2238;border:1.5px solid #f59e0b}' +
    '#sa-cookie button:focus-visible{outline:3px solid #f59e0b;outline-offset:2px}';

  function showBanner() {
    if (document.getElementById('sa-cookie')) return;
    if (!document.getElementById('sa-cookie-css')) {
      var st = document.createElement('style');
      st.id = 'sa-cookie-css';
      st.textContent = css;
      document.head.appendChild(st);
    }
    var b = document.createElement('div');
    b.id = 'sa-cookie';
    b.setAttribute('role', 'region');
    b.setAttribute('aria-label', 'Préférences cookies');
    b.innerHTML =
      '<p>Nous utilisons des cookies de mesure d\'audience (Google Analytics, Microsoft Clarity) pour améliorer le site. ' +
      'Ils ne sont déposés qu\'avec votre accord. <a href="/politique-confidentialite#cookies">En savoir plus</a></p>' +
      '<div class="sa-btns"><button type="button" class="sa-no">Refuser</button>' +
      '<button type="button" class="sa-yes">Accepter</button></div>';
    document.body.appendChild(b);
    b.querySelector('.sa-no').onclick = function () {
      var wasGranted = loaded;
      save('denied');
      b.remove();
      clearTrackerCookies();
      if (wasGranted) location.reload();
    };
    b.querySelector('.sa-yes').onclick = function () {
      save('granted');
      b.remove();
      loadTrackers();
    };
  }

  window.saManageCookies = function () { showBanner(); };

  function init() {
    // Aucun outil de mesure configuré : pas de cookie, donc pas de bandeau.
    if (!GA_ID && !CLARITY_ID) { window.saManageCookies = function () {}; return; }
    var c = read();
    if (c === 'granted') {
      if (document.readyState === 'complete') loadTrackers();
      else window.addEventListener('load', loadTrackers);
    } else if (c === null) {
      showBanner();
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
