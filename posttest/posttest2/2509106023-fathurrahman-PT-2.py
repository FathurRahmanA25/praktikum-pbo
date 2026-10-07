"""
POSTTEST 2 PBO - MANAJEMEN INVENTORI ALAT BANGUNAN
Nama : Fathur Rahman
NIM  : 2509106023

Lanjutan dari Posttest 1 (Pengguna, AlatBangunan, Inventori).

PEWARISAN (INHERITANCE)
  Pengguna     <- Admin, Kasir, Manager
  AlatBangunan <- AlatTangan, AlatListrik, MaterialBangunan

RELASI UML
  Asosiasi  : Admin / Kasir / Manager --menggunakan--> Inventori (lewat parameter method)
  Agregasi  : Inventori o-- AlatBangunan  (alat dibuat di luar, lalu didaftarkan)
              Inventori o-- Pengguna      (pengguna dibuat di luar, lalu didaftarkan)
  Komposisi : AlatBangunan *-- CatatanStok (catatan dibuat di dalam alat)
"""
import os

class CatatanStok:
    """Mutasi stok. Tidak punya arti mandiri tanpa alat tempat mutasi terjadi."""

    def __init__(self, id_catatan, tipe, jumlah, keterangan):
        self.id_catatan = id_catatan
        self.tipe = tipe               
        self.jumlah = jumlah
        self.keterangan = keterangan

    def __str__(self):
        simbol = "+" if self.tipe == "MASUK" else "-"
        return f"[{self.id_catatan}] {self.tipe:<6} {simbol}{self.jumlah} | Ket: {self.keterangan}"


class Pengguna:
    instansi = "CV Sumber Bangunan Jaya"
    role_tersedia = ["admin", "kasir", "manager"]
    total_pengguna_terdaftar = 0

    def __init__(self, username, password, role="kasir"):
        self.username = username
        self.role = role if role in Pengguna.role_tersedia else "kasir"
        self.__password = None             
        self.password = password
        self._status_aktif = True          
        self._log_aktivitas = []           
        Pengguna.total_pengguna_terdaftar += 1

    @property
    def password(self):
        """Getter untuk password (private). Tidak dicetak langsung demi keamanan."""
        return self.__password

    @password.setter
    def password(self, password_baru):
        """Setter password, wajib tervalidasi (tidak boleh kosong / < 4 karakter)."""
        if not isinstance(password_baru, str) or len(password_baru) < 4:
            print(f"[GAGAL] Password untuk '{self.username}' minimal 4 karakter.")
            return
        self.__password = password_baru

    @property
    def aktif(self):
        return self._status_aktif

    def verifikasi_password(self, password_input):
        """Mengecek apakah password_input cocok dengan password akun ini."""
        return self.__password == password_input

    def nonaktifkan(self):
        self._status_aktif = False

    def _catat_aktivitas(self, teks):
        """Protected: dipakai subclass untuk mencatat aktivitas."""
        self._log_aktivitas.append(teks)

    def tampilkan_log(self):
        print(f"[LOG] Aktivitas {self.username}:")
        if not self._log_aktivitas:
            print("   (belum ada aktivitas)")
        for i, teks in enumerate(self._log_aktivitas, 1):
            print(f"   {i}. {teks}")

    def hak_akses(self):
        """Hak akses dasar semua pengguna. Di-override oleh subclass."""
        return ["lihat_alat", "cari_alat", "kartu_stok"]

    def punya_akses(self, izin):
        return izin in self.hak_akses()

    def tampilkan_profil(self):
        print(f"[USER] {self.username} | Role: {self.role} | Instansi: {Pengguna.instansi}")

    @classmethod
    def dari_dict(cls, data):
        """Factory method: membuat objek Pengguna (atau subclass-nya sesuai role) dari dictionary."""
        peta_role = {"admin": Admin, "kasir": Kasir, "manager": Manager}
        if cls is Pengguna:
            kelas = peta_role.get(data.get("role", "kasir"), Pengguna)
        else:
            kelas = cls
        if kelas is Pengguna:
            return Pengguna(data["username"], data["password"], data.get("role", "kasir"))
        return kelas(data["username"], data["password"], **data.get("ekstra", {}))

    @classmethod
    def tambah_role(cls, role_baru):
        """Menambah jenis role baru yang berlaku untuk seluruh sistem."""
        if role_baru not in cls.role_tersedia:
            cls.role_tersedia.append(role_baru)
            print(f"[OK] Role '{role_baru}' ditambahkan ke sistem.")

    @staticmethod
    def validasi_format_username(username):
        """Utility: username wajib alfanumerik & minimal 3 karakter."""
        return isinstance(username, str) and username.isalnum() and len(username) >= 3


