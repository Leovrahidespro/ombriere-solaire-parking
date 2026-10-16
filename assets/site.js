/* Conversion : formulaires (validation, anti-spam, provenance, suivi), barre d'action mobile, suivi des appels. */
(function () {
  var PHONE = '06 47 32 65 72';
  var TEL = 'tel:+33647326572';
  var DEVIS_URL = '/devis-ombriere-solaire';

  function track(name, params) {
    try { if (window.gtag) window.gtag('event', name, params || {}); } catch (e) {}
    try { if (window.clarity) window.clarity('event', name); } catch (e) {}
  }

  /* ---------- Provenance de la visite (1re page vue de la session) ---------- */
  var SRC_KEY = 'osp_src';
  function getSource() {
    try {
      var s = JSON.parse(sessionStorage.getItem(SRC_KEY));
      if (s) return s;
    } catch (e) {}
    var p = new URLSearchParams(location.search);
    var s2 = {
      landing: location.pathname,
      referrer: document.referrer && document.referrer.indexOf(location.host) === -1 ? document.referrer : '',
      utm_source: p.get('utm_source') || '',
      utm_medium: p.get('utm_medium') || '',
      utm_campaign: p.get('utm_campaign') || '',
      gclid: p.get('gclid') ? 'oui' : ''
    };
    try { sessionStorage.setItem(SRC_KEY, JSON.stringify(s2)); } catch (e) {}
    return s2;
  }
  var source = getSource();

  function describeSource() {
    if (source.gclid) return 'Google Ads';
    if (source.utm_source) return [source.utm_source, source.utm_medium, source.utm_campaign].filter(Boolean).join(' / ');
    if (source.referrer) {
      try {
        var h = new URL(source.referrer).hostname.replace(/^www\./, '');
        return /google\.|bing\.|qwant\.|duckduckgo\.|ecosia\.|yahoo\./.test(h) ? 'Recherche (' + h + ')' : 'Lien (' + h + ')';
      } catch (e) { return 'Lien'; }
    }
    return 'Accès direct';
  }

  /* ---------- Styles injectés ---------- */
  var css =
    '.sa-err{display:block;margin-top:6px;padding:4px 10px;border-radius:6px;background:#fef2f2;color:#b91c1c;font:500 .8125rem/1.4 Inter,system-ui,sans-serif}' +
    '.sa-invalid{border-color:#dc2626!important;box-shadow:0 0 0 3px rgba(220,38,38,.15)!important}' +
    '.sa-alert{margin-top:12px;padding:10px 12px;border-radius:8px;background:#fef2f2;color:#991b1b;font:500 .875rem/1.5 Inter,system-ui,sans-serif;text-align:center}' +
    '.sa-alert a{color:inherit;font-weight:700}' +
    '.sa-done{background:#fff;color:#1a1a1a;border-radius:12px;padding:1.75rem 1.25rem;text-align:center;font-family:Inter,system-ui,sans-serif}' +
    '.sa-done-ic{width:56px;height:56px;margin:0 auto 1rem;border-radius:50%;background:#fef3c7;color:#b45309;display:flex;align-items:center;justify-content:center}' +
    '.sa-done h3{font-size:1.25rem;font-weight:800;margin:0 0 .5rem}' +
    '.sa-done p{font-size:.9375rem;color:#52525b;line-height:1.6;margin:0 0 .75rem}' +
    '.sa-done a{color:#b45309;font-weight:700}' +
    '#sa-bar{position:fixed;left:0;right:0;bottom:0;z-index:900;display:flex;gap:8px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));' +
    'background:rgba(255,255,255,.97);border-top:1px solid #d4d4d8;box-shadow:0 -4px 20px rgba(0,0,0,.08);transition:transform .25s}' +
    '#sa-bar.sa-hide{transform:translateY(110%)}' +
    '#sa-bar a{flex:1;display:flex;align-items:center;justify-content:center;gap:8px;height:48px;border-radius:10px;' +
    'font:700 .9375rem Inter,system-ui,sans-serif;text-decoration:none}' +
    '#sa-bar .sa-call{background:#fff;color:#0c2238;border:1.5px solid #0c2238;flex:0 0 42%}' +
    '#sa-bar .sa-quote{background:#f59e0b;color:#0c2238!important;color:#fff}' +
    '#sa-bar svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}' +
    '@media(min-width:1024px){#sa-bar{display:none}}' +
    '@media(max-width:1023px){body{padding-bottom:76px}}';
  var st = document.createElement('style');
  st.textContent = css;
  document.head.appendChild(st);

  /* ---------- Formulaires ---------- */
  function field(form, name) { return form.querySelector('[name="' + name + '"]'); }

  function setError(input, msg) {
    if (!input) return;
    var group = input.closest('.form-group') || input.parentNode;
    var e = group.querySelector('.sa-err');
    if (msg) {
      if (!e) { e = document.createElement('span'); e.className = 'sa-err'; e.id = (input.name || 'f') + '-err'; group.appendChild(e); }
      e.textContent = msg;
      input.classList.add('sa-invalid');
      input.setAttribute('aria-invalid', 'true');
      input.setAttribute('aria-describedby', e.id);
    } else {
      if (e) e.remove();
      input.classList.remove('sa-invalid');
      input.removeAttribute('aria-invalid');
    }
  }

  function cleanPhone(v) { return (v || '').replace(/[\s.\-()]/g, '').replace(/^(\+33|0033)/, '0'); }

  function validate(form) {
    var name = field(form, 'name'), phone = field(form, 'phone'), email = field(form, 'email'), cp = field(form, 'code_postal');
    var errors = [];
    function check(input, msg) { setError(input, msg); if (msg) errors.push(input); }
    if (name) check(name, name.value.trim().length < 2 ? 'Indiquez votre nom.' : '');
    var pv = phone ? cleanPhone(phone.value) : '', ev = email ? email.value.trim() : '';
    if (phone) check(phone, pv && !/^0[1-9]\d{8}$/.test(pv) ? 'Numéro invalide (10 chiffres, ex : 06 12 34 56 78).' :
      (!pv && !ev ? 'Indiquez un téléphone ou un e-mail pour être recontacté.' : ''));
    if (email) check(email, ev && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(ev) ? 'Adresse e-mail invalide.' : '');
    if (cp) check(cp, !/^\d{5}$/.test(cp.value.trim()) ? 'Code postal à 5 chiffres (ex : 69002).' : '');
    if (errors.length) errors[0].focus();
    return !errors.length;
  }

  function addHidden(form, name, value) {
    var i = field(form, name);
    if (!i) { i = document.createElement('input'); i.type = 'hidden'; i.name = name; form.appendChild(i); }
    i.value = value;
  }

  function successHtml() {
    return '<div class="sa-done" role="status" tabindex="-1">' +
      '<div class="sa-done-ic"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg></div>' +
      '<h3>Demande bien reçue</h3>' +
      '<p>Un installateur partenaire vous recontacte sous 48 h ouvrées pour étudier votre parking et préparer une étude chiffrée.</p>' +
      '<p>Une question d\'ici là ? <a href="' + TEL + '">' + PHONE + '</a></p></div>';
  }

  function enhance(form) {
    form.noValidate = true;
    var name = field(form, 'name'), phone = field(form, 'phone'), email = field(form, 'email'), cp = field(form, 'code_postal');
    if (name && !name.autocomplete) name.setAttribute('autocomplete', 'name');
    if (phone) { phone.setAttribute('autocomplete', 'tel'); phone.setAttribute('inputmode', 'tel'); }
    if (email) email.setAttribute('autocomplete', 'email');
    if (cp) { cp.setAttribute('autocomplete', 'postal-code'); cp.setAttribute('inputmode', 'numeric'); cp.setAttribute('maxlength', '5'); }
    // Anti-spam Web3Forms (case invisible, cochée seulement par les robots)
    if (!field(form, 'botcheck')) {
      var hp = document.createElement('input');
      hp.type = 'checkbox'; hp.name = 'botcheck'; hp.tabIndex = -1; hp.setAttribute('aria-hidden', 'true');
      hp.style.cssText = 'position:absolute;left:-9999px;opacity:0;';
      form.appendChild(hp);
    }
    [name, phone, email, cp].forEach(function (i) {
      if (i) i.addEventListener('input', function () { if (i.classList.contains('sa-invalid')) validate(form); });
    });

    var started = false;
    form.addEventListener('focusin', function () {
      if (!started) { started = true; track('form_start', { form_location: location.pathname }); }
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var old = form.querySelector('.sa-alert'); if (old) old.remove();
      if (!validate(form)) return;
      var btn = form.querySelector('[type="submit"]');
      var label = btn ? btn.innerHTML : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Envoi en cours…'; }

      if (!field(form, 'subject') || !field(form, 'subject').value) addHidden(form, 'subject', 'Nouvelle demande — ' + document.title.split('|')[0].trim());
      var cpv = cp ? cp.value.trim() : '';
      if (cpv) addHidden(form, 'subject', field(form, 'subject').value.replace(/ — CP \d{5}$/, '') + ' — CP ' + cpv);
      addHidden(form, 'from_name', 'ombriere-solaire-parking.fr');
      addHidden(form, 'page_demande', location.pathname);
      addHidden(form, 'page_arrivee', source.landing);
      addHidden(form, 'provenance', describeSource());
      if (phone && phone.value) phone.value = phone.value.trim();

      fetch('https://api.web3forms.com/submit', { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (!d.success) throw new Error(d.message || 'error');
          track('generate_lead', { form_location: location.pathname, lead_source: describeSource() });
          form.innerHTML = successHtml();
          var done = form.querySelector('.sa-done');
          done.focus();
          done.scrollIntoView({ behavior: 'smooth', block: 'center' });
        })
        .catch(function () {
          if (btn) { btn.disabled = false; btn.innerHTML = label; }
          var a = document.createElement('div');
          a.className = 'sa-alert'; a.setAttribute('role', 'alert');
          a.innerHTML = 'L\'envoi n\'a pas abouti. Réessayez dans un instant ou appelez-nous au <a href="' + TEL + '">' + PHONE + '</a>.';
          (btn ? btn.parentNode.insertBefore(a, btn.nextSibling) : form.appendChild(a));
          track('form_error', { form_location: location.pathname });
        });
    });
  }

  /* ---------- Barre d'action mobile ---------- */
  function stickyBar() {
    var form = document.querySelector('form[action*="web3forms"]');
    var bar = document.createElement('div');
    bar.id = 'sa-bar';
    bar.innerHTML =
      '<a class="sa-call" href="' + TEL + '"><svg viewBox="0 0 24 24"><path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/></svg>Appeler</a>' +
      '<a class="sa-quote" href="' + (form ? '#' + (form.closest('[id]') ? form.closest('[id]').id : '') : DEVIS_URL) + '">Étude gratuite</a>';
    document.body.appendChild(bar);
    var q = bar.querySelector('.sa-quote');
    if (form) {
      q.addEventListener('click', function (e) {
        e.preventDefault();
        form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        var first = form.querySelector('input:not([type=hidden]):not([type=checkbox])');
        if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 500);
        track('cta_click', { cta: 'barre_mobile_devis' });
      });
      // Masquer la barre quand le formulaire est à l'écran (ne pas couvrir les champs)
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (en) {
          bar.classList.toggle('sa-hide', en[0].isIntersecting);
        }, { threshold: 0.05 }).observe(form);
      }
    } else {
      q.addEventListener('click', function () { track('cta_click', { cta: 'barre_mobile_devis' }); });
    }
  }

  /* ---------- Suivi des clics ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('tel:') === 0) track('click_to_call', { link_location: location.pathname });
    else if (href.indexOf(DEVIS_URL) === 0 || href === '#devis') track('cta_click', { cta: (a.textContent || '').trim().slice(0, 40) });
  });

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll('form[action*="web3forms"]'), enhance);
    stickyBar();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
