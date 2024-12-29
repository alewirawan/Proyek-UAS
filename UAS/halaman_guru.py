from tabulate import tabulate
import sqlite3

def koneksi():
    conn = sqlite3.connect('UAS.db')
    cursor = conn.cursor()
    create_table(cursor)
    return conn, cursor

def create_table(cursor):
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS guru (
            id_guru INTEGER PRIMARY KEY AUTOINCREMENT,
            nama VARCHAR(40) UNIQUE,
            nip INTEGER UNIQUE,
            mata_pelajaran TEXT
        )
    ''')

def tambah_guru(cursor, conn):
    print("\nTambah Data Guru Baru")
    print("------------------------")

    while True:
        nama_guru = input("Nama Guru: ").strip().upper()
        if not nama_guru:
            print("Nama tidak boleh kosong!")
            continue
        if cursor.execute("SELECT COUNT(*) FROM guru WHERE nama = ?", (nama_guru,)).fetchone()[0] > 0:
            print("Nama sudah terdaftar!")
            continue
        break

    while True:
        try:
            nip = int(input("NIP: "))
            if cursor.execute("SELECT COUNT(*) FROM guru WHERE nip = ?", (nip,)).fetchone()[0] > 0:
                print("NIP sudah terdaftar!")
                continue
            break
        except ValueError:
            print("NIP harus berupa angka!")

    while True:
        mata_pelajaran = input("Mata Pelajaran: ").strip().upper()
        if not mata_pelajaran:
            print("Mata pelajaran tidak boleh kosong!")
            continue
        break

    try:
        cursor.execute("INSERT INTO guru (nama, nip, mata_pelajaran) VALUES (?, ?, ?)", (nama_guru, nip, mata_pelajaran))
        conn.commit()
        print("Data guru berhasil ditambahkan!\n")
    except sqlite3.Error as e:
        print(f"Terjadi kesalahan saat menambahkan data: {e}")

def lihat_guru(cursor):
    print("\nDaftar Guru")
    print("=" * 120)
    cursor.execute("SELECT * FROM guru")
    rows = cursor.fetchall()
    if rows:
        headers = ["ID", "Nama", "NIP", "Mata Pelajaran"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:   
        print("Data guru belum ditambahkan!\n")

def menu_guru():
    conn, cursor = koneksi()
    try:
        while True:
            print("\nSelamat Datang di Halaman Guru!")
            print("=" * 30)
            print("Pilih Menu:")
            print("1. Tambah Data Guru Baru")
            print("2. Lihat Daftar Guru")
            print("3. Kembali ke Menu Utama")
            print("=" * 30)

            try:
                pilih = int(input("Silahkan Pilih Menu: "))
                if pilih == 1:
                    tambah_guru(cursor, conn)
                elif pilih == 2:
                    lihat_guru(cursor)
                elif pilih == 3:
                    print("Kembali ke menu utama.\n")
                    break
                else:
                    print("Pilihan tidak valid!\n")
            except ValueError:
                print("Input harus berupa angka!\n")
    finally:
        conn.close()
        print("Koneksi database ditutup.")
