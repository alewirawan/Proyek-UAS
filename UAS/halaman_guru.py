import sqlite3

def koneksi() :
    conn = sqlite3.connect('UAS.db')
    cursor = conn.cursor()
    create_table(cursor, conn)
    return conn, cursor

def create_table(cursor, conn) :
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guru (
            id_guru INTEGER PRIMARY KEY AUTOINCREMENT,
            nama VARCHAR(40) UNIQUE,
            nip INTEGER UNIQUE,
            mata_pelajaran TEXT
        )
    ''')
    conn.commit()

def tambah_guru(cursor, conn) :
    print("\nTambah Data Guru Baru")
    print("------------------------")
    nama_guru = input("Nama Guru: ").strip().upper()
    
    while cursor.execute("SELECT COUNT(*) FROM guru WHERE nama = ?", (nama_guru,)).fetchone()[0] > 0:
        print("Nama sudah terdaftar!")
        nama_guru = input("Nama Guru: ").strip().upper()
        
    try :
        nip = int(input("NIP: "))
        while cursor.execute("SELECT COUNT(*) FROM guru WHERE nip = ?", (nip,)).fetchone()[0] > 0:
            print("NIP sudah terdaftar!")
            nip = int(input("NIP: "))
    except ValueError :
        print("NIP harus berupa angka!")
        return
    
    mata_pelajaran = input("Mata Pelajaran: ").strip().upper()
    while not mata_pelajaran:
        print("Mata pelajaran tidak boleh kosong!")
        mata_pelajaran = input("Mata Pelajaran: ").strip().upper()

    cursor.execute("INSERT INTO guru (nama, nip, mata_pelajaran) VALUES (?, ?, ?)", (nama_guru, nip, mata_pelajaran))
    conn.commit()
    conn.close()
    
    print("Data guru berhasil ditambahkan!")
    print("")
    
def lihat_guru(cursor, conn) :
    print("\nDaftar Guru")
    print("-----------")
    cursor.execute("SELECT * FROM guru")
    rows = cursor.fetchall()
    if rows :
        print(f"{'ID':<5} {'Nama':<60} {'NIP':<15} {'Mata Pelajaran':<20}")
        print("-"*100)
        for row in rows :
            print(f"{row[0]:<5} {row[1]:<60} {row[2]:<15} {row[3]:<20}")
        print("")
    else :
        print("Data guru belum ditambahkan!")
        print("")
    conn.close()
        
def halaman_guru() :
    conn, cursor = koneksi()
    while True :
        print("Selamat Datang di Halaman Guru!")
        print("-------------------------------")
        print("Pilih Menu:")
        print("1. Tambah Data Guru Baru")
        print("2. Lihat Daftar Guru")
        print("3. Kembali ke Menu Utama")
        print("-------------------------------")

        try:
            pilih = int(input("Pilih menu: "))
            if pilih == 1:
                tambah_guru(cursor, conn)
            elif pilih == 2:
                lihat_guru(cursor)
            elif pilih == 3:
                break
            else:
                print("Pilihan tidak valid!")
                print("")
        except ValueError:
            print("Input harus berupa angka!")
            print("")