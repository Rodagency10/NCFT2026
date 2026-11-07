# zip-comment

## Challenge

**Points :** 25  
**Catégorie :** warmup / forensics / zip  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `archive.zip`  
**Format du flag :** `NCTF{...}`

> `archive.zip` unzips to a single, unhelpful text file. The flag is not in the file — it is stored somewhere else in the archive. Look closer at the zip itself.

## Résolution

L’archive ne contient que `readme.txt`. Le format ZIP peut aussi porter un commentaire d’archive : il est écrit à la fin du fichier, juste après l’enregistrement de fin de répertoire central (`PK\x05\x06`). Les deux octets qui précèdent le commentaire donnent sa longueur.

La fin de `archive.zip` se termine par :

```
NCTF{look_inside_the_zip_comment}
```

C’est le commentaire ZIP, pas le contenu de `readme.txt`.

## Flag

```
NCTF{look_inside_the_zip_comment}
```
