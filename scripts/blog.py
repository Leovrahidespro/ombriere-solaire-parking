#!/usr/bin/env python3
"""Construit le blog à partir de content/articles/*.json.

- blog/<slug>/index.html : une page par article, dans le gabarit du site
- blog/index.html        : la liste des articles
- sitemap.xml            : entrées /blog mises à jour (les autres pages sont conservées)

Aucune dépendance externe : python3 scripts/blog.py
"""
import html
import json
import math
import os
import re
import sys
from datetime import date
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://www.ombriere-solaire-parking.fr'
ORG_ID = BASE + '/#organisation'
DEFAULT_IMAGE = BASE + '/og-image.png'
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août',
        'septembre', 'octobre', 'novembre', 'décembre']

# Pages du site vers lesquelles un article peut faire un lien interne.
PAGES_SITE = {
    '/': "Accueil : ombrières solaires de parking, étude gratuite",
    '/obligation-ombriere-parking': "Obligation loi APER : parkings concernés, échéances, exemptions",
    '/financement-ombriere-solaire': "Financer une ombrière : achat, tiers-investissement, location",
    '/ombriere-solaire-supermarche': "Ombrières pour supermarchés et commerces",
    '/ombriere-solaire-entreprise': "Ombrières pour parkings d'entreprise et sites industriels",
    '/ombriere-solaire-collectivite': "Ombrières pour collectivités et parkings publics",
    '/devis-ombriere-solaire': "Demande d'étude gratuite",
}


def p(*parts):
    return os.path.join(ROOT, *parts)


def esc(s):
    return html.escape(s or '', quote=True)


def date_fr(iso):
    y, m, d = (int(x) for x in iso.split('-'))
    return f"{d} {MOIS[m - 1]} {y}"


# ---------------------------------------------------------------------------
# Nettoyage du HTML produit par le générateur (liste blanche stricte)
# ---------------------------------------------------------------------------
ALLOWED = {'p', 'h3', 'ul', 'ol', 'li', 'strong', 'em', 'a', 'br', 'blockquote',
           'table', 'thead', 'tbody', 'tr', 'th', 'td'}
VOID = {'br'}


class Sanitizer(HTMLParser):
    def __init__(self, internal_ok):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.stack = []
        self.internal_ok = internal_ok
        self.dropped_links = []

    def handle_starttag(self, tag, attrs):
        if tag not in ALLOWED:
            return
        if tag == 'a':
            href = dict(attrs).get('href', '') or ''
            href = href.strip()
            if href.startswith(BASE):
                href = href[len(BASE):] or '/'
            if href.startswith('/'):
                path = href.split('#')[0].rstrip('/') or '/'
                if path not in self.internal_ok:
                    self.dropped_links.append(href)
                    self.stack.append('a-dropped')
                    return
                self.out.append(f'<a href="{esc(path)}">')
            elif href.startswith('https://'):
                self.out.append(f'<a href="{esc(href)}" rel="noopener" target="_blank">')
            else:
                self.stack.append('a-dropped')
                return
            self.stack.append('a')
            return
        if tag in VOID:
            self.out.append(f'<{tag}>')
            return
        self.out.append(f'<{tag}>')
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag not in ALLOWED or tag in VOID:
            return
        # ferme proprement jusqu'à la balise correspondante
        if tag == 'a' and self.stack and self.stack[-1] == 'a-dropped':
            self.stack.pop()
            return
        if tag in self.stack:
            while self.stack:
                t = self.stack.pop()
                if t != 'a-dropped':
                    self.out.append(f'</{t}>')
                if t == tag:
                    break

    def handle_data(self, data):
        self.out.append(html.escape(data, quote=False))

    def result(self):
        while self.stack:
            t = self.stack.pop()
            if t != 'a-dropped':
                self.out.append(f'</{t}>')
        return ''.join(self.out)


def sanitize(fragment, internal_ok):
    s = Sanitizer(internal_ok)
    s.feed(fragment or '')
    s.close()
    return s.result(), s.dropped_links


def plain(fragment):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', fragment or ''))).strip()


# ---------------------------------------------------------------------------
# Chargement
# ---------------------------------------------------------------------------
def load_articles():
    d = p('content', 'articles')
    arts = []
    for name in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if name.endswith('.json'):
            with open(os.path.join(d, name), encoding='utf-8') as fh:
                a = json.load(fh)
            a.setdefault('updated', a['date'])
            arts.append(a)
    arts.sort(key=lambda a: (a['date'], a['slug']), reverse=True)
    return arts


def internal_targets(articles):
    ok = set(PAGES_SITE) | {'/blog'}
    ok |= {'/blog/' + a['slug'] for a in articles}
    return ok


def word_count(a):
    txt = plain(a.get('intro_html', '')) + ' ' + ' '.join(
        s['h2'] + ' ' + plain(s['html']) for s in a['sections']) + ' ' + ' '.join(
        f['q'] + ' ' + plain(f['a']) for f in a.get('faq', []))
    return len(txt.split())


