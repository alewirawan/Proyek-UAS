import sqlite3

# Membuat atau terhubung ke database SQLite
conn = sqlite3.connect("UAS.db")
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS penilaian (
    id_siswa TEXT PRIMARY KEY,
    nama TEXT NOT NULL,
    nilai REAL NOT NULL
)
""")
conn.commit()

# Fungsi untuk menambahkan penilaian (Create)
def tambah_penilaian():
    id_siswa = input("Masukkan nisn Siswa: ")
    nama = input("Masukkan Nama Siswa: ")
    try:
        nilai = float(input("Masukkan Nilai Siswa: "))
        cursor.execute("INSERT INTO penilaian (id_siswa, nama, nilai) VALUES (?, ?, ?)", (id_siswa, nama, nilai))
        conn.commit()
        print("Penilaian berhasil ditambahkan.")
    except sqlite3.IntegrityError:
        print("ID Siswa sudah ada. Gunakan ID lain.")
    except ValueError:
        print("Nilai harus berupa angka.")

# Fungsi untuk melihat semua penilaian (Read)
def lihat_penilaian():
    cursor.execute("SELECT * FROM penilaian")
    data = cursor.fetchall()
    if not data:
        print("Belum ada data penilaian.")
    else:
        print("\nData Penilaian:")
        print("ID Siswa\tNama\t\tNilai")
        print("-" * 30)
        for id_siswa, nama, nilai in data:
            print(f"{id_siswa}\t\t{nama}\t\t{nilai}")
        print("-" * 30)

# Fungsi untuk mengupdate penilaian (Update)
def ubah_penilaian():
    id_siswa = input("Masukkan ID Siswa yang ingin diubah: ")
    cursor.execute("SELECT * FROM penilaian WHERE id_siswa = ?", (id_siswa,))
    data = cursor.fetchone()
    if data:
        print(f"Data saat ini: Nama: {data[1]}, Nilai: {data[2]}")
        nama = input("Masukkan Nama Baru (kosongkan jika tidak ingin diubah): ")
        nilai = input("Masukkan Nilai Baru (kosongkan jika tidak ingin diubah): ")
        
        if nama or nilai:
            if not nama:
                nama = data[1]
            if not nilai:
                nilai = data[2]
            else:
                try:
                    nilai = float(nilai)
                except ValueError:
                    print("Nilai harus berupa angka.")
                    return
            
            cursor.execute("UPDATE penilaian SET nama = ?, nilai = ? WHERE id_siswa = ?", (nama, nilai, id_siswa))
            conn.commit()
            print("Penilaian berhasil diperbarui.")
    else:
        print("ID Siswa tidak ditemukan.")

# Fungsi untuk menghapus penilaian (Delete)
def hapus_penilaian():
    id_siswa = input("Masukkan ID Siswa yang ingin dihapus: ")
    cursor.execute("DELETE FROM penilaian WHERE id_siswa = ?", (id_siswa,))
    if cursor.rowcount > 0:
        conn.commit()
        print("Penilaian berhasil dihapus.")
    else:
        print("ID Siswa tidak ditemukan.")

# Menu utama
def menu():
    while True:
        print("\n=== Halaman Penilaian ===")
        print("1. Tambah Penilaian")
        print("2. Lihat Penilaian")
        print("3. Ubah Penilaian")
        print("4. Hapus Penilaian")
        print("5. Keluar")
        pilihan = input("Pilih menu (1/2/3/4/5): ")
        
        if pilihan == "1":
            tambah_penilaian()
        elif pilihan == "2":
            lihat_penilaian()
        elif pilihan == "3":
            ubah_penilaian()
        elif pilihan == "4":
            hapus_penilaian()
        elif pilihan == "5":
            print("Keluar dari program. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Menjalankan menu
if __name__ == "__main__":
    menu()

# Menutup koneksi database
conn.close()
