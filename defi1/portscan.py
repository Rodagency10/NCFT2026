import socket, concurrent.futures as cf
HOST="13.37.197.230"
ports=[21,22,80,139,443,445,3000,3306,5000,5432,6379,8000,8080,8443,9000,9001,9090,2375,27017]+list(range(28480,28521))
def scan(p):
    s=socket.socket(); s.settimeout(3)
    try:
        s.connect((HOST,p))
        banner=""
        try:
            s.settimeout(2); banner=s.recv(80).decode(errors="replace").strip()
        except Exception: pass
        return (p,True,banner)
    except Exception:
        return (p,False,"")
    finally:
        s.close()
open_ports=[]
with cf.ThreadPoolExecutor(max_workers=40) as ex:
    for p,ok,b in ex.map(scan,ports):
        if ok:
            open_ports.append(p); print(f"OPEN {p}  {b[:60]!r}")
print("open:",sorted(open_ports))
