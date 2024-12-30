import sqlite3
from tabulate import tabulate

# Fungsi untuk membuat koneksi ke database
def create_connection():
    return sqlite3.connect("UAS.db")

# Fungsi untuk membuat tabel
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS penilaian (
        no INTEGER PRIMARY KEY AUTOINCREMENT,
        nisn INTEGER NOT NULL UNIQUE,
        mapel TEXT NOT NULL,
        nilai REAL NOT NULL CHECK(nilai >= 0 AND nilai <= 100)
    );
    """)
    conn.commit()
    conn.close()

# Fungsi untuk menambahkan data
def tambah_nilai():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Validasi input NISN
        while True:
            try:
                nisn = int(input("Masukkan NISN: "))
                cursor.execute("SELECT COUNT(*) FROM siswa WHERE nisn = ?", (nisn,))
                if cursor.fetchone()[0] > 0:
                    print("NISN sudah terdaftar. Anda dapat melanjutkan.")
                    break
                else:
                    print("NISN tidak terdaftar, coba lagi.")
            except ValueError:
                print("NISN harus berupa angka. Silakan coba lagi.")


        # Validasi input mata pelajaran
        while True:
            mapel = input("Masukkan mata pelajaran: ").strip()
            if mapel:  # Jika input tidak kosong
                break
            else:
                print("Mata pelajaran tidak boleh kosong. Silakan coba lagi.")

        # Input mata pelajaran

        mapel = input("Masukkan mata pelajaran: ").strip()
        mapel = input("Masukkan mata pelajaran: ").strip().upper()

        # Validasi input nilai siswa
        while True:
            try:
                nilai = float(input("Masukkan nilai siswa: "))
                if 0 <= nilai <= 100:
                    break
                else:
                    print("Nilai harus antara 0 dan 100. Silakan coba lagi.")
            except ValueError:
                print("Nilai harus berupa angka desimal. Silakan coba lagi.")

        # Menambahkan data ke tabel penilaian
        cursor.execute("INSERT INTO penilaian (nisn, mapel, nilai) VALUES (?, ?, ?)", (nisn, mapel, nilai))
        conn.commit()
        print("Data berhasil ditambahkan.")

    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Fungsi untuk membaca data
from tabulate import tabulate

def lihat_nilai():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Ambil daftar nama siswa dan NISN
    cursor.execute("SELECT nisn, nama FROM siswa ORDER BY nama")
    siswa_list = cursor.fetchall()
    
    if not siswa_list:
        print("Data siswa belum tersedia!")
        conn.close()
        return
    
    # Tampilkan daftar nama siswa
    print("\nDaftar Siswa:")
    headers = ["No", "NISN", "Nama Siswa"]
    siswa_table = [(i + 1, siswa[0], siswa[1]) for i, siswa in enumerate(siswa_list)]
    print(tabulate(siswa_table, headers=headers, tablefmt="grid"))
    
    # Pilih siswa berdasarkan nomor
    try:
        pilihan = int(input("\nPilih nomor siswa untuk melihat nilai: "))
        if pilihan < 1 or pilihan > len(siswa_list):
            print("Nomor yang dipilih tidak valid!")
            conn.close()
            return
        
        nisn_terpilih = siswa_list[pilihan - 1][0]
        nama_terpilih = siswa_list[pilihan - 1][1]
    except ValueError:
        print("Input harus berupa angka!")
        conn.close()
        return
    
    # Ambil data nilai berdasarkan NISN
    cursor.execute("""
        SELECT p.mapel, p.nilai
        FROM penilaian p
        WHERE p.nisn = ?
        ORDER BY p.mapel
    """, (nisn_terpilih,))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Tampilkan data nilai siswa
    print(f"\nData Nilai untuk Siswa: {nama_terpilih} (NISN: {nisn_terpilih})")
    print("=" * 40)
    if rows:
        headers = ["Mata Pelajaran", "Nilai"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("Data nilai siswa belum ditambahkan!\n")

# Fungsi untuk memperbarui data
def update_nilai():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        no = int(input("Masukkan No siswa yang ingin diperbarui: "))
        print("Isi data yang ingin diperbarui (tekan Enter untuk melewati):")
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
        query = query.rstrip(", ")
        query += " WHERE no = ?"
        params.append(no)
        
        cursor.execute(query, params)
        conn.commit()
        print("Data berhasil diperbarui.")
    except ValueError:
        print("Input salah. Pastikan NISN dan nilai berupa angka.")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Fungsi untuk menghapus data
def hapus_nilai():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        no = int(input("Masukkan No siswa yang ingin dihapus: "))
        cursor.execute("DELETE FROM penilaian WHERE no = ?", (no,))
        conn.commit()
        print("Data berhasil dihapus.")
    except ValueError:
        print("Input salah. Masukkan angka untuk No.")
    finally:
        conn.close()

# Menu utama
def menu_nilai():
    create_table()
    while True:
        print("\nSelamat Datang Di Halaman Penilaian Siswa!")
        print("="*50)
        print("1. Tambah Data")
        print("2. Tampilkan Data")
        print("3. Perbarui Data")
        print("4. Hapus Data")
        print("0. Keluar")
        print("="*50)
        
        choice = input("Pilih menu (1-5) : ")
        if choice == "1":
            tambah_nilai()
        elif choice == "2":
            lihat_nilai()
        elif choice == "3":
            update_nilai()
        elif choice == "4":
            hapus_nilai()
        elif choice == "0":
            print("")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")