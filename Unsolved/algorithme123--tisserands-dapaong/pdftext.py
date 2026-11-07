import zlib, re
raw = open('guide-motifs.pdf','rb').read()
full = b''
for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream', raw, re.S):
    s = m.group(1)
    try: s = zlib.decompress(s)
    except: pass
    full += s + b'\n'

i = 0; out = []
while i < len(full):
    if full[i:i+1] == b'(':
        j = i+1; buf = bytearray(); depth = 1
        while j < len(full):
            ch = full[j]
            if ch == 0x5c:
                buf.append(full[j]); buf.append(full[j+1]); j += 2; continue
            if ch == 0x28: depth += 1
            if ch == 0x29:
                depth -= 1
                if depth == 0: break
            buf.append(ch); j += 1
        out.append(bytes(buf)); i = j+1
    else:
        i += 1

def un(m): return bytes([int(m.group(1), 8)])
BS = bytes([0x5c])
for t in out:
    t2 = re.sub(rb'\\([0-7]{1,3})', un, t)
    t2 = t2.replace(BS + b'(', b'(').replace(BS + b')', b')').replace(BS + BS, BS)
    try: s = t2.decode('utf-8')
    except: s = t2.decode('latin-1')
    na = [(c, hex(ord(c))) for c in s if ord(c) > 127]
    print(repr(s), '| nonascii', na)
