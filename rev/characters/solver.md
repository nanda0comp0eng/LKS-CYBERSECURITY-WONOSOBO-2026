# Reverse CTF – Split Strings (Solve Write-up)

Category: Reverse Engineering
Difficulty: Easy

---

## Deskripsi Singkat

Binary meminta user memasukkan sebuah flag. Pada implementasi program, flag **tidak disimpan sebagai satu string utuh**, melainkan dipecah menjadi dua bagian dan digabung saat runtime.

Binary dikompilasi dengan `--static`, sehingga jumlah string sangat banyak dan hasil `strings` menjadi cukup noisy.

---

## Observasi Awal

Saat menjalankan program, terlihat bahwa input dibandingkan langsung dengan sebuah nilai rahasia.

Banner program juga memberi hint:

> Sometimes the answer is right in front of you...

Hal ini mengarah ke teknik dasar reverse: **mencari string di dalam binary**.

---

## Enumerasi String

Karena flag tidak disimpan sebagai satu string, maka pencarian langsung dengan satu pola penuh tidak akan berhasil.

Lakukan pencarian dengan potongan prefix terlebih dahulu.

```bash
strings characters | grep "LKSWNSB"
```

Hasil:

```
LKSWNSB{str1ngs_4re_
```

Terlihat bahwa bagian awal flag muncul, tetapi terpotong.

Selanjutnya, cari bagian penutup flag:

```bash
strings characters | grep "}"
```

Di antara banyak hasil (noise dari binary static), terdapat satu potongan yang sangat relevan:

```
y0ur_fr13nd}
```

---

## Analisis

Dari dua hasil tersebut, dapat disimpulkan bahwa flag disimpan dalam dua bagian terpisah di dalam binary:

Bagian pertama:

```
LKSWNSB{str1ngs_4re_
```

Bagian kedua:

```
y0ur_fr13nd}
```

Hal ini konsisten dengan implementasi program, di mana dua string literal digabung saat runtime sebelum dilakukan perbandingan dengan input user.

---

## Rekonstruksi Flag

Dengan menggabungkan kedua bagian tersebut:

```
LKSWNSB{str1ngs_4re_ + y0ur_fr13nd}
```

Didapatkan flag lengkap:

```
LKSWNSB{str1ngs_4re_y0ur_fr13nd}
```

---

## Verifikasi

Jalankan program dan masukkan flag hasil rekonstruksi.

```
LKSWNSB{str1ngs_4re_y0ur_fr13nd}
```

Program akan menampilkan pesan bahwa flag benar.

---

## Catatan

Banyaknya hasil acak saat melakukan `grep "}"` disebabkan oleh binary dikompilasi menggunakan `--static`, sehingga banyak string dari library juga ikut ter-embed ke dalam file.

Namun, karena bagian flag tetap disimpan sebagai string literal, teknik sederhana berbasis `strings` masih cukup untuk menyelesaikan challenge ini.

---

## Flag

```
LKSWNSB{str1ngs_4re_y0ur_fr13nd}
```
