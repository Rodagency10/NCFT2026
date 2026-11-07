import requests, time
B="http://13.37.197.230:28493"; TOK="d27bc68efbe0e9ae"
s=requests.Session()
def call(method,path,body=None):
    for _ in range(5):
        r=s.request(method,B+path,json=body,timeout=10)
        if r.status_code==429:
            print("  [429] cooldown 65s...",flush=True); time.sleep(65); continue
        try: return r.status_code,r.json()
        except: return r.status_code,r.text[:100]
        break
    return 429,{"error":"rate"}
def me(): return call("GET","/api/me")[1]
def step(label,fn):
    time.sleep(8); print(label,"->",fn(),flush=True)

print("initial cooldown 90s...",flush=True); time.sleep(90)
print("join:",call("POST","/api/join",{"token":TOK}),flush=True)
m=me(); print("me:",m,flush=True); mc=m.get("code")

ph="228"+str(int(time.time()*1000))[-8:]
time.sleep(8)
F=call("POST","/api/register",{"phone":ph,"parrain_code":mc}); print("register F:",F,flush=True)
fcode=F[1].get("code")

time.sleep(8); print("bonus BEFORE funding:",call("POST","/api/bonus/activation",{"filleul_code":fcode}),"| me:",me(),flush=True)
time.sleep(8); print("transfer 5000->F:",call("POST","/api/transfer",{"to_code":fcode,"montant":5000}),"| me:",me(),flush=True)
time.sleep(8); print("bonus AFTER transfer:",call("POST","/api/bonus/activation",{"filleul_code":fcode}),"| me:",me(),flush=True)
# si toujours non activé: tenter buy starter (parrain) puis bonus
time.sleep(8); print("buy starter(A):",call("POST","/api/buy",{"product":"starter","qty":1}),flush=True)
time.sleep(8); print("bonus AFTER buy:",call("POST","/api/bonus/activation",{"filleul_code":fcode}),"| me:",me(),flush=True)
print("FINAL me:",me(),flush=True)
