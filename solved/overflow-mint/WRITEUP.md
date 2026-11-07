# overflow-mint

## Challenge

**ID :** 13  
**Catégorie :** blockchain  
**Points :** 300  
**Auteurs :** hibris, Clawd  
**Fichiers :** `MintSale.sol`, `sale.json`  
**Format du flag :** `NCTF{...}`

> You get the Solidity source of a token pre-sale (`MintSale.sol`) and `sale.json` (the on-sale `price`, your wallet `budget_wei`, and a vault `cipher_hex`). Buying `n` tokens costs `n * price` wei; reaching `WIN_TOKENS` unlocks the vault. Your wallet holds only a few wei. Unlock the vault.

## Résolution

Le contrat est en Solidity 0.7 : `n * price` est calculé modulo `2^256`. Ici `price = 2^252 + 1`. Pour tout multiple de 16, le produit retombe sur `n` lui-même. `buy(16)` coûte donc 16 wei, bien en dessous du budget de 1000 wei, alors que le prix nominal déborde.

La note du coffre est un XOR. La clé est l'entier `16` écrit sur 32 octets, et le flux est `keccak256(clé || uint32_be(i))`.

## Flag

```
NCTF{unchecked_mul_wraps_to_zero_cost}
```
