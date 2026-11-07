# eui64-slaac

## Challenge

**Points :** 82  
**Catégorie :** networking / ipv6 / eui64  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `hosts.json`  
**Format du flag :** `NCTF{...}`

> A stateless address-autoconfig (SLAAC) inventory (`hosts.json`) lists 29 interfaces, each with a MAC address, a single shared /64 prefix, and a one-character `tag`. The interface identifiers were "omitted on purpose".
>
> Reconstruct each host's full IPv6 address, put the hosts in the right order, and read the tags in that order to recover the flag.

## Résolution

Le préfixe commun est `2001:db8:ac1d:64::/64`. L'identifiant d'interface EUI-64 se déduit de l'adresse MAC :

1. couper les 6 octets en deux moitiés de 3 ;
2. insérer `ff:fe` au milieu ;
3. inverser le bit U/L, le deuxième bit de poids faible du premier octet (`XOR 0x02`).

Exemple : `0c:19:c2:16:06:6b` devient `0e:19:c2:ff:fe:16:06:6b`, donc l'adresse `2001:db8:ac1d:64:e19:c2ff:fe16:66b`.

En triant les hôtes par cet identifiant, l'ordre est `node-00` … `node-28`. Les `tag` lus dans cet ordre forment le flag.

## Flag

```
NCTF{eui64_slaac_ll_bit_flip}
```
