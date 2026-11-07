import paramiko
HOST="85.190.114.70"; USER="administrator"; PW="s08Vo\\hq)in4"
c=paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(HOST, username=USER, password=PW, timeout=20, look_for_keys=False, allow_agent=False)
def run(cmd, t=30):
    i,o,e=c.exec_command(cmd, timeout=t)
    return (o.read().decode(errors="replace")+e.read().decode(errors="replace")).strip()
print("egress IP:", run("curl -s -m 6 https://ifconfig.me 2>&1 || echo FAIL"))
print("reach example.com:443:", run("curl -s -m 6 -o /dev/null -w '%{http_code}' https://example.com 2>&1 || echo FAIL"))
print("throne :28490 tcp:", run("timeout 6 bash -c 'cat < /dev/null > /dev/tcp/13.37.197.230/28490 && echo OPEN || echo CLOSED' 2>&1 || echo TIMEOUT"))
print("throne :28491 (citadel ssh):", run("timeout 6 bash -c 'cat < /dev/null > /dev/tcp/13.37.197.230/28491 && echo OPEN || echo CLOSED' 2>&1 || echo TIMEOUT"))
print("throne :22:", run("timeout 6 bash -c 'cat < /dev/null > /dev/tcp/13.37.197.230/22 && echo OPEN || echo CLOSED' 2>&1 || echo TIMEOUT"))
print("throne :80:", run("timeout 6 bash -c 'cat < /dev/null > /dev/tcp/13.37.197.230/80 && echo OPEN || echo CLOSED' 2>&1 || echo TIMEOUT"))
print("AWS reachable? 1.1.1.1:443:", run("timeout 6 bash -c 'cat < /dev/null > /dev/tcp/1.1.1.1/443 && echo OPEN || echo CLOSED' 2>&1 || echo TIMEOUT"))
c.close()