class Admin(Pengguna):
    def __init__(self, username, password, level_akses=1):
        super().__init__(username, password, "admin")
        self.level_akses = level_akses                 

    def hak_akses(self):                               
        return super().hak_akses() + ["tambah_alat", "hapus_alat", "restock", "kelola_pengguna"]

    def tampilkan_profil(self):                        
        super().tampilkan_profil()
        print(f"       Level akses: {self.level_akses}")

    # --- Asosiasi: Inventori diterima lewat parameter ---
    def tambah_alat(self, inventori, alat):
        print(f"[ADMIN {self.username}] menambahkan alat ke '{inventori.nama_gudang}'...")
        inventori.tambah_alat(alat)
        self._catat_aktivitas("Menambah alat ke gudang")

    def hapus_alat(self, inventori, kode_alat):
        print(f"[ADMIN {self.username}] menghapus alat {kode_alat} dari '{inventori.nama_gudang}'...")
        inventori.hapus_alat(kode_alat)
        self._catat_aktivitas(f"Menghapus alat {kode_alat}")

    def nonaktifkan_pengguna(self, inventori, username):
        target = inventori.cari_pengguna(username)
        if target is None:
            print(f"[GAGAL] Pengguna '{username}' tidak ditemukan.")
        elif target is self:
            print("[GAGAL] Admin tidak boleh menonaktifkan akunnya sendiri.")
        else:
            target.nonaktifkan()
            print(f"[OK] Akun '{username}' dinonaktifkan oleh {self.username}.")
            self._catat_aktivitas(f"Menonaktifkan akun {username}")


class Kasir(Pengguna):
    def __init__(self, username, password, shift="Pagi"):
        super().__init__(username, password, "kasir")
        self.shift = shift                             
        self.total_penjualan = 0                       

    def hak_akses(self):                               
        return super().hak_akses() + ["penjualan"]

    def tampilkan_profil(self):                        
        super().tampilkan_profil()
        print(f"       Shift: {self.shift} | Total penjualan: Rp{self.total_penjualan:,.0f}")


    def jual_barang(self, inventori, kode_alat, jumlah):
        alat = inventori.ambil_alat(kode_alat)
        if alat is None:
            print(f"[GAGAL] Alat dengan kode '{kode_alat}' tidak ditemukan.")
            return 0
        harga_satuan = alat.harga
        if inventori.catat_transaksi_keluar(kode_alat, jumlah, f"Penjualan oleh {self.username}"):
            total = harga_satuan * jumlah
            self.total_penjualan += total
            self._catat_aktivitas(f"Menjual {jumlah} {alat.nama} (Rp{total:,.0f})")
            print(f"[STRUK] {jumlah} x {alat.nama} @Rp{harga_satuan:,.0f} = Rp{total:,.0f}")
            return total
        return 0


class Manager(Pengguna):
    def __init__(self, username, password, batas_perubahan_persen=20):
        super().__init__(username, password, "manager")
        self.batas_perubahan_persen = batas_perubahan_persen   

    def hak_akses(self):                               
        return super().hak_akses() + ["ubah_harga", "restock"]

    def tampilkan_profil(self):                        
        super().tampilkan_profil()
        print(f"       Batas perubahan harga: {self.batas_perubahan_persen}%")

    def setujui_perubahan_harga(self, inventori, kode_alat, harga_baru):
        alat = inventori.ambil_alat(kode_alat)
        if alat is None:
            print(f"[GAGAL] Alat dengan kode '{kode_alat}' tidak ditemukan.")
            return
        selisih = abs(harga_baru - alat.harga) / alat.harga * 100
        if selisih > self.batas_perubahan_persen:
            print(f"[GAGAL] Perubahan {selisih:.1f}% melebihi batas wewenang "
                  f"manager ({self.batas_perubahan_persen}%).")
            return
        inventori.ubah_harga_alat(kode_alat, harga_baru)
        self._catat_aktivitas(f"Menyetujui harga {kode_alat} menjadi Rp{harga_baru:,.0f}")


