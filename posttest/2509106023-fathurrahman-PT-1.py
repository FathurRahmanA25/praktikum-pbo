
import os

class Pengguna:
    instansi = "CV Sumber Bangunan Jaya"
    role_tersedia = ["admin", "kasir", "manager"]
    total_pengguna_terdaftar = 0

    def __init__(self, username, password, role="kasir"):
        self.username = username           
        self.role = role if role in Pengguna.role_tersedia else "kasir"  
        self.__password = None             
        self.password = password           
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

    def verifikasi_password(self, password_input):
        """Mengecek apakah password_input cocok dengan password akun ini."""
        return self.__password == password_input

    def tampilkan_profil(self):
        print(f"[USER] {self.username} | Role: {self.role} | Instansi: {Pengguna.instansi}")

    @classmethod
    def dari_dict(cls, data):
        """Factory method: membuat objek Pengguna dari dictionary (mis. hasil baca file)."""
        return cls(data["username"], data["password"], data.get("role", "kasir"))

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

class AlatBangunan:
    kategori_default = "Material Umum"
    satuan_default = "pcs"
    total_alat_terdaftar = 0

    def __init__(self, kode_alat, nama, harga, stok):
        self.kode_alat = kode_alat          
        self.nama = nama                   
        self.__harga = 0                    
        self.__stok = 0                     
        self.harga = harga                  
        self.stok = stok                   
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
        return self.__stok

    @stok.setter
    def stok(self, nilai_baru):
        """Validasi: stok wajib bilangan bulat >= 0."""
        if not isinstance(nilai_baru, int) or nilai_baru < 0:
            print(f"[GAGAL] Stok '{nilai_baru}' tidak valid. Stok harus bilangan bulat >= 0.")
            return
        self.__stok = nilai_baru

    def tampilkan_info(self):
        print(f"[ALAT] {self.kode_alat} - {self.nama:<20} | "
              f"Harga: Rp{self.__harga:>10,.0f} | Stok: {self.__stok} {self.satuan_default}")

    def kurangi_stok(self, jumlah):
        if jumlah <= 0:
            print("[GAGAL] Jumlah pengurangan stok harus lebih dari 0.")
            return False
        if jumlah > self.__stok:
            print(f"[GAGAL] Stok '{self.nama}' tidak mencukupi (tersisa {self.__stok}).")
            return False
        self.__stok -= jumlah
        print(f"[OK] Stok '{self.nama}' berkurang {jumlah}. Sisa stok: {self.__stok}")
        return True

    def tambah_stok(self, jumlah):
        if jumlah <= 0:
            print("[GAGAL] Jumlah penambahan stok harus lebih dari 0.")
            return False
        self.__stok += jumlah
        print(f"[OK] Stok '{self.nama}' bertambah {jumlah}. Stok sekarang: {self.__stok}")
        return True

    @classmethod
    def dari_dict(cls, data):
        """Factory method: membuat objek AlatBangunan dari dictionary."""
        return cls(data["kode_alat"], data["nama"], data["harga"], data["stok"])

    @classmethod
    def ubah_kategori_default(cls, kategori_baru):
        cls.kategori_default = kategori_baru

    @staticmethod
    def validasi_kode_alat(kode):
        """Utility: cek apakah format kode alat valid (diawali 'AB-')."""
        return isinstance(kode, str) and kode.startswith("AB-") and len(kode) >= 5


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

    def login(self, username, password):
        pengguna = self.__daftar_pengguna.get(username)
        if pengguna and pengguna.verifikasi_password(password):
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

    def catat_transaksi_keluar(self, kode_alat, jumlah):
        """Interaksi antar objek: Inventori memakai method milik AlatBangunan."""
        if not Inventori.validasi_jumlah(jumlah):
            print("[GAGAL] Jumlah transaksi tidak valid.")
            return
        alat = self.__daftar_alat.get(kode_alat)
        if not alat:
            print(f"[GAGAL] Alat dengan kode '{kode_alat}' tidak ditemukan.")
            return
        if alat.kurangi_stok(jumlah):
            Inventori.total_transaksi_sistem += 1
            print(f"[TRANSAKSI #{Inventori.total_transaksi_sistem}] "
                  f"Keluar {jumlah} {alat.nama} dari '{self.nama_gudang}'.")

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


