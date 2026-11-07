import requests, urllib3
urllib3.disable_warnings()
HOST="13.37.197.230"
for scheme,port in [("https",443),("http",28493),("https",28493),("http",28494),("https",28494),("http",28495),("https",28495),("http",28492)]:
    url=f"{scheme}://{HOST}:{port}/"
    try:
        r=requests.get(url,timeout=6,verify=False)
        print(f"[{r.status_code}] {url}  server={r.headers.get('Server')} ctype={r.headers.get('Content-Type')} len={len(r.content)}")
        print("   ", r.text[:220].replace("\n","\\n"))
    except Exception as e:
        print(f"[ERR] {url}  {type(e).__name__}: {str(e)[:80]}")
