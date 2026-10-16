# Blog automatique — mode d'emploi

Chaque lundi vers 8 h (avec des tentatives de rattrapage dans la journée et le mardi matin, si GitHub saute un lancement), GitHub Actions (`.github/workflows/article-du-lundi.yml`) :

1. prend le premier sujet `"statut": "à faire"` de `content/plan.json` ;
2. fait rédiger l'article par l'API Claude (`scripts/generate_article.py`) ;
3. contrôle la qualité : longueur, liens internes valides, aucun montant en euros, aucun
   pourcentage ou statistique chiffrée, aucun faux témoignage, pas de « nous installons / nos chantiers ».
   En cas d'échec, une seconde version est demandée ; si elle échoue aussi, rien n'est publié
   et GitHub vous envoie un e-mail ;
4. construit la page dans le gabarit du site, met à jour `/blog` et `sitemap.xml` (`scripts/blog.py`) ;
5. publie (commit + push) : Vercel déploie automatiquement ;
6. signale la nouvelle page à Bing via IndexNow.

## Réglages

- **Clé API** : secret GitHub `ANTHROPIC_API_KEY` (Settings → Secrets and variables → Actions).
- **Modèle** (facultatif) : variable GitHub `CLAUDE_MODEL` (défaut : `claude-sonnet-5-5`).
- **Publier tout de suite** : onglet Actions → « Article du lundi » → « Run workflow ».

## Ajouter des sujets

Ajoutez des entrées à la fin de `content/plan.json` :

```json
{"slug": "mon-sujet", "sujet": "Titre du sujet", "mot_cle": "mot-clé principal",
 "categorie": "Guide", "angle": "Ce que l'article doit expliquer",
 "liens": ["/obligation-ombriere-parking"], "statut": "à faire"}
```

Les liens autorisés sont les pages listées dans `PAGES_SITE` (`scripts/blog.py`), `/blog` et les
articles déjà publiés. Si vous créez une nouvelle page sur le site, ajoutez-la à `PAGES_SITE`.

## Chiffres et réglementation

Les articles ne citent aucun montant en euros ni pourcentage : ils expliquent ce qui fait varier
le budget et renvoient à l'étude. Les seuls faits réglementaires autorisés figurent dans la « fiche
réglementaire » du prompt (`SYSTEM` dans `scripts/generate_article.py`) : mettez-la à jour si la loi
évolue (seuils, échéances, décrets).

## Pages fixes

Les pages du site (accueil, loi APER, financement, pages cibles, devis, pages légales) sont générées
par `scripts/pages.py`. Modifiez le texte dans ce fichier puis lancez `python3 scripts/pages.py`
et `python3 scripts/blog.py`.

## Corriger un article publié

Modifiez `content/articles/<slug>.json` (ajoutez `"updated": "AAAA-MM-JJ"`), puis lancez
`python3 scripts/blog.py` et publiez. Les fichiers de `blog/` sont régénérés : ne les modifiez pas à la main.
