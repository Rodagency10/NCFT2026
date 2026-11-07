import json, ipaddress

d = json.load(open('bgp_rib.json'))
ORIGIN = {'igp': 0, 'egp': 1, 'incomplete': 2}

# Decision order from the file:
#   1. highest local_pref  2. shortest as_path  3. lowest origin
#   4. lowest med          5. lowest peer_id
def key(r):
    return (-r['local_pref'], len(r['as_path']), ORIGIN[r['origin']], r['med'], r['peer_id'])

entries = []
for e in d['rib']:
    best = min(e['routes'], key=key)
    entries.append((ipaddress.ip_network(e['prefix']), best['label']))

# ascending prefix order = by network address, then prefix length
entries.sort(key=lambda x: (int(x[0].network_address), x[0].prefixlen))

flag = ''.join(label for _, label in entries)
print(flag)  # NCTF{bgp_bestpath_localpref_beats_aspath_len}
