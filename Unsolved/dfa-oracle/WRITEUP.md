# dfa-oracle

## Challenge

**ID :** 120  
**Catégorie :** ppc  
**Points :** 185 (dynamique, de 300 à 100)  
**Auteurs :** hibris, Clawd  
**Fichier :** `automaton.json`  
**Format du flag :** `NCTF{...}`

> `automaton.json` décrit un automate fini déterministe : un alphabet, un ensemble d'états, un état initial, des états acceptants et une table de transitions. Son langage contient exactement une chaîne. Trouver cette chaîne.

## Résolution

L'automate est complet : 39 états, un alphabet de 20 symboles, 780 transitions, un seul état acceptant. Toutes les transitions qui sortent du mot cherché aboutissent à un puits, `s999999`, qui n'atteint jamais l'acceptation.

On calcule d'abord les états qui peuvent encore mener à l'état acceptant (38 sur 39 : tout sauf le puits). Depuis l'état initial, un seul symbole garde l'automate dans cet ensemble. On suit cette transition, et on répète. Aucun choix, aucune boucle : le chemin fait 37 symboles et se termine sur l'unique état acceptant. Cette chaîne est le seul mot du langage.

## Flag

```
NCTF{regular_languages_have_one_word}
```
