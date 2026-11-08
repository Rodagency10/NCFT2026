# firmware-blob (hardware, easy)

**ID :** 110  
**Points :** 150  
**Auteurs :** hibris, Clawd  
**Fichier :** `firmware.bin`  
**Format :** `NCTF{...}`

`firmware.bin` a été lu sur la flash d'un appareil. Il commence par un petit en-tête maison et une table de sections nommées, puis les données brutes. Une section n'est pas du texte lisible. Il faut parser le conteneur, trouver la section du flag et en retrouver le contenu.

## Méthode

L'en-tête fait 8 octets : magic `FWB1`, octets de version `02 01`, puis le nombre de sections en `uint16` little-endian (`3`).

Chaque entrée de table fait 20 octets : nom sur 8 octets, offset `uint32` LE, taille `uint32` LE, drapeaux `uint32` LE.

| Section | Offset | Taille | Drapeaux | Contenu |
|---------|--------|--------|----------|---------|
| `.boot` | 68 | 34 | 0 | `bootloader v1.2 (c) acme embedded` |
| `.key` | 102 | 4 | 0 | `5a 13 a7 6c` |
| `.flag` | 106 | 35 | 1 | 35 octets illisibles |

Le drapeau `1` marque la section chiffrée. Les 35 octets se déchiffrent par XOR avec la clé de 4 octets, répétée.

## Flag

`NCTF{xor_section_firmware_unpacked}`
