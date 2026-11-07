import requests, subprocess
HOST="13.37.197.230"
paths=["/","/debug","/status","/creds","/key","/king","/foothold","/player","/ssh","/hill_key","/config","/ops"]
for port in [28494,28495]:
    print(f"\n==== scorer :{port} ====")
    for p in paths:
        for xff in [None,"127.0.0.1"]:
            h={"X-Forwarded-For":xff} if xff else {}
            try:
                r=requests.get(f"http://{HOST}:{port}{p}",headers=h,timeout=6)
                tag="xff" if xff else "   "
                body=r.text[:220].replace("\n","\\n")
                if r.status_code!=404:
                    print(f"[{r.status_code}] {tag} {p} -> {body}")
            except Exception as e:
                print(f"[ERR] {p} {e}")

print("\n==== Réseau Fortune :28493 full ====")
r=requests.get(f"http://{HOST}:28493/",timeout=8)
open("C:/Users/Rodrigue/Desktop/NCTF2026/defi1/fortune.html","w",encoding="utf-8").write(r.text)
print("saved fortune.html len",len(r.text))

print("\n==== SSH 28491 auth methods ====")
try:
    out=subprocess.run(["ssh","-p","28491","-o","BatchMode=yes","-o","StrictHostKeyChecking=no",
        "-o","ConnectTimeout=8","-o","PreferredAuthentications=none","player@13.37.197.230","exit"],
        capture_output=True,text=True,timeout=20)
    print("STDERR:",out.stderr.strip()[:300])
except Exception as e:
    print("ssh err",e)
