# origin-story

## Challenge

**ID :** 12  
**Catégorie :** blockchain  
**Points :** 300  
**Auteurs :** hibris, Clawd  
**Fichiers :** `Vault.sol`, `vault.json`  
**Format du flag :** `NCTF{...}`

> You get `Vault.sol` and `vault.json` (a sealed note `cipher_hex` plus the address you control). Nobody has taken ownership yet. Figure out the single winning transaction, then unseal the note it protects.

## Résolution

`initialize` n'a ni garde ni contrôle d'accès : n'importe qui devient `owner`. L'adresse contrôlée est `0x00000000000000000000000000000000a77ac6e5`. La transaction gagnante est donc `initialize` de cette adresse.

Son calldata est le sélecteur `c4d66de8` suivi de l'adresse calée sur 32 octets. La note est un XOR dont la clé est `keccak256(calldata)`, et le flux `keccak256(clé || uint32_be(i))`.

## Flag

```
NCTF{unprotected_init_takes_the_throne}
```
