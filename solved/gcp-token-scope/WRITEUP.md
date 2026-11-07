# NCTF2026 Togo — gcp-token-scope

**Catégorie :** Cloud / GCP / IAM  
**Flag :** `NCTF{sa_token_scope_read_the_bucket}`  
**Statut :** flag extrait localement, puis **confirmé accepté par l’utilisateur**. Nous n’avons effectué aucune soumission à la plateforme.

## 1. Contexte et objectif

L’énoncé fournit une clé de compte de service destinée à un assistant CI, la politique IAM du projet, un inventaire de buckets et un objet privé « scellé » pour la distribution du challenge.

Il faut répondre à deux questions :

1. Quels objets ce compte peut-il réellement lire dans le modèle fourni ?
2. Comment retrouver le contenu de l’objet de production qu’il ne devrait pas pouvoir atteindre ?

Le challenge se résout entièrement **hors ligne**. La clé privée comporte explicitement un marqueur de clé factice. Elle n’est ni nécessaire au déchiffrement ni utilisable comme justification pour contacter Google Cloud. Aucun accès réseau, aucune authentification et aucune création de jeton n’ont été effectués.

## 2. Fichiers fournis

| Fichier | Utilité |
|---|---|
| `challenge.json` | Énoncé, catégorie et format attendu du flag. |
| `sa-key.json` | Informations du compte de service ; le champ `private_key_id` sert à la dérivation locale. |
| `iam-policy.json` | Associations entre rôles IAM et identités. |
| `bucket-listing.json` | Buckets et chemins des objets disponibles dans le scénario. |
| `release-token.json` | Indication de scellement et chiffré encodé en Base64. |

Les cinq JSON analysés ont été comparés au ZIP source : ils sont identiques octet par octet. Le ZIP original n’a pas été modifié.

## 3. Identifier le défaut de permissions

Dans `iam-policy.json`, le compte de service CI est membre d’une association donnant le rôle :

```text
roles/storage.objectViewer
```

L’élément déterminant est sa **portée** : il s’agit de la politique IAM du **projet**, pas d’une autorisation limitée au bucket de cache CI.

Dans le modèle du challenge, ce rôle donne donc au compte des droits de lecture et de listage des objets des buckets du projet, y compris ceux de production. Le nom et la fonction supposée d’un compte ne constituent pas une restriction de sécurité : ce sont les autorisations effectivement accordées qui comptent.

L’inventaire contient trois buckets, dont celui des artefacts de production. L’objet sensible est :

```text
gs://kekeli-prod-artifacts/releases/RELEASE_TOKEN.enc
```

`release-token.json` représente précisément cet objet. Il n’est pas nécessaire de fabriquer un jeton OAuth pour poursuivre : toutes les données nécessaires sont déjà fournies localement. Plus généralement, un scope OAuth ne remplace pas une autorisation IAM ; les deux notions ne doivent pas être confondues.

## 4. Ouvrir l’objet scellé

### Indication explicite

Le champ `seal` annonce :

```text
XOR keystream = SHA256(service-account key private_key_id)
```

Le champ `ciphertext_b64`, une fois décodé en Base64, contient **36 octets**. Base64 est seulement un encodage de transport : son décodage ne déchiffre pas l’objet.

### Pourquoi le XOR direct échoue

Une première interprétation consiste à calculer `SHA256(private_key_id)` et à répéter ce condensat de 32 octets pour couvrir le chiffré.

Cette hypothèse produit une sortie commençant par :

```text
77 de e9 cc f0
```

Ce n’est pas un texte UTF-8 valide. Cela invalide cette interprétation, **pas le challenge lui-même** : le mot « keystream » peut désigner un flux construit à partir du condensat, plutôt que le condensat répété.

### Convention inférée et vérifiée

Des essais bornés ont exploré les représentations des données, les couches intermédiaires et plusieurs constructions de flux à compteur. La convention qui restitue le texte entier est :

