import socket, ssl, re, time

HOST='fgzzrrdkji6ouvb6.t.ctf.tg'; PORT=1337

class Oracle:
    def __init__(self):
        ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
        self.s=ctx.wrap_socket(socket.create_connection((HOST,PORT),timeout=15), server_hostname=HOST)
        self.banner=self._read(4)
    def _read(self,t=5):
        self.s.settimeout(t); data=b''
        try:
            while True:
                c=self.s.recv(8192)
                if not c: break
                data+=c
        except: pass
        return data.decode('utf-8','replace')
    def cmd(self,line,t=5):
        self.s.sendall(line.encode()+b'\n')
        return self._read(t)
    def echo(self,which,stone_int,t=5):
        return self.cmd('ECHO %s %x'%(which,stone_int),t)
    def close(self):
        try: self.s.close()
        except: pass

def parse_pub(banner):
    d={}
    for k in ['p','g','A','g_q']:
        m=re.search(k.replace('_','_')+r'\s*=\s*(\d+)',banner)
        if m: d[k]=int(m.group(1))
    return d

if __name__=='__main__':
    o=Oracle()
    pub=parse_pub(o.banner)
    print('pub:',pub)
    p=pub['p']; g=pub['g']; gq=pub['g_q']
    # order q from pubkey.txt factorization
    q=1432169896408345520421514629998326022891799177551
    smalls=[2,3,5,7,11,13,17,19,23,29,31,37,41,43]
    # test ECHO with g_q (deep current generator)
    print('--- ECHO deep g_q ---'); print(o.echo('deep', gq))
    print('--- ECHO shallow g_q ---'); print(o.echo('shallow', gq))
    # small-order element: h = g^((p-1)/3) has order 3
    h3=pow(g,(p-1)//3,p)
    print('h3 order-3 =',h3)
    print('--- ECHO shallow h3 ---'); print(o.echo('shallow', h3))
    print('--- ECHO deep h3 ---'); print(o.echo('deep', h3))
    # test ECHO with g itself
    print('--- ECHO shallow g ---'); print(o.echo('shallow', g))
    o.close()
