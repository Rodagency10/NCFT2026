# STATUS — boazak--evala (web medium, race condition) — EN ATTENTE

**Bloqué sur la découverte de l'endpoint d'achat.** Tout le reste est prêt.

## Vulnérabilité
TOCTOU / race condition : le handler d'achat vérifie le stock, `time.sleep(0.1)`,
puis décrémente (non atomique). Survente (stock < 0) via requêtes concurrentes →
le flag apparaît quand le stock passe sous zéro.

## Routes trouvées
- `GET /` → `{"message":"FlashSale API","stock":5}`
- `POST /login`, `POST /register` (racine) → JWT (flask-jwt-extended)
- `GET /api/stock` → `{"stock":5}` (Allow: GET/HEAD/OPTIONS seulement)
- **Endpoint d'achat : INCONNU** (le blocage)

## Testé sans succès (GET+POST, authentifié et non, 2 instances)
/buy /api/buy /purchase /api/purchase /order /api/order /api/orders /checkout
/api/checkout /sell /api/sell + variantes FR (/api/acheter /achat /commander
/vente /panier) + thématiques (/api/flashsale /flash /sale /evala /lutte /course)
+ paramètre d'item (/api/items/1/buy, /api/buy/1...) + OpenAPI/docs/swagger +
racine DRF /api/ (OPTIONS/GET auth) + common.txt (root et /api/). Tout 404.
Pas de frontend HTML/JS (API JSON pure). Raft complet = trop lent (~80 min).

## Pour reprendre
- Obtenir **la source** du challenge (app.py / .zip) → le nom de l'endpoint y est.
- Puis : `py race.py <BUY_PATH>` (voir race.py — crée un compte, prend un JWT,
  tire N=30 POST concurrents, guette `NCTF{`). Ajuster B= (URL instance fraîche)
  et BUY_BODY si besoin.
