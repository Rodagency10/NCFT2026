# strings-lie

## Challenge

**ID :** 191  
**Catégorie :** reverse  
**Points :** 139 (dynamique, de 150 à 50)  
**Auteurs :** hibris, Clawd  
**Fichier :** `chall` (ELF x86-64 statique, 14472 octets)  
**Format du flag :** `NCTF{...}`

> Un petit binaire « secret vault » affiche un flag dans sa bannière. Le soumettre le fait refuser. Retrouver le vrai flag. Tout est dans le fichier, sans réseau.

## Résolution

La bannière contient `NCTF{y0u_grepp3d_th3_f4ke_0ne}`. Ce n'est qu'une chaîne de `.rodata`. Le vrai flag est calculé après une passe-phrase.

La passe-phrase fait 23 octets. Pour l'indice `i`, avec `ecx = 3 + 7*i`, le binaire exige

`(pass[i] XOR 0x5A) + ecx` ≡ `table[i]` (octet bas)

La table est à l'adresse `0x20c0`. L'inversion donne `unw1nd_th3_math_by_h4nd`.

Le flag fait 31 octets. Il est produit par `pass[i % 23] XOR enc[i]`, où `enc` est la table de 31 octets à `0x20a0`. Le modulo 23 est la division compilée (`mul` par `0x642c8590b21642c9`).

## Flag

```
NCTF{str1ngs_l1e_read_the_c0de}
```
