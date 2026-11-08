# komisergio--shallow (crypto, medium)

**ID :** 538  
**Points :** 200  
**Auteur :** komisergio  
**Fichiers :** `pubkey.txt`, `river.enc`  
**Connexion :** `ncat --ssl {host} {port}`  
**Format :** `NCTF{...}`

Un passage près de Sokodé : cent gués peu profonds et un seul courant profond. Le passeur fait traverser un secret par Diffie-Hellman. Deux esprits répondent à une pierre, celui du gué et celui du courant profond. Le fichier `river.enc` est scellé avec le secret partagé. L'eau ne change pas ; les questions, si.

## Méthode

`pubkey.txt` donne le premier `p`, un générateur `g` et la pierre publique `A = g^x mod p`.

`p - 1` se factorise en quatorze petits premiers, tous à la puissance 1,

`2 · 3 · 5 · 7 · 11 · 13 · 17 · 19 · 23 · 29 · 31 · 37 · 41 · 43`,

puis un cofacteur premier de 160 bits. Le produit des petits premiers vaut `S = 13082761331670030`. L'exposant secret est plus petit que `S`, donc il est entièrement déterminé par ses restes modulo ces premiers.

Pohlig-Hellman sur chaque sous-groupe d'ordre `r | S` donne `x mod r`. Le théorème chinois les recolle :

`x = 5899745426912701`

Vérification : `g^x ≡ A (mod p)`.

L'oracle `ECHO shallow` renvoie simplement `pierre^x mod p`. Il est déterministe, et `ECHO shallow g` redonne `A`. `ECHO deep` change à chaque question : le courant profond ne porte pas le secret. Il ne sert pas à ouvrir le fichier.

`river.enc` (80 octets) est de l'AES-256-CBC. La clé est `SHA-256` des 7 octets big-endian de `x`. Les 16 premiers octets sont l'IV, le reste le chiffre, avec un bourrage PKCS7.

## Flag

`NCTF{the_deep_river_was_forded_by_shallow_crossings}`
