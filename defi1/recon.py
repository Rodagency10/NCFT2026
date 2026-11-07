import requests, json, sys
B="http://13.37.197.230:28490"
s=requests.Session()
s.headers.update({"User-Agent":"nctf-recon"})

def show(r):
    print(f"  status={r.status_code} len={len(r.content)} ctype={r.headers.get('Content-Type')}")
    for h in ("Server","X-Powered-By","WWW-Authenticate","Allow","Location"):
        if h in r.headers: print(f"  {h}: {r.headers[h]}")
    body=r.text
    print("  body:", (body[:600].replace("\n","\\n")))

for path in ["/","/throne","/debug","/debug/","/robots.txt","/status","/king","/favicon.ico"]:
    try:
        r=s.get(B+path, timeout=10, allow_redirects=False)
        print(f"GET {path}")
        show(r)
    except Exception as e:
        print(f"GET {path} ERR {e}")
    print("-"*60)

# POST /throne with various bodies to learn validation
tests=[
    ("empty", None),
    ("not-json", "hello"),
    ("missing-fields", {}),
    ("partial", {"team":"842d0f131b6b020f"}),
    ("full-bad-sig", {"team":"842d0f131b6b020f","ts":0,"sig":"00"}),
]
for name,body in tests:
    try:
        if isinstance(body,dict):
            r=s.post(B+"/throne", json=body, timeout=10)
        else:
            r=s.post(B+"/throne", data=body, timeout=10)
        print(f"POST /throne [{name}] -> {r.status_code}: {r.text[:300]}")
    except Exception as e:
        print(f"POST /throne [{name}] ERR {e}")
