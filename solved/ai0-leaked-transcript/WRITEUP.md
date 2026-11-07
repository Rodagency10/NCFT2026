# ai0-leaked-transcript

## Challenge

**Points :** 50  
**Catégorie :** ai  
**Difficulté :** beginner  
**Auteur :** Clawd  
**Fichier :** `transcript.json`  
**Format du flag :** `NCTF{...}`

> **HelixDesk** is Nimbus Robotics' internal support assistant. Someone exported one of its chat transcripts to JSON and shared the handout `transcript.json` in the wrong channel.
>
> In the visible conversation the assistant politely refuses to reveal anything sensitive. But an export is more than the words that were on screen. Somewhere in that file sits an internal "audit-handoff token" the assistant was told never to disclose — and it is the flag, only lightly obfuscated. Recover it.
>
> This is Level 0 of the AI track: zero inference, no live model, no service. Everything you need is in the single handout `transcript.json`.

## Résolution

La conversation visible ne contient que le refus de l’assistant. Le prompt système est pourtant copié dans `metadata.runtime_config.system_prompt`. Il y donne deux jetons d’audit :

- un ancien, « ROTATED OUT » le 2026-07-01 : `fXRuM3JydWNfdDBuX24zazB0X2QzdDR0MHJ7RlRDTg==`
- le jeton courant : `fWQzbDQzdjNyX3RwbTBycF9tM3Q1eXN7RlRDTg==`

Chacun est le flag écrit à l’envers, puis encodé en Base64. Le décodage Base64 suivi d’un retournement de la chaîne donne :

| Jeton | Clair |
|-------|-------|
| ancien | `NCTF{r0t4t3d_t0k3n_n0t_curr3nt}` |
| courant | `NCTF{sy5t3m_pr0mpt_r3v34l3d}` |

Le flag est celui marqué current.

## Flag

```
NCTF{sy5t3m_pr0mpt_r3v34l3d}
```
