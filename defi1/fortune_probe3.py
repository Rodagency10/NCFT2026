import requests, time
B="http://13.37.197.230:28493"; TOK="842d0f131b6b020f"
def J(r):
    try: return r.json()
    except: return f"{r.status_code}:{r.text[:120]}"
s=requests.Session(); s.post(B+"/api/join",json={"token":TOK},timeout=8)
def me(): return J(s.get(B+"/api/me",timeout=8))
mycode=me()["code"]; print("me:",me())

uniq=str(int(time.time()*1000))[-9:]
phone="228"+uniq[:8]
reg=J(s.post(B+"/api/register",json={"phone":phone,"parrain_code":mycode},timeout=8))
print("register:",reg)
fcode=reg.get("code")

print("\n== how to activate a filleul? try endpoints ==")
for path,body in [
    ("/api/activate",{"filleul_code":fcode}),
    ("/api/activate",{"code":fcode}),
    ("/api/activate",{"phone":phone}),
    ("/api/bonus/activation",{"filleul_code":fcode}),
    ("/api/filleul/activate",{"code":fcode}),
    ("/api/buy",{"product":"starter","qty":1,"as_code":fcode}),
    ("/api/buy",{"product":"starter","qty":1,"code":fcode}),
]:
    print(path,body,"->",J(s.post(B+path,json=body,timeout=8)))

print("\n== can a filleul (M-code) authenticate / act? ==")
for body in [{"token":fcode},{"code":fcode},{"phone":phone}]:
    sf=requests.Session()
    print("join",body,"->",J(sf.post(B+"/api/join",json=body,timeout=8)), "| me->",J(sf.get(B+"/api/me",timeout=8)))

print("\n== commission: does buying pay a sponsor? set ourselves as filleul ==")
# try to register OUR token-account under a parrain via our own phone
print("register me-phone under self:",J(s.post(B+"/api/register",json={"phone":"228"+uniq[:7]+"7","parrain_code":mycode},timeout=8)))
print("me now:",me())

print("\n== qty parsing tricks ==")
for q in ["1e3","0x10","  3  ","1_000","999999999999999999999","-0","nan","1,5"]:
    print("buy booster qty",repr(q),"->",J(s.post(B+"/api/buy",json={"product":"booster","qty":q},timeout=8)))
print("final me:",me())
