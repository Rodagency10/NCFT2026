# git-archaeology

## Challenge

**Points :** 50  
**Catégorie :** forensics / misc  
**Difficulté :** easy  
**Auteurs :** hibris, Clawd  
**Fichier :** `logparse-cli.tar.gz`  
**Format du flag :** `NCTF{...}`

> Our intern force-pushed away a mistake. "It's gone," they said.
>
> You're handed a snapshot of the `logparse-cli` repository (the full working tree **and** its `.git` directory). At some point a real production credential was committed and then "removed." Recover the leaked credential.
>
> There is one obviously-fake placeholder token in the repo to ignore; the real one is the upload_token that was scrubbed from the analytics config.

## Résolution

L'archive contient le dépôt `logparse-cli` avec son dossier `.git`. L'historique visible de `main` s'arrête avant le secret :

```
2f6f820 Add scratch NOTES.txt
45e2991 Add analytics upload (token loaded from local config, not committed)
b818baa Add HTTP status-code breakdown helper
876a5cf Initial import: logparse CLI + example config
```

`NOTES.txt` contient un leurre, `NCTF{example_token_not_the_real_flag}`. `config.ini.example` n'a que `upload_token = REPLACE_ME`.

Le reflog, lui, a gardé le commit retiré par `git reset HEAD~1` :

```
b818baa HEAD@{2}: reset: moving to HEAD~1
13e018d HEAD@{3}: commit: wire up analytics upload (temp: real token, will scrub)
```

`git show 13e018d` affiche le `config.ini` qui avait été ajouté puis effacé de la branche. La clé `upload_token` de la section `[analytics]` est le flag.

## Flag

```
NCTF{d4ngling_c0mmit_lives_in_ref10g}
```