class AlatBangunan:
    kategori_default = "Material Umum"
    satuan_default = "pcs"
    total_alat_terdaftar = 0

    def __init__(self, kode_alat, nama, harga, stok):
        self.kode_alat = kode_alat
        self.nama = nama
        self.__harga = 0                   
        self._stok = 0                     
        self._riwayat = []                  
        self.harga = harga
        self.stok = stok
        if self._stok > 0:
            self._buat_catatan("MASUK", self._stok, "Stok awal")
        AlatBangunan.total_alat_terdaftar += 1

    @property
    def harga(self):
        return self.__harga

    @harga.setter
    def harga(self, nilai_baru):
        """Validasi: harga wajib angka > 0."""
        if not isinstance(nilai_baru, (int, float)) or nilai_baru <= 0:
            print(f"[GAGAL] Harga '{nilai_baru}' tidak valid. Harga harus angka > 0.")
            return
        self.__harga = nilai_baru

    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, nilai_baru):
        """Validasi: stok wajib bilangan bulat >= 0."""
        if not isinstance(nilai_baru, int) or nilai_baru < 0:
            print(f"[GAGAL] Stok '{nilai_baru}' tidak valid. Stok harus bilangan bulat >= 0.")
            return
        self._stok = nilai_baru


    def _buat_catatan(self, tipe, jumlah, keterangan):
        id_baru = f"STK-{len(self._riwayat) + 1:04d}"
        self._riwayat.append(CatatanStok(id_baru, tipe, jumlah, keterangan))

    def tampilkan_info(self):
        print(f"[ALAT] {self.kode_alat} - {self.nama:<20} | "
              f"Harga: Rp{self.harga:>10,.0f} | Stok: {self._stok} {self.satuan_default}")

    def kurangi_stok(self, jumlah, keterangan="Barang keluar"):
        if jumlah <= 0:
            print("[GAGAL] Jumlah pengurangan stok harus lebih dari 0.")
            return False
        if jumlah > self._stok:
            print(f"[GAGAL] Stok '{self.nama}' tidak mencukupi (tersisa {self._stok}).")
            return False
        self._stok -= jumlah
        self._buat_catatan("KELUAR", jumlah, keterangan)
        print(f"[OK] Stok '{self.nama}' berkurang {jumlah}. Sisa stok: {self._stok}")
        return True

    def tambah_stok(self, jumlah, keterangan="Barang masuk"):
        if jumlah <= 0:
            print("[GAGAL] Jumlah penambahan stok harus lebih dari 0.")
            return False
        self._stok += jumlah
        self._buat_catatan("MASUK", jumlah, keterangan)
        print(f"[OK] Stok '{self.nama}' bertambah {jumlah}. Stok sekarang: {self._stok}")
        return True

    def tampilkan_kartu_stok(self):
        print(f"\n[KARTU STOK] {self.kode_alat} - {self.nama} ({type(self).__name__})")
        print(f"  Stok akhir: {self._stok}")
        for catatan in self._riwayat:
            print(f"    {catatan}")

    @classmethod
    def dari_dict(cls, data):
        """Factory method: membuat objek alat dari dictionary (atribut khusus lewat 'ekstra')."""
        return cls(data["kode_alat"], data["nama"], data["harga"], data["stok"],
                   **data.get("ekstra", {}))

    @classmethod
    def ubah_kategori_default(cls, kategori_baru):
        cls.kategori_default = kategori_baru

    @staticmethod
    def validasi_kode_alat(kode):
        """Utility: cek apakah format kode alat valid (diawali 'AB-')."""
        return isinstance(kode, str) and kode.startswith("AB-") and len(kode) >= 5


