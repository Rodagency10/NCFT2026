import requests
B="http://13.37.197.230:28493"
s=requests.Session(); s.post(B+"/api/join",json={"token":"842d0f131b6b020f"},timeout=8)
def desc(r):
    t=r.text
    is500 = r.status_code==500
    has_tb = "Traceback" in t or "werkzeug" in t.lower() or "console" in t.lower()
    return f"[{r.status_code}] len={len(t)} tb={has_tb} :: {t[:120].strip()}"

print("== endpoint enumeration ==")
eps=["/api/activate","/api/claim","/api/withdraw","/api/network","/api/filleuls","/api/orders",
     "/api/products","/api/commission","/api/commissions","/api/bonus","/api/bonus/parrainage",
     "/api/bonus/commission","/api/cashout","/api/sell","/api/me/network","/api/team","/api/reset",
     "/api/admin","/api/debug","/api/source","/api/stats"]
for e in eps:
    for m in ("GET","POST"):
        try:
            r=s.request(m,B+e,json={} if m=="POST" else None,timeout=6)
            if r.status_code!=404:
                print(f"{m} {e} -> {desc(r)}")
        except Exception as ex: print(f"{m} {e} ERR {ex}")

print("\n== try to trigger 500 / traceback ==")
cases=[
 ("/api/transfer",{"to_code":"T015747","montant":"abc"}),
 ("/api/transfer",{"to_code":"T015747","montant":[1]}),
 ("/api/transfer",{"to_code":None,"montant":1}),
 ("/api/buy",{"product":["booster"],"qty":1}),
 ("/api/buy",{"product":"booster","qty":[1]}),
 ("/api/refund",{"order_id":[1]}),
 ("/api/refund",{"order_id":{"x":1}}),
 ("/api/bonus/activation",{}),
 ("/api/bonus/activation",{"filleul_code":123}),
 ("/api/register",{"phone":12345,"parrain_code":None}),
 ("/api/join",{"token":123}),
]
for path,body in cases:
    try:
        r=s.post(B+path,json=body,timeout=6); print(f"POST {path} {body} -> {desc(r)}")
    except Exception as ex: print(f"POST {path} ERR {ex}")

# malformed JSON body
r=s.post(B+"/api/buy",data="{bad json",headers={"Content-Type":"application/json"},timeout=6)
print("malformed json ->",desc(r))
