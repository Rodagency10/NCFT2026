# base32-decode

## Challenge

**Points :** 32  
**Catégorie :** warmup / encoding / base32  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `secret.txt`  
**Format du flag :** `NCTF{...}`

> `secret.txt` holds only UPPERCASE letters A–Z and the digits 2–7, ending in a run of `=` padding. Decode it and read the flag.

## Résolution

Le contenu est une chaîne Base32 (alphabet `A–Z` et `2–7`) :

```
JZBVIRT3MJQXGZJTGJPXK43FONPW233SMVPWYZLUORSXE435
```

La chaîne fait 48 caractères, un multiple de 8, donc aucun `=` de padding n’est présent dans ce fichier. Chaque symbole encode 5 bits ; regroupés par octets, ils donnent le texte clair.

## Flag

```
NCTF{base32_uses_more_letters}
```
