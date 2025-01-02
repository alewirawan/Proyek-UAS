import sqlite3
from tabulate import tabulate

# Utilities
def warna_teks(teks, kode_warna): return f"\033[{kode_warna}m{teks}\033[0m"
def create_connection(): return sqlite3.connect("UAS.db")

# Database initialization
def create_table():
    with create_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS penilaian (
                no INTEGER PRIMARY KEY AUTOINCREMENT,
                nisn INTEGER NOT NULL,
                mapel TEXT NOT NULL,
                nilai REAL NOT NULL CHECK(nilai >= 0 AND nilai <= 100),
                FOREIGN KEY (nisn) REFERENCES siswa (nisn)
            )
        """)

# Constants
MAPEL_LIST = ["Matematika", "Kimia", "Fisika", "Pendidikan Pancasila", "Bahasa Inggris"]

def get_siswa_list(cursor):
    cursor.execute("SELECT nisn, nama FROM siswa ORDER BY nama")
    return cursor.fetchall()

def tampilkan_siswa(daftar_siswa):
    print(warna_teks("\nDaftar Siswa:", "1;32"))
    headers = [
        warna_teks("No", "1;33"),
        warna_teks("NISN", "1;33"),
        warna_teks("Nama Siswa", "1;33")
    ]
    tabel_siswa = [
        [warna_teks(str(i + 1), "1;37"), warna_teks(siswa[0], "1;37"), warna_teks(siswa[1], "1;37")]
        for i, siswa in enumerate(daftar_siswa)
    ]
    print(tabulate(tabel_siswa, headers=headers, tablefmt="double_grid"))

def validasi_input(prompt, nilai_min, nilai_maks, pesan_error):
 
    while True:
        try:
            nilai = float(input(warna_teks(prompt, "33")))
            if nilai_min <= nilai <= nilai_maks:
                return nilai
            print(warna_teks(pesan_error, "31"))
        except ValueError:
            print(warna_teks("Input harus berupa angka!", "31"))


def tambah_nilai():
    with create_connection() as conn:
        cursor = conn.cursor()
        siswa_list = get_siswa_list(cursor)
        
        if not siswa_list:
            print(warna_teks("Data siswa belum tersedia!", "31"))
            return
            
        tampilkan_siswa(siswa_list)
        
        # Input NISN
        while True:
            try:
                nisn = int(input(warna_teks("Masukkan NISN: ", "33")))
                if cursor.execute("SELECT COUNT(*) FROM siswa WHERE nisn = ?", (nisn,)).fetchone()[0]:
                    break
                print(warna_teks("NISN tidak terdaftar, coba lagi.", "31"))
            except ValueError:
                print(warna_teks("NISN harus berupa angka.", "31"))
        
        # Pilih mapel
        print(warna_teks("\nPilih Mata Pelajaran:", "34"))
        for i, mapel in enumerate(MAPEL_LIST, 1):
            print(warna_teks(f"{i}. {mapel}", "36"))
            
        while True:
            try:
                pilihan_mapel = int(input(warna_teks("Pilih nomor mata pelajaran: ", "33")))
                if 1 <= pilihan_mapel <= len(MAPEL_LIST):
                    mapel = MAPEL_LIST[pilihan_mapel - 1]
                    if not cursor.execute("SELECT COUNT(*) FROM penilaian WHERE nisn = ? AND mapel = ?", 
                                        (nisn, mapel)).fetchone()[0]:
                        break
                print(warna_teks("Pilihan tidak valid atau nilai sudah ada.", "31"))
            except ValueError:
                print(warna_teks("Input harus berupa angka.", "31"))
        
        # Input nilai
        nilai = validasi_input("Masukkan nilai siswa: ", 0, 100, 
                             "Nilai harus antara 0 dan 100.")
        
        cursor.execute("INSERT INTO penilaian (nisn, mapel, nilai) VALUES (?, ?, ?)",
                      (nisn, mapel, nilai))
        print(warna_teks("Data berhasil ditambahkan.", "32"))

def lihat_nilai():
    with create_connection() as conn:
        cursor = conn.cursor()
        siswa_list = get_siswa_list(cursor)
        
        if not siswa_list:
            print(warna_teks("Data siswa belum tersedia!", "31"))
            return
            
        tampilkan_siswa(siswa_list)
        
        try:
            pilihan = int(input(warna_teks("\nPilih nomor siswa untuk melihat nilai: ", "33")))
            if not (1 <= pilihan <= len(siswa_list)):
                print(warna_teks("Nomor tidak valid!", "31"))
                return
                
            nisn, nama = siswa_list[pilihan - 1]
            rows = cursor.execute("""
                SELECT mapel, nilai FROM penilaian 
                WHERE nisn = ? ORDER BY mapel
            """, (nisn,)).fetchall()
            
            print(warna_teks(f"\nData Nilai Siswa: {nama} (NISN: {nisn})", "34"))
            print(warna_teks("=" * 40, "36"))
            
            if rows:
                print(tabulate(rows, ["Mata Pelajaran", "Nilai"], tablefmt="double_grid"))
            else:
                print(warna_teks("Data nilai siswa belum ditambahkan!\n", "31"))
                
        except ValueError:
            print(warna_teks("Input harus berupa angka!", "31"))

def update_nilai():
    with create_connection() as conn:
        cursor = conn.cursor()
        data_nilai = cursor.execute("""
            SELECT p.no, s.nisn, s.nama, p.mapel, p.nilai
            FROM siswa s JOIN penilaian p ON s.nisn = p.nisn
            ORDER BY s.nama, p.mapel
        """).fetchall()
        
        if not data_nilai:
            print(warna_teks("Belum ada data nilai.", "1;33"))
            return
            
        print(warna_teks("\nDaftar Nilai Siswa:", "34"))
        headers = [warna_teks("No", "1;33"),
                    warna_teks("NISN", "1;33"),
                    warna_teks("Nama", "1;33"),
                    warna_teks ("Mata Pelajaran", "1;33"),
                    warna_teks("Nilai", "1;33")]
        table_color = [
            [
                warna_teks(str(i), "1;37"),
                warna_teks(nisn, "1;37"),
                warna_teks(nama, "1;37"),
                warna_teks(mapel, "1;37"),
                warna_teks(str(nilai), "1;37")
            ]
            for i, (no, nisn, nama, mapel, nilai) in enumerate(data_nilai, 1)
        ]
        print(tabulate(table_color, headers=headers, tablefmt="double_grid"))

        
        try:
            pilihan = input(warna_teks("\nMasukkan nomor urut data yang ingin diubah (0 untuk batal): ", "33"))
            if pilihan == '0':
                print(warna_teks("Pembaruan dibatalkan.", "33"))
                return
                
            pilihan = int(pilihan)
            if not (1 <= pilihan <= len(data_nilai)):
                print(warna_teks("Nomor urut tidak valid.", "31"))
                return
                
            data = data_nilai[pilihan-1]
            print(warna_teks(f"\nMengubah nilai:\nNISN: {data[1]}\nNama: {data[2]}\n"
                           f"Mata Pelajaran: {data[3]}\nNilai Saat Ini: {data[4]}", "36"))
            
            nilai_baru = tampilkan_siswa("\nMasukkan nilai baru (0-100): ", 0, 100,
                                      "Nilai harus antara 0-100")
            
            if input(warna_teks(f"Yakin mengubah nilai menjadi {nilai_baru}? (y/n): ", "33")).lower() == 'y':
                cursor.execute("UPDATE penilaian SET nilai = ? WHERE no = ?", 
                             (nilai_baru, data[0]))
                print(warna_teks("\nNilai berhasil diperbarui!", "32"))
            else:
                print(warna_teks("Pembaruan dibatalkan.", "33"))
                
        except ValueError:
            print(warna_teks("Input tidak valid.", "31"))

def hapus_nilai():
    with create_connection() as conn:
        cursor = conn.cursor()
        data_nilai = cursor.execute("""
            SELECT p.no, s.nisn, s.nama, p.mapel, p.nilai
            FROM siswa s JOIN penilaian p ON s.nisn = p.nisn
            ORDER BY s.nama, p.mapel
        """).fetchall()
        
        if not data_nilai:
            print(warna_teks("Belum ada data nilai.", "31"))
            return
            
        print(warna_teks("\nDaftar Nilai Siswa:", "34"))
        headers = [warna_teks("No", "1;33"),
                    warna_teks("NISN", "1;33"),
                    warna_teks("Nama", "1;33"),
                    warna_teks ("Mata Pelajaran", "1;33"),
                    warna_teks("Nilai", "1;33")]
        table_color = [
            [
                warna_teks(str(i), "1;37"),
                warna_teks(nisn, "1;37"),
                warna_teks(nama, "1;37"),
                warna_teks(mapel, "1;37"),
                warna_teks(str(nilai), "1;37")
            ]
            for i, (no, nisn, nama, mapel, nilai) in enumerate(data_nilai, 1)
        ]
        print(tabulate(table_color, headers=headers, tablefmt="double_grid"))

        
        try:
            no_nilai = input(warna_teks("\nMasukkan nomor data yang ingin dihapus (0 untuk batal): ", "33"))
            if no_nilai == "0":
                print(warna_teks("Penghapusan dibatalkan.", "33"))
                return
                
            no_nilai = int(no_nilai)
            nilai = cursor.execute("""
                SELECT s.nama, p.mapel, p.nilai FROM siswa s
                JOIN penilaian p ON s.nisn = p.nisn WHERE p.no = ?
            """, (no_nilai,)).fetchone()
            
            if not nilai:
                print(warna_teks("Nomor data tidak ditemukan.", "31"))
                return
                
            print(warna_teks(f"\nMenghapus nilai:\nNama: {nilai[0]}\n"
                           f"Mata Pelajaran: {nilai[1]}\nNilai: {nilai[2]}", "36"))
            
            if input(warna_teks("Yakin menghapus data ini? (y/n): ", "33")).lower() == 'y':
                cursor.execute("DELETE FROM penilaian WHERE no = ?", (no_nilai,))
                print(warna_teks("\nData nilai berhasil dihapus!", "32"))
            else:
                print(warna_teks("Penghapusan dibatalkan.", "33"))
                
        except ValueError:
            print(warna_teks("Input tidak valid.", "31"))

def menu_nilai():
    create_table()
    while True:
        print(warna_teks("=" * 40, "34"))
        print(warna_teks("Selamat Datang Di Halaman Penilaian Siswa!", "36"))
        print(warna_teks("=" * 40, "34"))
        print("=" * 50)
        
        menu_options = {
            "1": ("Tambahkan nilai siswa", tambah_nilai, "32"),
            "2": ("Tampilkan nilai siswa", lihat_nilai, "34"),
            "3": ("Perbarui nilai siswa", update_nilai, "33"),
            "4": ("Hapus nilai siswa", hapus_nilai, "31"),
            "0": ("Keluar", None, "35")
        }
        
        for key, (text, _, color) in menu_options.items():
            print(warna_teks(f"{key}. {text}", color))
        print("=" * 50)
        
        pilihan = input(warna_teks("➤ Pilih menu (1-4): ", "36"))
        if pilihan == "0":
            break
        elif pilihan in menu_options:
            menu_options[pilihan][1]()
        else:
            print(warna_teks("❗ Pilihan tidak valid. Silakan coba lagi.", "31"))

if __name__ == "__main__":
    menu_nilai()