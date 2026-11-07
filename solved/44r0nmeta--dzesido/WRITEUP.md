# 44r0nmeta--dzesido

## Challenge

**Points :** 58  
**Catégorie :** crypto  
**Auteur :** 44r0nMeta  
**Tags :** crypto, stage:prequals  
**Fichier :** `archive.zip`  
**Format du flag :** `NCTF{...}`

> A journalist left behind an encrypted archive. We also found a related article: https://fr.wikipedia.org/wiki/Sylvanus_Olympio

## Résolution

L'archive est chiffrée avec le ZipCrypto historique (bit de chiffrement dans les en-têtes). Elle contient trois fichiers :

| Fichier | Méthode | Taille claire |
|---------|---------|----------------|
| `Sylvanus_Olympio.jpg` | deflate | 40581 |
| `Armoiries_du_Togo.svg` | deflate | 33991 |
| `flag.txt` | stocké | 60 |

Les deux premiers noms sont ceux des fichiers de l'article Wikipédia. Le SVG des armoiries du Togo sur Wikimedia Commons fait exactement 33991 octets :

`https://upload.wikimedia.org/wikipedia/commons/2/2d/Armoiries_du_Togo.svg`

ZipCrypto chiffre le flux déjà compressé, plus un en-tête aléatoire de 12 octets. La taille chiffrée du SVG est 10375, donc le deflate fait 10363 octets. C'est précisément la taille obtenue avec un deflate brut zlib, niveau 6 (`wbits = -15`), sur ce SVG. Le texte clair compressé est donc connu.

ZipCrypto cède à l'attaque par texte clair connu de Biham et Kocher. Avec `bkcrack` et ce SVG comme clair :

```
bkcrack -C archive.zip -c Armoiries_du_Togo.svg -P plain.zip -p Armoiries_du_Togo.svg
```

Les clés internes sont `1be94178 4362c1a3 5fa12170`. Elles suffisent à déchiffrer toute l'archive, y compris `flag.txt`, sans retrouver le mot de passe.

## Flag

```
NCTF{kn0wn_pl41nt3xt_z1p_cr4ck_ftw_2f1512f54bd4a3049ce5c04e}
```
