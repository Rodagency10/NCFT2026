import requests, time
B="http://13.37.197.230:28493"
FORT="d27bc68efbe0e9ae"   # A = Hawk Eye (scoreur)
THRON="842d0f131b6b020f"  # B = compte sacrificiel qu'on controle
def mk(): return requests.Session()
def call(s,method,path,body=None):
    for _ in range(6):
        r=s.request(method,B+path,json=body,timeout=10)
        if r.status_code==429:
            print("  [429] cooldown 65s...",flush=True); time.sleep(65); continue
        try: return r.status_code,r.json()
        except: return r.status_code,r.text[:100]
    return 429,{"error":"rate"}

print("cooldown 45s...",flush=True); time.sleep(45)
A=mk(); call(A,"POST","/api/join",{"token":FORT})
ma=call(A,"GET","/api/me")[1]; Acode=ma.get("code")
print("A:",ma,flush=True)

# B joins WITH parrain_code = A
time.sleep(6)
Bs=mk()
jb=call(Bs,"POST","/api/join",{"token":THRON,"parrain_code":Acode})
print("B join w/ parrain:",jb,flush=True)
mb=call(Bs,"GET","/api/me")[1]; print("B me:",mb,flush=True)
Bcode=mb.get("code")

# si join n'a pas pris le parrain, tenter des endpoints dedies
if mb.get("sponsor")!=Acode:
    for path,body in [("/api/sponsor",{"parrain_code":Acode}),("/api/parrain",{"code":Acode}),
                      ("/api/register",{"parrain_code":Acode})]:
        time.sleep(6); print("set-sponsor",path,call(Bs,"POST",path,body),flush=True)
    mb=call(Bs,"GET","/api/me")[1]; print("B me after:",mb,flush=True)

print("\n== commission loop test ==")
a_before=call(A,"GET","/api/me")[1]; print("A before:",a_before,flush=True)
time.sleep(6); print("B buy vip:",call(Bs,"POST","/api/buy",{"product":"vip","qty":1}),flush=True)
a_mid=call(A,"GET","/api/me")[1]; print("A after B buy:",a_mid,flush=True)
time.sleep(6); print("B refund:",call(Bs,"POST","/api/refund",{"order_id":1}),flush=True)
a_after=call(A,"GET","/api/me")[1]; print("A after B refund:",a_after,flush=True)
print(f"\nA commissions {a_before.get('commissions')}->{a_after.get('commissions')} | net_gain {a_before.get('net_gain')}->{a_after.get('net_gain')}",flush=True)
