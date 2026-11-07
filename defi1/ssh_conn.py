import paramiko
HOST="85.190.114.70"; USER="administrator"; PW="s08Vo\\hq)in4"
c=paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(HOST, username=USER, password=PW, timeout=20, look_for_keys=False, allow_agent=False)
def run(cmd, t=30):
    i,o,e=c.exec_command(cmd, timeout=t)
    return (o.read().decode(errors="replace")+e.read().decode(errors="replace")).strip()
print("== TCP connect test (bash /dev/tcp) ==")
print(run("timeout 6 bash -c 'echo > /dev/tcp/13.37.197.230/28490 && echo OPEN || echo CLOSED' 2>&1"))
print("\n== curl with 5s timeout, show time + code ==")
print(run("curl -s -m 5 --connect-timeout 5 -o /dev/null -w 'code=%{http_code} connect=%{time_connect}s total=%{time_total}s\\n' http://13.37.197.230:28490/status 2>&1"))
print("\n== curl body ==")
print(run("curl -s -m 5 http://13.37.197.230:28490/status 2>&1"))
print("\n== traceroute-ish: ping ==")
print(run("ping -c 3 -W 2 13.37.197.230 2>&1"))
c.close()
