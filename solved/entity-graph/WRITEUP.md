# entity-graph (osint, easy)

**ID :** 163  
**Points :** 150  
**Auteurs :** hibris, Clawd  
**Fichiers :** `nodes.csv`, `edges.csv`  
**Format :** `NCTF{...}`

Le CERT.tg a exporté son graphe Maltego. Le persona `z3ro_237` a revendiqué la fuite. Il faut l'attribuer à une personne réelle. Le flag n'est pas écrit dans le dossier : il se dérive du chemin de pivot vérifié.

## Méthode

Les relations `mentions`, `similar_name` et `follows` mènent à des leurres. Yao Mensah porte le faux flag `NCTF{wrong_pivot_speculative_link}`. Ama Dede et Kodjo Ali ne sont pas l'opérateur.

Le seul chemin d'attributs confirmés, depuis la graine, est :

`z3ro_237` → `z3r0.lome@protomail.tg` → `cobra_lome` → `+22890114477` → `356938035643809` → `1KossiViAgbeko9xQwErTyUiOpAsDfGh` → `mining-togo.tg` → `Kossivi Agbeko`

La chaîne signée est celle des colonnes `value`, jointe par `|` :

`z3ro_237@x|z3r0.lome@protomail.tg|cobra_lome@social|+22890114477|356938035643809|1KossiViAgbeko9xQwErTyUiOpAsDfGh|mining-togo.tg|Kossivi Agbeko`

La clé HMAC-SHA256 est le `label` de la personne démasquée : `identity`. On garde les 24 premiers hexadécimaux.

## Flag

`NCTF{79dcf5d4d250f13b9940549a}`
