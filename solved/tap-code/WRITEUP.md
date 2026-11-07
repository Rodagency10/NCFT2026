# tap-code

## Challenge

**Points :** 25  
**Catégorie :** warmup / classical / tap-code  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `taps.txt`  
**Format du flag :** `NCTF{...}`

> `taps.txt` is a list of two-digit numbers. Each number is a row then a column in this 5x5 letter square (read across, then down):
>
> ```
>     1 2 3 4 5
>   1 A B C D E
>   2 F G H I J
>   3 L M N O P
>   4 Q R S T U
>   5 V W X Y Z
> ```
>
> So `44` is row 4, column 4 = `T`. A double space separates words. Decode it, then lowercase and join the words with underscores as the flag body.

## Résolution

Le fichier contient :

```
44 11 35  13 34 14 15  35 34 31 54 12 24 45 43
```

Le carré est l’alphabet sans `K` (le `C` et le `K` partagent la même case dans le tap code classique ; ici seule la grille fournie compte). Un espace simple sépare les lettres, un double espace sépare les mots.

| Nombre | Lettre |
|--------|--------|
| `44` | T |
| `11` | A |
| `35` | P |
| `13 34 14 15` | C O D E |
| `35 34 31 54 12 24 45 43` | P O L Y B I U S |

Le message est `TAP CODE POLYBIUS`. En minuscules, les espaces deviennent des `_`.

## Flag

```
NCTF{tap_code_polybius}
```
