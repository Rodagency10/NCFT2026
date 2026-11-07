import requests, hmac, hashlib, time, email.utils, threading, os

B="http://13.37.197.230:28490"
TEAM="842d0f131b6b020f"          # Hawk Eye
THREADS=2
SLEEP=0.10                       # ~5-6 req/s total (RTT-bound), cadence "loop" raisonnable
STOP_FILE=os.path.join(os.path.dirname(__file__),"STOP")
MAX_SECONDS=3600                 # garde-fou : arret auto apres 1h

state={"key":None,"off":0,"stop":False}
lock=threading.Lock()
posts=[0]*THREADS
mine=0; checks=0

def fetch_key():
    return requests.get(B+"/debug",headers={"X-Forwarded-For":"127.0.0.1"},timeout=10).json()["hill_key"]
def fetch_off():
    d=requests.get(B+"/status",timeout=10).headers.get("Date")
    return int(email.utils.parsedate_to_datetime(d).timestamp())-int(time.time()) if d else 0

def sign(ts):
    return hmac.new(state["key"].encode(),f"{TEAM}|{ts}".encode(),hashlib.sha1).hexdigest()

def worker(i):
    sess=requests.Session()
    while not state["stop"]:
        ts=int(time.time())+state["off"]
        try:
            sess.post(B+"/throne",json={"team":TEAM,"ts":ts,"sig":sign(ts)},timeout=10)
            posts[i]+=1
        except Exception: pass
        time.sleep(SLEEP)

def maintainer():
    # resync horloge + refetch cle toutes les 60s (au cas ou la cle tourne)
    while not state["stop"]:
        time.sleep(60)
        try: state["off"]=fetch_off()
        except Exception: pass
        try: state["key"]=fetch_key()
        except Exception: pass

def monitor(start):
    global mine, checks
    sess=requests.Session()
    while not state["stop"]:
        if os.path.exists(STOP_FILE) or time.time()-start>MAX_SECONDS:
            state["stop"]=True; break
        try:
            st=sess.get(B+"/status",timeout=10).json()
            m=st.get("king","").startswith(TEAM[:8]); mine+=m; checks+=1
            el=int(time.time()-start)
            print(f"[{el}s] posts={sum(posts)} (~{sum(posts)/max(1,el):.1f}/s) king={st.get('king')} "
                  f"mine={m} hold%={100*mine//max(1,checks)} claims={st.get('claims')}",flush=True)
        except Exception: pass
        time.sleep(15)

def main():
    if os.path.exists(STOP_FILE): os.remove(STOP_FILE)
    state["key"]=fetch_key(); state["off"]=fetch_off()
    print(f"HOLDER Hawk Eye start key={state['key']} off={state['off']}s threads={THREADS} sleep={SLEEP}s",flush=True)
    start=time.time()
    ts=[threading.Thread(target=worker,args=(i,),daemon=True) for i in range(THREADS)]
    for t in ts: t.start()
    threading.Thread(target=maintainer,daemon=True).start()
    monitor(start)
    print(f"END total_posts={sum(posts)} hold={mine}/{checks} = {100*mine//max(1,checks)}%",flush=True)

if __name__=="__main__": main()
