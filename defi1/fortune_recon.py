import requests, paramiko
HOST="13.37.197.230"
TOK_THRONE="842d0f131b6b020f"; TOK_CITADEL="290a8731c89d6d26"

# A) does 28492 accept password auth like 28491?
for port in (28491,28492):
    c=paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        c.connect(HOST,port=port,username="player",password="x",timeout=10,look_for_keys=False,allow_agent=False)
    except paramiko.AuthenticationException:
        print(f":{port} password-auth ENABLED (rejected test pw)")
    except Exception as e:
        print(f":{port} {type(e).__name__}: {str(e)[:70]}")
    finally:
        try:c.close()
        except:pass

# B) Fortune: try join with our tokens
B=f"http://{HOST}:28493"
for name,tok in [("throne",TOK_THRONE),("citadel",TOK_CITADEL)]:
    s=requests.Session()
    r=s.post(B+"/api/join",json={"token":tok},timeout=8)
    print(f"\n/api/join [{name} {tok}] -> {r.status_code}: {r.text[:200]}")
    if r.ok:
        for ep in ["/api/me","/api/leaderboard"]:
            rr=s.get(B+ep,timeout=8); print(f"  {ep} -> {rr.status_code}: {rr.text[:300]}")
        # map endpoints: try a harmless buy to see order structure
        rb=s.post(B+"/api/buy",json={"product":"booster","qty":1},timeout=8)
        print("  /api/buy booster x1 ->",rb.status_code, rb.text[:200])
        rm=s.get(B+"/api/me",timeout=8); print("  /api/me after buy ->", rm.text[:200])
        break
