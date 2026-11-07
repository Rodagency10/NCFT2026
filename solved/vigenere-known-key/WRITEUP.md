# vigenere-known-key

## Challenge

**Points :** 25  
**Catégorie :** warmup / classical / vigenere  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `cipher.txt`  
**Format du flag :** `NCTF{...}`

> `cipher.txt` was enciphered with a Vigenere cipher. The key is not a secret this time — it is `WARMUP`. Only the letters were shifted; digits and punctuation were left alone. Decrypt it and read the flag.

## Résolution

Le texte chiffré est :

```
JCKR{pxceeqlt_sikt_u_zjonz_etu}
```

Vigenère répète la clé `WARMUP` sous les lettres uniquement. `{`, `}` et `_` ne consomment pas de lettre de clé. Le déchiffrement d’une lettre est :

```
(chiffre - clé + 26) % 26
```

La casse du texte chiffré est conservée. Les six premières lettres `JCKR` sous `WARM` redonnent `NCTF`, puis le corps du flag.

## Flag

```
NCTF{vigenere_with_a_known_key}
```
