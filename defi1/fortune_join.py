import requests
B="http://13.37.197.230:28493"
for name,tok in [("throne","842d0f131b6b020f"),("citadel","290a8731c89d6d26")]:
    s=requests.Session()
    try:
        r=s.post(B+"/api/join",json={"token":tok},timeout=8)
        print(f"/api/join [{name} {tok}] -> {r.status_code}: {r.text[:200]}")
        if r.ok:
            me=s.get(B+"/api/me",timeout=8); print("  /api/me ->",me.status_code,me.text[:300])
            lb=s.get(B+"/api/leaderboard",timeout=8); print("  /api/leaderboard ->",lb.status_code,lb.text[:400])
    except Exception as e:
        print(f"[{name}] ERR {type(e).__name__}: {str(e)[:80]}")