def menu_interaktif(inventori, pengguna_aktif):
    clear_screen()
    print("\n=== MENU MANAJEMEN INVENTORI ALAT BANGUNAN ===")
    print("1. Tambah Alat")
    print("2. Lihat Semua Alat")
    print("3. Cari Alat")
    print("4. Ubah Harga Alat")
    print("5. Hapus Alat")
    print("6. Keluar")

    pilihan = input("Pilih menu (1-6): ")

    if pilihan == "1":
        kode = input("Kode alat (contoh AB-004): ")
        nama = input("Nama alat: ")
        try:
            harga = float(input("Harga: "))
            stok = int(input("Stok: "))
            inventori.tambah_alat(AlatBangunan(kode, nama, harga, stok))
        except ValueError:
            print("Input harga/stok tidak valid!")
    elif pilihan == "2":
        inventori.tampilkan_semua_alat()
    elif pilihan == "3":
        inventori.cari_alat(input("Kata kunci pencarian: "))
    elif pilihan == "4":
        kode = input("Kode alat yang harganya diubah: ")
        try:
            harga_baru = float(input("Harga baru: "))
            inventori.ubah_harga_alat(kode, harga_baru)
        except ValueError:
            print("Input harga tidak valid!")
    elif pilihan == "5":
        inventori.hapus_alat(input("Kode alat yang dihapus: "))
    elif pilihan == "6":
        print(f"Terima kasih, {pengguna_aktif.username}! Program selesai.")
        return
    else:
        print("Pilihan tidak valid!")

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
    print(" DEMO 1: Membuat objek Pengguna (min. 2 objek) + login")
    print("=" * 70)
    admin = Pengguna("admin1", "1234", "admin")
    kasir = Pengguna.dari_dict({"username": "kasir1", "password": "0000", "role": "kasir"})
    admin.tampilkan_profil()
    kasir.tampilkan_profil()

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
    print(" DEMO 2: Membuat objek AlatBangunan (min. 2 objek)")
    print("=" * 70)
    semen = AlatBangunan("AB-001", "Semen Gresik 40kg", 65000, 200)
    paku = AlatBangunan("AB-002", "Paku 5cm 1kg", 18000, 500)
    semen.tampilkan_info()
    paku.tampilkan_info()

    print("\n--- Uji classmethod: dari_dict() & ubah_kategori_default() ---")
    cat = AlatBangunan.dari_dict({"kode_alat": "AB-003", "nama": "Cat Tembok 5L",
                                   "harga": 150000, "stok": 80})
    cat.tampilkan_info()
    print("Kategori sebelum:", AlatBangunan.kategori_default)
    AlatBangunan.ubah_kategori_default("Material Finishing")
    print("Kategori sesudah:", AlatBangunan.kategori_default)

    print("\n--- Uji staticmethod: validasi_kode_alat() ---")
    print("Kode 'AB-001' valid?", AlatBangunan.validasi_kode_alat("AB-001"))
    print("Kode 'X1' valid?", AlatBangunan.validasi_kode_alat("X1"))

    print("\n--- Uji instance method & property setter (valid & tidak valid) ---")
    semen.kurangi_stok(50)     
    semen.kurangi_stok(-10)     
    semen.harga = -5000         
    semen.stok = -3             
    semen.tampilkan_info()

    print(f"\nTotal alat terdaftar di sistem: {AlatBangunan.total_alat_terdaftar}")

    print("\n" + "=" * 70)
    print(" DEMO 3: Membuat objek Inventori (min. 2 objek) & interaksi antar class")
    print("=" * 70)
    gudang_pusat = Inventori("Gudang Pusat", "Balikpapan")
    gudang_cabang = Inventori("Gudang Cabang", "Samarinda")

    gudang_pusat.daftarkan_pengguna(admin)
    gudang_pusat.daftarkan_pengguna(kasir)

    gudang_pusat.tambah_alat(semen)
    gudang_pusat.tambah_alat(paku)
    gudang_pusat.tambah_alat(cat)
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

    print("\n--- Uji instance method: catat_transaksi_keluar() ---")
    gudang_pusat.catat_transaksi_keluar("AB-002", 25)  
    gudang_pusat.catat_transaksi_keluar("AB-002", -5)   

    gudang_pusat.hapus_alat("AB-003")

    print("\n--- Uji classmethod: ubah_kapasitas_maksimal() ---")
    print("Kapasitas sebelum:", Inventori.kapasitas_maksimal)
    Inventori.ubah_kapasitas_maksimal(2000)
    Inventori.ubah_kapasitas_maksimal(-100)   
    print("Kapasitas sesudah:", Inventori.kapasitas_maksimal)

    print("\n--- Uji staticmethod: validasi_jumlah() ---")
    print("Jumlah 10 valid?", Inventori.validasi_jumlah(10))
    print("Jumlah -1 valid?", Inventori.validasi_jumlah(-1))

    print(f"\nNama instansi (atribut kelas Inventori): {Inventori.nama_instansi}")
    print(f"Total transaksi tercatat di sistem: {Inventori.total_transaksi_sistem}")

    if len(sys.argv) > 1 and sys.argv[1] == "interaktif":
        pengguna_login = login_interaktif(gudang_pusat)
        if pengguna_login:
            menu_interaktif(gudang_pusat, pengguna_login)