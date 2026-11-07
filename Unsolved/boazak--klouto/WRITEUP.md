# boazak--klouto (web / SSRF, easy)

**Flag :** `NCTF{5e09d78afa6035f8592a108e}`

## Contexte
"Linkify" = service d'aperçu d'URL : `GET /api/preview?url=...` fait récupérer la
page **par le serveur**. Un panneau d'administration interne n'est accessible que
depuis le serveur lui-même et contient le flag → **SSRF** classique
(indice : « on aperçoit l'intérieur depuis l'extérieur »).

## Exploitation
1. Le endpoint `/api/preview?url=` récupère n'importe quelle URL côté serveur,
   **sans filtrage** des IP privées/localhost (les erreurs verboses de `requests`
   servaient même d'oracle de scan de ports).
2. L'admin interne écoute sur **127.0.0.1:5100** (hint 2). Ce port héberge en fait
   la même app preview (il expose `/api/preview`), avec une route interne cachée.
3. La route du flag : **`/internal/flag`**.

```
GET /api/preview?url=http://127.0.0.1:5100/internal/flag
→ {"content":"{\"flag\":\"NCTF{5e09d78afa6035f8592a108e}\"}\n","status":200}
```

## Notes
- Le conteneur bindait l'app sur un port non standard (5100) ; seuls 127.0.0.1:5100
  et les gateways Docker répondaient. Le hint 2 (port 5100) a débloqué.
- Hitter 5100 via la SSRF = self-fetch de l'app → peu de workers → fuzzing lent,
  donc faible concurrence nécessaire.
- Route trouvée par fuzz ciblé après que les noms courants (`/admin`, `/flag`,
  `/dashboard`…) aient tous renvoyé 404 : le bon chemin était `/internal/flag`.
