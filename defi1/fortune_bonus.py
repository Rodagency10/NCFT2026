import requests, time
B="http://13.37.197.230:28493"; TOK="d27bc68efbe0e9ae"   # Hawk Eye FORTUNE token
s=requests.Session()
def call(method,path,body=None,retries=3):
    for _ in range(retries):
        r=s.request(method,B+path,json=body,timeout=8)
        if r.status_code==429:
            print("  [429] cooldown 62s..."); time.sleep(62); continue
        try: return r.status_code, r.json()
        except: return r.status_code, r.text[:120]
    return 429,{"error":"rate"}
def me():
    _,j=call("GET","/api/me"); return j

print("join:",call("POST","/api/join",{"token":TOK}))
m=me(); print("me:",m); mc=m.get("code")

ph="228"+str(int(time.time()*1000))[-8:]
print("register F:", (F:=call("POST","/api/register",{"phone":ph,"parrain_code":mc})))
fcode=F[1].get("code") if isinstance(F[1],dict) else None
print("fcode=",fcode)

print("\n== test bonus endpoints (measure net_gain delta) ==")
def test_bonus(path,body):
    before=me().get("net_gain")
    code,j=call("POST",path,body)
    after=me().get("net_gain")
    d = (after-before) if (isinstance(after,int) and isinstance(before,int)) else "?"
    print(f"{path} {body} -> [{code}] {j} | net_gain {before}->{after} (Δ{d})")
    return j

test_bonus("/api/bonus/parrainage",{"filleul_code":fcode})
test_bonus("/api/bonus/parrainage",{"code":fcode})
test_bonus("/api/bonus/commission",{"filleul_code":fcode})
# activation via gros transfert (seuil = prix starter ?)
print("transfer 5000 -> F:",call("POST","/api/transfer",{"to_code":fcode,"montant":5000}))
test_bonus("/api/bonus/activation",{"filleul_code":fcode})
print("\nfinal me:",me())
