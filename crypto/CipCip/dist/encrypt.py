import base64 as _b64

_x1 = 3
_x2 = "KEY"
_x3 = 5
_x4 = 8
_x5 = 2

def _fA(_s, _k):
    _o = ""
    for _c in _s:
        if _c.isalpha():
            _b = 65 if _c.isupper() else 97
            _o += chr((ord(_c) - _b + _k) % 26 + _b)
        else:
            _o += _c
    return _o

def _fB(_s):
    _o = ""
    for _c in _s:
        if _c.isalpha():
            _b = 65 if _c.isupper() else 97
            _o += chr(_b + 25 - (ord(_c) - _b))
        else:
            _o += _c
    return _o

def _fC(_s, _k):
    _o = ""
    _i = 0
    for _c in _s:
        if _c.isalpha():
            _v = ord(_k[_i % len(_k)].upper()) - 65
            _b = 65 if _c.isupper() else 97
            _o += chr((ord(_c) - _b + _v) % 26 + _b)
            _i += 1
        else:
            _o += _c
    return _o

def _fD(_s, _r):
    if _r == 2:
        return _s[::2] + _s[1::2]
    return _s

def _fE(_s):
    return _fA(_s, 13)

def _fF(_s, _a, _b):
    _o = ""
    for _c in _s:
        if _c.isalpha():
            _z = 65 if _c.isupper() else 97
            _x = ord(_c) - _z
            _o += chr((_a * _x + _b) % 26 + _z)
        else:
            _o += _c
    return _o

def _main():
    with open("flag.txt", "r", encoding="utf-8") as _r:
        _d = _r.read()

    _d = _fA(_d, _x1)
    _d = _fB(_d) 
    _d = _fC(_d, _x2)
    _d = _fD(_d, _x5)
    _d = _fE(_d) 
    _d = _fF(_d, _x3, _x4)
    _d = _b64.b64encode(_d.encode()).decode()

    with open("encrypted.txt", "w", encoding="utf-8") as _w:
        _w.write(_d)

    print("[+] done")

if __name__ == "__main__":
    _main()
