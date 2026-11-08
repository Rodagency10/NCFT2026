import socket, ssl, re
from sympy.ntheory.modular import crt

HOST='fgzzrrdkji6ouvb6.t.ctf.tg'; PORT=1337
p=18736736941112975355948146170840899734557629462200018283315496531
g=16326998516218999779682044863524121912387380625157210997950312047
A=9834203014839060825352429660836264532717980906418421253742877219
q=1432169896408345520421514629998326022891799177551
SMALLS=[2,3,5,7,11,13,17,19,23,29,31,37,41,43]

def connect():
    ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    s=ctx.wrap_socket(socket.create_connection((HOST,PORT),timeout=15), server_hostname=HOST)
    return s

def rd(s,t=6):
    s.settimeout(t); d=b''
    try:
        while True:
            c=s.recv(8192)
            if not c: break
            d+=c
            if b'ECHO' in d or len(c)<8192:
                # keep reading a bit more for the value line
                pass
    except: pass
    return d.decode('utf-8','replace')

def echo(s,which,stone,tries=3):
    for _ in range(tries):
        s.sendall(('ECHO %s %x'%(which,stone)).encode()+b'\n')
        r=rd(s,5)
        # the echoed value is a hex integer line (~52 hex chars). pick the longest hex token
        toks=re.findall(r'\b[0-9a-fA-F]{20,}\b', r)
        if toks:
            return int(max(toks,key=len),16)
    return None

s=connect(); rd(s,3)
residues={}
for d in SMALLS:
    h=pow(g,(p-1)//d,p)
    val=echo(s,'shallow',h)
    xd=None
    if val is not None:
        cur=1
        for i in range(d):
            if cur==val: xd=i; break
            cur=(cur*h)%p
    residues[d]=xd
    print('x mod %d = %s'%(d,xd))
s.close()

# retry any missing
missing=[d for d in SMALLS if residues[d] is None]
if missing:
    print('retrying',missing)
    s=connect(); rd(s,3)
    for d in missing:
        h=pow(g,(p-1)//d,p)
        val=echo(s,'shallow',h,5)
        xd=None
        if val is not None:
            cur=1
            for i in range(d):
                if cur==val: xd=i; break
                cur=(cur*h)%p
        residues[d]=xd
        print('retry x mod %d = %s'%(d,xd))
    s.close()

mods=[d for d in SMALLS if residues[d] is not None]
res=[residues[d] for d in mods]
x_smooth,M=crt(mods,res); x_smooth=int(x_smooth); M=int(M)
print('x mod %d = %d (M bits %d)'%(M,x_smooth,M.bit_length()))
print('g^x_smooth == A ?', pow(g,x_smooth,p)==A)
