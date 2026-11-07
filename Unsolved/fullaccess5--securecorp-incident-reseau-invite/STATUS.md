# STATUS — securecorp-incident-reseau-invite (forensics, 0 solve)

**État : 5 champs sur 6 verrouillés. Bloqué sur le wording exact de #3 (nom de l'attaque).**

Flag format : `NCTF{1_2_3_4_5_6}` = `NCTF{SSID_BSSID_attaque_heure_password_MITRE}`

## Champs CERTAINS (ne pas re-tester)

| # | Champ | Valeur | Preuve |
|---|---|---|---|
| 1 | SSID | `Wifi-Test` | bytes beacon `576966692d54657374`, un seul réseau dans la capture |
| 2 | BSSID | `ea:2a:ea:1e:a0:5a` | addr3 du beacon (canal 10) |
| 4 | Heure 1ʳᵉ trame 4-Way Handshake | `13:24:51` | 1er EAPOL = M1 à 13:24:51.624 UTC ; capture 13:24:09→13:36:47 UTC ; Togo = UTC+0 ; « vers 13h » OK ; format imposé HH:MM:SS |
| 5 | Password WPA2 | `30secondstomars` | **MIC HMAC-SHA1 validé** (crack rockyou) — cryptographiquement certain |
| 6 | MITRE Initial Access | `T1669` | hint 978 : « technique récente Initial Access dédiée à l'accès sans fil » = T1669 « Wi-Fi Networks » |

Détails techniques :
- Attaque = flood de **196 258 trames deauth** (reason code 7), src = BSSID (spoofé),
  dst = `ff:ff:ff:ff:ff:ff` (broadcast), à partir de 13:24:09.
- Handshake craqué : AP `ea:2a:ea:1e:a0:5a` ↔ client `e8:fb:1c:bc:8c:1d`, keyver=2 (WPA2).
- 2 hints (gratuits/−points) : 977 = filtrer EAPOL pour le handshake+horodatage ;
  978 = technique MITRE récente dédiée au sans-fil (= T1669).

## BLOCAGE : #3 = nom de l'attaque

Attaque = déauthentification (deauth flood). **Wordings déjà testés → tous `incorrect` :**
`Deauthentication`, `Deauth`, `Deauthentication Attack`, `Deauth Attack`,
`Deauthentication-Attack`, `Deauthentication Flood`, `Disassociation`,
`deauthentication`, `Deauthentication attack`, `désauthentification`,
`Deauthentification`, `deauthentification`, `Désauthentification`, `deauth`, `DeAuth`.

Variantes de fuseau (#4) testées aussi : 12/14/15:24:51 → toutes incorrect (confirme 13:24:51).
BSSID uppercase testé → incorrect.
(Toutes combinées avec T1669 + les champs certains.)

## PISTES À ESSAYER (à reprendre)

1. **Wordings #3 non encore testés** :
   - `Broadcast Deauthentication` / `Deauthentication Broadcast`
   - `802.11 Deauthentication` / `802.11 Deauth`
   - `Deauthentication Frame Flooding` / `Deauth Flooding`
   - `WiFi Deauthentication Attack`
   - terme français complet : `Attaque par désauthentification`
2. **Format d'un autre champ** (si #3 standard échoue toujours) :
   - BSSID sans `:` → `ea2aea1ea05a` (et majuscule)
   - heure sans `:` ou autre format
   - vérifier casse password/SSID
3. **Idée** : demander/chercher si l'auteur attend le nom tel qu'affiché par un outil
   précis (aircrack-ng, Wireshark Info column = « Deauthentication »).

## Reproduire
```bash
py analyze.py        # recon SSID/BSSID/deauth/EAPOL
py extract_hs.py     # -> hs.json (ANonce/SNonce/MIC/EAPOL M2)
py crack_mp.py rockyou.txt   # -> 30secondstomars
```

## Soumission (session arène)
- id challenge = 426
- ~24 tentatives faites, toutes `incorrect`. Consigne user : **ne pas re-spammer** ;
  tester seulement des wordings #3 ciblés, idéalement après confirmation du format attendu.
