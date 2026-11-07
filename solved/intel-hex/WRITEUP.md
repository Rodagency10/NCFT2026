# intel-hex

## Challenge

**Points :** 64  
**Catégorie :** hardware / intel-hex / memory-dump  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `image.hex`  
**Format du flag :** `NCTF{...}`

> `image.hex` is a dump of a microcontroller's memory in a common text hex format used by flashing tools. Once you rebuild the memory image, the flag sits at offset `0x40`, but it will not read as text straight away — the bytes went through a simple reversible transform on their way to the chip.
>
> Reconstruct memory, read offset `0x40`, and undo the transform.

## Résolution

Le fichier est de l'Intel HEX. Chaque ligne `:LLAAAATTDD…CC` place `LL` octets de données à l'adresse `AAAA` quand le type `TT` vaut `00`.

À l'offset `0x40`, les octets commencent par `E4 34 45 64 B7 …`. En échangeant les deux quartets de chaque octet (`E4` devient `4E`), on retrouve de l'ASCII :

| Octet | Après échange | Caractère |
|-------|----------------|-----------|
| `E4` | `4E` | N |
| `34` | `43` | C |
| `45` | `54` | T |
| `64` | `46` | F |
| `B7` | `7B` | { |
| … | | `intel_hex_offset_nibble_swap` |
| `D7` | `7D` | } |

## Flag

```
NCTF{intel_hex_offset_nibble_swap}
```
