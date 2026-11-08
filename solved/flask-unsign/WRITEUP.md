# flask-unsign (web, easy)

**ID :** 238  
**Points :** 150  
**Auteurs :** hibris, Clawd  
**Fichiers :** `app.py`, `session_cookie.txt`  
**Format :** `NCTF{...}`

Un panneau membres est fourni en source, avec un cookie de session capturé sur une inscription normale. Le panneau admin affiche un flag. Les inscriptions publiques restent au rôle `guest`.

Routes :

- `GET /signup` ouvre une session invité
- `GET /admin/flag` est réservé aux admins

Rien n'est en ligne. Tout est dans les fichiers.

## Méthode

`session_cookie.txt` est un cookie Flask signé. Décode, il contient `uid=7`, `role=guest`, `display=guest`. La clé de signature est en clair dans `app.py` :

`s3cr3t-flask-signing-key-do-not-share-8842`

`/admin/flag` refuse tant que `session["role"]` n'est pas `admin`. Le flag lui-même n'est pas en clair : `unseal_flag()` déchiffre `SEALED_FLAG_HEX`.

La clé du sceau est `SHA-256(secret_key UTF-8 + b"|panel-seal")`. Le flux est `SHA-256(clé || compteur uint32 big-endian)`, à partir de 0. Le clair est le XOR de ce flux avec le chiffré.

## Flag

`NCTF{itsdangerous_secret_key_resign_admin_session}`