class AlatTangan(AlatBangunan):
    def __init__(self, kode_alat, nama, harga, stok, bahan="Baja"):
        super().__init__(kode_alat, nama, harga, stok)
        self.bahan = bahan                             

    def tampilkan_info(self):                          
        super().tampilkan_info()
        print(f"        Bahan: {self.bahan}")


class AlatListrik(AlatBangunan):
    def __init__(self, kode_alat, nama, harga, stok, daya_watt=500, garansi_bulan=12):
        super().__init__(kode_alat, nama, harga, stok)
        self.daya_watt = daya_watt                     
        self.garansi_bulan = garansi_bulan             

    def tampilkan_info(self):                          
        super().tampilkan_info()
        print(f"        Daya: {self.daya_watt}W | Garansi: {self.garansi_bulan} bulan")

    def terima_retur_garansi(self, jumlah):
        """Subclass memanipulasi atribut protected (_stok) milik superclass secara langsung."""
        if jumlah <= 0:
            print("[GAGAL] Jumlah retur harus lebih dari 0.")
            return
        self._stok += jumlah
        self._buat_catatan("MASUK", jumlah, "Retur klaim garansi")
        print(f"[OK] {jumlah} unit '{self.nama}' kembali dari klaim garansi. Stok: {self._stok}")


class MaterialBangunan(AlatBangunan):
    def __init__(self, kode_alat, nama, harga, stok, satuan="sak", berat_per_unit=1.0):
        super().__init__(kode_alat, nama, harga, stok)
        self.satuan = satuan                           
        self.berat_per_unit = berat_per_unit           

    def hitung_berat_total(self):
        return self._stok * self.berat_per_unit        

    def kurangi_stok(self, jumlah, keterangan="Barang keluar"):   
        berhasil = super().kurangi_stok(jumlah, keterangan)
        if berhasil:
            print(f"[INFO] Total berat keluar: {jumlah * self.berat_per_unit:,.0f} kg")
        return berhasil

    def tampilkan_info(self):                          
        print(f"[MATERIAL] {self.kode_alat} - {self.nama:<20} | "
              f"Harga: Rp{self.harga:>10,.0f} | Stok: {self._stok} {self.satuan} "
              f"| Berat total: {self.hitung_berat_total():,.0f} kg")


