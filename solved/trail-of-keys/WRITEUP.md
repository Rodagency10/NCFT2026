# trail-of-keys

## Challenge

**ID :** 51  
**Catégorie :** cloud  
**Points :** 280 (dynamique, de 300 à 100)  
**Auteurs :** hibris, Clawd  
**Fichiers :** `cloudtrail.json`, `exfil-notes.json`  
**Format du flag :** `NCTF{...}`

> A CloudTrail export (`cloudtrail.json`) from one busy hour on the `kekeli-prod` account, plus an object (`exfil-notes.json`) that one session wrote to a scratch bucket. Someone read a sensitive secret and walked it out.
>
> Trace who did it, then open what they left behind. The flag is inside.

## Résolution

`cloudtrail.json` couvre une heure sur le compte `333322221111`. Quatre sessions apparaissent.

| Heure | Clé de session | Action |
|---|---|---|
| 09:01 | `ASIA5BACKUP0SESSION02` | `PutObject` d'une sauvegarde dans `kekeli-backups` |
| 09:05 | `ASIA5METRIC0SESSION3` | `GetMetricData` |
| 09:07 | `ASIA5EXFIL0SESSION07` | `ListSecrets`, puis `GetSecretValue` sur `prod/customer-export-Kd93js`, puis `PutObject` de `kekeli-scratch/tmp/notes.bin` |
| 09:10 | `ASIA5DECOY0SESSION09` | `GetSecretValue` sur `dev/grafana-Zz01` |

La session qui lit le secret de production et dépose l'objet est `ASIA5EXFIL0SESSION07`, assumée par l'utilisateur `session-9f2c` (`AKIALEAK0MALLORY0001`) via le rôle `support-readonly`. La lecture de `dev/grafana` est un leurre.

`exfil-notes.json` décrit le scellement : le flux XOR est dérivé du SHA-256 de cette clé `ASIA`. Le chiffré fait 40 octets. Répéter le digest de 32 octets ne suffit pas. La convention déjà vue sur `gcp-token-scope` et `sub-wildcard` ouvre le fichier :

```text
seed = SHA256(UTF8(ASIA5EXFIL0SESSION07)).digest()
bloc[i] = SHA256(seed || uint32_be(i)).digest()
flux = concaténation des blocs, tronquée à 40 octets
clair = chiffré XOR flux
```

Le compteur commence à 0. Les 40 octets prennent le bloc 0 entier et 8 octets du bloc 1.

## Flag

```
NCTF{cloudtrail_traced_the_asia_session}
```
