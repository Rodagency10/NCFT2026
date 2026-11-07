# typosquat-lockfile (supplychain, easy)

**Flag :** `NCTF{typ0squ4t_expres_not_express_7c2e}`

## Démarche
1. `package-lock.json` verrouille 5 paquets. 4 légitimes (`express`, `lodash`,
   `chalk`, `debug`) résolus depuis `https://registry.npmjs.org`.
2. **Dépendance frauduleuse : `expres` 4.18.9**
   - typosquat d'`express` (un seul `s`)
   - `resolved` depuis un registre pirate : `https://npm-registry-mirror.dev/...`
   - archive plus volumineuse (285 o vs ~188 o)
3. Extraction de `expres-4.18.9.tgz` → `package/index.js` :
   ```js
   // telemetry helper
   var _p = 'GxAHEag0rKNjp3S1AUEsMKujpzImK25iqS9yrUOlMKAmKmqwZzI9';
   module.exports = require('http');
   ```
4. Désobfuscation de `_p` : **ROT13 puis base64**
   - ROT13 → `TkNURnt0eXAwc3F1NHRfZXhwcmVzX25vdF9leHByZXNzXzdjMmV9`
   - base64 → `NCTF{typ0squ4t_expres_not_express_7c2e}`

## One-liner
```bash
py -c "import base64,codecs; print(base64.b64decode(codecs.encode('GxAHEag0rKNjp3S1AUEsMKujpzImK25iqS9yrUOlMKAmKmqwZzI9','rot13')).decode())"
```
