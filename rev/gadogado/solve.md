# Writeup: Reverse Engineering (Gado-gado)

## Analisis
Binary melakukan obfuscation pada flag dengan dua langkah utama:
1.  **Shift:** Mengurangi nilai ASCII setiap karakter sebesar `-3`.
2.  **Swap:** Menukar posisi karakter dengan logika indeks tertentu (yang efeknya mengacak urutan).

## Logika Penyelesaian
Untuk mendapatkan flag kembali, kita harus membalik urutan operasinya:
1.  **Un-Swap:** Jalankan logika swap yang sama (karena operasinya simetris) untuk mengembalikan posisi karakter.
2.  **Un-Shift:** Tambahkan `+3` ke nilai ASCII setiap karakter.
3.  **Reverse:** Hasil akhirnya terbalik (reverse string), jadi perlu dibalik lagi (`[::-1]`).

## Solver (Python)

```python
cipher = "MASUKAN CHIPERNYA"
chars = list(cipher)
length = len(chars)

# 1. Reverse Swap Logic
for j in range(0, length - 1, 2):
    target = (length - 1) - (j + 1)
    chars[j], chars[target] = chars[target], chars[j]

# 2. Reverse Shift Logic (+3) & Gabungkan
decoded = "".join([chr(ord(c) + 3) for c in chars])

# 3. Final Reverse
print(f"Flag: {decoded[::-1]}")
