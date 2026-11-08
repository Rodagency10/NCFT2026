# STATUS — cms-smuggle (web 500, HTTP request smuggling + cache poisoning) — EN COURS

## Cible
NovaCMS. Objectif : lire `/admin/flag` (403 `{"error":"admin only"}`) via empoisonnement de cache.

## Endpoints
- `POST /ingest` — corps brut ; réponse TOUJOURS `{"cache_poisoned":[],"ingested":true}`
  quel que soit le corps (urllib et socket brut). Corps par défaut :
  `POST /ingest\ncontent=bonjour tout le monde`
- `GET /page?p=<path>` — lit le cache (renvoyait `{"cached":null,"path":...}`).
- `GET /admin/flag` — 403 (même en socket brut).

## Écarté
- Bypass 403 par header (X-Forwarded-For/X-Real-IP/X-Internal/X-Admin = 127.0.0.1) → 403.
- Desync transport nginx↔backend : **nginx 1.27.5 rejette CL+TE ambigu (400)** → pas de CL.TE/TE.CL classique au niveau externe.
- Ingérer une requête HTTP brute (`GET /admin/flag HTTP/1.1...`) dans le corps → rien caché.

## Piste restante
Le smuggling est forcément **dans le corps `/ingest`** que le backend re-parse. Il faut
trouver le format EXACT qui fait que le backend **exécute/cache** une requête, puis
y glisser `GET /admin/flag` sans le marqueur externe qui déclenche le 403.
- Déterminer comment une page arrive dans le cache (quel format d'ingest rend `cache_poisoned` non vide).
- NB : vers la fin, `GET /page?p=/...` s'est mis à renvoyer le HTML de la console (à investiguer — cache nginx ?).
- Probablement nécessaire : **débloquer un hint** (arène ramait, fetch API en échec) pour le format d'ingestion.

Outils : `raw.py` (client TLS brut : `raw.send_raw(bytes)`).