# ---------------------------------------------------------------------------
# Rendu
# ---------------------------------------------------------------------------
def shell():
    with open(p('scripts', 'templates', 'shell.html'), encoding='utf-8') as fh:
        return fh.read()


def form_html():
    with open(p('scripts', 'templates', 'form.html'), encoding='utf-8') as fh:
        return fh.read()


def og_tags(url, title, desc, image, kind='article', published=None):
    t = (f'<meta property="og:type" content="{kind}">\n<meta property="og:site_name" content="Ombrière Solaire Parking">\n'
         f'<meta property="og:locale" content="fr_FR">\n<meta property="og:url" content="{esc(url)}">\n'
         f'<meta property="og:title" content="{esc(title)}">\n<meta property="og:description" content="{esc(desc)}">\n'
         f'<meta property="og:image" content="{esc(image)}">\n<meta name="twitter:card" content="summary_large_image">\n')
    if published:
        t += f'<meta property="article:published_time" content="{published}">\n'
    return t


def fill(tpl, **kw):
    for k, v in kw.items():
        tpl = tpl.replace('{{' + k + '}}', v)
    assert '{{' not in tpl, 'champ de gabarit non rempli'
    return tpl


FAQ_ITEM = ('<div class="faq-item{open}">\n      <button class="faq-btn" onclick="toggleFaq(this)" aria-expanded="{exp}">\n'
            '        <span>{q}</span>\n        <svg class="faq-chevron" width="20" height="20" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg>\n'
            '      </button>\n      <div class="faq-answer"><p>{a}</p></div>\n    </div>')

CTA_BOX = ('<div class="cta-box"><strong>Votre parking est-il concerné ?</strong>'
           '<p>Décrivez votre site en une minute : un installateur partenaire vérifie l\'obligation, la faisabilité '
           'et les modes de financement. Étude gratuite et sans engagement.</p>'
           '<a href="#devis" class="btn btn-sun">Recevoir mon étude gratuite</a></div>')


def render_article(a, articles, ok):
    url = f"{BASE}/blog/{a['slug']}"
    intro, d1 = sanitize(a['intro_html'], ok)
    body, dropped = [], list(d1)
    for i, s in enumerate(a['sections']):
        h, d = sanitize(s['html'], ok)
        dropped += d
        body.append(f'<h2>{esc(s["h2"])}</h2>\n{h}')
        if i == 1:
            body.append(CTA_BOX)
    faq = [(esc(f['q']), sanitize(f['a'], set())[0]) for f in a.get('faq', [])]
    minutes = max(3, math.ceil(word_count(a) / 220))
    related = [x for x in a.get('related', []) if x in ok and x != '/blog/' + a['slug']][:4]
    others = [x for x in articles if x['slug'] != a['slug']][:3]
    links = ''.join(f'<a href="{esc(u)}" class="link-card">{esc(PAGES_SITE.get(u, u))}</a>' for u in related if u in PAGES_SITE)
    links += ''.join(f'<a href="/blog/{esc(x["slug"])}" class="link-card">{esc(x["h1"])}</a>' for x in others)
    main = f"""<section class="post-hero">
  <div class="post-hero-inner">
    <span class="post-tag">{esc(a.get('category', 'Guide'))}</span>
    <h1>{esc(a['h1'])}</h1>
    <p class="post-meta">Publié le <time datetime="{a['date']}">{date_fr(a['date'])}</time> · {minutes} min de lecture</p>
  </div>
</section>
<article class="content post">
<div class="lead">{intro}</div>
{chr(10).join(body)}
</article>
{form_html()}"""
    if faq:
        items = ''.join(FAQ_ITEM.format(open=' open' if i == 0 else '', exp='true' if i == 0 else 'false', q=q, a=ans)
                        for i, (q, ans) in enumerate(faq))
        main += f"""<section class="section alt">
  <div class="wrap">
    <div class="s-head center"><h2>Questions fréquentes</h2></div>
    <div class="faq-list">{items}</div>
  </div>
</section>
"""
    if links:
        main += f"""<section class="links">
  <div class="wrap">
    <h3>À lire aussi</h3>
    <div class="links-grid">{links}</div>
  </div>
</section>
"""
    graph = [
        {'@type': 'Organization', '@id': ORG_ID, 'name': 'Ombrière Solaire Parking', 'url': BASE, 'telephone': '+33647326572',
         'logo': BASE + '/apple-touch-icon.png'},
        {'@type': 'BlogPosting', 'headline': a['h1'], 'description': a['meta_description'], 'datePublished': a['date'],
         'dateModified': a['updated'], 'inLanguage': 'fr-FR', 'mainEntityOfPage': url, 'url': url,
         'image': a.get('image', DEFAULT_IMAGE), 'author': {'@id': ORG_ID}, 'publisher': {'@id': ORG_ID},
         'keywords': a.get('keyword', '')},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Accueil', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': BASE + '/blog'},
            {'@type': 'ListItem', 'position': 3, 'name': a['h1'], 'item': url}]},
    ]
    if faq:
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': html.unescape(q), 'acceptedAnswer': {'@type': 'Answer', 'text': plain(ans)}}
            for q, ans in faq]})
    page = fill(shell(),
                TITLE=esc(a['title']), DESC=esc(a['meta_description']), CANONICAL=url,
                OG=og_tags(url, a['title'], a['meta_description'], a.get('image', DEFAULT_IMAGE), 'article', a['date']),
                JSONLD=json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1),
                BREADCRUMB=f'<a href="/">Accueil</a><span>›</span><a href="/blog">Blog</a><span>›</span>{esc(a["h1"])}',
                MAIN=main)
    return page, dropped


