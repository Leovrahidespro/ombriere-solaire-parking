#!/usr/bin/env python3
"""Génère l'article de la semaine avec l'API Claude, puis reconstruit le blog.

1. Prend le premier sujet « à faire » de content/plan.json
2. Demande l'article à l'API Claude (sortie structurée via un outil imposé)
3. Contrôle la qualité (longueur, structure, pas de montants en euros ni de statistiques, pas de faux témoignages)
   et redemande une fois avec les corrections si nécessaire
4. Enregistre content/articles/<slug>.json, marque le sujet « publié » et lance scripts/blog.py

Variables d'environnement :
  ANTHROPIC_API_KEY  (obligatoire)
  MODEL              (facultatif, défaut : claude-sonnet-5-5)
  DRY_RUN=1          (facultatif : n'écrit rien, affiche le résultat)
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blog  # noqa: E402

API_URL = os.environ.get('ANTHROPIC_API_URL', 'https://api.anthropic.com/v1/messages')
MODEL = os.environ.get('MODEL') or 'claude-sonnet-5-5'
PLAN = blog.p('content', 'plan.json')


def fail(msg):
    """Arrête l'exécution avec un message visible dans le résumé GitHub Actions."""
    print(f"::error title=Article non publié::{msg.replace(chr(10), ' | ')}")
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a', encoding='utf-8') as fh:
            fh.write(f"### Article non publié\n\n{msg}\n")
    sys.exit(msg)


TOOL = {
    'name': 'publier_article',
    'description': "Enregistre l'article de blog terminé.",
    'input_schema': {
        'type': 'object',
        'required': ['title', 'meta_description', 'h1', 'excerpt', 'intro_html', 'sections', 'faq', 'related'],
        'properties': {
            'title': {'type': 'string', 'description': 'Balise title SEO, 45 à 60 caractères, contient le mot-clé.'},
            'meta_description': {'type': 'string', 'description': '130 à 155 caractères, mot-clé + bénéfice concret.'},
            'h1': {'type': 'string', 'description': "Titre principal de l'article (peut être plus long que le title)."},
            'excerpt': {'type': 'string', 'description': 'Résumé de 100 à 160 caractères pour la carte du blog.'},
            'intro_html': {'type': 'string', 'description': 'Introduction en 1 ou 2 balises <p>.'},
            'sections': {'type': 'array', 'minItems': 5, 'maxItems': 8, 'items': {
                'type': 'object', 'required': ['h2', 'html'],
                'properties': {'h2': {'type': 'string'}, 'html': {'type': 'string', 'description': 'Contenu HTML de la section.'}}}},
            'faq': {'type': 'array', 'minItems': 3, 'maxItems': 5, 'items': {
                'type': 'object', 'required': ['q', 'a'],
                'properties': {'q': {'type': 'string'}, 'a': {'type': 'string', 'description': 'Réponse en texte simple, 2 à 4 phrases.'}}}},
            'related': {'type': 'array', 'items': {'type': 'string'}, 'description': 'URL internes recommandées en fin d’article (2 à 4).'},
        },
    },
}

