import sqlite3
from datetime import datetime
from tabulate import tabulate
from validasi import validasi_tanggal, validasi_angkatan, validasi_input, nisn_ai

def tambah_siswa():
    with sqlite3.connect('UAS.db') as conn:
        cursor = conn.cursor()
        
        print("\nSelamat Datang Di Menu Input")
        nama_siswa, jk, tanggal_lahir, angkatan = validasi_input(cursor)
        
        nisn = nisn_ai(cursor)
        
        cursor.execute(
            "INSERT INTO siswa (nama, nisn, jenis_kelamin, tanggal_lahir, angkatan) VALUES (?, ?, ?, ?, ?)", 
            (nama_siswa, nisn, jk, tanggal_lahir, angkatan)
        )
        conn.commit()
        print("Data Siswa Berhasil Ditambahkan!")

def lihat_siswa():
    with sqlite3.connect('UAS.db') as conn:
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

def edit_siswa():
    with sqlite3.connect('UAS.db') as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM siswa")
        rows = cursor.fetchall()
        
        if not rows:
            print("Data Masih Kosong!")
            return
        
        try:
            id_siswa = int(input("Masukkan ID Siswa yang Ingin Di Edit: "))
            if id_siswa <= 0:
                print("Range Angka Harus Diatas 0!")
                return
        except ValueError:
            print("Input Harus Berupa Angka!")
            return

        print("Data Sebelum Pembaruan: ")
        cursor.execute("SELECT * FROM siswa WHERE id = ?", (id_siswa,))
        row = cursor.fetchone()
        if row:
            print(row)
        else:
            print("ID Siswa Tidak Ada!")
            return

        print("Masukkan Update Data: ")
        nama_siswa, jk, tanggal_lahir, angkatan = validasi_input(cursor)
        cursor.execute("""
            UPDATE siswa
            SET nama = ?, jenis_kelamin = ?, tanggal_lahir = ?, angkatan = ? 
            WHERE id = ?""", (nama_siswa, jk, tanggal_lahir, angkatan, id_siswa))
        conn.commit()

        print("Data Setelah Pembaruan: ")
        cursor.execute("SELECT * FROM siswa WHERE id = ?", (id_siswa,))
        row = cursor.fetchone()
        print(row)

def hapus_siswa():
    with sqlite3.connect('UAS.db') as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM siswa")
        rows = cursor.fetchall()
        
        if not rows:
            print("Data Masih Kosong!")
            return
        
        try:
            id_siswa = int(input("Masukkan ID Siswa yang Ingin Di Hapus: "))
            if id_siswa <= 0:
                print("Range Angka Harus Diatas 0!")
                return
        except ValueError:
            print("Input Harus Berupa Angka!")
            return

        print("Data Sebelum Penghapusan: ")
        cursor.execute("SELECT * FROM siswa WHERE id = ?", (id_siswa,))
        row = cursor.fetchone()
        if row:
            print(row)
        else:
            print("ID Siswa Tidak Ada!")
            return
        
        cursor.execute("DELETE FROM siswa WHERE id = ?", (id_siswa,))
        conn.commit()

        print("Data Setelah Penghapusan: ")
        cursor.execute("SELECT * FROM siswa")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("Data sudah tidak ada.")

def menu_siswa():
    with sqlite3.connect('UAS.db') as conn:
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

    while True:
        print("\nSelamat Datang Di Menu Halaman Siswa")
        print("1. Tambah Data Siswa")
        print("2. Lihat Data Siswa")
        print("3. Update Data Siswa")
        print("4. Hapus Data Siswa")
        print("0. Kembali Ke Menu Utama")
        try:
            pilih = int(input("Silakan Pilih Menu: "))
            if pilih == 1:
                tambah_siswa()
            elif pilih == 2:
                lihat_siswa()
            elif pilih == 3:
                edit_siswa()
            elif pilih == 4:
                hapus_siswa()
            elif pilih == 0:
                break
            else:
                print("Pilihan Tidak Valid!")
        except ValueError:
            print("Input Harus Berupa Angka!")

