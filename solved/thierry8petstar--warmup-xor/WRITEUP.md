# thierry8petstar--warmup-xor

## Challenge

**ID :** 419  
**Catégorie :** crypto  
**Points :** 80 (dynamique, de 100 à 50)  
**Auteur :** thierry8petstar  
**Fichier :** `output.txt`  
**Format du flag :** `NCTF{...}`

> Un développeur a créé son propre système de chiffrement « ultra sécurisé » basé sur un XOR avec une petite clé répétée.
>
> Il affirme que personne ne pourra retrouver son secret.
>
> Le ciphertext intercepté est fourni dans le fichier output.txt.
>
> Pouvez-vous retrouver le message original ?

## Résolution

`output.txt` contient 56 octets en hexadécimal. Le clair commence par `NCTF{`. XOR des cinq premiers octets du chiffré avec ce préfixe donne `13371`. La clé qui se répète est donc `1337` : le cinquième octet du flux est de nouveau `1`.

Déchiffrer tout le message avec cette clé de quatre octets produit un texte ASCII qui se termine par `}`.

## Flag

```
NCTF{xor_is_not_a_str0ng_c1pher_F0r_us_It_!s_R3v3r51bl3}
```
