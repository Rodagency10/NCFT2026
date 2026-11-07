# oxdefault--flush

## Challenge

**Points :** 106  
**Catégorie :** forensics  
**Difficulté :** medium  
**Auteur :** Oxdefault  
**Fichier :** `capture.pcap`  
**Format du flag :** `NCTF{...}`

> Un sous-traitant sur le départ a exfiltré des documents d'un poste de travail en enchaînant des périphériques USB de plus en plus discrets ; le SOC avait une capture `usbmon` en cours. Trois appareils ont été saisis. On les analyse dans l'ordre.
>
> **Épisode 1 — la clé.** Premier appareil : une simple clé USB de stockage de masse, branchée pendant la capture, sur laquelle un fichier a été copié. C'est le point d'entrée de l'enquête : retrouve le fichier, le flag est dedans.

## Résolution

La capture est au format `usbmon` (link type 220). Le trafic utile est du Bulk-Only Transport : des CBW `USBC` portent des commandes SCSI `WRITE(10)`, suivies des données écrites sur la clé.

Les écritures commencent au LBA 2048, par blocs de 512 octets. Recollées dans l'ordre des LBA, elles forment un PNG (`89 50 4E 47` … `IEND`). L'image affiche le flag.

## Flag

```
NCTF{t0ut_c3_qu1_3st_3cr1t_r3st3}
```
