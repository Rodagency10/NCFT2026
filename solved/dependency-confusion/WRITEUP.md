# dependency-confusion

## Challenge

**ID :** 203  
**Catégorie :** supplychain  
**Points :** 300 (dynamique, de 300 à 100)  
**Auteurs :** hibris, Clawd  
**Fichiers :** `registry-internal.json`, `registry-public.json`, `acme-telemetry-1.2.3.tgz`, `acme-telemetry-9.9.9.tgz`  
**Format du flag :** `NCTF{...}`

> Notre chaîne de build a récupéré le paquet interne `acme-telemetry` — mais deux registres le publient. On vous donne les métadonnées des deux registres (`registry-internal.json`, `registry-public.json`) et toutes les archives `.tgz` correspondantes.
>
> Reproduisez ce que l'installeur a réellement téléchargé, inspectez cette archive et récupérez le flag qui y est dissimulé.

## Résolution

Le registre interne marque `1.2.3` comme `latest`. Le registre public marque `9.9.9`. Les empreintes SHA1 des deux archives correspondent aux champs `dist.shasum`.

npm retient la version sémantique la plus haute lorsqu'il voit le même nom sur les deux registres. L'archive réellement installée est donc `acme-telemetry-9.9.9.tgz`.

Son `package.json` définit un script `postinstall`. L'argument passé à `node -e` est une chaîne base64. Son décodage contient le flag. La commande n'a pas été exécutée.

## Flag

```
NCTF{d3p_c0nfusion_higher_version_wins_a1f7}
```
