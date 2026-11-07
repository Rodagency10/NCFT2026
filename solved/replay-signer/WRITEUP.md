# replay-signer

## Challenge

**ID :** 16  
**Catégorie :** blockchain  
**Points :** 450  
**Auteurs :** hibris, Clawd  
**Fichiers :** `SignedTreasury.sol`, `signatures.json`  
**Format du flag :** `NCTF{...}`

> You captured two withdrawal requests signed by the same treasury key (`signatures.json`) and the source of the authorizer (`SignedTreasury.sol`). The vault note in `cipher_hex` is sealed with that key. Recover it.

## Résolution

Les deux signatures partagent le même `r` : le nonce ECDSA `k` a été réutilisé. Sur secp256k1, avec `h` le `keccak256` du message en clair :

```text
k = (h1 − h2) · (s1 − s2)^(−1)  mod n
d = (s1 · k − h1) · r^(−1)       mod n
```

Les messages sont `withdraw:100 to treasury` et `withdraw:250 to treasury`. On obtient

```text
d = 0xc0ffee1234567890abcdef0011223344556677889900aabbccddeeff01020304
```

La clé publique non compressée, passée à `keccak256`, redonne le signataire `0xd9e1e661bec5730b28c98918270bd24027bb8ca8`.

La note est un XOR. La clé est `d` sur 32 octets, et le flux est `keccak256(clé || uint32_be(i))`.

## Flag

```
NCTF{same_nonce_leaks_the_whole_key}
```