SYSTEM = """Tu es rédacteur web spécialisé en photovoltaïque et en réglementation des parcs de stationnement pour le site ombriere-solaire-parking.fr (Ombrière Solaire Parking).
Le site met en relation des propriétaires et gestionnaires de parkings (grandes surfaces, entreprises, sites logistiques et industriels, collectivités, établissements publics, copropriétés, bailleurs) avec des installateurs d'ombrières photovoltaïques partenaires, partout en France. Le lecteur est un décideur (directeur de site, responsable patrimoine ou services techniques, élu, gestionnaire) : il veut comprendre ses obligations et préparer un projet, sans jargon inutile ni discours commercial.

Fiche réglementaire de référence (seuls faits chiffrés autorisés, à formuler prudemment) :
- Article 40 de la loi n° 2023-175 du 10 mars 2023 (loi APER) : obligation d'ombrières intégrant un procédé de production d'énergie renouvelable sur les parcs de stationnement extérieurs de plus de 1 500 m², sur au moins la moitié de leur surface.
- Échéances pour les parkings non concédés : 1er juillet 2026 au-delà de 10 000 m², 1er juillet 2028 de 1 500 à 10 000 m². Parkings en concession ou délégation de service public : à la conclusion ou au renouvellement du contrat.
- Loi du 26 novembre 2025 de simplification de l'urbanisme (loi Huwart) : l'ombrage peut combiner ombrières photovoltaïques et ombrage végétal, avec une part minimale de photovoltaïque. Un décret de 2026 prévoit des délais supplémentaires sous conditions pour les projets engagés.
- Exemptions possibles et justifiées : contraintes techniques, de sécurité, architecturales, patrimoniales ou environnementales ; coût économiquement inacceptable ; parking déjà ombragé par des arbres sur plus de la moitié de sa surface ; parking appelé à disparaître dans une opération d'aménagement.
- Sanction : amende annuelle tant que le parking n'est pas conforme (ne cite aucun montant).
Ces textes sont récents : rappelle quand c'est utile qu'il faut vérifier sa situation au regard des textes en vigueur.

Règles impératives :
- Français correct avec tous les accents, vouvoiement, phrases courtes et claires.
- 1 100 à 1 500 mots au total. 5 à 7 sections avec un intertitre h2 explicite. Des listes quand c'est utile.
- Balises autorisées dans le HTML : p, h3, ul, ol, li, strong, em, a, table, thead, tbody, tr, th, td, blockquote. Pas de h1 ni de h2 dans le HTML (les h2 sont dans le champ dédié), pas d'attributs autres que href.
- Intègre 2 à 4 liens internes pertinents, uniquement vers les URL de la liste fournie, avec un texte d'ancre naturel.
- AUCUN montant en euros, aucun prix au kWc ou au m², aucun tarif d'achat, aucun montant d'aide ou d'amende ; aucun pourcentage (écris « la moitié » plutôt que « 50 % ») ni statistique. Explique ce qui fait varier les coûts et les revenus, et renvoie à l'étude gratuite.
- N'invente aucun autre chiffre, seuil, date, numéro de texte ni nom d'organisme : si tu n'es pas sûr, reste général.
- Ne cite aucun témoignage, client, chantier, réalisation ni entreprise réelle : le site n'en publie pas.
- Ne parle pas à la place de l'installateur (« nous installons », « nos techniciens », « nos chantiers ») : parle des installateurs partenaires ou de l'installateur en général.
- Pas de promesse de résultat ni de pression commerciale. Une seule mention discrète de l'étude gratuite suffit (un encadré d'appel à l'action est ajouté automatiquement).
- Le mot-clé principal apparaît dans le title, le h1, l'introduction et 2 ou 3 fois dans le texte, toujours intégré naturellement dans une phrase correcte : décline-le plutôt que de le recopier tel quel, et ne le mets jamais entre guillemets.
Réponds uniquement en appelant l'outil publier_article."""

BANNED = [
    (r'\d[\d\s.,\u00a0]*\s*(?:€|euros?\b|EUR\b|k€|M€)', 'montant en euros'),
    (r'\d+(?:[.,]\d+)?\s*(?:c€|cts?|centimes?)\s*(?:/|par)\s*kWh', 'tarif en centimes par kWh'),
    (r'\d+(?:[.,]\d+)?\s*%', 'pourcentage ou statistique chiffrée'),
    (r'témoign', 'témoignage'),
    (r'\bnos (?:techniciens|poseurs|clients|chantiers|réalisations|installations|équipes)\b', 'formulation installateur / clients'),
    (r'\bnous (?:installons|posons|réalisons|avons (?:installé|réalisé|posé))\b', 'formulation installateur'),
]


def today_paris():
    # Europe/Paris sans dépendance : UTC+1 (hiver) ou UTC+2 (été) — la date suffit ici
    now = datetime.now(timezone.utc) + timedelta(hours=2)
    return now.date().isoformat()


