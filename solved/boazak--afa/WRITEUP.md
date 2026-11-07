# boazak--afa

## Challenge

**ID :** 396  
**Catégorie :** crypto  
**Points :** 143 (dynamique, de 150 à 50)  
**Auteur :** KodjoDoDjango  
**Fichier :** `challenge.txt`  
**Format du flag :** `NCTF{...}`

> **Origine du nom :** Afa est la divination éwé et fon : lire l'avenir dans les graines et les noix de palme — ici, prédire les prochaines sorties du générateur.
>
> Pour produire son « hasard », l'application a utilisé une simple suite linéaire congruente (`LCG`). Quelques sorties suffisent pour retrouver les paramètres et prédire la suite du flux, qui a servi à chiffrer le flag en XOR.
>
> Reconstituez le flux et déchiffrez le flag dans `challenge.txt`.

## Résolution

La suite est `x → (a·x + b) mod M`, avec `M = 2305843009213693951` (`2^61 − 1`). Six sorties consécutives sont données. Deux écarts suffisent :

```text
a ≡ (x2 − x1) · (x1 − x0)^(−1)  (mod M)
b ≡ x1 − a·x0                   (mod M)
```

On obtient `a = 1797134120141453326` et `b = 668502270603154449`. Les quatre transitions suivantes confirment ces paramètres.

Le chiffré `c1` fait 30 octets. Le flux est la suite des états **après** les six sorties publiées, chacun écrit en 8 octets big-endian, tronqué à 30 octets. Le XOR avec `c1` donne le flag.

## Flag

```
NCTF{LCG_N0T_C5PRN6_661839204}
```