class Inventori:
    nama_instansi = "CV Sumber Bangunan Jaya"
    kapasitas_maksimal = 1000
    total_transaksi_sistem = 0

    def __init__(self, nama_gudang, lokasi):
        self.nama_gudang = nama_gudang
        self.lokasi = lokasi
        self.__daftar_alat = {}               
        self.__daftar_pengguna = {}            

    @property
    def daftar_alat(self):
        """Getter, mengembalikan salinan dict alat (private tidak diubah dari luar)."""
        return dict(self.__daftar_alat)

    def daftarkan_pengguna(self, pengguna_obj):
        if not isinstance(pengguna_obj, Pengguna):
            print("[GAGAL] Objek yang didaftarkan bukan Pengguna.")
            return
        self.__daftar_pengguna[pengguna_obj.username] = pengguna_obj
        print(f"[OK] Akun '{pengguna_obj.username}' terdaftar di '{self.nama_gudang}'.")

    def cari_pengguna(self, username):
        return self.__daftar_pengguna.get(username)

    def login(self, username, password):
        pengguna = self.__daftar_pengguna.get(username)
        if pengguna and pengguna.verifikasi_password(password):
            if not pengguna.aktif:
                print(f"[GAGAL] Akun '{username}' sudah dinonaktifkan.")
                return None
            print(f"[OK] Login berhasil. Selamat datang, {username} ({pengguna.role})!")
            return pengguna
        print("[GAGAL] Username atau password salah.")
        return None

    def tambah_alat(self, alat_obj):
        if not isinstance(alat_obj, AlatBangunan):
            print("[GAGAL] Data yang ditambahkan harus berupa objek AlatBangunan.")
            return
        if alat_obj.kode_alat in self.__daftar_alat:
            print(f"[GAGAL] Alat dengan kode '{alat_obj.kode_alat}' sudah ada.")
            return
        self.__daftar_alat[alat_obj.kode_alat] = alat_obj
        print(f"[OK] '{alat_obj.nama}' ditambahkan ke gudang '{self.nama_gudang}'.")

    def ambil_alat(self, kode_alat):
        return self.__daftar_alat.get(kode_alat)

    def cari_alat(self, keyword):
        hasil = [a for a in self.__daftar_alat.values() if keyword.lower() in a.nama.lower()]
        if hasil:
            print(f"\nDitemukan {len(hasil)} hasil untuk '{keyword}':")
            for a in hasil:
                a.tampilkan_info()
        else:
            print(f"Alat dengan kata kunci '{keyword}' tidak ditemukan.")
        return hasil

    def ubah_harga_alat(self, kode_alat, harga_baru):
        alat = self.__daftar_alat.get(kode_alat)
        if not alat:
            print(f"[GAGAL] Alat dengan kode '{kode_alat}' tidak ditemukan.")
            return
        alat.harga = harga_baru

    def hapus_alat(self, kode_alat):
        if kode_alat in self.__daftar_alat:
            nama = self.__daftar_alat.pop(kode_alat).nama
            print(f"[OK] Alat '{nama}' ({kode_alat}) telah dihapus.")
        else:
            print(f"[GAGAL] Alat dengan kode '{kode_alat}' tidak ditemukan.")

    def tampilkan_semua_alat(self):
        print(f"--- Daftar alat di {self.nama_gudang} ({self.lokasi}) ---")
        if not self.__daftar_alat:
            print("  (belum ada alat terdaftar)")
        for alat in self.__daftar_alat.values():
            alat.tampilkan_info()      

    def restock_alat(self, kode_alat, jumlah, oleh="sistem"):
        alat = self.__daftar_alat.get(kode_alat)
        if not alat:
            print(f"[GAGAL] Alat dengan kode '{kode_alat}' tidak ditemukan.")
            return False
        return alat.tambah_stok(jumlah, f"Restock oleh {oleh}")

    def catat_transaksi_keluar(self, kode_alat, jumlah, keterangan="Barang keluar"):
        """Interaksi antar objek: Inventori memakai method milik AlatBangunan."""
        if not Inventori.validasi_jumlah(jumlah):
            print("[GAGAL] Jumlah transaksi tidak valid.")
            return False
        alat = self.__daftar_alat.get(kode_alat)
        if not alat:
            print(f"[GAGAL] Alat dengan kode '{kode_alat}' tidak ditemukan.")
            return False
        if alat.kurangi_stok(jumlah, keterangan):
            Inventori.total_transaksi_sistem += 1
            print(f"[TRANSAKSI #{Inventori.total_transaksi_sistem}] "
                  f"Keluar {jumlah} {alat.nama} dari '{self.nama_gudang}'.")
            return True
        return False

    @classmethod
    def ubah_kapasitas_maksimal(cls, kapasitas_baru):
        if isinstance(kapasitas_baru, int) and kapasitas_baru > 0:
            cls.kapasitas_maksimal = kapasitas_baru
            print(f"[OK] Kapasitas maksimal sistem diubah menjadi {kapasitas_baru}.")
        else:
            print("[GAGAL] Kapasitas baru tidak valid.")

    @staticmethod
    def validasi_jumlah(jumlah):
        """Utility: cek apakah jumlah transaksi adalah bilangan bulat positif."""
        return isinstance(jumlah, int) and jumlah > 0


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def cek_akses(pengguna, izin):
    if pengguna.punya_akses(izin):
        return True
    print(f"[GAGAL] Role '{pengguna.role}' tidak punya akses '{izin}'.")
    return False


