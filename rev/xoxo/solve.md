Berikut versi **rapih, konsisten, dan siap dikumpulkan** dari `solve.md` kamu (tanpa mengubah isi teknisnya).

---

# Reverse CTF – Simple XOR

**Solve Write-up**

**Category:** Reverse Engineering
**Difficulty:** Easy / Medium
**Target Architecture:** ELF 32-bit LSB (x86)

---

## Deskripsi Singkat

Challenge ini merupakan soal reverse engineering sederhana di mana user diminta memasukkan sebuah flag. Program akan memvalidasi input melalui beberapa fungsi pengecekan (decoy) dan sebuah algoritma kriptografi sederhana sebelum menentukan apakah flag benar.

---

## Observasi Awal

Berdasarkan analisis statik menggunakan Ghidra, alur program secara umum adalah sebagai berikut:

1. Program menampilkan banner dan meminta input dari user.
2. Program memanggil fungsi `decoy_check_1` dan `decoy_check_2` yang berisi pengecekan palsu.
3. Program memanggil fungsi utama `check_flag` untuk memvalidasi input yang sebenarnya.

---

## Analisis Fungsi

### 1. Fungsi Jebakan (Decoy)

Terdapat dua fungsi yang hanya berfungsi untuk mengecoh analis.

* **`decoy_check_1`**
  Mengandung string palsu `flag{fake_key}`.
  Jika panjang input lebih dari 5 karakter, program akan mencetak pesan:

  ```
  nooooo its fakeeee
  ```

* **`decoy_check_2`**
  Mengandung string `password123`.
  Jika input diawali dengan karakter `'C'`, program mencetak:

  ```
  palsu lagi wkkakwkawk...
  ```

Kedua fungsi ini tidak berpengaruh terhadap validasi flag yang sebenarnya.

---

### 2. Algoritma Utama (`decrypt_flag`)

Fungsi `check_flag` memanggil fungsi `decrypt_flag` yang menjadi inti dari challenge.

Dari hasil disassembly, ditemukan instruksi berikut:

```assembly
00011211 83 f0 07    XOR    EAX, 0x7
```

Instruksi tersebut menunjukkan bahwa proses dekripsi dilakukan menggunakan **single-byte XOR** dengan kunci:

```
0x07
```

---

## Ekstraksi Ciphertext

Di dalam fungsi `check_flag`, data ciphertext disimpan pada beberapa variabel lokal dalam bentuk integer dan disusun dalam format **little-endian**.

Nilai-nilai tersebut harus diubah ke urutan byte yang benar sebelum didekripsi.

| Variabel | Hex (Little-Endian) | Bytes (Urutan Benar) |
| -------- | ------------------- | -------------------- |
| local_2a | `0x50544c4b`        | `4b 4c 54 50`        |
| local_26 | `0x7c455449`        | `49 54 45 7c`        |
| local_22 | `0x5875687f`        | `7f 68 75 58`        |
| local_1e | `0x6e60666b`        | `6b 66 60 6e`        |
| local_1a | `0x75687f58`        | `58 7f 68 75`        |
| local_16 | `0x60666b58`        | `58 6b 66 60`        |
| local_12 | `0x7a6e`            | `6e 7a`              |

Sehingga seluruh ciphertext dalam bentuk byte adalah:

```
4b 4c 54 50 49 54 45 7c 7f 68 75 58
6b 66 60 6e 58 7f 68 75 58 6b 66 60
6e 7a
```

---

## Rekonstruksi Flag

Setiap byte ciphertext di-XOR dengan key `0x07`.

Script Python yang digunakan:

```python
ciphertext = [
    0x4b, 0x4c, 0x54, 0x50, 0x49, 0x54, 0x45, 0x7c,
    0x7f, 0x68, 0x75, 0x58, 0x6b, 0x66, 0x60, 0x6e,
    0x58, 0x7f, 0x68, 0x75, 0x58, 0x6b, 0x66, 0x60,
    0x6e, 0x7a
]

flag = "".join(chr(b ^ 0x07) for b in ciphertext)
print(flag)
```

---

## Hasil Dekripsi

Hasil dekripsi adalah:

```
LKS_NIT{xord_is_anywhere}
```

---

## Verifikasi

Masukkan hasil dekripsi ke program:

```
Enter the flag: LKS_NIT{xord_is_anywhere}
```

Program akan menampilkan:

```
CORRECT! KAMU NEMU FLAG ASLINYA!
Great job reverse engineering!
```

---

## Kesimpulan

Challenge ini melatih:

* analisis alur program menggunakan Ghidra,
* identifikasi operasi XOR sederhana pada level assembly,
* serta pemahaman tentang representasi **little-endian** saat mengekstrak data dari variabel lokal di stack.

---

## Flag

```
LKS_NIT{xord_is_anywhere}
```
