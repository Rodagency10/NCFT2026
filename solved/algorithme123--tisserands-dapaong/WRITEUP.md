# algorithme123--tisserands-dapaong

## Challenge

**Points :** 250  
**Catégorie :** stego  
**Difficulté :** easy-medium  
**Auteur :** Algorithme123  
**Fichiers :** `affiche.png`, `guide-motifs.pdf`, `README_vitrine.txt`  
**Format du flag :** `NCTF{...}`

> Festival fictif Dapaong Terre & Fibres : affiche officielle + guide des motifs.
> Retrouve le message tissé destiné aux partenaires.

## Résolution

Le guide (`guide-motifs.pdf`) et le commentaire PNG fixent la lecture :

- le fil rouge, c'est le canal rouge ;
- les quatre premiers octets sont une longueur `uint32` big-endian ;
- la suite est une chaîne UTF-8 de motifs ;
- les consonnes et les chiffres sont des glyphes latins en majuscules (`n` → `N`, `b` → `B`, etc.) ;
- les voyelles sont un glyphe de l'affiche ;
- le chiffre hexa `a` reste cette voyelle, ce n'est pas la lettre `B`.

Les 39 bandes colorées sont un tissage déterministe (rouge de période 20, vert de période 25, bleu fixe à 40). Elles ne portent pas le message. Le damier `vitrine.local` non plus : le README le place hors périmètre.

Le message est dans le bit de poids faible du canal rouge, lu en ligne, bit de poids fort d'abord. Les 43 premiers octets donnent :

```
00 00 00 27
NCTF{D4P40NG_T1SS3R4NDS_29549DB55○2C}
```

`0x27` = 39 octets. Le caractère `○` (U+25CB) est le glyphe de voyelle. Les lectures avec `a` sont refusées. L'arène accepte le glyphe comme `e`, une fois tout le message passé en minuscules.

## Flag

```
NCTF{d4p40ng_t1ss3r4nds_29549db55e2c}
```
