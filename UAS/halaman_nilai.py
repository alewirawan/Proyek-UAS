import sqlite3
from tabulate import tabulate

# Fungsi untuk membuat koneksi ke database
def create_connection():
    return sqlite3.connect("UAS.db")

# Fungsi untuk membuat tabel siswa dan penilaian
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Tabel siswa
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS siswa (
            nisn INTEGER PRIMARY KEY,
            nama TEXT NOT NULL
        );
        """)

        # Tabel penilaian
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS penilaian (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nisn INTEGER NOT NULL,
            mapel TEXT NOT NULL,
            nilai REAL NOT NULL,
            FOREIGN KEY (nisn) REFERENCES siswa(nisn),
            UNIQUE (nisn, mapel)
        );
        """)
        conn.commit()
        print("Tabel berhasil dibuat.")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()

# Fungsi untuk menambahkan nilai
def tambah_nilai():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Ambil daftar siswa
        cursor.execute("SELECT nisn, nama FROM siswa ORDER BY nama")
        siswa_list = cursor.fetchall()

        if not siswa_list:
            print("Data siswa belum tersedia!")
            return

        # Tampilkan daftar siswa
        print("\nDaftar Siswa:")
        headers = ["No", "NISN", "Nama Siswa"]
        siswa_table = [(i + 1, siswa[0], siswa[1]) for i, siswa in enumerate(siswa_list)]
        print(tabulate(siswa_table, headers=headers, tablefmt="grid"))

        # Input NISN siswa
        while True:
            try:
                nisn = int(input("\nMasukkan NISN siswa: "))
                if any(s[0] == nisn for s in siswa_list):
                    break
                else:
                    print("NISN tidak terdaftar! Silakan coba lagi.")
            except ValueError:
                print("NISN harus berupa angka. Silakan coba lagi.")

        # Input mata pelajaran
        while True:
            mapel = input("Masukkan mata pelajaran: ").strip()
            if mapel:
                break
            else:
                print("Mata pelajaran tidak boleh kosong!")

        # Input nilai
        while True:
            try:
                nilai = float(input("Masukkan nilai (0-100): "))
                if 0 <= nilai <= 100:
                    break
                else:
                    print("Nilai harus antara 0 dan 100.")
            except ValueError:
                print("Nilai harus berupa angka.")

        # Tambahkan nilai ke tabel
        cursor.execute("INSERT INTO penilaian (nisn, mapel, nilai) VALUES (?, ?, ?)", (nisn, mapel, nilai))
        conn.commit()
        print("Data nilai berhasil ditambahkan.")
    except sqlite3.IntegrityError:
        print("Data nilai sudah ada untuk siswa ini.")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()

# Fungsi untuk melihat nilai
def lihat_nilai():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT nisn, nama FROM siswa ORDER BY nama")
        siswa_list = cursor.fetchall()

        if not siswa_list:
            print("Data siswa belum tersedia!")
            return

        # Tampilkan daftar siswa
        print("\nDaftar Siswa:")
        headers = ["No", "NISN", "Nama Siswa"]
        siswa_table = [(i + 1, siswa[0], siswa[1]) for i, siswa in enumerate(siswa_list)]
        print(tabulate(siswa_table, headers=headers, tablefmt="grid"))

        # Pilih siswa
        while True:
            try:
                pilihan = int(input("\nPilih nomor siswa untuk melihat nilai: "))
                if 1 <= pilihan <= len(siswa_list):
                    nisn_terpilih = siswa_list[pilihan - 1][0]
                    nama_terpilih = siswa_list[pilihan - 1][1]
                    break
                else:
                    print("Pilihan tidak valid!")
            except ValueError:
                print("Input harus berupa angka.")

        # Ambil data nilai
        cursor.execute("SELECT mapel, nilai FROM penilaian WHERE nisn = ? ORDER BY mapel", (nisn_terpilih,))
        nilai_list = cursor.fetchall()

        # Tampilkan nilai siswa
        print(f"\nData Nilai Siswa: {nama_terpilih} (NISN: {nisn_terpilih})")
        if nilai_list:
            print(tabulate(nilai_list, headers=["Mata Pelajaran", "Nilai"], tablefmt="grid"))
        else:
            print("Data nilai belum tersedia.")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()

# Fungsi untuk memperbarui nilai
def update_nilai():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        lihat_nilai()

        # Input ID untuk diperbarui
        id_nilai = int(input("Masukkan ID nilai yang akan diperbarui: "))
        mapel = input("Mata pelajaran baru: ").strip() or None
        nilai = input("Nilai baru: ").strip()
        nilai = float(nilai) if nilai else None

        query = "UPDATE penilaian SET "
        params = []
        if mapel:
            query += "mapel = ?, "
            params.append(mapel)
        if nilai is not None:
            query += "nilai = ?, "
            params.append(nilai)
        query = query.rstrip(", ") + " WHERE id = ?"
        params.append(id_nilai)

        cursor.execute(query, params)
        conn.commit()
        print("Data berhasil diperbarui.")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()

# Fungsi untuk menghapus nilai
def hapus_nilai():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        lihat_nilai()

        # Input ID untuk dihapus
        id_nilai = int(input("Masukkan ID nilai yang akan dihapus: "))
        cursor.execute("DELETE FROM penilaian WHERE id = ?", (id_nilai,))
        conn.commit()
        print("Data berhasil dihapus.")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()

# Menu utama
def menu_nilai():
    create_tables()
    while True:
        print("\nMenu Penilaian Siswa")
        print("=" * 50)
        print("1. Tambahkan nilai siswa")
        print("2. Tampilkan nilai siswa")
        print("3. Perbarui nilai siswa")
        print("4. Hapus nilai siswa")
        print("0. Keluar")
        print("=" * 50)

        choice = input("Pilih menu (0-4): ")
        if choice == "1":
            tambah_nilai()
        elif choice == "2":
            lihat_nilai()
        elif choice == "3":
            update_nilai()
        elif choice == "4":
            hapus_nilai()
        elif choice == "0":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")

# Jalankan menu
menu_nilai()
