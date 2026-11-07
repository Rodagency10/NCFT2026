# calldata-cache

## Challenge

**Points :** 62  
**Catégorie :** blockchain / evm / abi  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichiers :** `calldata.txt`, `abi.json`, `NotesRegistry.sol`  
**Format du flag :** `NCTF{...}`

> You captured one transaction's raw calldata (`calldata.txt`) and the target contract's ABI (`abi.json`) plus source (`NotesRegistry.sol`). Decode the call and recover the hidden argument.

## Résolution

`NotesRegistry.store(uint256 id, address who, string note)` est la seule fonction. Son calldata ABI est :

1. 4 octets de sélecteur : `00c63b11`
2. `id` sur 32 octets
3. `who` sur 32 octets (adresse alignée à droite)
4. offset de la chaîne `note`, sur 32 octets
5. à cet offset : la longueur, puis les octets UTF-8, complétés à un multiple de 32

`calldata.txt` se découpe ainsi :

| Mot | Hex | Valeur |
|-----|-----|--------|
| sélecteur | `00c63b11` | `store(uint256,address,string)` |
| `id` | `0x2a` | 42 |
| `who` | `0xc0ffee99` | `0x0000…c0ffee99` |
| offset | `0x60` | la chaîne commence au 4e mot |
| longueur | `0x22` | 34 octets |
| données | `4e4354467b…647d` | le texte |

Les 34 octets `4e4354467b6162695f63616c6c646174615f6465636f6465645f62795f68616e647d` sont de l’ASCII.

## Flag

```
NCTF{abi_calldata_decoded_by_hand}
```
