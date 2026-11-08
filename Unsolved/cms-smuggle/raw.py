import socket, ssl, sys

HOST='j75a3l6wbljzmfdm.t.ctf.tg'; PORT=443

def send_raw(payload: bytes, read_timeout=6):
    ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    s=ctx.wrap_socket(socket.create_connection((HOST,PORT),timeout=15), server_hostname=HOST)
    s.sendall(payload)
    s.settimeout(read_timeout)
    data=b''
    try:
        while True:
            c=s.recv(8192)
            if not c: break
            data+=c
    except: pass
    s.close()
    return data

def normal(path, method='GET', body=b'', extra=''):
    req = f'{method} {path} HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n'
    if body:
        req += f'Content-Length: {len(body)}\r\n'
    req += extra + '\r\n'
    return send_raw(req.encode()+body)

if __name__=='__main__':
    # sanity: normal GET /admin/flag
    print('=== normal GET /admin/flag ===')
    print(normal('/admin/flag').decode('latin-1')[:400])
