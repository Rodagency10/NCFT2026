# binary-ascii

## Challenge

**Points :** 27  
**Catégorie :** warmup / encoding / binary  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `bits.txt`  
**Format du flag :** `NCTF{...}`

> `bits.txt` is nothing but groups of eight 0s and 1s separated by spaces. Each group is one character. Reassemble the message and read the flag.

## Résolution

Le fichier contient des octets binaires séparés par des espaces :

```
01001110 01000011 01010100 01000110 01111011 ...
```

Chaque groupe de 8 bits est un code ASCII. On le lit en base 2, puis on le convertit en caractère (`parseInt(groupe, 2)` puis `String.fromCharCode`).

| Binaire | Décimal | Caractère |
|---------|---------|-----------|
| `01001110` | 78 | `N` |
| `01000011` | 67 | `C` |
| `01010100` | 84 | `T` |
| `01000110` | 70 | `F` |
| `01111011` | 123 | `{` |
| `01100010` … | | `binary_ones_and_zeros` |
| `01111101` | 125 | `}` |

## Flag

```
NCTF{binary_ones_and_zeros}
```
