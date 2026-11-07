# proxy-collision

## Challenge

**ID :** 15  
**Catégorie :** blockchain  
**Points :** 300  
**Auteurs :** hibris, Clawd  
**Fichiers :** `Proxy.sol`, `Logic.sol`, `proxy_storage.json`  
**Format du flag :** `NCTF{...}`

> You get an upgradeable `Proxy.sol`, its `Logic.sol` implementation, and a raw storage dump of the proxy (`proxy_storage.json`). One slot holds the note you want. Work out the storage layout to read it.

## Résolution

Le proxy range `implementation`, `admin` et `paused` dans les slots 0, 1 et 2. `Logic.value` est aussi déclaré en premier, donc dans le slot 0. Un `delegatecall` vers `setValue` écrit donc l'implémentation du proxy.

Dans le dump, le slot 0 contient le flag en ASCII, complété par des zéros. Le slot 3 commence par `NCTF{wrong_slot_try_the_collisio` et ne se ferme pas : c'est un leurre.

## Flag

```
NCTF{delegatecall_hits_slot0}
```
