# thierry8petstar--ghostflag (web, easy)

**Flag :** `NCTF{bf37a7d26fd874193ae4aa79}`

## Démarche (content discovery + leurres)
1. **Source de `/`** : commentaires HTML truffés d'indices pointant vers
   `/secret_files/fnd_password/`, un pattern `backup_dd_mm_yyyy.sql`, une API, etc.
2. **`/robots.txt`** confirme : `Disallow: /secret_files/`, `/backup`, `/admin`.
3. **Leurres identifiés :**
   - `/api/agent/check` (POST `{agent_id:"GHOST-xxxx"}`) → **faux flag**
     `NCTF{FAK3_F14G_TR0P_F4CILE_OUBIEN?}`.
   - `/admin`, `/backup` → `403 Acces interdit` (blocage dur, pas de bypass).
   - `/secret_files/fnd_password/credentials.txt` → creds "DEPRECATED" (leurre).
   - `/secret_files/fnd_password/backup.txt` → hash bcrypt marqué "leurre".
4. **L'app est un Flask catch-all** : toute route inconnue renvoie l'index.
   Les vrais fichiers (servis) renvoient leur contenu → on les trouve en
   filtrant les réponses ≠ index.
5. **Vrai flag** par fuzz de noms de fichiers dans le dossier, avec plusieurs
   extensions :
   ```
   GET /secret_files/fnd_password/flag.json
   → {"mission":"ECHO-7","flag":"NCTF{bf37a7d26fd874193ae4aa79}",
      "agent":"ECHO-7-ALPHA","clearance":"TOP_SECRET"}
   ```
   (Piège : `flag.txt` renvoie l'index ; c'était `flag.json`.)

## Leçon
Classique « exposed sensitive directory » : robots.txt + commentaires révèlent un
dossier, truffé de leurres pour noyer le poisson. Fuzzer les extensions (.json,
pas que .txt) et filtrer la page catch-all pour isoler les vrais fichiers.
