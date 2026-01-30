# CTF Write‑Up – Multi‑Layer Crypto (solve.md)

## Ringkasannya

File `encrypt.py` melakukan enkripsi berlapis terhadap isi `flag.txt` menggunakan beberapa teknik kriptografi klasik, lalu hasil akhirnya di-*base64*.

Urutan enkripsi yang dipakai adalah:

1. Caesar cipher (+3)
2. Atbash
3. Vigenère cipher (key = `KEY`)
4. Custom shuffle (even index lalu odd index)
5. ROT13
6. Affine cipher (a = 5, b = 8)
7. Base64

Tugas solver adalah membalik seluruh proses tersebut dengan urutan terbalik.

---

## Analisis encrypt.py

Potongan utama pada `encrypt.py`:

```python
_d = _fA(_d, _x1)     # Caesar +3
_d = _fB(_d)         # Atbash
_d = _fC(_d, _x2)    # Vigenere KEY
_d = _fD(_d, _x5)    # Shuffle
_d = _fE(_d)         # ROT13
_d = _fF(_d, _x3, _x4)  # Affine (5, 8)
_d = base64(...)
```

Dengan parameter:

```
_x1 = 3
_x2 = "KEY"
_x3 = 5
_x4 = 8
_x5 = 2
```

Sehingga pipeline final:

```
PLAINTEXT
 → Caesar(+3)
 → Atbash
 → Vigenere(KEY)
 → Shuffle
 → ROT13
 → Affine(5,8)
 → Base64
```

Catatan penting: semua fungsi hanya memproses karakter alfabet (`isalpha()`), karakter lain dibiarkan apa adanya.

---

## Analisis tiap layer

### 1. Caesar (+3)

Fungsi `_fA` adalah Caesar shift standar.

### 2. Atbash

Fungsi `_fB` membalik huruf alfabet:

```
A ↔ Z, B ↔ Y, ...
```

### 3. Vigenère (KEY)

Fungsi `_fC` adalah Vigenère klasik, key = `KEY`.
Index key hanya bertambah saat karakter alfabet.

### 4. Shuffle

Fungsi `_fD` untuk `_r == 2`:

```python
return _s[::2] + _s[1::2]
```

Artinya:

* ambil semua karakter index genap
* lalu semua karakter index ganjil
* gabungkan

### 5. ROT13

Fungsi `_fE` memanggil Caesar +13.

### 6. Affine cipher

Fungsi `_fF`:

```
E(x) = (a * x + b) mod 26
```

Dengan:

```
a = 5
b = 8
```

### 7. Base64

Tahap akhir hanya encoding Base64.

---

## Strategi dekripsi

Karena semua transformasi bersifat reversible, maka dekripsi dilakukan dengan urutan terbalik:

```
Base64 decode
 → inverse affine
 → ROT13
 → undo shuffle
 → Vigenere decrypt
 → Atbash
 → Caesar(-3)
```

---

## Penjelasan solver.py

Pipeline pada `solver.py` sudah sesuai dengan kebalikan dari `encrypt.py`.

### 1. Base64 decode

```python
data = base64.b64decode(ciphertext).decode()
```

---

### 2. Inverse affine

Affine yang dipakai saat enkripsi:

```
E(x) = (5x + 8) mod 26
```

Untuk membaliknya diperlukan invers modulo dari 5 (mod 26):

```
5⁻¹ mod 26 = 21
```

Implementasi:

```python
data = inv_affine(data, 5, 8)
```

---

### 3. Undo ROT13

ROT13 adalah involutif (jika diaplikasikan dua kali kembali ke semula), sehingga cukup dipanggil lagi:

```python
data = rot13(data)
```

---

### 4. Undo shuffle

Enkripsi:

```
enc = s[::2] + s[1::2]
```

Maka untuk membaliknya, string hasil dibagi dua bagian lalu disusun kembali dengan pola:

```
first[0] + second[0] + first[1] + second[1] + ...
```

Implementasinya ada di fungsi:

```python
undo_shuffle()
```

---

### 5. Vigenère decrypt

Karena enkripsi menambahkan nilai key:

```
(c + v) mod 26
```

maka dekripsi mengurangkannya:

```python
data = vigenere_decrypt(data, "KEY")
```

---

### 6. Atbash

Atbash juga involutif, sehingga dipanggil kembali:

```python
data = atbash(data)
```

---

### 7. Caesar -3

Langkah terakhir membalik Caesar +3:

```python
data = caesar_minus(data, 3)
```

---

## Urutan final solver

Potongan inti solver:

```python
data = base64.b64decode(ciphertext).decode()
data = inv_affine(data, 5, 8)
data = rot13(data)
data = undo_shuffle(data)
data = vigenere_decrypt(data, "KEY")
data = atbash(data)
data = caesar_minus(data, 3)
```

Hasil akhirnya adalah plaintext (flag).

---

## Kesimpulan

Challenge ini adalah kombinasi beberapa cipher klasik (Caesar, Atbash, Vigenère, ROT13, dan Affine) yang disusun berlapis dengan satu operasi tambahan berupa custom shuffle.

Kunci utama penyelesaian adalah:

1. Mengidentifikasi urutan transformasi pada `encrypt.py`.
2. Menentukan fungsi invers untuk tiap layer.
3. Menerapkan kembali transformasi dalam urutan terbalik.