def call_api(messages):
    key = os.environ.get('ANTHROPIC_API_KEY')
    if not key:
        fail("ANTHROPIC_API_KEY manquant : ajoutez-le dans les secrets GitHub du dépôt.")
    body = json.dumps({
        'model': MODEL, 'max_tokens': 8000, 'system': SYSTEM, 'messages': messages,
        'tools': [TOOL], 'tool_choice': {'type': 'auto'},
    }).encode('utf-8')
    for attempt in range(4):
        req = urllib.request.Request(API_URL, data=body, method='POST', headers={
            'x-api-key': key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.loads(r.read())
            for block in data.get('content', []):
                if block.get('type') == 'tool_use':
                    return block['input'], data
            # Le modèle a répondu en texte : on lui redemande d'utiliser l'outil
            if attempt < 3:
                messages = messages + [{'role': 'assistant', 'content': data.get('content') or [{'type': 'text', 'text': '…'}]},
                                       {'role': 'user', 'content': "Envoie maintenant l'article complet en appelant l'outil publier_article."}]
                body = json.dumps({'model': MODEL, 'max_tokens': 8000, 'system': SYSTEM, 'messages': messages,
                                   'tools': [TOOL], 'tool_choice': {'type': 'auto'}}).encode('utf-8')
                continue
            fail('Le modèle n’a pas renvoyé l’article dans le format attendu.')
        except urllib.error.HTTPError as e:
            detail = e.read().decode('utf-8', 'replace')[:500]
            if e.code in (429, 500, 502, 503, 529) and attempt < 3:
                time.sleep(20 * (attempt + 1))
                continue
            fail(f'Erreur API {e.code} : {detail}')
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < 3:
                time.sleep(20 * (attempt + 1))
                continue
            fail(f'API injoignable : {e}')


def check(art, ok_links):
    problems = []
    text = ' '.join([art['intro_html']] + [s['h2'] + ' ' + s['html'] for s in art['sections']] +
                    [f['q'] + ' ' + f['a'] for f in art['faq']])
    words = len(blog.plain(text).split())
    if words < 900:
        problems.append(f"article trop court ({words} mots, minimum 1 100 attendu)")
    if not 30 <= len(art['title']) <= 65:
        problems.append(f"title de {len(art['title'])} caractères (45 à 60 attendus)")
    if not 110 <= len(art['meta_description']) <= 160:
        problems.append(f"meta description de {len(art['meta_description'])} caractères (130 à 155 attendus)")
    for pat, label in BANNED:
        m = re.search(pat, text, re.I)
        if m:
            problems.append(f"contenu interdit ({label}) : « {m.group(0)} »")
    if re.search(r'<h[12]\b', text, re.I):
        problems.append('h1/h2 présents dans le HTML')
    links = set(re.findall(r'href="([^"]+)"', text))
    internal = {l for l in links if l.startswith('/')}
    if len(internal & ok_links) < 2:
        problems.append('moins de 2 liens internes valides')
    if internal - ok_links:
        problems.append(f"liens vers des pages inexistantes : {sorted(internal - ok_links)}")
    return problems, words


def deja_publie_cette_semaine():
    """Vrai si un article est déjà paru cette semaine (lundi à dimanche, heure de Paris)."""
    today = datetime.fromisoformat(today_paris()).date()
    lundi = today - timedelta(days=today.weekday())
    return any(lundi.isoformat() <= a['date'] <= today.isoformat() for a in blog.load_articles())


def main():
    # Lancements planifiés multiples : on ne publie qu'une fois par semaine.
    # Un lancement manuel (« Run workflow ») publie toujours.
    if os.environ.get('GITHUB_EVENT_NAME') == 'schedule' and deja_publie_cette_semaine():
        print('Article de la semaine déjà publié : rien à faire.')
        return
    with open(PLAN, encoding='utf-8') as fh:
        plan = json.load(fh)
    todo = [t for t in plan if t.get('statut') != 'publié']
    if not todo:
        fail('Plus aucun sujet « à faire » dans content/plan.json : ajoutez des sujets.')
    topic = todo[0]
    articles = blog.load_articles()
    if any(a['slug'] == topic['slug'] for a in articles):
        fail(f"Le slug {topic['slug']} existe déjà.")
    ok_links = blog.internal_targets(articles)
    pages = '\n'.join(f'- {u} : {d}' for u, d in blog.PAGES_SITE.items())
    posts = '\n'.join(f"- /blog/{a['slug']} : {a['h1']}" for a in articles) or '- (aucun)'
    prompt = f"""Rédige l'article de blog suivant.

Sujet : {topic['sujet']}
Mot-clé principal : {topic['mot_cle']}
Angle à traiter : {topic['angle']}
Liens internes à privilégier : {', '.join(topic.get('liens', []))}

Pages du site (seules URL internes autorisées) :
{pages}

Articles déjà publiés (évite de répéter leur contenu ; tu peux y faire un lien si c'est pertinent) :
{posts}"""
    messages = [{'role': 'user', 'content': prompt}]
    art, raw = call_api(messages)
    problems, words = check(art, ok_links)
    if problems:
        print('Première version refusée :', *problems, sep='\n  - ')
        messages += [
            {'role': 'assistant', 'content': [b for b in raw['content'] if b.get('type') == 'tool_use']},
            {'role': 'user', 'content': [{'type': 'tool_result', 'tool_use_id': next(b['id'] for b in raw['content'] if b.get('type') == 'tool_use'),
                                          'is_error': True,
                                          'content': 'Article refusé. Corrige ces points et renvoie l’article complet :\n- ' + '\n- '.join(problems)}]},
        ]
        art, raw = call_api(messages)
        problems, words = check(art, ok_links)
        if problems:
            fail('Article refusé après correction, rien n’est publié :\n  - ' + '\n  - '.join(problems))
    art.update({'slug': topic['slug'], 'date': today_paris(), 'category': topic.get('categorie', 'Guide'),
                'keyword': topic['mot_cle'], 'model': MODEL})
    print(f"Article prêt : {art['h1']} ({words} mots)")
    if os.environ.get('DRY_RUN'):
        print(json.dumps(art, ensure_ascii=False, indent=1)[:3000])
        return
    with open(blog.p('content', 'articles', topic['slug'] + '.json'), 'w', encoding='utf-8') as fh:
        json.dump(art, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    topic['statut'], topic['date'] = 'publié', art['date']
    with open(PLAN, 'w', encoding='utf-8') as fh:
        json.dump(plan, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    blog.build()
    with open(os.environ.get('GITHUB_OUTPUT', os.devnull), 'a') as fh:
        fh.write(f"slug={topic['slug']}\ntitle={art['h1']}\n")
    remaining = len(todo) - 1
    if remaining <= 4:
        print(f"Attention : plus que {remaining} sujet(s) dans le planning.")


if __name__ == '__main__':
    main()
