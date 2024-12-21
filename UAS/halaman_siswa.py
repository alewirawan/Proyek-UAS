import sqlite3
from datetime import datetime
from validasi import validasi_tanggal, validasi_angkatan, nisn_ai
from tabulate import tabulate

def tambah_siswa() :
    conn = sqlite3.connect('UAS.db')
    cursor = conn.cursor()
    
    print("\nSelamat Datang Di Menu Input")
    while True :
        nama_siswa = input("Masukkan Nama Siswa : ").strip().upper()
        if not nama_siswa :
            print("Nama Siswa Tidak Boleh Kosong !\n")
            continue        
        cursor.execute("SELECT COUNT(*) FROM siswa WHERE nama = ?", (nama_siswa,))
        if cursor.fetchone()[0] > 0 :
            print("Nama Sudah Terdaftar !")
        else :
            break
    
    while True :
        jk = input("Masukkan Jenis Kelamin (L/P) : ").upper()
        if jk not in ["L", "P"]:
            print("INPUT HARUS L ATAU P SAJA!")
        else :
            jk = 'Laki-Laki' if jk == "L" else 'Perempuan'
            break
    
    while True :
        tanggal_lahir_input = input("Masukkan Tanggal Lahir (YYYY/MM/DD) : ")
        tanggal_lahir = validasi_tanggal(tanggal_lahir_input)
        
        if tanggal_lahir :
            break
            
    while True :
        angkatan_input = input("Masukkan Angkatan (tahun) : ")
        angkatan = validasi_angkatan(angkatan_input)
        
        if angkatan is not None:
            break
    
    nisn = nisn_ai(cursor)
    
    cursor.execute(
        "INSERT INTO siswa (nama, nisn, jenis_kelamin, tanggal_lahir, angkatan) VALUES (?, ?, ?, ?, ?)", 
        (nama_siswa, nisn, jk, tanggal_lahir, angkatan)
    )
    conn.commit()
    print("Data Siswa Berhasil Ditambahkan !")
    
    conn.close()

def lihat_siswa() :
    conn = sqlite3.connect('UAS.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM siswa")
    rows = cursor.fetchall()

    if rows:
        headers = ['ID', 'Nama', 'NISN', 'Jenis Kelamin', 'Tanggal Lahir', 'Angkatan']
        
        formatted_rows = []
        for row in rows:
            tanggal_lahir = row[4]
            tanggal_obj = datetime.strptime(tanggal_lahir, '%Y-%m-%d')
            tanggal_formatted = tanggal_obj.strftime('%d %B %Y')
            formatted_rows.append([row[0], row[1], row[2], row[3], tanggal_formatted, row[5]])

        print(tabulate(formatted_rows, headers=headers, tablefmt="grid"))
    else:
        print("Data Siswa Belum Ditambahkan!")

    conn.close()

def menu_siswa() :
    conn = sqlite3.connect('UAS.db')
    cursor = conn.cursor()
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS siswa
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nama VARCHAR(40) UNIQUE,  
        nisn INTEGER UNIQUE, 
        jenis_kelamin TEXT CHECK(jenis_kelamin IN ('Laki-Laki', 'Perempuan')),
        tanggal_lahir DATE,
        angkatan INTEGER CHECK (angkatan BETWEEN 1900 AND 2100))'''  
    )
    conn.commit()
    conn.close()

    while True :
        print("\nSelamat Datang Di Menu Halaman Siswa")
        print("="*30)
        print("1. Tambah Data Siswa")
        print("2. Lihat Data Siswa")
        print("3. Kembali Ke Menu Utama")
        print("="*30)
        try :
            pilih = int(input("Silakan Pilih Menu : "))
            if pilih == 1 :
                tambah_siswa()
            elif pilih == 2 :
                lihat_siswa()
            elif pilih == 3 :
                print("")
                break
            else :
                print("Pilihan Tidak Valid !")
        except ValueError:
            print("Input Harus Berupa Angka !")