def render_index(articles):
    url = BASE + '/blog'
    title = 'Blog ombrières solaires de parking : guides et loi APER'
    desc = ("Guides pratiques sur les ombrières photovoltaïques de parking : obligation loi APER, surface, "
            "financement, raccordement, recharge et montage de projet.")
    cards = ''.join(f"""<a href="/blog/{esc(a['slug'])}" class="blog-card">
  <span class="blog-card-tag">{esc(a.get('category', 'Guide'))}</span>
  <h2>{esc(a['h1'])}</h2>
  <p>{esc(a['excerpt'])}</p>
  <span class="blog-card-meta"><time datetime="{a['date']}">{date_fr(a['date'])}</time><span class="blog-card-link">Lire l'article →</span></span>
</a>
""" for a in articles)
    main = f"""<section class="blog-hero">
  <div class="blog-hero-inner">
    <span class="eyebrow"><i></i>Guides &amp; réglementation</span>
    <h1>Le blog des ombrières solaires de parking</h1>
    <p>Loi APER, surface concernée, financement, raccordement, recharge : des guides concrets pour préparer le projet d'ombrières de votre parking.</p>
  </div>
</section>
<div class="blog-list">
{cards}</div>
<section class="final">
  <h2>Votre parking est concerné ?</h2>
  <p>Étude gratuite et sans engagement par un installateur partenaire, partout en France.</p>
  <div class="ctas"><a href="/devis-ombriere-solaire" class="btn btn-sun btn-lg">Demander mon étude gratuite</a></div>
</section>
"""
    graph = [
        {'@type': 'Organization', '@id': ORG_ID, 'name': 'Ombrière Solaire Parking', 'url': BASE},
        {'@type': 'Blog', 'name': 'Le blog des ombrières solaires de parking', 'url': url, 'inLanguage': 'fr-FR', 'publisher': {'@id': ORG_ID},
         'blogPost': [{'@type': 'BlogPosting', 'headline': a['h1'], 'url': f"{BASE}/blog/{a['slug']}", 'datePublished': a['date']}
                      for a in articles]},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Accueil', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': url}]},
    ]
    return fill(shell(), TITLE=esc(title), DESC=esc(desc), CANONICAL=url,
                OG=og_tags(url, title, desc, DEFAULT_IMAGE, 'website'),
                JSONLD=json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1),
                BREADCRUMB='<a href="/">Accueil</a><span>›</span>Blog', MAIN=main)


def update_sitemap(articles):
    path = p('sitemap.xml')
    with open(path, encoding='utf-8') as fh:
        s = fh.read()
    s = re.sub(r'\s*<url>\s*<loc>' + re.escape(BASE) + r'/blog[^<]*</loc>.*?</url>', '', s, flags=re.S)
    last = articles[0]['date'] if articles else date.today().isoformat()
    def entry(loc, mod, freq, prio):
        return (f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{mod}</lastmod>\n'
                f'    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>')
    entries = [entry(f'{BASE}/blog', last, 'weekly', '0.7')]
    entries += [entry(f'{BASE}/blog/{a["slug"]}', a['updated'], 'monthly', '0.6') for a in articles]
    s = s.rstrip()
    s = s.replace('</urlset>', '\n'.join(entries) + '\n</urlset>') + '\n'
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(s)


def build():
    articles = load_articles()
    if not articles:
        print('Aucun article : rien à construire.')
        return []
    ok = internal_targets(articles)
    problems = []
    for a in articles:
        page, dropped = render_article(a, articles, ok)
        if dropped:
            problems.append(f"{a['slug']} : liens internes retirés (pages inexistantes) : {dropped}")
        out = p('blog', a['slug'])
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8') as fh:
            fh.write(page)
    with open(p('blog', 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(render_index(articles))
    update_sitemap(articles)
    for line in problems:
        print('Avertissement :', line)
    print(f'{len(articles)} article(s) construits, page /blog et sitemap à jour.')
    return articles


if __name__ == '__main__':
    build()
    sys.exit(0)
