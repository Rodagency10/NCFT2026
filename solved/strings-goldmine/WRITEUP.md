# strings-goldmine

## Challenge

**Points :** 70  
**Catégorie :** mobile / android  
**Difficulté :** beginner  
**Auteurs :** hibris, Clawd  
**Fichier :** `app-release.apk`  
**Format du flag :** `NCTF{...}`

> We pulled `app-release.apk` off a payments handset. Unzip it like any APK and poke around the decompiled sources and resources. One premium feature is unlocked from data shipped inside the app itself.
>
> Recover the unlock token. It is the flag. No network required.

## Résolution

Un APK est une archive ZIP. Celle-ci contient les sources décompilées et les ressources en clair.

`res/values/strings.xml` transporte un blob :

```
PSgLKhIeUS0QBG9UVVA8UlJIPV4KbRZBAVoxCxopHTIYGg==
```

`sources/com/vault/app/BuildConfig.java` contient la clé :

```
API_SECRET = "sk_live_tg_0f4c9a1b7d2e5"
```

`MainActivity.java` décode le blob en Base64, puis XOR chaque octet avec `API_SECRET`, en boucle. Le résultat est le jeton premium.

## Flag

```
NCTF{h4rdc0d3d_k3y_in_str1ngs_xml}
```
