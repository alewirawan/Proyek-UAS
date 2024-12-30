from tabulate import tabulate
import sqlite3

def koneksi() :
    conn = sqlite3.connect('UAS.db')
    cursor = conn.cursor()
    create_table(cursor)
    return conn, cursor

def create_table(cursor) :
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS guru (
            id_guru INTEGER PRIMARY KEY AUTOINCREMENT,
            nama VARCHAR(40) UNIQUE,
            nip INTEGER UNIQUE,
            mata_pelajaran TEXT
        )
    ''')

def tambah_guru(cursor, conn) :
    print("\nTambah Data Guru Baru")
    print("-"*50)

    while True :
        nama_guru = input("Nama Guru : ").strip().upper()
        if not nama_guru :
            print("Nama tidak boleh kosong!\n")
            continue
        if cursor.execute("SELECT COUNT(*) FROM guru WHERE nama = ?", (nama_guru,)).fetchone()[0] > 0 :
            print("Nama sudah terdaftar!")
            continue
        break

    while True :
        try :
            nip = int(input("NIP : "))
            if cursor.execute("SELECT COUNT(*) FROM guru WHERE nip = ?", (nip,)).fetchone()[0] > 0 :
                print("NIP sudah terdaftar!\n")
                continue
            break
        except ValueError :
            print("NIP harus berupa angka!\n")

    while True :
        mata_pelajaran = input("Mata Pelajaran : ").strip().upper()
        if not mata_pelajaran :
            print("Mata pelajaran tidak boleh kosong!")
            continue
        break

    try :
        cursor.execute("INSERT INTO guru (nama, nip, mata_pelajaran) VALUES (?, ?, ?)", (nama_guru, nip, mata_pelajaran))
        conn.commit()
        print("Data guru berhasil ditambahkan!")
    except sqlite3.Error as e :
        print(f"Terjadi kesalahan saat menambahkan data: {e}")

def lihat_guru(cursor) :
    print("\nDaftar Guru")
    print("-" * 50)
    cursor.execute("SELECT * FROM guru")
    rows = cursor.fetchall()
    if rows :
        headers = ["ID", "Nama", "NIP", "Mata Pelajaran"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else :   
        print("Data guru belum ditambahkan!")
        
def edit_guru(cursor, conn) :
    print("\nData Guru")
    print("-"*50)
    cursor.execute("SELECT * FROM guru")
    rows = cursor.fetchall()
    if not rows :
        print("Data Guru Masih Kosong!")
        return
    
    try :
        id_guru = int(input("Masukkan ID Guru yang Ingin Di Edit : "))
        if id_guru <= 0 :
            print("Range Angka Harus Diatas 0!")
            return
    except ValueError :
        print("Input Harus Berupa Angka!")
        return

    cursor.execute("SELECT * FROM guru WHERE id_guru = ?", (id_guru,))
    row = cursor.fetchone()
    if not row :
        print("\nID Guru Tidak Ada!")
        return
    else :
        print("\nData Sebelum Pembaruan : ")
        print(row)
        
    print("\nMasukkan Update Data : ")
    while True :
        nama_guru = input("Nama Guru : ").strip().upper()
        if not nama_guru :
            print("Nama tidak boleh kosong!\n")
            continue
        if cursor.execute("SELECT COUNT(*) FROM guru WHERE nama = ?", (nama_guru,)).fetchone()[0] > 0 :
            print("Nama sudah terdaftar!")
            continue
        break

    while True :
        try :
            nip = int(input("NIP : "))
            if cursor.execute("SELECT COUNT(*) FROM guru WHERE nip = ?", (nip,)).fetchone()[0] > 0 :
                print("NIP sudah terdaftar!\n")
                continue
            break
        except ValueError :
            print("NIP harus berupa angka!\n")

    while True :
        mata_pelajaran = input("Mata Pelajaran : ").strip().upper()
        if not mata_pelajaran :
            print("Mata pelajaran tidak boleh kosong!")
            continue
        break
    cursor.execute("""
        UPDATE guru
        SET nama = ?, nip = ?, mata_pelajaran = ? 
        WHERE id_guru = ?""", (nama_guru, nip, mata_pelajaran, id_guru))
    conn.commit()
    
    print("\nData Setelah Pembaruan: ")
    cursor.execute("SELECT * FROM guru WHERE id_guru = ?", (id_guru,))
    row = cursor.fetchone()
    print(row)

def hapus_guru(cursor, conn) :
    cursor.execute("SELECT * FROM guru")
    rows = cursor.fetchall()
        
    if not rows :
        print("Data Guru Masih Kosong!")
        return
        
    try :
        id_guru = int(input("Masukkan ID Guru yang Ingin Di Hapus: "))
        if id_guru <= 0 :
            print("Range Angka Harus Diatas 0!")
            return
    except ValueError:
        print("Input Harus Berupa Angka!")
        return
    
    print("Data Sebelum Penghapusan : ")
    cursor.execute("SELECT * FROM guru")
    rows = cursor.fetchall()    
    if rows :
        headers = ["ID", "Nama", "NIP", "Mata Pelajaran"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else :
        print("ID Guru Tidak Ada!")
        return
    
    cursor.execute("DELETE FROM guru WHERE id_guru = ?", (id_guru,))
    conn.commit()
    print("\nData Setelah Penghapusan : ")
    cursor.execute("SELECT * FROM guru")
    rows = cursor.fetchall()
    if rows :
        headers = ["ID", "Nama", "NIP", "Mata Pelajaran"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else :
        print("Data sudah tidak ada.")


def menu_guru() :
    conn, cursor = koneksi()
    while True :
        print("\nSelamat Datang di Halaman Guru!")
        print("=" * 50)
        print("Pilih Menu :")
        print("1. Tambah Data Guru Baru")
        print("2. Lihat Daftar Guru")
        print("3. Update Data Guru")
        print("4. Hapus Data Guru")
        print("0. Kembali ke Menu Utama")
        print("=" * 50)
        try :
            pilih = int(input("Silahkan Pilih Menu : "))
            if pilih == 1 :
                tambah_guru(cursor, conn)
            elif pilih == 2 :
                lihat_guru(cursor)
            elif pilih == 3 :
                edit_guru(cursor, conn)
            elif pilih == 4 :
                hapus_guru(cursor, conn)
            elif pilih == 0 :
                conn.close()
                print("")
                break
            else:
                print("Pilihan tidak valid!\n")
        except ValueError:
            print("Input harus berupa angka!\n")