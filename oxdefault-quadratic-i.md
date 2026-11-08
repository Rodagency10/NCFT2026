# Writeup – oxdefault--quadratic-i (crypto, hard, 500 pts)

**Flag : `NCTF{unstructur3d_MQ__cr0ssbr3d_b34ts_na1v3_gr0bn3r}`**

## 1. L'énoncé

- `system.txt` : 81 équations quadratiques à 57 inconnues `x0..x56` sur GF(2), chacune égale à 0. On y trouve des termes `xi*xj`, des termes linéaires et parfois la constante `1`.
- `vault.txt` :
  ```
  # AES-256-GCM, clef = SHA-256(octets de la solution, MSB first)
  nonce = 7a61e3eca5c4a48d793cadb0
  ciphertext = acc4d8bc...475db3e7d198cb6e   (68 octets)
  ```
- Les indices disent que tout se passe modulo 2, qu'un calcul de Gröbner classique fait exploser la RAM, et qu'il faut un solveur hybride académique.

Il s'agit donc d'une instance du problème **MQ** (Multivariate Quadratic), qui est NP-difficile. On récupère l'unique solution, on en dérive une clé AES et on déchiffre.

## 2. Analyse : pas de raccourci structurel

Avant de lancer une grosse machine, on vérifie qu'il n'y a pas de faiblesse cachée :
- aucune variable qui n'apparaît que linéairement,
- aucune équation qui se factorise, et pas de forme quadratique de faible rang,
- toutes les variables sont présentes et le système est dense.

Le système est aléatoire et sans structure, d'où le « unstructured MQ » du flag. Il faut donc l'attaquer de front.

## 3. Pourquoi les approches naïves échouent

| Approche | Coût |
|---|---|
| Force brute | 2^57 ≈ 1,4·10^17 évaluations, soit des semaines sur 8 cœurs même avec l'énumération en code de Gray de libFES |
| Linéarisation directe | 57·58/2 + 57 ≈ 1 700 monômes pour seulement 81 équations, impossible |
| Gröbner (F4/F5) | le degré de semi-régularité vaut 8, donc des matrices de Macaulay gigantesques et une RAM qui explose (indice 2) |
| Hybride « deviner k variables puis linéariser » | il faudrait deviner environ 45 variables, encore 2^45 systèmes |

## 4. L'attaque Crossbred (Joux–Vitse, 2017)

Crossbred mélange l'algèbre linéaire et l'énumération :

1. **On sépare les variables** en deux groupes : k variables « gardées » (ici k = 16) et les n − k = 41 autres, qui seront énumérées.
2. **Prétraitement (Macaulay de degré D = 4).** On multiplie les équations par des monômes jusqu'au degré 4, puis on cherche des combinaisons linéaires qui éliminent tous les monômes de degré supérieur à 1 dans les 16 variables gardées. On obtient des polynômes qui, une fois les 41 autres variables fixées, deviennent **linéaires** dans les 16 variables gardées. Cette étape se fait une seule fois, par algèbre linéaire creuse (Lanczos par blocs).
3. **Énumération.** Pour chacune des 2^41 affectations des variables énumérées, on évalue rapidement ces polynômes (code de Gray, instructions vectorielles) et on obtient un petit système linéaire en 16 inconnues, résolu par élimination de Gauss. Si ce système est cohérent, on teste le candidat sur les 81 équations d'origine.

On remplace ainsi 2^57 par 2^41 petites résolutions linéaires très rapides.

### Implémentation utilisée

[hpXbred](https://gitlab.lip6.fr/almasty/hpXbred) (LIP6, équipe ALMASTY) est l'implémentation de référence de Crossbred, utilisée pour les records du MQ Challenge.

```bash
# conversion de system.txt au format d'entrée de hpXbred -> challenge.in
python3 hpXbred.py challenge.in --workdir run --dry-run
make --jobs --directory run
```

Paramètres choisis par l'outil pour m = 81, n = 57 :
- `degree: 4`, `kept_variables: 16`
- `inner_hybridation: 3`, soit 2^3 = 8 sous-tâches en parallèle, une par cœur
- algèbre linéaire avec `lanczos`

Temps mesurés sur mon ordi (8 cœurs, AVX-512) : environ 110 s de prétraitement, puis environ 36 min pour les 8 énumérations en parallèle.

## 5. La solution

Une seule solution trouvée, dans l'ordre `x0` à `x56` :

```
100101011101100011110010101001110110001101100001100100011
```

On la vérifie en la réinjectant dans les 81 équations d'origine : toutes valent 0.

## 6. Le piège : convertir la solution en octets

Les 57 bits ne font pas un nombre entier d'octets (57 = 7×8 + 1). Les interprétations « naturelles » échouent toutes à l'authentification GCM : entier big-endian sur 8 octets, padding à droite (`...80`), ordre inversé, bits ASCII, etc. J'en ai testé environ 450.

La bonne lecture de « MSB first » consiste à découper la chaîne en paquets de 8 bits **dans l'ordre**, chaque paquet étant lu MSB d'abord. Le dernier paquet ne contient qu'un bit, `1`, qui devient l'octet `0x01` sans décalage :

```python
packed = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
# 95 d8 f2 a7 63 61 91 01
```

## 7. Déchiffrement

```python
import hashlib
from Crypto.Cipher import AES

bits = "100101011101100011110010101001110110001101100001100100011"
key = hashlib.sha256(bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))).digest()
nonce = bytes.fromhex("7a61e3eca5c4a48d793cadb0")
ct = bytes.fromhex("acc4d8bcd6e9de3aa6ee5209d45e554b30fe96c265b4069c074b889507327bf8864ebde27aa0291bef7308510cd7c27ec03a827df5645752a239df4b475db3e7d198cb6e")
print(AES.new(key, AES.MODE_GCM, nonce=nonce).decrypt_and_verify(ct[:-16], ct[-16:]))
```

- Clé SHA-256 : `e75248e78e7511df89faefca53b180d7662fcda00a9902620cafb285049c41a8`
- Les 16 derniers octets sont le tag, il n'y a pas d'AAD, et l'authentification passe.

```
NCTF{unstructur3d_MQ__cr0ssbr3d_b34ts_na1v3_gr0bn3r}
```

## 8. À retenir

- Pour un système MQ aléatoire sur GF(2) avec m un peu plus grand que n, autour de 50 à 60 variables, Crossbred (hpXbred) est l'outil à utiliser, pas Gröbner.
- On vérifie toujours d'abord s'il existe une structure exploitable, avant de lancer le calcul lourd.
- Quand le nombre de bits n'est pas un multiple de 8, il faut tester les différentes conversions en octets : le tag GCM sert d'oracle pour reconnaître la bonne.
