"""Encrypt data.json -> data.enc.json for the GitHub Pages brief.
usage: python3 banks/encrypt.py PASSCODE data.json data.enc.json   (decrypt check: add --check)"""
import json, os, base64, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
ITER = 250000
def key(pw, salt): return PBKDF2HMAC(hashes.SHA256(), 32, salt, ITER).derive(pw.encode())
b = lambda x: base64.b64encode(x).decode()
if __name__ == '__main__':
    pw, src, dst = sys.argv[1:4]
    data = open(src, 'rb').read(); json.loads(data)
    salt, iv = os.urandom(16), os.urandom(12)
    ct = AESGCM(key(pw, salt)).encrypt(iv, data, None)
    json.dump({"v": 1, "iter": ITER, "salt": b(salt), "iv": b(iv), "ct": b(ct)}, open(dst, 'w'))
    E = json.load(open(dst)); d = base64.b64decode
    assert AESGCM(key(pw, d(E['salt']))).decrypt(d(E['iv']), d(E['ct']), None) == data
    print('encrypted + verified', dst)
