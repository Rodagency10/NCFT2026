import requests, time
B="http://13.37.197.230:28493"; TOK="842d0f131b6b020f"
def J(r):
    try: return r.json()
    except: return r.text[:150]
s=requests.Session()
s.post(B+"/api/join",json={"token":TOK},timeout=8)
def me(): return J(s.get(B+"/api/me",timeout=8))
print("start me:",me())
mycode=me()["code"]

print("\n== buy edge cases ==")
for body in [{"product":"booster","qty":0},{"product":"booster","qty":-1},
             {"product":"booster","qty":-100},{"product":"vip","qty":1000000000},
             {"product":"nonexistent","qty":1},{"product":"booster"},
             {"product":"booster","qty":1.5},{"product":"booster","qty":"2"}]:
    print(body,"->",J(s.post(B+"/api/buy",json=body,timeout=8)))
print("me after buys:",me())

print("\n== refund edge cases (non-owned / weird ids) ==")
for oid in [0,-1,3,9999,1.0,"1",None]:
    print("refund",oid,"->",J(s.post(B+"/api/refund",json={"order_id":oid},timeout=8)))
print("me:",me())

print("\n== referral chain + commission/prime ==")
ph=str(int(time.time()))[-8:]
reg=J(s.post(B+"/api/register",json={"phone":"228"+ph,"parrain_code":mycode},timeout=8))
print("register filleul under me:",reg)
fcode=reg.get("code") if isinstance(reg,dict) else None
print("bonus activation (my filleul):",J(s.post(B+"/api/bonus/activation",json={"filleul_code":fcode},timeout=8)),"| me:",me())
print("bonus activation AGAIN:",J(s.post(B+"/api/bonus/activation",json={"filleul_code":fcode},timeout=8)),"| me:",me())

print("\n== self-sponsor / circular ==")
print("register self phone w/ my parrain:",J(s.post(B+"/api/register",json={"phone":"228"+ph+"9","parrain_code":mycode},timeout=8)))
# transfer between our two token-accounts
s2=requests.Session(); s2.post(B+"/api/join",json={"token":"290a8731c89d6d26"},timeout=8)
code2=J(s2.get(B+"/api/me",timeout=8))["code"]
print("our 2nd acct:",code2)
print("transfer 10000 me->acct2:",J(s.post(B+"/api/transfer",json={"to_code":code2,"montant":10000},timeout=8)),"| me:",me())
print("acct2 me:",J(s2.get(B+"/api/me",timeout=8)))
