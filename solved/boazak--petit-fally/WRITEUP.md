# boazak--petit-fally

## Challenge

**Points :** 50  
**Catégorie :** misc  
**Difficulté :** easy  
**Auteur :** KodjoDoDjango  
**Fichier :** `Petit-Fally.jpg`  
**Format du flag :** `NCTF{...}`

> Dans l'ombre de l'an 78, sous la lune d'argent,  
> Marchaient 67 braves, au pas lourd et pesant.  
> …  
> La porte 125 s'ouvrit enfin sur le poème.

## Résolution

Chaque nombre du poème est un code ASCII. Dans l'ordre d'apparition :

| Nombre | Caractère |
|--------|-----------|
| 78 | N |
| 67 | C |
| 84 | T |
| 70 | F |
| 123 | { |
| 82 48 83 51 115 … | `R0S3s_4R3_R3D_V10L375_4R3_8LU3_48391726` |
| 125 | } |

Le texte qui en sort se lit « roses are red, violets are blue », en leet speak.

## Flag

```
NCTF{R0S3s_4R3_R3D_V10L375_4R3_8LU3_48391726}
```
