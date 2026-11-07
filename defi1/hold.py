import requests, hmac, hashlib, time, email.utils, os, sys

B="http://13.37.197.230:28490"
TEAM="842d0f131b6b020f"
INTERVAL=2.0
STOP_FILE=os.path.join(os.path.dirname(__file__),"STOP")
MAX_SECONDS=3600  # garde-fou : s'arrete tout seul au bout d'1h
s=requests.Session()

def get_key():
    r=s.get(B+"/debug", headers={"X-Forwarded-For":"127.0.0.1"}, timeout=10)
    return r.json()["hill_key"]

def server_offset():
    r=s.get(B+"/status", timeout=10)
    d=r.headers.get("Date")
    if d:
        return int(email.utils.parsedate_to_datetime(d).timestamp())-int(time.time())
    return 0

def sign(key, ts):
    return hmac.new(key.encode(), f"{TEAM}|{ts}".encode(), hashlib.sha1).hexdigest()

def main():
    key=get_key()
    off=server_offset()
    print(f"key={key} offset={off}s interval={INTERVAL}s", flush=True)
    start=time.time(); n=0; ok=0; mine_at_check=0; checks=0
    while True:
        if os.path.exists(STOP_FILE): print("STOP file -> exit", flush=True); break
        if time.time()-start>MAX_SECONDS: print("max duration -> exit", flush=True); break
        ts=int(time.time())+off
        try:
            r=s.post(B+"/throne", json={"team":TEAM,"ts":ts,"sig":sign(key,ts)}, timeout=10)
            n+=1
            if r.status_code==200: ok+=1
            else:
                # cle sig echoue -> la cle a peut-etre tourne
                if r.status_code in (400,401) and "sig" in r.text.lower():
                    try: key=get_key(); print("key refreshed:",key, flush=True)
                    except Exception: pass
        except Exception as e:
            pass
        # toutes les ~10s : qui est roi ?
        if n % 5 == 0:
            try:
                st=s.get(B+"/status", timeout=10).json()
                checks+=1
                mine = st.get("king","").startswith(TEAM[:8])
                if mine: mine_at_check+=1
                print(f"[{int(time.time()-start)}s] posts={n} ok={ok} king={st.get('king')} mine={mine} "
                      f"hold%={100*mine_at_check//max(1,checks)}", flush=True)
            except Exception: pass
        time.sleep(INTERVAL)
    print(f"END posts={n} ok={ok} checks={checks} mine_at_check={mine_at_check}", flush=True)

if __name__=="__main__":
    main()
