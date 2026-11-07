# the-darknova--mirage-1

## Challenge

**ID :** 428  
**Catégorie :** forensics  
**Points :** 100 (dynamique, de 100 à 50)  
**Auteur :** The-darknova  
**Fichier :** `mirage-1.pcapng` (8234420 octets)  
**Format du flag :** `NCTF{...}`

> Lors d'une ronde de surveillance de routine, notre SOC a détecté une transmission inhabituelle transitant sur le réseau. L'analyste de garde affirme avoir vu passer un « fantôme » à travers le flux avant que la connexion ne soit coupée. À vous d'inspecter la capture réseau et de lever le voile sur ce mirage.

## Résolution

La capture compte 7550 paquets. Le flux qui sort du trafic courant est l'UDP `192.168.98.7:42387` vers `192.168.8.93:5000` : 3758 datagrammes de 1328 octets, sans trou de séquence.

Chaque datagramme commence par un en-tête RTP version 2, type de charge 33. Ce type transporte du MPEG-TS. Après les 12 octets d'en-tête, la charge fait 1316 octets, soit exactement 7 paquets TS de 188 octets, tous synchronisés sur `0x47`. Le programme contient une vidéo H.264 360×640 à 30 images par seconde (environ 30 s) et une piste AAC. Les PID présents sont le PAT, la PMT, la vidéo `0x41` et l'audio `0x42`.

La vidéo est une caméra de nuit. Le texte « Not letting yall forget about this » reste affiché. En comparant chaque image à l'image médiane, un bandeau sombre n'existe que sur quelques images, collé en haut du cadre (lignes 96 à 117). Le seuil des pixels blancs de ce bandeau donne les glyphes `N`, `C`, `TF{oo`, `h`, `h`, `h`, `_a`, `_g`, `host_g`, `g}`.

## Flag

```
NCTF{oohhh_a_ghost_gg}
```
