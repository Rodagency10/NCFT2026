# trailing-zip

## Challenge

**ID :** 198  
**Catégorie :** stego  
**Points :** 90 (dynamique, de 100 à 50)  
**Auteurs :** hibris, Clawd  
**Fichier :** `banner.bmp` (19416 octets)  
**Format du flag :** `NCTF{...}`

> `banner.bmp` s'ouvre dans n'importe quel visualiseur, mais le fichier est bien trop gros pour une si petite image. Trouver ce qui est accroché à la suite et lire le secret.

## Résolution

L'en-tête BMP annonce une taille de 19254 octets (`bfSize`). Le fichier en fait 19416 : les 162 octets qui suivent commencent par `PK\x03\x04`, une archive ZIP. Elle contient `secret/flag.txt`, compressé en deflate.

## Flag

```
NCTF{zip_hides_past_the_pixels}
```
