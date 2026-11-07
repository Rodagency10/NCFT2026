# rot13-decode

## Challenge

**Points :** 25  
**Catégorie :** warmup / classical / rot13  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `secret_.txt`  
**Format du flag :** `NCTF{...}`

> `secret.txt` reads almost like the flag, but every letter has been rotated halfway around the alphabet. Rotate it back and read the flag.

## Résolution

Le texte chiffré est :

```
APGS{ebg13_gjvpr_vf_abguvat}
```

ROT13 décale chaque lettre de 13 positions, soit la moitié de l’alphabet de 26 lettres. `A` devient `N`, `B` devient `O`, et ainsi de suite. Appliquer ROT13 une seconde fois revient au texte d’origine. La casse est conservée, et les chiffres, `_` et accolades ne bougent pas.

| Chiffré | Clair |
|---------|-------|
| `APGS` | `NCTF` |
| `ebg13` | `rot13` |
| `gjvpr` | `twice` |
| `vf` | `is` |
| `abguvat` | `nothing` |

## Flag

```
NCTF{rot13_twice_is_nothing}
```
