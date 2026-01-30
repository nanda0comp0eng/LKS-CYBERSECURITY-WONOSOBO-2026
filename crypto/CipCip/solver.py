import base64
import string

_x1 = 3
_x2 = "KEY"
_x3 = 5
_x4 = 8
_x5 = 2

ciphertext = input("masukan Chiper Text: ")

# =====================
# Helpers
# =====================

def inv_affine(s, a, b):
    # modular inverse of a mod 26
    a_inv = pow(a, -1, 26)
    out = ""
    for c in s:
        if c.isalpha():
            z = 65 if c.isupper() else 97
            y = ord(c) - z
            x = (a_inv * (y - b)) % 26
            out += chr(x + z)
        else:
            out += c
    return out

def rot13(s):
    out = ""
    for c in s:
        if c.isalpha():
            b = 65 if c.isupper() else 97
            out += chr((ord(c) - b + 13) % 26 + b)
        else:
            out += c
    return out

def undo_shuffle(s):
    # undo: s[::2] + s[1::2]
    half = len(s) // 2
    if len(s) % 2:
        first = s[:half+1]
        second = s[half+1:]
    else:
        first = s[:half]
        second = s[half:]

    out = ""
    for i in range(len(second)):
        out += first[i] + second[i]
    if len(first) > len(second):
        out += first[-1]
    return out

def vigenere_decrypt(s, key):
    out = ""
    i = 0
    for c in s:
        if c.isalpha():
            v = ord(key[i % len(key)].upper()) - 65
            b = 65 if c.isupper() else 97
            out += chr((ord(c) - b - v) % 26 + b)
            i += 1
        else:
            out += c
    return out

def atbash(s):
    out = ""
    for c in s:
        if c.isalpha():
            b = 65 if c.isupper() else 97
            out += chr(b + 25 - (ord(c) - b))
        else:
            out += c
    return out

def caesar_minus(s, k):
    out = ""
    for c in s:
        if c.isalpha():
            b = 65 if c.isupper() else 97
            out += chr((ord(c) - b - k) % 26 + b)
        else:
            out += c
    return out

# =====================
# Decrypt pipeline
# =====================

data = base64.b64decode(ciphertext).decode()
data = inv_affine(data, _x3, _x4)
data = rot13(data)
data = undo_shuffle(data)
data = vigenere_decrypt(data, _x2)
data = atbash(data)
data = caesar_minus(data, _x1)

print("[+] Decrypted:", data)