def buat_alat_interaktif():
    kode = input("Kode alat (contoh AB-004): ")
    if not AlatBangunan.validasi_kode_alat(kode):
        print("[GAGAL] Format kode harus diawali 'AB-' (contoh AB-004).")
        return None
    nama = input("Nama alat: ")
    harga = float(input("Harga: "))
    stok = int(input("Stok: "))
    jenis = input("Jenis (1=Alat Tangan, 2=Alat Listrik, 3=Material, lainnya=Umum): ")
    if jenis == "1":
        return AlatTangan(kode, nama, harga, stok, bahan=input("Bahan: "))
    if jenis == "2":
        daya = int(input("Daya (watt): "))
        garansi = int(input("Garansi (bulan): "))
        return AlatListrik(kode, nama, harga, stok, daya, garansi)
    if jenis == "3":
        satuan = input("Satuan (sak/kg/kaleng): ")
        berat = float(input("Berat per satuan (kg): "))
        return MaterialBangunan(kode, nama, harga, stok, satuan, berat)
    return AlatBangunan(kode, nama, harga, stok)


def menu_interaktif(inventori, pengguna_aktif):
    clear_screen()
    print("\n=== MENU MANAJEMEN INVENTORI ALAT BANGUNAN ===")
    print(f"Login sebagai: {pengguna_aktif.username} ({pengguna_aktif.role})")
    print("1. Tambah Alat            (admin)")
    print("2. Lihat Semua Alat")
    print("3. Cari Alat")
    print("4. Ubah Harga Alat        (manager)")
    print("5. Hapus Alat             (admin)")
    print("6. Restock Alat           (admin/manager)")
    print("7. Jual Alat              (kasir)")
    print("8. Lihat Kartu Stok")
    print("9. Keluar")

    pilihan = input("Pilih menu (1-9): ")

    try:
        if pilihan == "1":
            if cek_akses(pengguna_aktif, "tambah_alat"):
                alat = buat_alat_interaktif()
                if alat:
                    pengguna_aktif.tambah_alat(inventori, alat)
        elif pilihan == "2":
            inventori.tampilkan_semua_alat()
        elif pilihan == "3":
            inventori.cari_alat(input("Kata kunci pencarian: "))
        elif pilihan == "4":
            if cek_akses(pengguna_aktif, "ubah_harga"):
                kode = input("Kode alat yang harganya diubah: ")
                pengguna_aktif.setujui_perubahan_harga(inventori, kode, float(input("Harga baru: ")))
        elif pilihan == "5":
            if cek_akses(pengguna_aktif, "hapus_alat"):
                pengguna_aktif.hapus_alat(inventori, input("Kode alat yang dihapus: "))
        elif pilihan == "6":
            if cek_akses(pengguna_aktif, "restock"):
                kode = input("Kode alat: ")
                inventori.restock_alat(kode, int(input("Jumlah restock: ")), pengguna_aktif.username)
        elif pilihan == "7":
            if cek_akses(pengguna_aktif, "penjualan"):
                kode = input("Kode alat: ")
                pengguna_aktif.jual_barang(inventori, kode, int(input("Jumlah: ")))
        elif pilihan == "8":
            alat = inventori.ambil_alat(input("Kode alat: "))
            if alat:
                alat.tampilkan_kartu_stok()
            else:
                print("[GAGAL] Alat tidak ditemukan.")
        elif pilihan == "9":
            print(f"Terima kasih, {pengguna_aktif.username}! Program selesai.")
            return
        else:
            print("Pilihan tidak valid!")
    except ValueError:
        print("Input angka tidak valid!")

    input("\nTekan Enter untuk kembali ke menu...")
    menu_interaktif(inventori, pengguna_aktif)


def login_interaktif(inventori):
    print("=== SISTEM LOGIN ===")
    percobaan = 0
    while percobaan < 3:
        username = input("Masukkan username: ")
        password = input("Masukkan password: ")
        pengguna = inventori.login(username, password)
        if pengguna:
            return pengguna
        percobaan += 1
    print("\nTerlalu banyak percobaan. Program berhenti.")
    return None


