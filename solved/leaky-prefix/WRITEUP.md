# leaky-prefix

## Challenge

**Points :** 70  
**Catégorie :** cloud / aws / s3 / bucket-policy  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichiers :** `bucket-policy.json`, `object-index.json`, et les corps d'objets  
**Format du flag :** `NCTF{...}`

> A snapshot of the `kekeli-media-prod` S3 bucket: its live bucket policy (`bucket-policy.json`), the object inventory (`object-index.json`), and every object body under `objects/`. Marketing swears only their public assets are world-readable.
>
> Find the object an anonymous visitor can actually read. The flag is in it.

## Résolution

La policy autorise `s3:GetObject` à `Principal: "*"` sur une seule ressource :

```
arn:aws:s3:::kekeli-media-prod/assets/public*
```

Le `*` est un préfixe de chaîne, et il n'y a pas de `/` après `public`. Donc tout objet dont la clé commence par `assets/public` est lisible, y compris un dossier qui n'est pas `assets/public/`.

| Clé | Lisible anonymement |
|-----|---------------------|
| `assets/public/logo.txt` | oui |
| `assets/public/banner.txt` | oui |
| `assets/public/press-kit.txt` | oui |
| `assets/public-backup/db-snapshot-note.txt` | oui, à cause du `*` |
| `internal/roadmap.txt` | non |
| `internal/old-ctf-note.txt` | non |

`old-ctf-note.txt` contient un leurre, `NCTF{not_the_flag_internal_only}`, et n'est de toute façon pas couvert par l'Allow. Le fichier réellement public hors du dossier marketing est `assets/public-backup/db-snapshot-note.txt`.

## Flag

```
NCTF{public_read_on_the_wrong_prefix}
```