```text
seed = SHA256(UTF8(private_key_id)).digest()
bloc[i] = SHA256(seed || uint32_be(i)).digest()
flux = bloc[0] || bloc[1] || ...
clair = chiffré XOR flux
```

Les détails importants sont :

- `seed` est le condensat **brut**, pas ses caractères hexadécimaux ;
- `||` signifie une concaténation d’octets ;
- le compteur commence à **zéro** ;
- il occupe **quatre octets**, en ordre **big-endian** ;
- le flux est tronqué à la longueur du chiffré.

Pour 36 octets, on utilise donc les 32 octets du premier bloc, puis les quatre premiers du deuxième.

**Cette expansion n’était pas explicitement décrite dans l’indication.** Elle a été inférée par les tests, puis confirmée par un flag intégral cohérent. Le rechiffrement restitue exactement le Base64 fourni. Cette dernière vérification contrôle la reproductibilité du calcul ; l’acceptation confirmée ensuite par l’utilisateur valide le flag auprès de la plateforme.

## 5. Solveur Python autonome

Ce script utilise uniquement la bibliothèque standard. Il lit seulement les deux fichiers nécessaires et n’affiche ni clé privée ni identifiant de clé.

```python
#!/usr/bin/env python3
import argparse
import base64
import hashlib
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser(description="Solveur local gcp-token-scope")
parser.add_argument("dossier", nargs="?", default=".", type=Path)
root = parser.parse_args().dossier

key_id = json.loads(
    (root / "sa-key.json").read_text(encoding="utf-8")
)["private_key_id"]
encoded = json.loads(
    (root / "release-token.json").read_text(encoding="utf-8")
)["ciphertext_b64"]
ciphertext = base64.b64decode(encoded, validate=True)

seed = hashlib.sha256(key_id.encode("utf-8")).digest()
blocks = []
for counter in range((len(ciphertext) + 31) // 32):
    counter_bytes = counter.to_bytes(4, "big")
    blocks.append(hashlib.sha256(seed + counter_bytes).digest())
keystream = b"".join(blocks)[:len(ciphertext)]

plaintext = bytes(c ^ k for c, k in zip(ciphertext, keystream))
flag = plaintext.decode("utf-8")
if not re.fullmatch(r"NCTF\{[^{}\r\n]+\}", flag):
    raise ValueError("La sortie ne respecte pas le format du flag")

reencrypted = bytes(p ^ k for p, k in zip(plaintext, keystream))
if base64.b64encode(reencrypted).decode("ascii") != encoded:
    raise ValueError("Le contrôle de rechiffrement a échoué")

print(flag)
print(f"Longueur du clair : {len(plaintext)} octets")
print("Rechiffrement : identique au Base64 fourni.")
```

Exécution depuis n’importe quel dossier, en indiquant le chemin des ressources :

```sh
python3 /workspace/nctf2026/gcp-token-scope/analysis/solve-writeup.py /workspace/nctf2026/gcp-token-scope
```

Sans argument, les deux JSON sont recherchés dans le dossier courant.

Sortie obtenue lors de la vérification locale :

```text
NCTF{sa_token_scope_read_the_bucket}
Longueur du clair : 36 octets
Rechiffrement : identique au Base64 fourni.
```

## 6. Conclusion et remédiation

Le défaut de sécurité illustré est un compte CI doté de permissions de lecture trop larges au niveau du projet. Le scellement local sert uniquement à matérialiser l’objet dans le challenge.

La remédiation conceptuelle est d’appliquer le **moindre privilège** : limiter les rôles aux buckets strictement nécessaires, séparer les identités CI et production, et retirer les droits hérités trop larges. Ajouter une restriction sur un bucket ne suffit pas si le même compte conserve un accès global hérité du projet.

Le point clé de la résolution était de distinguer **la graine SHA256** du **flux XOR dérivé par compteur**.
