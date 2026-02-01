
# tinggal run aja pythonnya, eehhh

cipher = "TEtTV05TQntQeXRob25faXNfdmVyeV9zZW5zaXRpdmVfdG9faW5kZW50YXRpb259"

_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def decode(s):
bits = ""

    for c in s:
        if c == "=":
        continue
        v = _table.index(c)
        bits += format(v, "06b")

    out = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
        break
        out += chr(int(byte, 2))

    return out


if __name__ == "__main__":
print(decode(cipher))
