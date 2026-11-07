# url-encoding

## Challenge

**Points :** 25  
**Catégorie :** warmup / web / encoding  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `encoded.txt`  
**Format du flag :** `NCTF{...}`

> `encoded.txt` is a string full of `%` signs followed by two hex digits, like you would see stuffed into a web address. Decode it back to plain text and read the flag.

## Résolution

Le fichier contient :

```
NCTF%7Bpercent_encoding_for_urls%7D
```

`%HH` est le percent-encoding : `HH` est le code ASCII du caractère en hexadécimal. Ici seules les accolades sont encodées.

| Séquence | Hex | Caractère |
|----------|-----|-----------|
| `%7B` | 0x7B | `{` |
| `%7D` | 0x7D | `}` |

## Flag

```
NCTF{percent_encoding_for_urls}
```
