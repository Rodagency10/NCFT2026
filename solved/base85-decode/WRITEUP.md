# base85-decode

## Challenge

**Points :** 29  
**Catégorie :** warmup / encoding / base85  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `secret (5).txt`  
**Format du flag :** `NCTF{...}`

> `secret.txt` looks like line noise: a dense mix of letters, digits and punctuation, but no spaces. It packs binary into printable ASCII more tightly than the usual suspects. Decode it and read the flag.

## Résolution

Le fichier contient une seule chaîne, sans espaces :

```
PD4~idu3^7XmojBW@&b1UvP41ZggQ{Y-L|#Xkl`5eE
```

Ce n’est pas de l’Ascii85 Adobe (`!` à `u`) : des caractères comme `` ` ``, `{`, `|` et `~` sortent de cet alphabet. C’est du Base85 RFC 1924, le même que `base64.b85decode` en Python. Son alphabet de 85 symboles est :

```
0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~
```

Cinq caractères codent quatre octets : chaque symbole est un chiffre en base 85, et la valeur sur 32 bits est redécoupée en quatre octets. La chaîne fait 42 caractères (8 groupes de 5, plus 2), donc le dernier groupe est complété avant de ne garder que les octets utiles.

## Flag

```
NCTF{eighty_five_printable_chars}
```
