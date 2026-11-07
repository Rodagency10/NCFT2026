# fullaccess5 — securecorp-incident-reseau-invite (forensics, medium)

**Capture :** `traffic-04.cap` (pcap-LE, 283 933 paquets, 802.11)

## Les 6 éléments du flag `NCTF{1_2_3_4_5_6}`

| # | Élément | Valeur |
|---|---|---|
| 1 | SSID ciblé | `Wifi-Test` |
| 2 | BSSID | `ea:2a:ea:1e:a0:5a` |
| 3 | Attaque de déconnexion | Deauthentication |
| 4 | 1ʳᵉ trame du 4-Way Handshake | `13:24:51` |
| 5 | Mot de passe WPA2 | `30secondstomars` |
| 6 | MITRE ATT&CK Initial Access | `T1669` (Wi-Fi Networks) |

**Flag proposé :**
`NCTF{Wifi-Test_ea:2a:ea:1e:a0:5a_Deauthentication_13:24:51_30secondstomars_T1669}`
(#3 = wording exact non confirmé — voir STATUS.md)

## Démarche

Tout en Python/scapy (pas de tshark/aircrack dispo).

1. **SSID / BSSID / canal** — parse des beacons :
   `ea:2a:ea:1e:a0:5a` → SSID `Wifi-Test`, canal 10.
2. **Attaque** — 196 258 trames **deauth** (reason code 7), source = BSSID
   (spoofé), destination `ff:ff:ff:ff:ff:ff` (broadcast), à partir de 13:24:09.
   = attaque par **déauthentification** (flood) pour forcer la reconnexion.
3. **Handshake** — filtre EAPOL : 265 trames. 1ʳᵉ trame (M1) à **13:24:51**
   entre AP `ea:2a:ea:1e:a0:5a` et client `e8:fb:1c:bc:8c:1d`.
   keyver=2 (WPA2, HMAC-SHA1). Togo = UTC+0 → heure = 13:24:51.
4. **Crack WPA2** — extraction ANonce (M1) + SNonce/MIC (M2), reconstruction
   PTK (PBKDF2-HMAC-SHA1 4096, SSID=salt) + vérif MIC HMAC-SHA1.
   Cracker multiprocessing sur rockyou → **`30secondstomars`** (MIC validé).
5. **MITRE** — obtention d'un accès au réseau via le PSK WiFi cracké (credential
   valide) = **T1669 Wi-Fi Networks** (confirmé hint) (tactique Initial Access).

## Scripts
- `analyze.py` — recon (SSID/BSSID/deauth/EAPOL)
- `extract_hs.py` — extraction du 4-way handshake → `hs.json`
- `crack.py` / `crack_mp.py` — crack WPA2 (mono / multiprocessing)
