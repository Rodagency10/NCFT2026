# off-by-one-auth

## Challenge

**ID :** 178  
**Catégorie :** pwn  
**Points :** 130 (dynamique, de 150 à 50)  
**Auteurs :** hibris, Clawd  
**Fichier :** `chall` (ELF x86-64, 16216 octets)  
**Format du flag :** `NCTF{...}`

> You are given a single x86-64 Linux binary, `chall`. It asks how many bytes you want to send (up to 32), reads them, and then decides whether you are authorized. By default you are denied.
>
> Become authorized and read what the program prints.

## Résolution

`main` réserve un tampon de 32 octets en `rbp-0x30` et un mot de 8 octets en `rbp-0x10`, initialisé à zéro. Ce mot est le drapeau d'autorisation.

La longueur demandée est acceptée jusqu'à 32 inclus. La boucle de lecture s'arrête avec `jle`, donc elle écrit `longueur + 1` octets. Avec 32, le 33e octet tombe sur l'octet de poids faible du mot en `rbp-0x10`. S'il est non nul, le programme affiche `authorized.` puis appelle la routine qui imprime le secret.

Cette routine décode 37 octets situés en `0x402040` par un XOR avec `0x77`, puis les écrit sur la sortie.

## Flag

```
NCTF{off_by_one_authorized_true_1337}
```
