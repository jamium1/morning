"""Encrypt/decrypt the brief for GitHub Pages.
encrypt: python3 banks/encrypt.py PASSCODE data.json data.enc.json
decrypt: python3 banks/encrypt.py --decrypt PASSCODE data.enc.json data.json"""
import json, os, base64, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
ITER = 250000
def key(pw, salt, it=ITER): return PBKDF2HMAC(hashes.SHA256(), 32, salt, it).derive(pw.encode())
b = lambda x: base64.b64encode(x).decode(); d = base64.b64decode
def decrypt(pw, path):
    E = json.load(open(path)); return AESGCM(key(pw, d(E['salt']), E['iter'])).decrypt(d(E['iv']), d(E['ct']), None)
if __name__ == '__main__':
    if sys.argv[1] == '--decrypt':
        pw, src, dst = sys.argv[2:5]; open(dst, 'wb').write(decrypt(pw, src)); print('decrypted', dst); sys.exit()
    pw, src, dst = sys.argv[1:4]
    data = open(src, 'rb').read(); json.loads(data)
    salt, iv = os.urandom(16), os.urandom(12)
    ct = AESGCM(key(pw, salt)).encrypt(iv, data, None)
    json.dump({"v": 1, "iter": ITER, "salt": b(salt), "iv": b(iv), "ct": b(ct)}, open(dst, 'w'))
    assert decrypt(pw, dst) == data
    print('encrypted + verified', dst)
