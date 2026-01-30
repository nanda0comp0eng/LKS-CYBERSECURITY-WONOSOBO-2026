# randKey – Solve Write‑up

Category: Cryptography
Difficulty: Easy

---

## Deskripsi Singkat

File `dist.txt` berisi deretan angka desimal (0–255) yang merepresentasikan byte hasil enkripsi.
Dari deskripsi challenge dan pola umum CTF, dapat diasumsikan bahwa skema yang digunakan adalah **single‑byte XOR cipher**.

---

## Given

Isi file `dist/dist.txt`:

```
161 166 190 186 163 190 175 150 149 130 159 178 140 137 140 129 140 133 178 134 132 131 138 178 140 129 138 130 178 139 130 159 178 142 159 148 157 153 130 178 153 136 149 153 158 136 153 136 129 140 133 132 131 132 142 152 128 143 140 137 132 143 152 140 153 143 132 140 159 142 133 140 129 129 131 148 140 157 140 131 135 140 131 138 140 135 140 158 132 133 178 143 132 140 159 134 136 129 132 140 153 140 131 158 152 158 140 133 157 140 137 140 133 140 129 138 140 128 157 140 131 138 143 140 131 138 136 153 148 140 140 140 144
```

---

## Analisis

Setiap angka berada pada rentang 0–255, sehingga sangat cocok diperlakukan sebagai byte.
Jika ini adalah single‑byte XOR, maka:

```
plaintext_byte = ciphertext_byte ^ key
```

Karena key hanya satu byte, kita bisa melakukan **bruteforce untuk seluruh kemungkinan key (0–255)** dan memeriksa hasil plaintext yang printable.

Selain itu, format flag sudah umum di CTF, yaitu:

```
XXXX{...}
```

Hal ini memudahkan kita untuk memverifikasi key yang benar.

---

## Bruteforce

Gunakan script Python berikut untuk mencoba semua kemungkinan key.

```python
ct = [161,166,190,186,163,190,175,150,149,130,159,178,140,137,140,129,140,133,178,134,132,131,138,178,140,129,138,130,178,139,130,159,178,142,159,148,157,153,130,178,153,136,149,153,158,136,153,136,129,140,133,132,131,132,142,152,128,143,140,137,132,143,152,140,153,143,132,140,159,142,133,140,129,129,131,148,140,157,140,131,135,140,131,138,140,135,140,158,132,133,178,143,132,140,159,134,136,129,132,140,153,140,131,158,152,158,140,133,157,140,137,140,133,140,129,138,140,128,157,140,131,138,143,140,131,138,136,153,148,140,140,140,144]

for key in range(256):
    try:
        pt = bytes([b ^ key for b in ct])
        text = pt.decode('ascii')
    except:
        continue

    # hanya tampilkan hasil yang seluruh karakternya printable
    if all(32 <= c < 127 for c in pt):
        if "{" in text and "}" in text:
            print(key, text)
```

---

## Hasil

Dari hasil bruteforce, hanya satu key yang menghasilkan plaintext yang jelas dan valid sebagai flag.

```
Key = 237 (0xED)
```

Plaintext:

```
LKSWNSB{xor_adalah_king_algo_for_crypto_textsetelahinicumbadibuatbiarchallnyapanjangajasih_biarkeliatansusahpadahalgampangbangetyaaa}
```

---

## Kesimpulan

Challenge ini menggunakan **single‑byte XOR cipher**.
Dengan melakukan bruteforce seluruh kemungkinan key (0–255), key yang benar dapat ditemukan dengan mudah.

---

## Flag

```
LKSWNSB{xor_adalah_king_algo_for_crypto_textsetelahinicumbadibuatbiarchallnyapanjangajasih_biarkeliatansusahpadahalgampangbangetyaaa}
```
