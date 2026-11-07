# boazak--niamtougou

## Challenge

**ID :** 410  
**Catégorie :** crypto  
**Points :** 83 (dynamique, de 250 à 83)  
**Auteur :** KodjoDoDjango  
**Fichier :** `challenge.txt`  
**Format du flag :** `NCTF{...}`

> Niamtougou est une ville du nord du Togo et le siège d'un aéroport international — ici, c'est le hasard qui prend l'avion : un PRNG trop prévisible.
>
> Un générateur a produit 624 sorties de 32 bits (une période complète du générateur de nombres pseudo-aléatoires de Python), puis a chiffré le flag par XOR avec la clé tirée juste après.
>
> Le flag est dans `challenge.txt`, avec les 624 sorties et le flux chiffré `enc`.

## Résolution

Les 624 valeurs sont une période complète de MT19937, le générateur de `random` en Python. Chaque sortie est l'état interne après le tempérage. En inversant les quatre étapes (`>> 11`, `<< 7`, `<< 15`, `>> 18`), on retrouve les 624 mots d'état. L'index est placé à 624, donc le tirage suivant fait tourner le générateur comme le ferait Python.

`enc` fait 49 octets. La clé est la concaténation big-endian des `getrandbits(32)` qui suivent, tronquée à 49 octets. Le XOR donne le flag.

## Flag

```
NCTF{N14M70UG0U_MT19937_5T4T3_R3C0V3RY_483726591}
```
