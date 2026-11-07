# alias-slip

## Challenge

**ID :** 212  
**Catégorie :** sysadmin  
**Points :** 150  
**Auteurs :** hibris, Clawd  
**Fichiers :** `nginx.conf`, `index.html`, `logo.txt`, `settings.py.bak`  
**Format du flag :** `NCTF{nginx_alias_offbyslash_<token>}`

> Un site nginx : la config et l'arbre servi. Un répertoire privé doit rester inaccessible, mais une sauvegarde oubliée y contient le token admin. Aucun fichier ne contient le flag tel quel. Lire la config, trouver le passage, récupérer le token.

## Résolution

`location /assets` n'a pas de slash final, alors que `alias /srv/kekeli/public/assets/` en a un. Nginx recolle le reste de l'URI derrière l'alias. La requête `/assets../config/settings.py.bak` est donc lue comme :

`/srv/kekeli/public/assets/../config/settings.py.bak`

soit `/srv/kekeli/public/config/settings.py.bak`. Cette URI matche `location /assets`, pas `location /config`, donc le `deny all` ne s'applique pas.

La sauvegarde contient `ADMIN_API_TOKEN = "a7f3c0de91"`.

## Flag

```
NCTF{nginx_alias_offbyslash_a7f3c0de91}
```
