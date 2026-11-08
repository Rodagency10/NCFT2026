# chunk-hunt (forensics, easy)

**ID :** 119  
**Points :** 150  
**Auteurs :** hibris, Clawd  
**Fichier :** `badge.png`  
**Format :** `NCTF{...}`

Un badge d'entreprise a été exporté en PNG (`badge.png`). L'image ne contient rien. Le fichier transporte autre chose que des pixels : il faut ouvrir le conteneur et réassembler ce qui y a été caché.

## Méthode

Le PNG fait 96×96. Les chunks utiles sont des `tEXt` ancillaires, en plus d'un commentaire `created with the office badge maker`. Dix chunks ont un mot-clé `frg00` … `frg09` et une valeur de 5 caractères. Ils ne sont pas dans l'ordre dans le fichier.

On les trie par numéro, on concatène les valeurs :

`PD4~idtq*4X>4p^a(Q2HZf9R(XmxIDb6;a&a&mcJb7f<4Wps0W`

C'est du base85 (alphabet RFC, pas Ascii85). Le décodage donne 40 octets, le flag.

## Flag

`NCTF{ancillary_png_chunks_carry_secrets}`
