# oxdefault--quadratic-i (crypto, hard)

**ID :** 513  
**Points :** 500  
**Auteur :** Oxdefault  
**Fichiers :** `system.txt`, `vault.txt`  
**Format :** `NCTF{...}`

Un système de 81 équations quadratiques à 57 inconnues sur GF(2) (`system.txt`) a une unique solution. Elle ouvre le coffre `vault.txt`.

**Flag : `NCTF{unstructur3d_MQ__cr0ssbr3d_b34ts_na1v3_gr0bn3r}`**

## Énoncé

- `system.txt` : 81 équations quadratiques à 57 inconnues `x0..x56` sur GF(2), chacune égale à 0. On y trouve des termes `xi*xj`, des termes linéaires et parfois la constante `1`.
- `vault.txt` : AES-256-GCM. La clef est `SHA-256` des octets de la solution, MSB first. Nonce `7a61e3eca5c4a48d793cadb0`. Le ciphertext fait 68 octets.

C'est une instance du problème MQ (Multivariate Quadratic). On récupère l'unique solution, on en dérive une clé AES et on déchiffre.

## Pas de raccourci structurel

Avant le calcul lourd :

- aucune variable n'apparaît seulement de façon linéaire ;
- aucune équation ne se factorise, et aucune forme quadratique n'est de faible rang ;
- toutes les variables sont présentes et le système est dense.

Le système est aléatoire, d'où le « unstructured MQ » du flag.

## Pourquoi les approches naïves échouent

| Approche | Coût |
|---|---|
| Force brute | 2^57 évaluations |
| Linéarisation directe | environ 1 700 monômes pour 81 équations |
| Gröbner (F4/F5) | degré de semi-régularité 8, matrices de Macaulay trop grosses |
| Hybride « deviner k variables puis linéariser » | environ 45 variables à deviner, soit 2^45 systèmes |

## Crossbred (Joux–Vitse, 2017)

Crossbred mélange l'algèbre linéaire et l'énumération.

1. On sépare les variables : 16 variables gardées, 41 énumérées.
2. Prétraitement (Macaulay de degré 4). On multiplie les équations par des monômes jusqu'au degré 4, puis on cherche des combinaisons linéaires qui éliminent tous les monômes de degré supérieur à 1 dans les 16 variables gardées. Une fois les 41 autres variables fixées, ces polynômes deviennent linéaires dans les 16 variables gardées. Cette étape se fait une seule fois, par algèbre linéaire creuse (Lanczos par blocs).
3. Énumération. Pour chacune des 2^41 affectations, on évalue ces polynômes (code de Gray) et on résout le petit système linéaire en 16 inconnues. Un candidat cohérent est testé sur les 81 équations d'origine.

L'implémentation utilisée est [hpXbred](https://gitlab.lip6.fr/almasty/hpXbred).

```bash
python3 hpXbred.py challenge.in --workdir run --dry-run
make --jobs --directory run
```

Paramètres retenus pour m = 81, n = 57 : degré 4, 16 variables gardées, hybridation interne 3 (8 sous-tâches), algèbre linéaire Lanczos. Sur 8 cœurs AVX-512 : environ 110 s de prétraitement, puis environ 36 min d'énumération.

## Solution

Une seule solution, de `x0` à `x56` :

```
100101011101100011110010101001110110001101100001100100011
```

Réinjectée dans les 81 équations, toutes valent 0.

Les 57 bits ne font pas un nombre entier d'octets. L'entier big-endian sur 8 octets, le padding à droite, l'ordre inversé et les bits ASCII échouent tous au tag GCM. La lecture « MSB first » découpe la chaîne en paquets de 8 bits dans l'ordre. Le dernier paquet ne contient que le bit `1`, qui devient l'octet `0x01` :

```python
packed = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
# 95 d8 f2 a7 63 61 91 01
```

## Déchiffrement

```python
import hashlib
from Crypto.Cipher import AES

bits = "100101011101100011110010101001110110001101100001100100011"
key = hashlib.sha256(bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))).digest()
nonce = bytes.fromhex("7a61e3eca5c4a48d793cadb0")
ct = bytes.fromhex("acc4d8bcd6e9de3aa6ee5209d45e554b30fe96c265b4069c074b889507327bf8864ebde27aa0291bef7308510cd7c27ec03a827df5645752a239df4b475db3e7d198cb6e")
print(AES.new(key, AES.MODE_GCM, nonce=nonce).decrypt_and_verify(ct[:-16], ct[-16:]))
```

Clé SHA-256 : `e75248e78e7511df89faefca53b180d7662fcda00a9902620cafb285049c41a8`. Les 16 derniers octets sont le tag, sans AAD.

## Flag

`NCTF{unstructur3d_MQ__cr0ssbr3d_b34ts_na1v3_gr0bn3r}`
