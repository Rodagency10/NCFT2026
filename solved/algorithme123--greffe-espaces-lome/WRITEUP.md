# algorithme123--greffe-espaces-lome

## Challenge

**Points :** 108  
**Catégorie :** stego / whitespace  
**Difficulté :** easy  
**Auteur :** Algorithme123  
**Fichiers :** `arrete-greffe-lome.txt`, `note-mise-en-page.txt`  
**Format du flag :** `NCTF{...}`

> Le greffe du tribunal de Lomé (fictif) publie un arrêté en texte brut. Quelque chose cloche dans la mise en page…

## Résolution

`note-mise-en-page.txt` décrit le canal :

- un espace en fin de ligne est le bit 0 ;
- une tabulation en fin de ligne est le bit 1 ;
- les bits se lisent de haut en bas, regroupés par octets, bit de poids fort d'abord.

Chaque ligne de `arrete-greffe-lome.txt` se termine par exactement un de ces deux caractères. 248 bits donnent 31 octets.

La ligne `# NCTF{brouillon_greffe}` est une annotation visible, pas le flag.

## Flag

```
NCTF{gr3ff3_sp4c3_43e9df0e3a4e}
```
