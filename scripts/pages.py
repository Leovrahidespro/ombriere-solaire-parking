#!/usr/bin/env python3
"""Génère les pages fixes du site (accueil, pages de service, devis, pages légales, 404).

Le contenu de chaque page est défini dans ce fichier. Pour modifier un texte :
éditez-le ici, puis lancez  python3 scripts/pages.py  (et  python3 scripts/blog.py
si le menu ou le pied de page ont changé). Le blog est généré séparément par blog.py.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blog  # noqa: E402

BASE = blog.BASE
ORG_ID = blog.ORG_ID
TODAY = '2026-10-19'
WEB3FORMS_KEY = '2e53f8a9-5573-446d-98e3-cc33d5558802'
esc = blog.esc

TICK = '<span class="tick"><svg width="12" height="12" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg></span>'
ARROW = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'
PHONE_IC = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/></svg>'
ICONS = {
    'law': '<path d="M12 3v18M5 7h14M7 7l-3 7a4 4 0 0 0 6 0zM17 7l-3 7a4 4 0 0 0 6 0z"/>',
    'euro': '<path d="M17 6a7 7 0 1 0 0 12"/><path d="M4 10h9M4 14h9"/>',
    'cart': '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M3 4h2l2.4 11h11.2L21 8H6.2"/>',
    'factory': '<path d="M3 21V10l6 4V10l6 4V6l6 3v12z"/><path d="M7 17h2M12 17h2M17 17h2"/>',
    'city': '<path d="M4 21V8l8-5 8 5v13"/><path d="M9 21v-6h6v6"/><path d="M9 10h.01M15 10h.01"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'map': '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
    'shield': '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    'bolt': '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    'car': '<path d="M5 17h14v-4l-2-5H7l-2 5z"/><circle cx="8" cy="17" r="2"/><circle cx="16" cy="17" r="2"/>',
    'lock': '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    'one': '<circle cx="12" cy="8" r="3.5"/><path d="M5 20a7 7 0 0 1 14 0"/>',
    'doc': '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M9 14h6M9 18h4"/>',
}


def ic(name, size=22):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


HERO_ART = '''<svg class="hero-art" viewBox="0 0 520 230" role="img" aria-label="Illustration d'une ombrière photovoltaïque au-dessus de places de parking">
  <defs><linearGradient id="pv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2d6aa8"/><stop offset="1" stop-color="#173b63"/></linearGradient></defs>
  <g fill="none" stroke="none">
    <circle cx="452" cy="44" r="26" fill="#f59e0b"/>
    <g stroke="#f59e0b" stroke-width="4" stroke-linecap="round" opacity=".7"><path d="M452 6v-0M490 44h8M414 44h-8M479 17l6-6M425 17l-6-6"/></g>
    <rect x="0" y="200" width="520" height="30" fill="#1b3a58"/>
    <g stroke="#3d5f80" stroke-width="3"><path d="M40 204v22M150 204v22M260 204v22M370 204v22M480 204v22"/></g>
    <g fill="#9fb3c8"><rect x="62" y="98" width="7" height="104" rx="2"/><rect x="246" y="98" width="7" height="104" rx="2"/><rect x="430" y="98" width="7" height="104" rx="2"/></g>
    <path d="M18 104 L500 70 L504 92 L22 126 Z" fill="url(#pv)"/>
    <g stroke="#7fb0e0" stroke-width="1.2" opacity=".55">
      <path d="M78 100l3 22M138 96l3 22M198 92l3 22M258 88l3 22M318 83l3 22M378 79l3 22M438 75l3 22"/>
      <path d="M20 115 L502 81"/>
    </g>
    <g>
      <rect x="86" y="164" width="96" height="34" rx="9" fill="#f59e0b"/><path d="M100 164l12-18h46l14 18z" fill="#f8b84a"/><circle cx="108" cy="198" r="9" fill="#0c2238"/><circle cx="160" cy="198" r="9" fill="#0c2238"/>
      <rect x="290" y="164" width="96" height="34" rx="9" fill="#e5edf5"/><path d="M304 164l12-18h46l14 18z" fill="#ffffff"/><circle cx="312" cy="198" r="9" fill="#0c2238"/><circle cx="364" cy="198" r="9" fill="#0c2238"/>
      <rect x="196" y="176" width="22" height="24" rx="4" fill="#0f9d6b"/><path d="M207 182l-4 7h5l-3 7" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
  </g>
</svg>'''

TYPES = ['Commerce / supermarché', 'Entreprise / site industriel', 'Collectivité / établissement public', 'Copropriété / bailleur', 'Autre']


def form_card(prefix, subject, preselect=None, title='Votre étude gratuite', sub='Un installateur partenaire vous recontacte sous 48&nbsp;h ouvrées'):
    chips = '\n'.join(
        f'          <label class="chip"><input type="radio" name="type_site" value="{esc(t)}"{" checked" if (preselect or TYPES[0]) == t else ""}><span>{esc(t)}</span></label>'
        for t in TYPES)
    return f'''<div class="form-card" id="devis">
      <form action="https://api.web3forms.com/submit" method="POST" novalidate>
        <input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">
        <input type="hidden" name="subject" value="{esc(subject)}">
        <input type="hidden" name="redirect" value="false">
        <p class="fc-title">{title}</p>
        <p class="fc-sub">{sub}</p>
        <fieldset class="chips">
          <legend>Votre parking appartient à…</legend>
{chips}
        </fieldset>
        <div class="form-group"><label for="{prefix}-surface">Surface du parking</label>
          <select id="{prefix}-surface" name="surface_parking">
            <option>Je ne sais pas encore</option>
            <option>Moins de 1 500 m²</option>
            <option>De 1 500 à 10 000 m²</option>
            <option>Plus de 10 000 m²</option>
          </select></div>
        <div class="form-row">
          <div class="form-group"><label for="{prefix}-name">Nom et fonction</label><input type="text" id="{prefix}-name" name="name" placeholder="Ex : Julie Martin, directrice" autocomplete="name"/></div>
          <div class="form-group"><label for="{prefix}-org">Société ou organisme</label><input type="text" id="{prefix}-org" name="societe" placeholder="Ex : Supermarché du Centre" autocomplete="organization"/></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="{prefix}-phone">Téléphone</label><input type="tel" id="{prefix}-phone" name="phone" placeholder="06 00 00 00 00" autocomplete="tel"/></div>
          <div class="form-group"><label for="{prefix}-email">E-mail</label><input type="email" id="{prefix}-email" name="email" placeholder="vous@societe.fr" autocomplete="email"/></div>
        </div>
        <div class="form-group"><label for="{prefix}-cp">Code postal du parking</label><input type="text" id="{prefix}-cp" name="code_postal" placeholder="Ex : 69007" inputmode="numeric" maxlength="5" autocomplete="postal-code"/></div>
        <button type="submit" class="btn btn-submit">Recevoir mon étude gratuite {ARROW}</button>
        <p class="reassure"><span>Gratuit</span><span>Sans engagement</span><span>Partout en France</span></p>
        <p class="privacy">Vos coordonnées sont transmises à un seul installateur partenaire, uniquement pour votre projet, et ne sont jamais revendues. <a href="/politique-confidentialite">Confidentialité</a></p>
      </form>
    </div>'''


def hero(eyebrow, h1, sub, points, subject, preselect=None, art=False, form_title='Votre étude gratuite'):
    pts = ''.join(f'<li>{TICK}{p}</li>' for p in points)
    return f'''<section class="hero">
  <div class="hero-grid">
    <div>
      <span class="eyebrow"><i></i>{eyebrow}</span>
      <h1>{h1}</h1>
      <p class="hero-sub">{sub}</p>
      <ul class="hero-points">{pts}</ul>
      <a href="tel:0647326572" class="hero-phone">{PHONE_IC}<span>Une question ? <strong>06 47 32 65 72</strong></span></a>
      {HERO_ART if art else ''}
    </div>
    {form_card('f', subject, preselect, title=form_title)}
  </div>
</section>
'''


TRUST = [('clock', 'Étude gratuite', "Un premier retour sous 48 h ouvrées, sans engagement."),
         ('map', 'Partout en France', "Des installateurs qui interviennent dans votre région."),
         ('law', 'Loi APER', "Un accompagnement sur l'obligation et ses échéances."),
         ('euro', 'Financement', "Achat, tiers-investissement ou location : vous comparez.")]


def trust():
    items = ''.join(f'<div class="trust-item"><span class="trust-ic">{ic(i, 20)}</span><div><strong>{t}</strong><p>{d}</p></div></div>' for i, t, d in TRUST)
    return f'<section class="trust"><div class="trust-grid">{items}</div></section>\n'


ENGAGEMENTS = [('euro', 'Gratuit, sans engagement', "L'étude ne vous coûte rien. Vous restez libre de ne pas donner suite."),
               ('one', 'Un seul installateur', "Votre demande est confiée à un seul installateur partenaire, pas diffusée à une liste."),
               ('lock', 'Données jamais revendues', "Vos coordonnées servent uniquement à l'étude de votre projet."),
               ('shield', 'Pas de démarchage', "Seul l'installateur à qui votre demande est confiée vous contacte, et uniquement pour votre projet.")]


def engagements(title='Nos engagements', alt=False):
    items = ''.join(f'<div class="trust-item"><span class="trust-ic">{ic(i, 20)}</span><div><strong>{t}</strong><p>{d}</p></div></div>' for i, t, d in ENGAGEMENTS)
    return f'''<section class="section{' alt' if alt else ''}">
  <div class="wrap">
    <div class="s-head"><span class="kicker">Confiance</span><h2>{title}</h2></div>
    <div class="trust-grid" style="padding:1.6rem 0 0">{items}</div>
    <p class="signature">— L'équipe Ombrière Solaire Parking</p>
  </div>
</section>
'''


def cta_row(label='Recevoir mon étude gratuite', note='Gratuit · sans engagement · partout en France'):
    return f'<div class="cta-row"><a href="#devis" class="btn btn-sun btn-lg">{label} {ARROW}</a><span>{note}</span></div>'


def faq(items, title='Questions fréquentes'):
    body = ''.join(blog.FAQ_ITEM.format(open=' open' if i == 0 else '', exp='true' if i == 0 else 'false', q=esc(q), a=esc(a))
                   for i, (q, a) in enumerate(items))
    return f'''<section class="section alt" id="faq">
  <div class="wrap">
    <div class="s-head center"><h2>{title}</h2></div>
    <div class="faq-list">{body}</div>
  </div>
</section>
'''


def final(h2='Votre parking est concerné ?', p="Décrivez votre site en une minute : un installateur partenaire vous recontacte avec une première analyse et, si le projet est pertinent, une étude chiffrée."):
    return f'''<section class="final">
  <h2>{h2}</h2>
  <p>{p}</p>
  <div class="ctas"><a href="#devis" class="btn btn-sun btn-lg">Recevoir mon étude gratuite {ARROW}</a><a href="tel:0647326572" class="btn btn-ghost btn-lg">06 47 32 65 72</a></div>
</section>
'''


def links(items, title='Pour aller plus loin'):
    cards = ''.join(f'<a href="{u}" class="link-card">{esc(blog.PAGES_SITE.get(u, u))}</a>' for u in items)
    return f'<section class="links"><div class="wrap"><h3>{title}</h3><div class="links-grid">{cards}</div></div></section>\n'


def graph(path, title, desc, faqs=None, crumbs=None, extra=None):
    url = BASE + path
    g = [{'@type': 'Organization', '@id': ORG_ID, 'name': 'Ombrière Solaire Parking', 'url': BASE + '/',
          'telephone': '+33647326572', 'logo': BASE + '/apple-touch-icon.png', 'areaServed': 'FR'},
         {'@type': 'WebPage', 'name': title, 'url': url, 'description': desc, 'inLanguage': 'fr-FR', 'isPartOf': {'@id': BASE + '/#website'}}]
    if path == '/':
        g.insert(0, {'@type': 'WebSite', '@id': BASE + '/#website', 'name': 'Ombrière Solaire Parking',
                     'alternateName': 'ombriere-solaire-parking.fr', 'url': BASE + '/', 'inLanguage': 'fr-FR'})
    if crumbs:
        g.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Accueil', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': crumbs, 'item': url}]})
    if faqs:
        g.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]})
    if extra:
        g.append(extra)
    return json.dumps({'@context': 'https://schema.org', '@graph': g}, ensure_ascii=False, indent=1)


def write(path, title, desc, main, crumb=None, faqs=None, noindex=False, extra=None):
    url = BASE + (path if path != '/' else '/')
    page = blog.fill(blog.shell(), TITLE=esc(title), DESC=esc(desc), CANONICAL=url,
                     OG=blog.og_tags(url, title, desc, blog.DEFAULT_IMAGE, 'website'),
                     JSONLD=graph(path, title, desc, faqs, crumb, extra),
                     BREADCRUMB=(f'<a href="/">Accueil</a><span>›</span>{esc(crumb)}' if crumb else '<span class="bc-tag">Ombrières photovoltaïques de parking, partout en France</span>'),
                     MAIN=main)
    if noindex:
        page = page.replace('content="index, follow"', 'content="noindex, follow"').replace(f'<link rel="canonical" href="{url}">\n', '')
    out = blog.p('404.html') if path == '/404' else blog.p(path.strip('/'), 'index.html') if path != '/' else blog.p('index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write(page)


# ---------------------------------------------------------------------------
# ACCUEIL
# ---------------------------------------------------------------------------
HOME_FAQ = [
    ("Mon parking est-il concerné par l'obligation d'ombrières ?",
     "La loi APER vise les parkings extérieurs de plus de 1 500 m², existants ou à créer. La surface prise en compte comprend les places, les voies de circulation et les zones d'accès, avec certaines exclusions. Un installateur peut vérifier la surface réellement concernée à partir d'un plan ou d'une vue aérienne."),
    ("Quelles sont les échéances ?",
     "Pour les parkings non concédés, l'échéance est fixée au 1er juillet 2026 au-delà de 10 000 m² et au 1er juillet 2028 entre 1 500 et 10 000 m². Des cas particuliers et des possibilités de délai existent : faites vérifier votre situation au regard des textes en vigueur."),
    ("Combien coûte une ombrière photovoltaïque ?",
     "Le budget dépend de la surface couverte, de la structure (portée, hauteur, fondations), du raccordement au réseau et du mode de valorisation de l'électricité. Selon le montage choisi, l'investissement peut être porté par un tiers. Seule une étude sur votre site permet de chiffrer le projet."),
    ("Peut-on installer des ombrières sans investir ?",
     "Oui, avec le tiers-investissement : un opérateur finance, installe et exploite les ombrières, et vous verse en général un loyer ou vous fait bénéficier d'une partie de l'électricité. Il faut alors examiner de près la durée du contrat, les responsabilités et la fin de contrat."),
    ("Qui va me recontacter ?",
     "Votre demande est transmise à un installateur partenaire intervenant dans votre région. Il vous rappelle pour comprendre votre site, puis vous propose si le projet est pertinent une étude de faisabilité. Vous restez libre de donner suite ou non."),
]


def page_home():
    main = hero('Loi APER · étude gratuite partout en France',
                "Ombrières solaires pour votre parking : <em>conformité et énergie</em> en un seul projet",
                "Votre parking dépasse 1 500 m² ? L'obligation d'ombrières approche. Décrivez votre site en une minute : un installateur partenaire étudie la faisabilité, le financement et le calendrier.",
                ["Vérification de l'obligation loi APER et des échéances", "Comparaison achat, tiers-investissement et location", "Étude de faisabilité gratuite et sans engagement"],
                'Ombrière solaire — accueil (haut de page)', art=True)
    main += trust()
    cards = [('law', 'Obligation loi APER', "Surface concernée, échéances 2026 et 2028, exemptions et sanctions : ce que vous devez savoir.", '/obligation-ombriere-parking'),
             ('euro', 'Financement', "Investir vous-même, confier le projet à un tiers-investisseur ou louer votre parking : les trois modèles.", '/financement-ombriere-solaire'),
             ('cart', 'Commerces et supermarchés', "Grandes surfaces, retail parks, galeries : des parkings souvent concernés en premier.", '/ombriere-solaire-supermarche'),
             ('factory', 'Entreprises et sites industriels', "Parkings salariés, plateformes logistiques, sièges : autoconsommation et recharge électrique.", '/ombriere-solaire-entreprise'),
             ('city', 'Collectivités', "Parkings publics, hôpitaux, établissements scolaires : obligations et montages adaptés.", '/ombriere-solaire-collectivite')]
    cs = ''.join(f'<a href="{u}" class="card"><span class="card-ic">{ic(i)}</span><h3>{t}</h3><p>{d}</p><span class="more">En savoir plus →</span></a>' for i, t, d, u in cards)
    main += f'''<section class="section">
  <div class="wrap">
    <div class="s-head"><span class="kicker">Votre situation</span><h2>Un projet d'ombrières se prépare selon votre site</h2><p>Les contraintes ne sont pas les mêmes pour un supermarché, une plateforme logistique ou un parking communal. Choisissez votre cas pour aller à l'essentiel.</p></div>
    <div class="cards">{cs}</div>
  </div>
</section>
<section class="section dark">
  <div class="wrap">
    <div class="s-head"><span class="kicker">Loi APER</span><h2>Deux échéances à retenir</h2><p>Pour les parkings extérieurs non concédés, au moins la moitié de la surface doit être couverte par des ombrières intégrant un procédé de production d'énergie renouvelable, avec une part d'ombrage végétal désormais possible.</p></div>
    <div class="timeline">
      <div class="tl"><b>1er juillet 2026</b><span>Plus de 10 000 m²</span><p>Les plus grands parkings sont les premiers concernés. Des délais supplémentaires existent sous conditions.</p></div>
      <div class="tl"><b>1er juillet 2028</b><span>De 1 500 à 10 000 m²</span><p>Une étude, des autorisations et un raccordement se préparent bien à l'avance : mieux vaut lancer le projet tôt.</p></div>
      <div class="tl"><b>Chaque année</b><span>Sanction en cas de retard</span><p>Une amende annuelle peut s'appliquer tant que le parking n'est pas en conformité, sauf exemption justifiée.</p></div>
    </div>
    {cta_row('Vérifier si mon parking est concerné')}
    <p class="note" style="color:rgba(255,255,255,.6)">Informations générales, mises à jour en octobre 2026. Les textes évoluent : faites vérifier votre situation précise. <a href="/obligation-ombriere-parking" style="text-decoration:underline">Lire notre guide complet</a>.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="s-head"><span class="kicker">Comment ça marche</span><h2>De votre demande à la mise en service</h2></div>
    <div class="steps">
      <div class="step"><h3>Vous décrivez votre parking</h3><p>Type de site, surface approximative, code postal : une minute suffit. Nous confions votre demande à un seul installateur qui intervient dans votre secteur.</p></div>
      <div class="step"><h3>Un appel sous 48&nbsp;h ouvrées</h3><p>L'installateur vous rappelle pour comprendre votre site : surface concernée, échéance loi APER, priorités (conformité, économies, recharge).</p></div>
      <div class="step"><h3>Visite et étude de faisabilité</h3><p>Si le projet est pertinent, il étudie votre parking : implantation, production estimée, raccordement, autorisations, financement.</p></div>
      <div class="step"><h3>Vous décidez, librement</h3><p>Vous recevez une proposition chiffrée. Tout ce qui précède est gratuit et ne vous engage à rien.</p></div>
    </div>
    {cta_row()}
  </div>
</section>
<section class="section alt">
  <div class="wrap split">
    <div>
      <span class="kicker">Au-delà de l'obligation</span>
      <h2 style="margin-top:.4rem;font-size:clamp(1.6rem,3.2vw,2.25rem);font-weight:800;letter-spacing:-.03em;line-height:1.15;color:var(--ink)">Une ombrière, c'est aussi un équipement utile</h2>
      <ul class="checklist">
        <li>{TICK}<span><strong>Produire votre électricité</strong> et la consommer sur place, ou la vendre au réseau.</span></li>
        <li>{TICK}<span><strong>Recharger des véhicules électriques</strong> : les ombrières se prêtent bien à l'installation de bornes.</span></li>
        <li>{TICK}<span><strong>Protéger vos visiteurs et leurs véhicules</strong> du soleil, de la pluie et de la grêle.</span></li>
        <li>{TICK}<span><strong>Valoriser votre site</strong> et vos engagements environnementaux auprès de vos clients et salariés.</span></li>
      </ul>
    </div>
    <div class="callout" style="margin-top:0;background:#fff">
      <strong>Pourquoi passer par Ombrière Solaire Parking ?</strong>
      <p style="margin-top:.6rem">Trouver le bon installateur, comparer les modèles de financement et comprendre la réglementation prend du temps. Nous transmettons votre demande à un professionnel qui intervient dans votre région, qui vous rappelle avec une première analyse. Le service est gratuit pour vous.</p>
      <div class="cta-row" style="margin-top:1.2rem"><a href="#devis" class="btn btn-ink btn-lg">Demander mon étude {ARROW}</a></div>
    </div>
  </div>
</section>
'''
    import villes
    chips = ''.join(f'<a href="{villes.path(v)}" class="link-card">{esc(v["nom"])}</a>' for v in villes.VILLES)
    main += f'''<section class="section">
  <div class="wrap">
    <div class="s-head"><span class="kicker">Près de chez vous</span><h2>Ombrières solaires autour de Lyon</h2><p>Nos installateurs partenaires interviennent dans toute la région. Retrouvez les sites concernés et les contraintes locales de votre secteur.</p></div>
    <div class="links-grid" style="margin-top:1.6rem">{chips}<a href="{villes.HUB}" class="link-card">Toutes nos zones d'intervention →</a></div>
  </div>
</section>
'''
    main += engagements(alt=True)
    main += faq(HOME_FAQ)
    main += final()
    write('/', "Ombrière Solaire Parking : Loi APER & Étude Gratuite",
          "Parking de plus de 1 500 m² ? Vérifiez l'obligation d'ombrières de la loi APER et recevez une étude gratuite d'un installateur partenaire, partout en France.",
          main, faqs=HOME_FAQ)


# ---------------------------------------------------------------------------
# OBLIGATION LOI APER
# ---------------------------------------------------------------------------
APER_FAQ = [
    ("La loi APER concerne-t-elle les parkings privés ?", "Oui. Le critère est la surface du parking extérieur, pas son caractère public ou privé. Un parking de supermarché, d'entreprise ou de copropriété peut être concerné s'il dépasse le seuil."),
    ("Les arbres peuvent-ils remplacer les ombrières ?", "En partie. Depuis la loi du 26 novembre 2025, l'ombrage peut combiner ombrières photovoltaïques et ombrage végétal, avec une part minimale de photovoltaïque. Un parking déjà ombragé à plus de 50 % par des arbres peut aussi relever d'une exemption, à justifier."),
    ("Qui est responsable de la mise en conformité ?", "En principe le propriétaire du parc de stationnement, sauf lorsque son exploitation a été confiée à un tiers dans le cadre d'un contrat de longue durée, comme une concession. En location, vérifiez ce que prévoit votre bail."),
    ("Que se passe-t-il si l'échéance est dépassée ?", "Une sanction financière annuelle peut être prononcée tant que le parking n'est pas conforme, sauf exemption justifiée. Lancer l'étude rapidement permet souvent de bénéficier des délais prévus pour les projets engagés."),
]


def page_aper():
    main = hero('Guide · mis à jour en octobre 2026',
                "Obligation d'ombrières de parking : <em>ce que prévoit la loi APER</em>",
                "Surface concernée, échéances, part à couvrir, exemptions et sanctions : l'essentiel pour savoir si votre parking est concerné et comment vous y préparer.",
                ["Parkings extérieurs de plus de 1 500 m²", "Échéances au 1er juillet 2026 et au 1er juillet 2028", "Vérification gratuite de votre situation"],
                'Ombrière solaire — page loi APER', form_title='Vérifier mon obligation')
    main += f'''<article class="content">
<h2>D'où vient l'obligation ?</h2>
<p>L'article 40 de la loi n° 2023-175 du 10 mars 2023 relative à l'accélération de la production d'énergies renouvelables, dite <strong>loi APER</strong>, impose d'équiper les parcs de stationnement extérieurs d'une certaine taille d'ombrières intégrant un procédé de production d'énergie renouvelable. Un décret de novembre 2024 en a précisé les modalités, notamment le calcul de la surface.</p>
<p>La loi du 26 novembre 2025 de simplification de l'urbanisme, dite <strong>loi Huwart</strong>, puis un décret de septembre 2026 ont assoupli certaines règles : combinaison possible avec un ombrage végétal et délais supplémentaires sous conditions. Ces textes sont récents : faites toujours vérifier votre cas au regard de la version en vigueur.</p>

<h2>Quels parkings sont concernés ?</h2>
<ul>
<li>Les <strong>parcs de stationnement extérieurs de plus de 1 500 m²</strong>, qu'ils soient publics ou privés.</li>
<li>Les parkings <strong>existants</strong>, ainsi que ceux dont la demande d'autorisation d'urbanisme a été déposée après l'entrée en vigueur de la loi.</li>
<li>La surface retenue comprend les emplacements, les voies de circulation et les zones d'accès. Certains espaces en sont exclus, comme les espaces verts ou certaines zones de stockage : la surface « réglementaire » peut donc différer de la surface cadastrale.</li>
</ul>
<p>Sur les sites industriels classés (ICPE), des règles spécifiques peuvent réduire la surface prise en compte autour des bâtiments et installations.</p>

<h2>Les échéances</h2>
<table>
<thead><tr><th>Situation</th><th>Échéance</th></tr></thead>
<tbody>
<tr><td>Parking non concédé de plus de 10 000 m²</td><td>1er juillet 2026</td></tr>
<tr><td>Parking non concédé de 1 500 à 10 000 m²</td><td>1er juillet 2028</td></tr>
<tr><td>Parking géré en concession ou délégation de service public</td><td>Lors de la conclusion ou du renouvellement du contrat, selon les règles prévues par les textes</td></tr>
</tbody>
</table>
<p>Des délais supplémentaires peuvent être accordés aux projets déjà engagés (commande passée, acompte versé) et dans certaines situations particulières. Les conditions sont précises : un installateur ou un conseil juridique pourra vérifier si vous pouvez en bénéficier.</p>

<h2>Quelle part du parking couvrir ?</h2>
<p>Au moins <strong>la moitié de la surface</strong> du parking doit être couverte par des ombrières intégrant un procédé de production d'énergie renouvelable. Depuis la loi Huwart, cette moitié peut combiner ombrières photovoltaïques et ombrage végétal (arbres, pergolas végétalisées), avec une part minimale de photovoltaïque. Un autre procédé de production d'énergie renouvelable d'efficacité équivalente peut également être admis.</p>

<h2>Les cas d'exemption</h2>
<p>Les textes prévoient des exemptions, qui doivent être justifiées :</p>
<ul>
<li>contraintes techniques, de sécurité, architecturales, patrimoniales ou environnementales ;</li>
<li>coût économiquement inacceptable du projet ;</li>
<li>parking déjà ombragé par des arbres sur au moins la moitié de sa surface ;</li>
<li>parking appelé à disparaître ou à être transformé dans le cadre d'une opération d'aménagement autorisée.</li>
</ul>
<p>Une exemption se démontre, généralement avec une étude : elle ne se présume pas.</p>

<h2>Les sanctions</h2>
<p>En cas de non-respect, une <strong>sanction financière annuelle</strong> peut être prononcée, dont le montant maximal dépend de la taille du parking, et ce chaque année jusqu'à la mise en conformité. Au-delà du risque de sanction, attendre le dernier moment expose à des délais d'étude, de raccordement et d'approvisionnement plus longs.</p>

<h2>Comment se préparer ?</h2>
<ol>
<li><strong>Mesurer la surface réglementaire</strong> de votre parking, à partir d'un plan ou d'une vue aérienne.</li>
<li><strong>Identifier le responsable</strong> : propriétaire, exploitant, bailleur ou preneur.</li>
<li><strong>Faire réaliser une étude de faisabilité</strong> : implantation, production, raccordement, autorisations.</li>
<li><strong>Choisir un mode de financement</strong> : achat, tiers-investissement ou location (voir notre page <a href="/financement-ombriere-solaire">financement des ombrières</a>).</li>
<li><strong>Planifier</strong> les autorisations d'urbanisme, la demande de raccordement et les travaux.</li>
</ol>
<div class="callout"><strong>À retenir :</strong> ces informations sont générales et à jour à la date indiquée. Elles ne constituent pas un conseil juridique. Pour une décision, appuyez-vous sur les textes publiés au Journal officiel et sur l'avis d'un professionnel.</div>
{cta_row('Faire vérifier mon parking')}
</article>
'''
    main += faq(APER_FAQ)
    main += links(['/financement-ombriere-solaire', '/ombriere-solaire-supermarche', '/ombriere-solaire-entreprise', '/ombriere-solaire-collectivite'])
    main += final()
    write('/obligation-ombriere-parking', "Obligation Ombrière Parking : Loi APER 2026-2028",
          "Loi APER : parkings de plus de 1 500 m², échéances 2026 et 2028, moitié de la surface à couvrir, exemptions, sanctions. Le guide complet, à jour.",
          main, crumb='Obligation loi APER', faqs=APER_FAQ,
          extra={'@type': 'Article', 'headline': "Obligation d'ombrières de parking : ce que prévoit la loi APER", 'dateModified': TODAY,
                 'inLanguage': 'fr-FR', 'author': {'@id': ORG_ID}, 'publisher': {'@id': ORG_ID}, 'mainEntityOfPage': BASE + '/obligation-ombriere-parking'})


# ---------------------------------------------------------------------------
# FINANCEMENT
# ---------------------------------------------------------------------------
FIN_FAQ = [
    ("Quel est le modèle le plus intéressant ?", "Il n'y a pas de réponse unique. L'achat maximise les gains si vous disposez de la trésorerie et consommez beaucoup d'électricité sur place. Le tiers-investissement évite d'investir mais partage la valeur. La comparaison doit se faire sur toute la durée du contrat."),
    ("Autoconsommation ou vente totale ?", "L'autoconsommation est intéressante quand le site consomme pendant la journée (commerce, bureaux, logistique, recharge de véhicules). La vente totale convient mieux aux sites qui consomment peu. Des formules mixtes, avec vente du surplus, existent aussi."),
    ("Que devient l'ombrière en fin de contrat de tiers-investissement ?", "Selon le contrat : démontage par l'opérateur, cession au propriétaire ou prolongation. C'est un point à négocier dès le départ, au même titre que l'entretien, l'assurance et la remise en état."),
    ("Existe-t-il des aides ?", "Les dispositifs de soutien (tarifs d'achat ou complément de rémunération, appels d'offres pour les grandes puissances) évoluent régulièrement. L'installateur vous indiquera ceux qui s'appliquent à votre projet au moment de l'étude."),
]


def page_fin():
    main = hero('Financement', "Financer une ombrière solaire : <em>achat, tiers-investissement ou location</em>",
                "Une ombrière photovoltaïque peut être financée de plusieurs façons, avec ou sans investissement de votre part. Voici comment comparer les trois modèles pour votre parking.",
                ["Les trois modèles expliqués simplement", "Autoconsommation, vente du surplus ou vente totale", "Comparaison chiffrée lors de l'étude gratuite"],
                'Ombrière solaire — page financement', form_title='Comparer les financements')
    main += f'''<article class="content">
<h2>Ce qui fait le coût d'une ombrière</h2>
<p>Le budget d'une ombrière photovoltaïque dépend surtout :</p>
<ul>
<li>de la <strong>surface couverte</strong> et de la configuration des places (simple ou double rangée) ;</li>
<li>de la <strong>structure</strong> : portée, hauteur, résistance au vent et à la neige, type de fondations selon le sol ;</li>
<li>du <strong>raccordement</strong> au réseau, qui peut nécessiter des travaux importants selon la puissance ;</li>
<li>des <strong>options</strong> : bornes de recharge, éclairage, récupération des eaux de pluie, bardage ;</li>
<li>des <strong>contraintes du chantier</strong> : maintien de l'activité du parking pendant les travaux, réseaux enterrés.</li>
</ul>
<p>Pour une estimation fiable, l'installateur a besoin d'un plan ou d'une vue aérienne du parking et de vos consommations d'électricité.</p>

<h2>Modèle 1 : vous investissez</h2>
<p>Vous financez l'installation, sur fonds propres ou par un emprunt ou un crédit-bail, et vous en êtes propriétaire. Vous profitez de toute l'électricité produite : consommée sur place, elle réduit votre facture ; vendue, elle génère un revenu.</p>
<ul>
<li><strong>Pour vous :</strong> la totalité des gains sur la durée de vie de l'installation, la maîtrise du projet.</li>
<li><strong>À prévoir :</strong> la trésorerie ou la capacité d'emprunt, l'entretien, l'assurance et le suivi de production.</li>
</ul>

<h2>Modèle 2 : le tiers-investissement</h2>
<p>Un opérateur finance, construit et exploite les ombrières pendant une longue durée. Il se rémunère sur la vente de l'électricité et, selon les contrats, vous verse un loyer ou vous vend l'électricité produite à un prix convenu à l'avance.</p>
<ul>
<li><strong>Pour vous :</strong> aucun investissement, la conformité réglementaire assurée, souvent un revenu ou une électricité à prix stable.</li>
<li><strong>À vérifier :</strong> la durée du contrat, la répartition de l'entretien et des responsabilités, les conditions de sortie et le devenir des ombrières en fin de contrat.</li>
</ul>

<h2>Modèle 3 : la location de votre parking</h2>
<p>Variante du tiers-investissement : vous mettez votre parking à disposition d'un producteur, par un bail de longue durée, en échange d'un loyer. Ce modèle convient bien aux propriétaires qui veulent avant tout se mettre en conformité sans gérer d'installation.</p>

<h2>Que faire de l'électricité produite ?</h2>
<table>
<thead><tr><th>Mode</th><th>Principe</th><th>Adapté si…</th></tr></thead>
<tbody>
<tr><td>Autoconsommation</td><td>Vous consommez l'électricité sur place, le surplus éventuel est vendu</td><td>Le site consomme en journée : commerce, bureaux, froid, recharge</td></tr>
<tr><td>Autoconsommation collective</td><td>L'électricité est partagée avec des consommateurs voisins</td><td>Zones d'activités, collectivités, groupes de sites proches</td></tr>
<tr><td>Vente totale</td><td>Toute la production est injectée et vendue sur le réseau</td><td>Le site consomme peu ou la priorité est le revenu</td></tr>
</tbody>
</table>
<p>Coupler l'ombrière à des <strong>bornes de recharge</strong> est souvent pertinent : l'électricité produite en journée alimente directement les véhicules garés dessous.</p>

<h2>Comment comparer les offres ?</h2>
<ol>
<li>Comparez sur <strong>toute la durée</strong> du contrat, pas seulement la première année.</li>
<li>Demandez les <strong>hypothèses</strong> de production et de prix de l'électricité retenues.</li>
<li>Vérifiez qui prend en charge l'<strong>entretien</strong>, l'<strong>assurance</strong> et les <strong>pannes</strong>.</li>
<li>Faites relire les contrats de longue durée par un <strong>conseil juridique</strong>.</li>
</ol>
{cta_row('Recevoir une étude comparative')}
</article>
'''
    main += faq(FIN_FAQ)
    main += links(['/obligation-ombriere-parking', '/ombriere-solaire-entreprise', '/ombriere-solaire-supermarche', '/devis-ombriere-solaire'])
    main += final()
    write('/financement-ombriere-solaire', "Financer une Ombrière Solaire : Achat ou Tiers-Investisseur",
          "Ombrière photovoltaïque : investir vous-même, tiers-investissement ou location de parking ? Avantages, points de vigilance et choix de l'autoconsommation.",
          main, crumb='Financement', faqs=FIN_FAQ)


# ---------------------------------------------------------------------------
# PAGES CIBLES
# ---------------------------------------------------------------------------
def page_target(path, crumb, title, desc, eyebrow, h1, sub, points, preselect, subject, sections, faqs, related):
    main = hero(eyebrow, h1, sub, points, subject, preselect=preselect)
    main += f'<article class="content">\n{sections}\n{cta_row()}\n</article>\n'
    main += faq(faqs)
    main += links(related)
    main += final()
    write(path, title, desc, main, crumb=crumb, faqs=faqs)


SUPER_FAQ = [
    ("Mon supermarché est-il concerné ?", "Si son parking extérieur dépasse 1 500 m², très probablement. Les grandes surfaces font partie des sites les plus souvent concernés, avec des échéances qui dépendent de la surface. Une vérification de la surface réglementaire permet de le confirmer."),
    ("Faut-il fermer le parking pendant les travaux ?", "Rarement en totalité. Les travaux sont généralement organisés par zones, pour maintenir l'accès des clients. Le phasage est un point à prévoir dès l'étude."),
    ("Je suis locataire des murs, qui doit agir ?", "La responsabilité de principe revient au propriétaire du parking, mais le bail peut répartir les obligations différemment. Vérifiez votre bail commercial et échangez tôt avec votre bailleur."),
    ("Les ombrières peuvent-elles alimenter le magasin ?", "Oui. Un magasin consomme beaucoup en journée, notamment pour le froid et l'éclairage : c'est un bon profil pour l'autoconsommation de l'électricité produite."),
]
ENT_FAQ = [
    ("Un parking d'entreprise privé est-il concerné ?", "Oui, s'il s'agit d'un parking extérieur de plus de 1 500 m². L'obligation ne dépend pas de l'ouverture au public."),
    ("Peut-on combiner ombrières et bornes de recharge ?", "C'est l'un des intérêts majeurs : l'électricité produite en journée alimente les véhicules des salariés ou de la flotte. Le dimensionnement se fait ensemble dans l'étude."),
    ("Notre site est classé ICPE, est-ce un problème ?", "Pas forcément, mais des règles spécifiques s'appliquent, notamment des distances autour de certaines installations. L'étude doit en tenir compte dès le départ."),
    ("Combien de temps dure un projet ?", "Il faut compter l'étude, les autorisations d'urbanisme, la demande de raccordement puis le chantier. Le raccordement est souvent l'étape la plus longue : mieux vaut lancer le projet tôt."),
]
COLL_FAQ = [
    ("Une collectivité doit-elle passer un marché public ?", "En général, oui : l'installation ou la mise à disposition d'un parking à un opérateur passe par une procédure de mise en concurrence adaptée. Un échange en amont avec des installateurs aide à définir le besoin."),
    ("Les parkings en concession sont-ils concernés ?", "Oui, avec des règles propres : l'obligation s'applique lors de la conclusion ou du renouvellement du contrat. Vérifiez la date et les clauses de vos contrats."),
    ("Que faire de l'électricité produite ?", "Elle peut alimenter des bâtiments publics proches, être partagée en autoconsommation collective avec d'autres consommateurs, ou être vendue. Le bon choix dépend des consommations à proximité."),
    ("Comment concilier ombrières et patrimoine ?", "Dans les sites sensibles, l'insertion paysagère est étudiée avec les services concernés. Une impossibilité avérée peut aussi relever d'une exemption, à justifier."),
]


def page_super():
    page_target('/ombriere-solaire-supermarche', 'Commerces et supermarchés',
        "Ombrière Solaire Supermarché : Loi APER et Projet Complet",
        "Supermarché, retail park, centre commercial : votre parking est concerné par la loi APER ? Étude gratuite d'ombrières solaires par un installateur partenaire.",
        'Commerces · grandes surfaces · retail parks',
        "Ombrières solaires pour <em>supermarchés et commerces</em>",
        "Les parkings de grandes surfaces sont parmi les premiers concernés par la loi APER. Bien conçues, les ombrières protègent vos clients, alimentent le magasin et peuvent accueillir des bornes de recharge.",
        ["Parkings clients de grandes surfaces et retail parks", "Travaux par zones pour maintenir l'accès", "Autoconsommation pour le froid et l'éclairage"],
        'Commerce / supermarché', 'Ombrière solaire — page commerces',
        '''<h2>Pourquoi les commerces sont en première ligne</h2>
<p>Les supermarchés, hypermarchés, retail parks et centres commerciaux disposent souvent de parkings de plusieurs milliers de mètres carrés. Selon leur surface, ils relèvent de l'échéance du 1er juillet 2026 ou de celle du 1er juillet 2028. Pour une enseigne qui gère plusieurs magasins, la question se pose site par site.</p>
<h2>Un projet qui sert aussi le magasin</h2>
<ul>
<li><strong>Électricité consommée sur place :</strong> un magasin consomme beaucoup en journée (froid alimentaire, éclairage, climatisation), au moment où les ombrières produisent.</li>
<li><strong>Confort des clients :</strong> places ombragées l'été, abritées sous la pluie.</li>
<li><strong>Recharge électrique :</strong> des bornes sous ombrières attirent une clientèle qui reste plus longtemps.</li>
<li><strong>Image :</strong> un engagement visible pour les clients et les collectivités locales.</li>
</ul>
<h2>Les points à préparer</h2>
<ul>
<li><strong>Qui porte le projet :</strong> propriétaire des murs, exploitant ou foncière. Le bail commercial peut répartir les obligations.</li>
<li><strong>Le phasage du chantier :</strong> travaux par zones, horaires adaptés, sécurité des clients.</li>
<li><strong>Les réseaux enterrés et la nature du sol</strong>, qui conditionnent les fondations.</li>
<li><strong>Le mode de financement :</strong> investissement, tiers-investissement ou location du parking. Voir notre page <a href="/financement-ombriere-solaire">financement</a>.</li>
</ul>''',
        SUPER_FAQ, ['/obligation-ombriere-parking', '/financement-ombriere-solaire', '/ombriere-solaire-entreprise'])


def page_ent():
    page_target('/ombriere-solaire-entreprise', 'Entreprises',
        "Ombrière Solaire Entreprise : Parking Salariés et Logistique",
        "Ombrières photovoltaïques pour parkings d'entreprise, sites industriels et logistiques : loi APER, autoconsommation, bornes de recharge. Étude gratuite.",
        'Entreprises · industrie · logistique',
        "Ombrières solaires pour <em>parkings d'entreprise</em>",
        "Parking salariés, plateforme logistique, site industriel ou siège : les ombrières répondent à la loi APER tout en produisant une électricité que votre site peut consommer directement.",
        ["Parkings salariés, visiteurs et poids lourds", "Couplage avec la recharge des véhicules", "Prise en compte des contraintes ICPE"],
        'Entreprise / site industriel', 'Ombrière solaire — page entreprises',
        '''<h2>Les entreprises concernées</h2>
<p>Tout parking extérieur de plus de 1 500 m² est concerné, qu'il soit ouvert au public ou réservé aux salariés. C'est fréquent pour les sièges sociaux, les zones d'activités, les plateformes logistiques et les sites industriels.</p>
<h2>Les bénéfices pour votre site</h2>
<ul>
<li><strong>Autoconsommation :</strong> bureaux, ateliers et entrepôts consomment en journée, au moment de la production.</li>
<li><strong>Recharge de la flotte et des salariés :</strong> les ombrières sont un support naturel pour les bornes de recharge.</li>
<li><strong>Stabilité du coût de l'énergie :</strong> une part de votre électricité produite sur place, à coût prévisible.</li>
<li><strong>Engagements RSE :</strong> un projet concret et visible dans votre démarche environnementale.</li>
</ul>
<h2>Les spécificités à anticiper</h2>
<ul>
<li><strong>Sites classés ICPE :</strong> règles de distance et de sécurité autour de certaines installations, qui peuvent modifier la surface concernée.</li>
<li><strong>Circulation des poids lourds :</strong> hauteur libre et implantation des poteaux adaptées.</li>
<li><strong>Raccordement :</strong> selon la puissance, le délai de raccordement peut être long. À lancer tôt.</li>
<li><strong>Locataire ou propriétaire :</strong> vérifiez qui porte l'obligation dans votre bail. Voir notre guide de la <a href="/obligation-ombriere-parking">loi APER</a>.</li>
</ul>''',
        ENT_FAQ, ['/obligation-ombriere-parking', '/financement-ombriere-solaire', '/ombriere-solaire-supermarche'])


def page_coll():
    page_target('/ombriere-solaire-collectivite', 'Collectivités',
        "Ombrière Solaire Collectivité : Parkings Publics et Loi APER",
        "Communes, hôpitaux, établissements publics : ombrières solaires sur parkings publics, concessions, autoconsommation collective. Étude gratuite.",
        'Collectivités · établissements publics',
        "Ombrières solaires pour <em>parkings publics</em>",
        "Parkings de mairie, de gare, d'hôpital, de lycée ou de zone de loisirs : les collectivités et établissements publics sont concernés par la loi APER et peuvent faire des ombrières un levier pour leur politique énergétique.",
        ["Parkings publics et parkings en concession", "Autoconsommation collective avec les bâtiments voisins", "Préparation du besoin avant mise en concurrence"],
        'Collectivité / établissement public', 'Ombrière solaire — page collectivités',
        '''<h2>Des obligations propres aux acteurs publics</h2>
<p>Les parkings extérieurs de plus de 1 500 m² gérés par une collectivité ou un établissement public sont concernés, avec des règles particulières pour ceux qui sont exploités en concession ou en délégation de service public : l'obligation s'applique alors lors de la conclusion ou du renouvellement du contrat.</p>
<h2>Les montages possibles</h2>
<ul>
<li><strong>Investissement direct</strong> par la collectivité, avec un marché de travaux.</li>
<li><strong>Mise à disposition du parking</strong> à un opérateur, qui finance et exploite les ombrières en échange d'une redevance.</li>
<li><strong>Société de projet locale</strong>, associant parfois des acteurs du territoire.</li>
</ul>
<p>Dans la plupart des cas, une procédure de mise en concurrence est nécessaire. Échanger en amont avec des installateurs aide à définir un besoin réaliste et à rédiger le cahier des charges.</p>
<h2>Valoriser l'électricité sur le territoire</h2>
<ul>
<li>Alimenter des <strong>bâtiments publics</strong> proches : écoles, gymnases, services techniques.</li>
<li>Partager l'électricité en <strong>autoconsommation collective</strong> avec d'autres consommateurs du secteur.</li>
<li>Installer des <strong>bornes de recharge</strong> pour les habitants et les agents.</li>
</ul>
<p>Pour les sites patrimoniaux ou sensibles, l'insertion paysagère s'étudie avec les services concernés. Voir notre guide de la <a href="/obligation-ombriere-parking">loi APER</a> pour les cas d'exemption.</p>''',
        COLL_FAQ, ['/obligation-ombriere-parking', '/financement-ombriere-solaire', '/ombriere-solaire-entreprise'])


ABOUT_FAQ = [
    ("Ombrière Solaire Parking est-il un installateur ?", "Non. Nous informons, nous qualifions votre projet et nous le confions à un installateur partenaire qui intervient dans votre secteur. C'est lui qui réalise l'étude, puis les travaux si vous donnez suite, sous sa propre responsabilité."),
    ("Ma demande sera-t-elle envoyée à plusieurs entreprises ?", "Non. Votre demande est confiée à un seul installateur partenaire. Vous n'êtes pas sollicité par une série d'entreprises."),
    ("Puis-je refuser la proposition ?", "Oui, à tout moment. L'appel, la visite et l'étude sont gratuits et sans engagement : vous restez libre de ne pas donner suite."),
]


def page_about():
    main = f'''<section class="post-hero"><div class="post-hero-inner">
  <span class="post-tag">Qui sommes-nous</span>
  <h1>Un interlocuteur pour votre projet d'ombrières, du premier appel à la décision</h1>
  <p class="post-meta">Ombrière Solaire Parking aide les propriétaires et gestionnaires de parkings à répondre à la loi APER, sans y passer des semaines.</p>
</div></section>
<article class="content">
<h2>Pourquoi ce service existe</h2>
<p>Avec la loi APER, des milliers de parkings extérieurs de plus de 1&nbsp;500&nbsp;m² doivent s'équiper d'ombrières photovoltaïques. Pour un directeur de magasin, un gestionnaire de site ou une collectivité, les questions s'accumulent vite : mon parking est-il concerné ? Quelle est mon échéance ? Faut-il investir ou passer par un tiers-investisseur ? À qui faire confiance ?</p>
<p>Nous avons créé Ombrière Solaire Parking pour répondre à ces questions simplement, et pour vous mettre en relation avec un installateur sérieux qui intervient près de chez vous.</p>

<h2>Ce que nous faisons, et ce que nous ne faisons pas</h2>
<ul>
<li><strong>Nous vous informons</strong> : obligation, échéances, exemptions, financement. Nos <a href="/obligation-ombriere-parking">guides</a> et notre <a href="/blog">blog</a> sont mis à jour au fil des textes.</li>
<li><strong>Nous qualifions votre projet</strong> : type de site, surface, localisation, pour que l'installateur vous rappelle en connaissant déjà l'essentiel.</li>
<li><strong>Nous confions votre demande à un seul installateur partenaire</strong>, qui intervient dans votre secteur.</li>
<li><strong>Nous ne vendons pas de panneaux et ne réalisons pas les travaux.</strong> L'étude et le chantier sont réalisés par l'installateur, sous sa propre responsabilité.</li>
</ul>

<h2>Votre demande, étape par étape</h2>
<ol>
<li><strong>Vous décrivez votre parking</strong> en une minute dans le formulaire : type de site, surface approximative, code postal, coordonnées.</li>
<li><strong>Nous transmettons votre demande</strong> à un installateur partenaire qui intervient dans votre secteur, et à lui seul.</li>
<li><strong>Il vous rappelle sous 48&nbsp;h ouvrées</strong> pour un premier échange : surface concernée, échéance, priorités.</li>
<li><strong>Si le projet est pertinent, il étudie votre site</strong> : implantation, production estimée, raccordement, autorisations et modes de financement.</li>
<li><strong>Vous recevez une proposition</strong> et vous décidez librement. Jusque-là, tout est gratuit et sans engagement.</li>
</ol>

<h2>Nos engagements</h2>
<ul>
<li><strong>Gratuit et sans engagement</strong> : vous ne payez rien pour l'appel, la visite ou l'étude.</li>
<li><strong>Un seul installateur</strong> : votre demande n'est pas diffusée à une liste d'entreprises.</li>
<li><strong>Vos données ne sont jamais revendues</strong> : elles servent uniquement à l'étude de votre projet. Voir notre <a href="/politique-confidentialite">politique de confidentialité</a>.</li>
<li><strong>Pas de démarchage</strong> : seul l'installateur à qui votre demande est confiée vous contacte, et uniquement pour votre projet.</li>
</ul>
<p>Une question avant de vous lancer ? Appelez-nous au <a href="tel:0647326572">06&nbsp;47&nbsp;32&nbsp;65&nbsp;72</a>.</p>
<p class="signature">— L'équipe Ombrière Solaire Parking</p>
{cta_row('Demander mon étude gratuite')}
</article>
'''
    main = main.replace('href="#devis"', 'href="/devis-ombriere-solaire"')
    main += faq(ABOUT_FAQ)
    main += links(['/obligation-ombriere-parking', '/financement-ombriere-solaire', '/zones-intervention', '/devis-ombriere-solaire'])
    main += final().replace('href="#devis"', 'href="/devis-ombriere-solaire"')
    write('/qui-sommes-nous', "Qui Sommes-Nous | Ombrière Solaire Parking",
          "Ombrière Solaire Parking aide les propriétaires de parkings à répondre à la loi APER : information, étude gratuite, un seul installateur partenaire, données jamais revendues.",
          main, crumb='Qui sommes-nous', faqs=ABOUT_FAQ)


DEVIS_FAQ = [
    ("Que faut-il préparer pour l'étude ?", "L'adresse du parking, sa surface approximative, si possible un plan ou une capture d'une vue aérienne, et vos factures d'électricité si vous envisagez l'autoconsommation."),
    ("Combien de temps pour être recontacté ?", "Un installateur partenaire vous recontacte en général sous 48 heures ouvrées pour un premier échange, puis organise l'étude si le projet est pertinent."),
    ("L'étude m'engage-t-elle ?", "Non. L'étude et les échanges sont gratuits et sans engagement : vous décidez librement de la suite."),
]


def page_devis():
    main = hero('Étude gratuite · sans engagement', "Demandez votre <em>étude d'ombrières solaires</em>",
                "Une minute pour décrire votre parking. Un installateur partenaire qui intervient dans votre région vous recontacte pour une première analyse : obligation, faisabilité, financement.",
                ["Premier retour sous 48 h ouvrées", "Vérification de l'obligation loi APER", "Comparaison des modes de financement"],
                'Ombrière solaire — page devis', form_title='Votre étude gratuite')
    main += trust()
    main += f'''<section class="section">
  <div class="wrap">
    <div class="s-head"><h2>Comment se déroule l'étude ?</h2></div>
    <div class="steps">
      <div class="step"><h3>Premier échange</h3><p>L'installateur vous rappelle pour comprendre votre site, vos échéances et vos priorités.</p></div>
      <div class="step"><h3>Analyse du parking</h3><p>Surface réglementaire, implantation possible, contraintes du sol et des réseaux, raccordement.</p></div>
      <div class="step"><h3>Proposition</h3><p>Production estimée, budget ou loyer selon le financement retenu, calendrier.</p></div>
    </div>
  </div>
</section>
'''
    main += engagements(alt=True)
    main += faq(DEVIS_FAQ)
    write('/devis-ombriere-solaire', "Devis Ombrière Solaire Parking : Étude Gratuite",
          "Demandez une étude gratuite d'ombrières photovoltaïques pour votre parking : obligation loi APER, faisabilité, financement. Réponse sous 48 h ouvrées.",
          main, crumb='Étude gratuite', faqs=DEVIS_FAQ)


# ---------------------------------------------------------------------------
# PAGES LÉGALES
# ---------------------------------------------------------------------------
def T(s):
    return f'<mark class="todo">[À COMPLÉTER : {s}]</mark>'


def page_legal():
    ml = f'''<article class="content legal">
<h1>Mentions légales</h1>
<p class="updated">Dernière mise à jour : {T('date')}</p>
<h2>Éditeur du site</h2>
<p>Le site <strong>ombriere-solaire-parking.fr</strong> est édité par :</p>
<ul>
<li>Nom ou raison sociale : {T('nom et prénom, ou raison sociale')}</li>
<li>Forme juridique : {T('micro-entreprise, EI, SASU, SAS…')} — capital social : {T('montant, si société')}</li>
<li>Adresse du siège : {T('adresse postale complète')}</li>
<li>SIRET : {T('numéro SIRET')}</li>
<li>RCS : {T('ville et numéro RCS, si inscrit')}</li>
<li>N° de TVA intracommunautaire : {T('numéro, ou « non assujetti »')}</li>
<li>Téléphone : <a href="tel:0647326572">06 47 32 65 72</a></li>
<li>E-mail : {T('adresse e-mail de contact')}</li>
<li>Directeur de la publication : {T('nom et prénom')}</li>
</ul>
<h2>Hébergeur</h2>
<p>Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, États-Unis — <a href="https://vercel.com" rel="nofollow noopener">vercel.com</a></p>
<h2>Nature du service</h2>
<p>Ombrière Solaire Parking est un service d'information et de mise en relation entre les propriétaires et gestionnaires de parcs de stationnement ayant un projet d'ombrières photovoltaïques et des installateurs partenaires. Les demandes envoyées via les formulaires du site sont transmises à un installateur partenaire, qui réalise l'étude et, le cas échéant, l'installation sous sa propre responsabilité. {T('vérifier que cette description correspond à votre activité')}</p>
<h2>Propriété intellectuelle</h2>
<p>L'ensemble des contenus du site (textes, illustrations, logo, structure) est la propriété de l'éditeur, sauf mention contraire. Toute reproduction ou représentation, totale ou partielle, sans autorisation écrite préalable est interdite.</p>
<h2>Responsabilité</h2>
<p>Les informations publiées sur ce site, notamment sur la réglementation des parcs de stationnement, les échéances, les modes de financement et les dispositifs de soutien, sont données à titre indicatif et peuvent évoluer. Elles ne constituent ni une offre contractuelle, ni un conseil juridique ou financier. Seuls les textes officiels font foi, et seul le devis remis par l'installateur engage celui-ci.</p>
<h2>Données personnelles et cookies</h2>
<p>Le traitement de vos données personnelles et l'utilisation éventuelle de cookies sont décrits dans notre <a href="/politique-confidentialite">politique de confidentialité</a>.</p>
</article>
'''
    write('/mentions-legales', 'Mentions légales | Ombrière Solaire Parking', "Mentions légales du site Ombrière Solaire Parking : éditeur, hébergeur, nature du service de mise en relation.", ml, crumb='Mentions légales')
    pc = f'''<article class="content legal">
<h1>Politique de confidentialité</h1>
<p class="updated">Dernière mise à jour : {T('date')}</p>
<h2>Responsable du traitement</h2>
<p>{T('nom ou raison sociale')}, {T('adresse')}, SIRET {T('numéro')}. Contact pour toute question relative à vos données : {T('adresse e-mail')}.</p>
<h2>Données collectées</h2>
<p>Lorsque vous remplissez un formulaire, nous collectons : votre nom et votre fonction, le nom de votre société ou organisme, votre numéro de téléphone, votre adresse e-mail, le code postal du parking, le type de site et sa surface approximative. Nous enregistrons aussi la page depuis laquelle la demande est envoyée et la provenance de votre visite (moteur de recherche, lien, campagne), afin de mesurer l'efficacité du site.</p>
<h2>Finalités et bases légales</h2>
<table>
<tr><th>Finalité</th><th>Base légale</th></tr>
<tr><td>Traiter votre demande et la transmettre à un installateur partenaire pour l'étude de votre projet</td><td>Mesures précontractuelles prises à votre demande (art. 6.1.b RGPD)</td></tr>
<tr><td>Vous recontacter au sujet de votre demande</td><td>Mesures précontractuelles prises à votre demande (art. 6.1.b RGPD)</td></tr>
<tr><td>Mesure d'audience du site, si elle est activée</td><td>Votre consentement (art. 6.1.a RGPD et art. 82 de la loi Informatique et Libertés)</td></tr>
</table>
<h2>Destinataires</h2>
<ul>
<li><strong>Installateurs partenaires</strong> : votre demande est transmise à un installateur intervenant dans votre région, uniquement pour l'étude de votre projet. {T('liste des partenaires, ou catégories de partenaires')}</li>
<li><strong>Prestataires techniques</strong> : Vercel (hébergement), Web3Forms (acheminement des formulaires), Google (polices de caractères) et, si la mesure d'audience est activée et acceptée, Google Analytics et Microsoft Clarity.</li>
</ul>
<h2>Transferts hors de l'Union européenne</h2>
<p>Certains prestataires peuvent traiter des données aux États-Unis. Ces transferts sont encadrés par le Data Privacy Framework UE–États-Unis ou par les clauses contractuelles types de la Commission européenne.</p>
<h2>Durée de conservation</h2>
<p>Les données de votre demande sont conservées pendant 3 ans à compter de notre dernier échange, puis supprimées.</p>
<h2>Vos droits</h2>
<p>Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation, d'opposition et de portabilité de vos données. Pour les exercer, écrivez à {T('adresse e-mail')}. Vous pouvez aussi adresser une réclamation à la CNIL (<a href="https://www.cnil.fr" rel="nofollow noopener">www.cnil.fr</a>).</p>
<h2 id="cookies">Cookies</h2>
<p>Le site ne dépose aucun cookie de mesure d'audience sans votre accord. Si un outil de mesure est activé, un bandeau vous permet de l'accepter ou de le refuser, et vous pouvez modifier votre choix à tout moment via le lien « Gérer les cookies » en bas de page.</p>
</article>
'''
    write('/politique-confidentialite', 'Politique de confidentialité | Ombrière Solaire Parking', "Comment Ombrière Solaire Parking traite vos données personnelles et utilise les cookies.", pc, crumb='Politique de confidentialité')
    nf = '''<article class="content legal">
<h1>Page introuvable</h1>
<p>La page que vous cherchez n'existe pas ou a été déplacée.</p>
<ul>
<li><a href="/">Retour à l'accueil</a></li>
<li><a href="/obligation-ombriere-parking">Obligation loi APER</a></li>
<li><a href="/devis-ombriere-solaire">Demander une étude gratuite</a></li>
<li><a href="/blog">Blog</a></li>
</ul>
</article>
'''
    write('/404', 'Page introuvable | Ombrière Solaire Parking', "Cette page n'existe pas ou a été déplacée.", nf, crumb='Page introuvable', noindex=True)


SITEMAP_PAGES = [('/', '1.0', 'weekly'), ('/obligation-ombriere-parking', '0.9', 'monthly'), ('/financement-ombriere-solaire', '0.8', 'monthly'),
                 ('/ombriere-solaire-supermarche', '0.8', 'monthly'), ('/ombriere-solaire-entreprise', '0.8', 'monthly'),
                 ('/ombriere-solaire-collectivite', '0.8', 'monthly'), ('/devis-ombriere-solaire', '0.7', 'monthly'),
                 ('/qui-sommes-nous', '0.5', 'monthly'), ('/mentions-legales', '0.2', 'yearly'), ('/politique-confidentialite', '0.2', 'yearly')]


def sitemap_base():
    """Écrit la partie fixe du sitemap (le blog l'enrichit ensuite)."""
    import villes
    pages_all = SITEMAP_PAGES + [(u, '0.7', 'monthly') for u in villes.all_paths()]
    rows = ''.join(f'  <url>\n    <loc>{BASE}{u if u != "/" else "/"}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{f}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n'
                   for u, pr, f in pages_all)
    with open(blog.p('sitemap.xml'), 'w', encoding='utf-8') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '</urlset>\n')


def blog_form_template():
    """Formulaire inséré dans chaque article de blog (scripts/templates/form.html)."""
    pts = ''.join(f'<li>{TICK}{t}</li>' for t in ["Vérification de l'obligation loi APER", "Faisabilité, production et raccordement", "Comparaison des modes de financement"])
    tpl = f'''<section class="form-section">
  <div class="form-inner">
    <div class="form-left">
      <h2>Faites étudier votre parking gratuitement</h2>
      <p>Un installateur partenaire qui intervient dans votre région vous recontacte sous 48&nbsp;h ouvrées pour une première analyse, sans engagement.</p>
      <ul>{pts}</ul>
    </div>
    {form_card('b', 'Ombrière solaire — article du blog')}
  </div>
</section>
'''
    with open(blog.p('scripts', 'templates', 'form.html'), 'w', encoding='utf-8') as fh:
        fh.write(tpl)


if __name__ == '__main__':
    blog_form_template()
    page_home(); page_aper(); page_fin(); page_super(); page_ent(); page_coll(); page_devis(); page_about(); page_legal()
    import villes
    villes.build()
    if '--sitemap' in sys.argv or not os.path.exists(blog.p('sitemap.xml')):
        sitemap_base()
    print('Pages générées.')
