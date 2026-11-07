# bitvault-psbt

## Challenge

**ID :** 537  
**Catégorie :** blockchain  
**Points :** 350  
**Auteurs :** hibris, Clawd  
**Fichiers :** `ENVELOPE_FORMAT.md`, `treasury_screen.py`, `settlement_relay.py`, `cosigner.py`, `signed_draft.txt`, `incident_brief.md`  
**Format du flag :** `NCTF{...}`

> **BitVault**'s treasury moves funds through a 2-of-2 co-signer. Every payout is screened against the operation the desk approved and only then relayed to the network. Last cycle a routine payroll payout was co-signed -- and what settled on-chain instead swept the whole treasury to an address nobody recognizes.
>
> No server is running. The desk's post-mortem note is sealed under the settlement the co-signer *actually relayed*; reconstruct that settlement from the shipped files alone and recover the note.

## Résolution

L'enveloppe `BVLT-COSIGN/2` peut contenir plusieurs segments. Les deux composants ne lisent pas le même :

- `treasury_screen.first_segment` autorise le **premier** segment. Il doit payer exactement `499990000` sat vers `76a914b0bfa5e2c1d3e4f5a6b7c8d9e0f1a2b3c4d5e6f788ac` et porter les deux endorsements.
- `settlement_relay.last_segment` diffuse le **dernier** segment, sans revérifier le destinataire.

Le brouillon signé (`signed_draft.txt`) passe l'écran. On lui accole un second segment qui reprend ses deux entrées (`300000000` + `200000000` sat) et les verse toutes, sans rendu, vers le script relevé sur le nœud :

```text
0014deadbeefcafebabe0011223344556677889900ab    500000000 sat
```

Le premier segment est le JSON du brouillon, sans le saut de ligne final du fichier. La note se déchiffre avec la clé prévue par `recover_note` : `SHA256(segment_écran || "|" || règlement || "|vault-note-seal")`, puis un flux `SHA256(clé || uint32_be(i))`.

## Flag

```
NCTF{polyglot_envelope_drains_the_cosigned_treasury}
```
