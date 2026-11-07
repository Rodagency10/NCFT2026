from scapy.all import PcapReader, Dot11, Dot11Beacon, Dot11Elt, Dot11Deauth, EAPOL, Dot11ProbeResp
import collections, datetime

ssids = collections.Counter()          # bssid -> ssid
bssid_ssid = {}
beacon_count = collections.Counter()
deauth = []
eapol = []
mgmt_subtypes = collections.Counter()
chan = {}

n = 0
for pkt in PcapReader('traffic-04.cap'):
    n += 1
    if not pkt.haslayer(Dot11):
        continue
    d = pkt[Dot11]
    # Beacon / ProbeResp -> SSID + BSSID + channel
    if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
        bssid = d.addr3
        elt = pkt.getlayer(Dot11Elt)
        while isinstance(elt, Dot11Elt):
            if elt.ID == 0:  # SSID
                try: s = elt.info.decode('utf-8', 'replace')
                except: s = str(elt.info)
                if bssid: bssid_ssid[bssid] = s
            elif elt.ID == 3 and len(elt.info) >= 1:  # DS param = channel
                if bssid: chan[bssid] = elt.info[0]
            elt = elt.payload.getlayer(Dot11Elt)
        if pkt.haslayer(Dot11Beacon) and bssid:
            beacon_count[bssid] += 1
    # Deauth
    if pkt.haslayer(Dot11Deauth):
        deauth.append((pkt.time, d.addr1, d.addr2, d.addr3, pkt[Dot11Deauth].reason))
    # EAPOL (4-way handshake)
    if pkt.haslayer(EAPOL):
        eapol.append((pkt.time, d.addr1, d.addr2, d.addr3))

print('total packets:', n)
print('\n=== Networks (BSSID -> SSID, channel, beacons) ===')
for bssid, s in bssid_ssid.items():
    print(f'  {bssid}  SSID={s!r}  ch={chan.get(bssid)}  beacons={beacon_count.get(bssid,0)}')

print('\n=== Deauth frames:', len(deauth), '===')
for t, a1, a2, a3, r in deauth[:10]:
    print('  ', datetime.datetime.utcfromtimestamp(float(t)).strftime('%H:%M:%S'), 'dst', a1, 'src', a2, 'bssid', a3, 'reason', r)
if deauth:
    print('  ... deauth bssids:', collections.Counter(d[3] for d in deauth))

print('\n=== EAPOL frames:', len(eapol), '===')
for t, a1, a2, a3 in eapol[:12]:
    print('  ', datetime.datetime.utcfromtimestamp(float(t)).strftime('%H:%M:%S.%f')[:-3], 'dst', a1, 'src', a2, 'bssid', a3)
if eapol:
    first = min(e[0] for e in eapol)
    print('  FIRST EAPOL utc:', datetime.datetime.utcfromtimestamp(float(first)).strftime('%H:%M:%S'),
          '| local:', datetime.datetime.fromtimestamp(float(first)).strftime('%H:%M:%S'))
