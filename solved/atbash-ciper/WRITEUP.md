# atbash-cipher

## Challenge

**Points :** 25  
**Catégorie :** warmup / classical / atbash  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `secret (1).txt`  
**Format du flag :** `NCTF{...}`

> `secret.txt` was made by mirroring the alphabet: A swaps with Z, B with Y, and so on. Mirror it back and read the flag.

## Résolution

Le texte chiffré est :

```
MXGU{zgyzhs_nriilih_gsv_zokszyvg}
```

L’Atbash remplace chaque lettre par son symétrique dans l’alphabet : `A↔Z`, `B↔Y`, `C↔X`, … `M↔N`. La casse est conservée, et les caractères hors alphabet (`{`, `}`, `_`) restent inchangés.

La position miroir d’une lettre est `dernière - (position - première)` :

- majuscule : `'Z' - (c - 'A')`
- minuscule : `'z' - (c - 'a')`

| Chiffré | Clair |
|---------|-------|
| `MXGU` | `NCTF` |
| `zgyzhs` | `atbash` |
| `nriilih` | `mirrors` |
| `gsv` | `the` |
| `zokszyvg` | `alphabet` |

## Flag

```
NCTF{atbash_mirrors_the_alphabet}
```
