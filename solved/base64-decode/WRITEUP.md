# base64-decode

## Challenge

**Catégorie :** warmup / encoding / base64  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `secret (2).txt`  
**Format du flag :** `NCTF{...}`

> `secret.txt` est une chaîne Base64. La décoder et lire le flag.

## Résolution

Le fichier contient une seule chaîne Base64, alphabet `A–Z`, `a–z`, `0–9`, `+`, `/`, avec un `=` de padding :

```
TkNURntiYXNlNjRfaXNfbm90X2VuY3J5cHRpb259
```

Base64 regroupe les bits d’entrée par 6. Ici le décodage standard (`Buffer.from(s, "base64")`) redonne directement le texte clair. Le contenu du flag le rappelle : Base64 est un encodage, pas un chiffrement.

## Flag

```
NCTF{base64_is_not_encryption}
```
