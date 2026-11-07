import requests, json
B="http://13.37.197.230:28493"; TOK="842d0f131b6b020f"  # Hawk Eye (throne token)
def J(r):
    try: return r.json()
    except: return r.text[:150]

# identity stability: two joins same token, same session vs new session
s1=requests.Session(); a=J(s1.post(B+"/api/join",json={"token":TOK},timeout=8))
me1=J(s1.get(B+"/api/me",timeout=8))
a2=J(s1.post(B+"/api/join",json={"token":TOK},timeout=8))   # re-join same session
s2=requests.Session(); b=J(s2.post(B+"/api/join",json={"token":TOK},timeout=8))  # new session same token
print("join#1:",a)
print("me#1:",me1)
print("rejoin same-session:",a2)
print("join new-session same token:",b)

# use s1 as our working session
s=s1
def me(): return J(s.get(B+"/api/me",timeout=8))
print("\n--- learn economy (small legit ops) ---")
print("buy booster x1:", J(s.post(B+"/api/buy",json={"product":"booster","qty":1},timeout=8)), "| me:",me())
print("buy starter x1:", J(s.post(B+"/api/buy",json={"product":"starter","qty":1},timeout=8)), "| me:",me())
# refund order 1
print("refund order1:", J(s.post(B+"/api/refund",json={"order_id":1},timeout=8)), "| me:",me())
print("refund order1 AGAIN:", J(s.post(B+"/api/refund",json={"order_id":1},timeout=8)), "| me:",me())
# register a filleul then activation bonus
reg=J(s.post(B+"/api/register",json={"phone":"22890000001","parrain_code":(me() or {}).get("code")},timeout=8))
print("register filleul:",reg)
fcode=reg.get("code") if isinstance(reg,dict) else None
print("bonus activation:", J(s.post(B+"/api/bonus/activation",json={"filleul_code":fcode},timeout=8)), "| me:",me())
print("bonus activation AGAIN:", J(s.post(B+"/api/bonus/activation",json={"filleul_code":fcode},timeout=8)), "| me:",me())
# transfer tests (to self, negative)
mycode=(me() or {}).get("code")
print("transfer -1000000 to self:", J(s.post(B+"/api/transfer",json={"to_code":mycode,"montant":-1000000},timeout=8)), "| me:",me())
