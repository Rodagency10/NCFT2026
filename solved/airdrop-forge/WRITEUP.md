# airdrop-forge

## Challenge

**ID :** 8  
**Catégorie :** blockchain  
**Points :** 300  
**Auteurs :** hibris, Clawd  
**Fichiers :** `MerkleAirdrop.sol`, `tree.json`  
**Format du flag :** `NCTF{...}`

> You get a Merkle-root airdrop contract (`MerkleAirdrop.sol`) and `tree.json`: the full list of leaves, the `root`, a high-value target claim, and a sealed bonus `cipher_hex`. Produce what the contract needs to accept the target claim, and open the bonus.

## Résolution

Une feuille est `keccak256(abi.encodePacked(address, uint256))`. Pour la cible `0x00000000000000000000000000000000000000f0` et le montant `999999`, cela redonne la feuille d'indice 3.

L'arbre trie chaque paire avant de la hasher, comme `claim`. Avec 8 feuilles, la preuve de l'indice 3 est le voisin puis les deux oncles :

```text
0x5e69b50287fd8a78728dc06abe9fcd4b62b7f039ebe73f85b8d65e55c6ed61ec
0xd0c386ab2cfa17ac05dfb1fa0991800a6d838917d7520fce68dd13cfc9ac0cb9
0xaa2f0c67c674900f81c9de08570ded3bc7412f5f7f5e321f6d73d0950d55c484
```

Cette preuve remonte bien à la racine `0x8be02da013db3aee9b376a809754f2f30694b0238baf028e57463ad502d9dc17`.

Le bonus est un XOR. La clé vaut `keccak256` des trois mots de preuve concaténés, et le flux est `keccak256(clé || uint32_be(i))` pour `i = 0, 1, ...`.

## Flag

```
NCTF{merkle_proof_forged_offline}
```
