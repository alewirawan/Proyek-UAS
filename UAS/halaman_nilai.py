import sqlite3

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
        nama VARCHAR(40) NOT NULL,
        nisn INTEGER NOT NULL UNIQUE,
        mapel TEXT NOT NULL,
        nilai REAL NOT NULL CHECK(nilai >= 0 AND nilai <= 100)
    );
    """)
    conn.commit()
    conn.close()

# Fungsi untuk menambahkan data
def add_record():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Input data dari pengguna
    try:
        nama = input("Masukkan nama siswa: ")
        nisn = int(input("Masukkan NISN siswa: "))
        mapel = input("Masukkan mata pelajaran: ")
        nilai = float(input("Masukkan nilai siswa: "))

        cursor.execute("INSERT INTO penilaian (nama, nisn, mapel, nilai) VALUES (?, ?, ?, ?)",
                       (nama, nisn, mapel, nilai))
        conn.commit()
        print("Data berhasil ditambahkan.")
    except ValueError:
        print("Input salah. Pastikan NISN berupa angka dan nilai berupa angka desimal.")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Fungsi untuk membaca data
def read_records():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM penilaian")
    rows = cursor.fetchall()
    conn.close()

    print("\nData Penilaian Siswa:")
    print("-" * 40)
    print(f"{'No':<5} {'Nama':<20} {'NISN':<10} {'Mapel':<15} {'Nilai':<5}")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<10} {row[3]:<15} {row[4]:<5}")
    print("-" * 40)

# Fungsi untuk memperbarui data
def update_record():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        no = int(input("Masukkan No siswa yang ingin diperbarui: "))
        print("Isi data yang ingin diperbarui (tekan Enter untuk melewati):")
        nama = input("Nama baru: ").strip() or None
        nisn = input("NISN baru: ").strip()
        nisn = int(nisn) if nisn else None
        mapel = input("Mata pelajaran baru: ").strip() or None
        nilai = input("Nilai baru: ").strip()
        nilai = float(nilai) if nilai else None

        query = "UPDATE penilaian SET "
        params = []
        if nama:
            query += "nama = ?, "
            params.append(nama)
        if nisn:
            query += "nisn = ?, "
            params.append(nisn)
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
def delete_record():
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
def main():
    create_table()
    while True:
        print("\nMenu Penilaian Siswa:")
        print("1. Tambah Data")
        print("2. Tampilkan Data")
        print("3. Perbarui Data")
        print("4. Hapus Data")
        print("5. Keluar")
        
        choice = input("Pilih menu (1-5): ")
        if choice == "1":
            add_record()
        elif choice == "2":
            read_records()
        elif choice == "3":
            update_record()
        elif choice == "4":
            delete_record()
        elif choice == "5":
            print("Keluar dari program. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Jalankan program
if __name__ == "__main__":
    main()
