# auth-timeline

## Challenge

**ID :** 97  
**Catégorie :** forensics  
**Points :** 132 (dynamique, de 150 à 50)  
**Auteurs :** hibris, Clawd  
**Fichier :** `auth.log`  
**Format du flag :** `NCTF{...}`

> A public-facing server was compromised overnight. All we salvaged before the box was reimaged is its `auth.log`. It is mostly internet background noise, but one intruder actually got in and ran a command.
>
> Reconstruct what happened, find the command the intruder ran, and recover the string it left behind. That string is your flag.

## Résolution

Le journal est surtout une pluie d'échecs SSH. Trois connexions par clé publique (`deploy`, `ubuntu`, `git`) lancent des commandes anodines : redémarrage de nginx, lecture de `syslog`, `git pull`.

L'intrusion est la seule authentification par mot de passe qui aboutit. L'adresse `203.0.113.45` enchaîne les échecs sur `root` et `admin`, puis :

```text
Mar 11 10:44:42 web01 sshd[25605]: Accepted password for root from 203.0.113.45 port 41200 ssh2
Mar 11 10:45:22 web01 sshd[25605]: pam_unix(sshd:session): session opened for user root by (uid=0)
Mar 11 10:46:10 web01 audit[25605]: USER_CMD uid=0 cmd="echo ZmxhZz1OQ1RGe2JydXQzZjByYzNfdGgzbl9zdWNjM3NzXzBuX3IwMHR9 | base64 -d > /root/.ok"
```

Le même PID `25605` relie l'acceptation, l'ouverture de session et la commande. Le base64 décodé est `flag=NCTF{brut3f0rc3_th3n_succ3ss_0n_r00t}`, écrit dans `/root/.ok`.

## Flag

```
NCTF{brut3f0rc3_th3n_succ3ss_0n_r00t}
```
