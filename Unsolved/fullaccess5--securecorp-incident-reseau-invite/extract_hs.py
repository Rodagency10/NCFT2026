from scapy.all import PcapReader, Dot11, EAPOL, Raw
import struct

AP = 'ea:2a:ea:1e:a0:5a'
CLIENT = 'e8:fb:1c:bc:8c:1d'

def mac2b(m): return bytes(int(x,16) for x in m.split(':'))

msgs = []  # (idx, time, src, dst, keyinfo, replay, nonce, mic, eapol_bytes)
n = 0
for pkt in PcapReader('traffic-04.cap'):
    if not pkt.haslayer(EAPOL):
        continue
    d = pkt[Dot11]
    if d.addr2 not in (AP, CLIENT) or d.addr1 not in (AP, CLIENT):
        continue
    eap = bytes(pkt[EAPOL])
    # EAPOL-Key: type 3. Parse key frame
    if len(eap) < 95 or eap[1] != 3:
        continue
    # eap: ver(1) type(1) len(2) descr(1) keyinfo(2) keylen(2) replay(8) nonce(32) iv(16) rsc(8) id(8) mic(16) datalen(2) data
    keyinfo = struct.unpack('>H', eap[5:7])[0]
    replay = eap[9:17]
    nonce = eap[17:49]
    mic = eap[81:97]
    msgs.append((len(msgs), float(pkt.time), d.addr2, d.addr1, keyinfo, replay.hex(), nonce.hex(), mic.hex(), eap.hex()))
    if len(msgs) >= 8:
        break

for m in msgs:
    idx, t, src, dst, ki, replay, nonce, mic, eap = m
    # decode key info flags
    pairwise = (ki >> 3) & 1
    install = (ki >> 6) & 1
    ack = (ki >> 7) & 1
    micf = (ki >> 8) & 1
    secure = (ki >> 9) & 1
    # classify
    if ack and not micf: msg='M1'
    elif micf and not install and not ack and not secure: msg='M2'
    elif micf and install and ack: msg='M3'
    elif micf and secure and not ack: msg='M4'
    else: msg='?'
    print(f'{msg} src={src} dst={dst} ki={ki:#06x} replay={replay} nonce={nonce[:16]}... mic={mic}')

# Save first M1 (ANonce) and the M2 (SNonce + MIC + eapol) for cracking
import json
out={'ssid':'Wifi-Test','ap':AP,'client':CLIENT}
for m in msgs:
    idx,t,src,dst,ki,replay,nonce,mic,eap=m
    ack=(ki>>7)&1; micf=(ki>>8)&1; install=(ki>>6)&1; secure=(ki>>9)&1
    if ack and not micf and 'anonce' not in out:
        out['anonce']=nonce
    if micf and not install and not ack and not secure and 'snonce' not in out:
        out['snonce']=nonce; out['mic']=mic; out['eapol2']=eap; out['keyver']=ki & 0x7
open('hs.json','w').write(json.dumps(out,indent=1))
print('\nsaved hs.json keys:',list(out.keys()))
