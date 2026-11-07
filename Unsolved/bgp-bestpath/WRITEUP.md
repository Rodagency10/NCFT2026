# bgp-bestpath (networking, easy)

**Flag:** `NCTF{bgp_bestpath_localpref_beats_aspath_len}`

## Approche
`bgp_rib.json` liste, pour chaque préfixe, plusieurs routes candidates. Le routeur
installe **une seule** route par préfixe selon l'ordre de décision donné dans le fichier :

1. `local_pref` le plus **haut**
2. `as_path` le plus **court**
3. `origin` le plus **bas** : `igp` < `egp` < `incomplete`
4. `med` le plus **bas**
5. `peer_id` le plus **bas** (tie-break)

Pour chaque préfixe on prend la route gagnante, on lit son `label` (1 caractère),
puis on concatène les labels **dans l'ordre croissant des préfixes** (tri par
adresse réseau puis longueur de préfixe). 45 préfixes → 45 caractères = le flag.

## Résolution
```bash
py solve.py
```
