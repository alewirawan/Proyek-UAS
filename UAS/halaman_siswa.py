import sqlite3
from datetime import datetime
from validasi import validasi_tanggal, validasi_angkatan, validasi_input, nisn_ai

def tambah_siswa() :
    conn = sqlite3.connect('UAS.db')
    cursor = conn.cursor()
    
    print("\nSelamat Datang Di Menu Input")
    nama_siswa, jk, tanggal_lahir, angkatan = validasi_input(cursor)
    
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

    if rows :
        print("="*120)
        print(f"{'ID':<5} {'Nama':<40} {'NISN':<15} {'Jenis Kelamin':<15} {'Tanggal Lahir':<20} {'Angkatan':<6}")
        print("="*120)
        
        for row in rows:
            tanggal_lahir = row[4]
            tanggal_obj = datetime.strptime(tanggal_lahir, '%Y-%m-%d')
            tanggal_formatted = tanggal_obj.strftime('%d %B %Y')

            print(f"{row[0]:<5} {row[1]:<40} {row[2]:<15} {row[3]:<15} {tanggal_formatted:<20} {row[5]:<6}")
    else:
        print("Data Siswa Belum Ditambahkan!")

    conn.close()

def edit_siswa() :
    conn = sqlite3.connect('UAS.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM siswa")
    rows = cursor.fetchall()
    
    if not rows :
        print("Data Masih Kosong !")
    else :
        try :
            id_siswa = int(input("Masukkan ID Siswa yang Ingin Di Edit : "))
            if id_siswa == 0 :
                print("Range Angka Harus Diatas 0 !")
        except ValueError : 
            print("Input Harus Berupa Angka !")
        print("Data Sebelum Pembaruan : ")
        cursor.execute("SELECT * FROM siswa WHERE id = ?", (id_siswa,))
        row = cursor.fetchone()
        if row :
            print(row)
        else :
            print("ID Siswa Tidak Ada !")
        print("Masukkan Update Data : ")
        nama_siswa, jk, tanggal_lahir, angkatan = validasi_input(cursor)
        cursor.execute("""
                       UPDATE siswa
                       SET nama = ?, jenis_kelamin = ?, tanggal_lahir = ?, angkatan = ? 
                       WHERE id = ?""", (nama_siswa, jk, tanggal_lahir, angkatan, id_siswa))
        conn.commit()
        print("Data Setelah Pembaruan : ")
        cursor.execute("SELECT * FROM siswa WHERE id = ?", (id_siswa,))
        row = cursor.fetchone()
        print(row)
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
        print("1. Tambah Data Siswa")
        print("2. Lihat Data Siswa")
        print("3. Update Data Siswa")
        print("4. Kembali Ke Menu Utama")
        try :
            pilih = int(input("Silakan Pilih Menu : "))
            if pilih == 1 :
                tambah_siswa()
            elif pilih == 2 :
                lihat_siswa()
            elif pilih == 3 :
                edit_siswa()
            elif pilih == 4 :
                print("")
                break
            else :
                print("Pilihan Tidak Valid!")
        except ValueError:
            print("Input Harus Berupa Angka!")