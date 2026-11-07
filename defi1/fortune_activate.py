import requests, time
B="http://13.37.197.230:28493"; TOK="842d0f131b6b020f"
def J(r):
    try: return r.json()
    except: return f"{r.status_code}:{r.text[:80]}"
print("cooldown 60s..."); time.sleep(60)
s=requests.Session(); s.post(B+"/api/join",json={"token":TOK},timeout=8)
def me(): return J(s.get(B+"/api/me",timeout=8))
def P(path,body):
    time.sleep(1.5); return J(s.post(B+path,json=body,timeout=8))
mc=me()["code"]; print("me:",me())

ph="228"+str(int(time.time()*1000))[-8:]
F=P("/api/register",{"phone":ph,"parrain_code":mc}); print("register F:",F)
fcode=F.get("code") if isinstance(F,dict) else None

print("\n[H1] transfer -> filleul M-code puis bonus")
print("transfer A->F:",P("/api/transfer",{"to_code":fcode,"montant":1000}))
print("bonus F:",P("/api/bonus/activation",{"filleul_code":fcode}),"| me:",me())

print("\n[H2] buy 'pour' le filleul (variantes de param)")
for key in ["filleul_code","beneficiaire","for","membre","filleul","target_code"]:
    r=P("/api/buy",{"product":"starter","qty":1,key:fcode})
    b=P("/api/bonus/activation",{"filleul_code":fcode})
    print(f"buy {key}={fcode} -> {r} | bonus -> {b}")
    if isinstance(b,dict) and b.get("ok"):
        print("  *** ACTIVATION via",key,"*** me:",me()); break
print("\nfinal me:",me())
