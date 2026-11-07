# boazak--bras-arme

## Challenge

**ID :** 423  
**Catégorie :** forensics  
**Points :** 212 (dynamique, de 250 à 83)  
**Auteur :** KodjoDoDjango  
**Fichiers :** `bras_arme.zip`, `wordlist.txt`  
**Format du flag :** `NCTF{...}`

> Un agent infiltré a récupéré un fichier ZIP sur un serveur ennemi, mais il est verrouillé. On dit que ce fichier contient des indices. Mais attention, l'ennemi est malicieux et aime les leurres. Trouvez le vrai flag caché dans ce labyrinthe numérique.
>
> Le fichier ZIP est disponible en téléchargement.
>
> **Note :** Le bras armé a des règles à suivre.

Aucun service distant n'est nécessaire. La wordlist compte 1 116 lignes, soit 958 mots distincts. Les originaux ne sont pas modifiés : la signature ZIP est restaurée dans une copie.

## Résolution

### Réparer l'archive

Le répertoire central est intact. Les quatre premiers octets du premier en-tête local ont été remplacés par des zéros. Tant que la signature n'est pas restaurée, un outil ZIP refuse l'archive avant même de tester le mot de passe.

```text
Offsets 0–3 : 00 00 00 00 → 50 4b 03 04
```

La note sur les « règles » désigne une règle de John the Ripper appliquée à la wordlist, pas un mot brut. La règle gagnante est une **initiale majuscule suivie d'un suffixe numérique de trois chiffres**. Elle ouvre les trois fichiers :

| Fichier | Taille claire | CRC32 |
|---|---:|---|
| `message.txt` | 130 | `dc3b689c` |
| `image_1.png` | 22 547 | `f71e4141` |
| `image_2.jpeg` | 192 488 | `81e18c4b` |

`message.txt` se présente comme un leurre, puis donne la suite : les extensions sont les bonnes, mais quelque chose cloche.

### Réparer les images

Les huit premiers octets des deux images sont nuls. Le reste du fichier permet de remettre l'en-tête sans toucher aux données :

```text
PNG  : 89 50 4e 47 0d 0a 1a 0a
JPEG : ff d8 ff e0 00 10 4a 46
```

Le PNG réparé fait 785 × 390. Ses chunks sont valides jusqu'à `IEND`, sans donnée après la fin. Il montre le logo ANCy et le commentaire « Tu connais mon bras armé ??? ». Le JPEG, 1 024 × 571, montre un bâtiment marqué CDA. Ce sont des leurres : ni le sigle, ni les métadonnées, ni les plans de bits ne portent le flag.

### Couche steghide

Le JPEG est un conteneur steghide (`rijndael-128` CBC). `stegseek --seed` repère un en-tête cohérent d'environ 215 octets compressés, sans donner le mot de passe.

Une autre entrée de la wordlist, transformée par la même famille de règle, extrait une seconde archive. Le nom annoncé par le conteneur est `flag.zip`. Son SHA-256 est :

```text
e24e4eb21be8b0bff3d6179a0c2e05aabfa97884bd773c973a36bd0a58506a39
```

### Dernière archive

`flag.zip` ne contient que `flag.txt`. Les deux mots de passe précédents ne l'ouvrent pas. Une troisième entrée, toujours avec une initiale majuscule et un suffixe de trois chiffres, déchiffre le fichier.

Le texte confirme que le flag est bien là. `flag.txt` fait 68 octets, CRC32 `c5768826`, SHA-256 :

```text
8d78a5451e39c22b9d36d999023efe4568fae5271a6d381760fa2789c95203d2
```

Les CRC des archives et du PNG sont contrôlés. Une réextraction steghide indépendante de stegseek, puis Info-ZIP, restituent les mêmes octets que Python.

## Flag

```
NCTF{h3x_m4g1c_byt3s_4nd_j0hn_runn3r}
```
