#!/usr/bin/env python3
"""Signale les nouvelles pages à Bing et aux moteurs IndexNow (Google ne l'utilise pas)."""
import json, os, sys, urllib.request
KEY = 'f011b8376f9c8dc9e85d3b51e4875f96'
HOST = 'www.ombriere-solaire-parking.fr'
slug = os.environ.get('SLUG') or (sys.argv[1] if len(sys.argv) > 1 else '')
urls = [f'https://{HOST}/blog', f'https://{HOST}/sitemap.xml'] + ([f'https://{HOST}/blog/{slug}'] if slug else [])
body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': f'https://{HOST}/{KEY}.txt', 'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body, method='POST',
                             headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print('IndexNow :', r.status, urls)
except Exception as e:  # non bloquant
    print('IndexNow non envoyé :', e)
