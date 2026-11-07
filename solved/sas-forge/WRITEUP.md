# sas-forge

## Challenge

**ID :** 49  
**Catégorie :** cloud  
**Points :** 450  
**Auteurs :** hibris, Clawd  
**Fichiers :** `leaked-account-key.txt`, `sas-example.txt`, `blob-index.json`, `sas-params.json`, `flag-blob.enc`  
**Format du flag :** `NCTF{...}`

> An Azure Storage account key leaked into a backup (`leaked-account-key.txt`), a working SAS URL for a public sample blob (`sas-example.txt`), the container inventory (`blob-index.json`), the SAS parameters for a private blob (`sas-params.json`), and that private blob sealed for the handout (`flag-blob.enc`).
>
> Reach the private blob offline, then open it. The flag is inside.

## Résolution

La clé de compte est le base64 `a2VrZWxpLWRldi1mYWtlLXN0b3JhZ2Uta2V5LTAwMDA=`, soit les 32 octets `kekeli-dev-fake-storage-key-0000`. Elle signe un SAS de service (version `2020-12-06`) pour le blob privé.

La chaîne à signer, champs séparés par `\n`, est :

```text
r

2026-12-31T23:59:59Z
/blob/kekelistorage/private-releases/media-svc/RELEASE_NOTES.enc



https
2020-12-06
b
```

Les champs vides (`st`, `si`, `sip`, `sst`, `ses` et les `rsc*`) restent présents. La signature est `base64(HMAC-SHA256(clé, chaîne))` :

```text
muTn0LxbLhmJ4/qklPNQ3el5LPCULr+yeLF4PIwqG5Q=
```

`flag-blob.enc` indique que le flux XOR est dérivé de cette signature. La graine est `SHA256` du base64, puis chaque bloc `i` vaut `SHA256(graine || uint32_be(i))`. Répéter le seul condensat ne redonne pas le texte.

## Flag

```
NCTF{forged_service_sas_with_leaked_key}
```
