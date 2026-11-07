# morse-code

## Challenge

**Points :** 25  
**Catégorie :** warmup / classical / morse  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `signal.txt`  
**Format du flag :** `NCTF{...}`

> `signal.txt` is a line of dots (`.`) and dashes (`-`). Letters are separated by spaces and words by `/`. Decode the message, then wrap the lowercase words with underscores as the flag body.
>
> Example: if it spelled `HELLO WORLD`, the flag is `NCTF{hello_world}`.

## Résolution

Le signal est :

```
-- --- .-. ... . / -.-. --- -.. . / .. ... / . .- ... -.--
```

Les espaces séparent les lettres, `/` sépare les mots. Alphabet Morse usuel (`.` court, `-` long) :

| Morse | Lettre |
|-------|--------|
| `--` | M |
| `---` | O |
| `.-.` | R |
| `...` | S |
| `.` | E |
| `-.-.` | C |
| `-..` | D |
| `..` | I |
| `.-` | A |
| `-.--` | Y |

Le message clair est `MORSE CODE IS EASY`. En minuscules, les espaces deviennent des `_`.

## Flag

```
NCTF{morse_code_is_easy}
```
