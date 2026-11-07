# html-entities

## Challenge

**Catégorie :** warmup / web / encoding  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `page_snippet.txt`  
**Format du flag :** `NCTF{...}`

> `page_snippet.txt` is a run of `&#NNN;` codes — the kind a web page uses to spell out characters. Turn each code back into its character and read the flag.

## Résolution

Le fichier ne contient que des entités numériques HTML : `&#NNN;`, où `NNN` est le code décimal du caractère.

```
&#78;&#67;&#84;&#70;&#123;&#97;&#109;&#112;&#101;&#114;&#115;&#97;&#110;&#100;&#95;&#104;&#97;&#115;&#104;&#95;&#101;&#110;&#116;&#105;&#116;&#105;&#101;&#115;&#125;
```

Chaque code se convertit avec `String.fromCharCode` (ou `html.unescape`) :

| Entité | Caractère |
|--------|-----------|
| `&#78;` | `N` |
| `&#67;` | `C` |
| `&#84;` | `T` |
| `&#70;` | `F` |
| `&#123;` | `{` |
| `&#97;` … | `ampersand_hash_entities` |
| `&#125;` | `}` |

## Flag

```
NCTF{ampersand_hash_entities}
```
