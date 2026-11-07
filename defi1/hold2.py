import requests, hmac, hashlib, time, email.utils, threading, statistics, sys

B="http://13.37.197.230:28490"; TEAM="842d0f131b6b020f"
DURATION=int(sys.argv[1]) if len(sys.argv)>1 else 40
THREADS=int(sys.argv[2]) if len(sys.argv)>2 else 3
RATE_PER_THREAD=float(sys.argv[3]) if len(sys.argv)>3 else 3.0  # posts/sec/thread -> ~9/s total

def key():
    return requests.get(B+"/debug",headers={"X-Forwarded-For":"127.0.0.1"},timeout=10).json()["hill_key"]
def offset():
    d=requests.get(B+"/status",timeout=10).headers.get("Date")
    return int(email.utils.parsedate_to_datetime(d).timestamp())-int(time.time()) if d else 0

K=key(); OFF=offset()
print(f"key={K} offset={OFF}s threads={THREADS} rate/thread={RATE_PER_THREAD}/s dur={DURATION}s",flush=True)

# measure HTTP RTT
rtts=[]
for _ in range(5):
    t=time.time(); requests.get(B+"/status",timeout=10); rtts.append((time.time()-t)*1000)
print(f"HTTP RTT ~ {statistics.median(rtts):.0f} ms (min {min(rtts):.0f})",flush=True)

stop=time.time()+DURATION
sig_cache={}
posts=[0]*THREADS; lock=threading.Lock()
def sig_for(ts):
    v=sig_cache.get(ts)
    if v is None:
        v=hmac.new(K.encode(),f"{TEAM}|{ts}".encode(),hashlib.sha1).hexdigest()
        sig_cache[ts]=v
    return v
def worker(i):
    sess=requests.Session()
    delay=1.0/RATE_PER_THREAD
    while time.time()<stop:
        ts=int(time.time())+OFF
        try:
            sess.post(B+"/throne",json={"team":TEAM,"ts":ts,"sig":sig_for(ts)},timeout=10)
            posts[i]+=1
        except Exception: pass
        time.sleep(delay)
ths=[threading.Thread(target=worker,args=(i,),daemon=True) for i in range(THREADS)]
for t in ths: t.start()

# monitor king share
mon=requests.Session()
mine=0; tot=0
while time.time()<stop:
    try:
        st=mon.get(B+"/status",timeout=10).json()
        m=st.get("king","").startswith(TEAM[:8]); mine+=m; tot+=1
    except Exception: pass
    time.sleep(1)
print(f"total_posts={sum(posts)} (~{sum(posts)/DURATION:.1f}/s)  king_share={mine}/{tot} = {100*mine//max(1,tot)}%",flush=True)
