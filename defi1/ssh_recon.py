import paramiko, sys
HOST="85.190.114.70"; USER="administrator"; PW="s08Vo\\hq)in4"
c=paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    c.connect(HOST, username=USER, password=PW, timeout=20, look_for_keys=False, allow_agent=False)
except Exception as e:
    print("CONNECT FAIL:", e); sys.exit(1)
print("CONNECTED ok")
def run(cmd):
    i,o,e=c.exec_command(cmd, timeout=40)
    out=o.read().decode(errors="replace"); err=e.read().decode(errors="replace")
    return (out+ ("\n[err] "+err if err.strip() else "")).strip()

cmds=[
  "whoami; id -un; hostname",
  "uname -a",
  "python3 --version 2>&1; which python3 pip3 screen tmux nohup 2>&1",
  "df -h / | tail -1; free -m | head -2",
  # latence vers le trone (Paris)
  r"for i in 1 2 3 4 5; do curl -s -o /dev/null -w '%{time_total}\n' http://13.37.197.230:28490/status; done",
  # est-ce que le port sort bien ?
  "curl -s http://13.37.197.230:28490/status",
]
for cmd in cmds:
    print("\n$ "+cmd); print(run(cmd))
c.close()
