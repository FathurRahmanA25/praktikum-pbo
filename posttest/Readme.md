# Sistem Manajemen Inventori Alat Bangunan

## Struktur Class

### 1. `Pengguna`
Menangani akun & proses login (pengganti `dict users{}` pada program lama).

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `instansi`, `role_tersedia`, `total_pengguna_terdaftar` | dipakai bersama semua objek |
| Atribut instance | `username` (public), `role` (public), `__password` (private) | unik tiap objek |
| Property | `password` (getter & setter, validasi minimal 4 karakter) | |
| Instance method | `verifikasi_password()`, `tampilkan_profil()` | |
| Class method | `dari_dict()` (factory), `tambah_role()` | |
| Static method | `validasi_format_username()` | |

### 2. `AlatBangunan`
Menangani data satu alat bangunan (pengganti `dict inventory{}`).

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `kategori_default`, `satuan_default`, `total_alat_terdaftar` | |
| Atribut instance | `kode_alat` (public), `nama` (public), `__harga` (private), `__stok` (private) | |
| Property | `harga` (validasi > 0), `stok` (validasi bilangan bulat ≥ 0) | |
| Instance method | `tampilkan_info()`, `tambah_stok()`, `kurangi_stok()` | |
| Class method | `dari_dict()` (factory), `ubah_kategori_default()` | |
| Static method | `validasi_kode_alat()` | |

### 3. `Inventori`
Mengelola banyak `AlatBangunan` & `Pengguna` sekaligus (pengganti fungsi
`tambah_alat()`, `cari_alat()`, `ubah_data_alat()`, `hapus_alat()`, `login()`, `menu()`
pada program lama).

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `nama_instansi`, `kapasitas_maksimal`, `total_transaksi_sistem` | |
| Atribut instance | `nama_gudang` (public), `lokasi` (public), `__daftar_alat` (private), `__daftar_pengguna` (private) | |
| Property | `daftar_alat` (getter, mengembalikan salinan data) | |
| Instance method | `daftarkan_pengguna()`, `login()`, `tambah_alat()`, `cari_alat()`, `ubah_harga_alat()`, `hapus_alat()`, `tampilkan_semua_alat()`, `catat_transaksi_keluar()` | |
| Class method | `ubah_kapasitas_maksimal()` | |
| Static method | `validasi_jumlah()` | |

`Inventori` **berinteraksi** dengan objek `AlatBangunan` (menyimpan & memanggil
method-nya, mis. `kurangi_stok()`) dan objek `Pengguna` (menyimpan & memverifikasi
login) — tanpa pewarisan, murni komposisi objek.

## Cara Menjalankan

### Mode demo otomatis (default, untuk pengujian/penilaian)
```bash
python 2509106023-fathurrahman-PT-1.py
```
Akan membuat minimal 2 objek per class, memanggil seluruh instance/class/static
method, serta menguji setter dengan data valid dan tidak valid (harga/stok negatif,
password terlalu pendek, jumlah transaksi negatif, dsb).

### Mode interaktif (opsional, gaya program lama: login lalu menu)
```bash
python 2509106023-fathurrahman-PT-1.py interaktif
```
Login menggunakan salah satu akun demo:
- `admin1` / `rahasia123`
- `kasir1` / `0000`

Lalu pilih menu 1–6 (Tambah Alat, Lihat Semua Alat, Cari Alat, Ubah Harga Alat,
Hapus Alat, Keluar).

## Panduan Pengujian Singkat

1. Jalankan mode demo → perhatikan baris `[OK]` (aksi berhasil) dan `[GAGAL]`
   (validasi menolak input tidak valid).
2. Contoh validasi yang diuji:
   - `harga`/`stok` diisi angka negatif → ditolak oleh property setter.
   - `password` diisi kurang dari 4 karakter → ditolak.
   - Kapasitas gudang diisi angka negatif lewat `ubah_kapasitas_maksimal()` → ditolak.
   - Login dengan password salah → ditolak.
3. Total objek yang terdaftar dapat dicek lewat atribut kelas, misalnya
   `Pengguna.total_pengguna_terdaftar` dan `AlatBangunan.total_alat_terdaftar`.

## Requirements
Python 3.8+ (tidak ada dependensi eksternal, hanya modul bawaan `os` dan `sys`).