if __name__ == "__main__":
    import sys

    print("=" * 70)
    print(" DEMO 1: Pewarisan Pengguna (Admin, Kasir, Manager) + login")
    print("=" * 70)
    admin = Admin("admin1", "1234", level_akses=2)
    kasir = Pengguna.dari_dict({"username": "kasir1", "password": "0000",
                                "role": "kasir", "ekstra": {"shift": "Siang"}})
    manager = Manager("manager1", "5678", batas_perubahan_persen=20)

    print(f"Objek hasil dari_dict() bertipe: {type(kasir).__name__}")
    print("\n--- Polimorfisme: tampilkan_profil() di-override tiap subclass ---")
    for p in (admin, kasir, manager):
        p.tampilkan_profil()

    print("\n--- Hak akses (method hak_akses() di-override) ---")
    for p in (admin, kasir, manager):
        print(f"{p.username:<9}: {p.hak_akses()}")

    print("\n--- Uji classmethod: tambah_role() ---")
    print("Role tersedia sebelum:", Pengguna.role_tersedia)
    Pengguna.tambah_role("supervisor")
    print("Role tersedia sesudah:", Pengguna.role_tersedia)

    print("\n--- Uji staticmethod: validasi_format_username() ---")
    print("Username 'admin1' valid?", Pengguna.validasi_format_username("admin1"))
    print("Username 'a!' valid?", Pengguna.validasi_format_username("a!"))

    print("\n--- Uji property setter password (valid & tidak valid) ---")
    admin.password = "rahasia123"
    admin.password = "abc"
    print("Verifikasi password benar:", admin.verifikasi_password("rahasia123"))
    print("Verifikasi password salah:", admin.verifikasi_password("salah"))

    print(f"\nTotal pengguna terdaftar: {Pengguna.total_pengguna_terdaftar}")

    print("\n" + "=" * 70)
    print(" DEMO 2: Pewarisan AlatBangunan (AlatTangan, AlatListrik, MaterialBangunan)")
    print("=" * 70)
    semen = MaterialBangunan("AB-001", "Semen Gresik 40kg", 65000, 200, satuan="sak", berat_per_unit=40)
    paku = MaterialBangunan("AB-002", "Paku 5cm 1kg", 18000, 500, satuan="kg", berat_per_unit=1)
    cat = MaterialBangunan.dari_dict({"kode_alat": "AB-003", "nama": "Cat Tembok 5L",
                                      "harga": 150000, "stok": 80,
                                      "ekstra": {"satuan": "kaleng", "berat_per_unit": 5}})
    palu = AlatTangan("AB-004", "Palu Konde", 45000, 30, bahan="Baja Karbon")
    bor = AlatListrik("AB-005", "Bor Listrik 650W", 350000, 10, daya_watt=650, garansi_bulan=12)
    for alat in (semen, paku, cat, palu, bor):
        alat.tampilkan_info()

    print("\n--- Uji classmethod & staticmethod ---")
    print("Kategori sebelum:", AlatBangunan.kategori_default)
    AlatBangunan.ubah_kategori_default("Material Finishing")
    print("Kategori sesudah:", AlatBangunan.kategori_default)
    print("Kode 'AB-001' valid?", AlatBangunan.validasi_kode_alat("AB-001"))
    print("Kode 'X1' valid?", AlatBangunan.validasi_kode_alat("X1"))

    print("\n--- Uji method overriding kurangi_stok() & property setter ---")
    semen.kurangi_stok(50)       
    semen.kurangi_stok(-10)
    palu.kurangi_stok(5)         
    semen.harga = -5000
    semen.stok = -3

    print("\n--- Subclass memakai atribut protected: retur garansi ---")
    bor.terima_retur_garansi(2)

    print(f"\nTotal alat terdaftar di sistem: {AlatBangunan.total_alat_terdaftar}")

    print("\n" + "=" * 70)
    print(" DEMO 3: AGREGASI - Inventori memiliki Alat & Pengguna")
    print("=" * 70)
    gudang_pusat = Inventori("Gudang Pusat", "Balikpapan")
    gudang_cabang = Inventori("Gudang Cabang", "Samarinda")

    gudang_pusat.daftarkan_pengguna(admin)
    gudang_pusat.daftarkan_pengguna(kasir)
    gudang_pusat.daftarkan_pengguna(manager)

    for alat in (semen, paku, cat, palu, bor):
        gudang_pusat.tambah_alat(alat)
    gudang_pusat.tambah_alat("bukan objek alat")
    gudang_cabang.tambah_alat(paku)      

    gudang_pusat.tampilkan_semua_alat()

    print("\n--- Uji login via Inventori (valid & tidak valid) ---")
    gudang_pusat.login("admin1", "rahasia123")
    gudang_pusat.login("admin1", "salah")

    print("\n--- Uji cari_alat(), ubah_harga_alat(), hapus_alat() ---")
    gudang_pusat.cari_alat("paku")
    gudang_pusat.ubah_harga_alat("AB-002", 19000)
    gudang_pusat.ubah_harga_alat("AB-002", -100)
    gudang_pusat.hapus_alat("AB-003")

    print("\n--- Uji classmethod & staticmethod Inventori ---")
    Inventori.ubah_kapasitas_maksimal(2000)
    Inventori.ubah_kapasitas_maksimal(-100)
    print("Jumlah 10 valid?", Inventori.validasi_jumlah(10))
    print("Jumlah -1 valid?", Inventori.validasi_jumlah(-1))

    print("\n--- Bukti agregasi: gudang cabang dibubarkan, alat tetap ada ---")
    del gudang_cabang
    paku.tampilkan_info()
    print("Paku masih terdaftar di Gudang Pusat?", gudang_pusat.ambil_alat("AB-002") is paku)

    print("\n" + "=" * 70)
    print(" DEMO 4: ASOSIASI - Pengguna memakai Inventori lewat parameter")
    print("=" * 70)
    admin.tambah_alat(gudang_pusat, AlatTangan("AB-006", "Obeng Set", 35000, 25, bahan="Krom Vanadium"))
    admin.tambah_alat(gudang_pusat, AlatTangan("AB-006", "Obeng Duplikat", 1000, 1))

    print()
    kasir.jual_barang(gudang_pusat, "AB-002", 10)
    kasir.jual_barang(gudang_pusat, "AB-001", 20)
    kasir.jual_barang(gudang_pusat, "AB-999", 1)
    kasir.jual_barang(gudang_pusat, "AB-005", 500)

    print()
    manager.setujui_perubahan_harga(gudang_pusat, "AB-005", 380000)
    manager.setujui_perubahan_harga(gudang_pusat, "AB-005", 600000)

    print()
    gudang_pusat.restock_alat("AB-004", 15, manager.username)

    print()
    admin.nonaktifkan_pengguna(gudang_pusat, "kasir1")
    gudang_pusat.login("kasir1", "0000")

    print()
    admin.tampilkan_log()
    kasir.tampilkan_log()
    manager.tampilkan_log()
    print(f"\nTotal transaksi tercatat di sistem: {Inventori.total_transaksi_sistem}")

    print("\n" + "=" * 70)
    print(" DEMO 5: KOMPOSISI - AlatBangunan terdiri dari CatatanStok")
    print("=" * 70)
    semen.tampilkan_kartu_stok()
    paku.tampilkan_kartu_stok()
    bor.tampilkan_kartu_stok()

    print("\n" + "=" * 70)
    print(" DEMO 6: Cek relasi pewarisan & akses private")
    print("=" * 70)
    print("isinstance(admin, Pengguna)      :", isinstance(admin, Pengguna))
    print("isinstance(admin, Kasir)         :", isinstance(admin, Kasir))
    print("isinstance(bor, AlatBangunan)    :", isinstance(bor, AlatBangunan))
    print("isinstance(bor, MaterialBangunan):", isinstance(bor, MaterialBangunan))
    print("issubclass(AlatTangan, AlatBangunan):", issubclass(AlatTangan, AlatBangunan))
    print("MRO MaterialBangunan:", [k.__name__ for k in MaterialBangunan.mro()])
    try:
        print(admin.__password)
    except AttributeError as e:
        print(f"Akses langsung ke atribut private gagal: {e}")

    if len(sys.argv) > 1 and sys.argv[1] == "interaktif":
        pengguna_login = login_interaktif(gudang_pusat)
        if pengguna_login:
            menu_interaktif(gudang_pusat, pengguna_login)