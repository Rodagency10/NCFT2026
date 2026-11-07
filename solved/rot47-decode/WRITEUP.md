# rot47-decode

## Challenge

**Points :** 25  
**Catégorie :** warmup / classical / rot47  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `secret.txt`  
**Format du flag :** `NCTF{...}`

> `secret.txt` is a jumble of visible punctuation and characters. It is the flag with every printable symbol rotated by a fixed amount across a 94-character range. Undo the rotation and read the flag.

## Résolution

Le texte chiffré est :

```
}r%uLC@Ecf0D9:7ED0E9608=JA9DN
```

ROT47 travaille sur les 94 caractères imprimables ASCII, de `!` (33) à `~` (126). Chaque symbole est décalé de 47 positions dans cet intervalle. Comme 47 + 47 = 94, appliquer ROT47 une seconde fois revient au texte d’origine.

Pour un code `c` entre 33 et 126 :

```
((c - 33 + 47) % 94) + 33
```

## Flag

```
NCTF{rot47_shifts_the_glyphs}
```
