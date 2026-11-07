# sub-wildcard — NCTF2026 Togo

## Résultat

`NCTF{oidc_sub_wildcard_assumed_the_role}`

Flag extrait et vérifié localement, **non soumis à la plateforme**.

## Contexte et garanties

L'énoncé décrit explicitement un CTF cloud avec cinq jetons représentés par des
ensembles de claims JSON et un secret « sealed for this handout ». Il ne fournit
pas de JWT signés à utiliser comme credentials réels. L'analyse n'a fait aucune
connexion réseau, authentification AWS, émission de jeton ou prise de rôle réelle.
Aucun programme fourni n'a été exécuté. Aucun WRITEUP n'a été consulté.

Les cinq JSON ont été extraits individuellement du ZIP après contrôle de chemin,
taille et type ; ils sont identiques aux entrées originales. Les quatre fichiers
alternatifs dans `fresh/` sont eux aussi identiques aux ressources principales.
Le ZIP original n'a pas été modifié.

## 1. Identifier le candidat compatible

Le rôle `ci-deployer` autorise conceptuellement `sts:AssumeRoleWithWebIdentity`
avec le fournisseur GitHub Actions configuré dans sa trust policy. Les contraintes
pertinentes sont :

- fournisseur correspondant à l'émetteur GitHub Actions ;
- `StringEquals` sur l'audience : `sts.amazonaws.com` ;
- `StringLike` sur le sujet : `repo:kekeli-cloud/*`.

Dans ces ressources, les cinq candidats ont le bon émetteur et la bonne audience.
Seul le candidat **#3**, décrit comme un fork dans l'organisation autorisée, a
le préfixe de sujet requis.

| Candidat | Résultat du modèle | Raison |
|---|---|---|
| #1 | Rejeté | Organisation différente. |
| #2 | Rejeté | Organisation prolongée par un suffixe : le `/` après le nom attendu manque à la position requise. |
| #3 | Compatible | Fork situé dans l'organisation attendue. |
| #4 | Rejeté | Nom d'organisation contracté, différent du préfixe littéral. |
| #5 | Rejeté | Découpage organisation/dépôt différent. |

Le piège n'est donc pas un nom d'organisation ressemblant au bon : c'est un dépôt
non prévu **dans** la bonne organisation. Le `*` accepte toute la suite du sujet,
y compris le nom du dépôt, les séparateurs et la référence de branche. Aucune
condition de la politique ne limite le sujet à un dépôt précis ni à une branche
protégée. Les autres claims descriptifs ne créent pas de restrictions implicites.

Cela prouve la compatibilité avec les règles **fournies**, pas une prise de rôle
réelle : signatures, validité temporelle et configuration effective du fournisseur
ne sont pas vérifiables à partir de ces seuls ensembles de claims.

## 2. Vérifier l'accès au secret

La politique attachée au rôle autorise `secretsmanager:GetSecretValue` sur le motif
de ressource correspondant aux secrets `prod/release-signing-*` du scénario.
L'ARN de l'objet `prod/release-signing-key` satisfait ce motif, suffixe compris.
La chaîne conceptuelle est donc : candidat #3 compatible avec la confiance → rôle
auquel la lecture du secret est accordée → récupération locale du secret scellé.

## 3. Déchiffrement local

Le champ `Note` annonce un flux XOR fondé sur SHA256 du sujet OIDC admissible.
Le champ `SecretStringCiphertextB64` se décode en **40 octets**. Il s'agit d'un
encodage Base64, pas d'un JWT et pas encore du flag en clair.

Comme dans `gcp-token-scope`, l'indication de scellement ne précise pas entièrement
l'expansion du flux. Répéter directement le digest SHA256 ne donne pas du UTF-8.
La convention déjà découverte sur l'autre challenge a ensuite été testée ici :

```text
seed = SHA256(UTF8(sub du candidat admissible)).digest()
bloc[i] = SHA256(seed brut || uint32_be(i)).digest()
flux = concaténation des blocs, tronquée à la longueur du chiffré
clair = chiffré XOR flux
```

Le compteur commence à zéro et occupe quatre octets big-endian. Pour 40 octets,
on utilise le bloc zéro entier puis huit octets du bloc un. Le digest brut n'est
pas remplacé par sa représentation hexadécimale.

L'expansion reste une convention **inférée**, non une précision explicitement
écrite dans la Note. Sa validation ici repose sur :

1. un flag intégral cohérent, et pas seulement un préfixe reconnaissable ;
2. un rechiffrement identique au champ Base64 d'origine ;
3. une seconde implémentation calculant le flux octet par octet, avec `struct.pack` ;
4. un test des cinq sujets, dont seul celui du candidat #3 donne un flag complet ;
5. une vérification indépendante du choix #3 par simple préfixe littéral.

Le rechiffrement contrôle la cohérence du calcul mais ne remplace pas une validation
sur la plateforme. Celle-ci n'a pas été effectuée par nous.

## Reproduction

Bibliothèque standard Python uniquement :

```sh
python3 /workspace/nctf2026/sub-wildcard/analysis/solve.py
python3 /workspace/nctf2026/sub-wildcard/analysis/verify.py
```

`solve.py` accepte aussi un chemin de dossier en argument. Il ne sort aucun
contenu de jeton, identifiant de clé ou clé privée.

Sortie du solveur :

```text
Candidat #1 : rejeté
Candidat #2 : rejeté
Candidat #3 : compatible
Candidat #4 : rejeté
Candidat #5 : rejeté
Permission GetSecretValue : autorisée pour le secret fourni
NCTF{oidc_sub_wildcard_assumed_the_role}
Clair : 40 octets ; rechiffrement Base64 identique
Analyse locale uniquement ; flag non soumis à la plateforme.
```

Les contrôles sont aussi enregistrés dans `verification.json`.

## Remédiation conceptuelle

Restreindre la confiance au dépôt et à la référence/environnement nécessaires,
plutôt qu'à tous les sujets d'une organisation ; contrôler qui peut créer et
modifier ses dépôts ; limiter séparément les secrets accessibles au rôle.
Ne pas confondre un contrôle de confiance OIDC avec les permissions que le rôle
possède une fois la confiance satisfaite.
