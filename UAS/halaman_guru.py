import sqlite3
import os
from tabulate import tabulate

def warna_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def connect_db():
    conn = sqlite3.connect("UAS.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guru (
            id_guru INTEGER PRIMARY KEY AUTOINCREMENT,
            nama VARCHAR(40) UNIQUE,
            nip INTEGER UNIQUE,
            mata_pelajaran TEXT
        )
    """)
    return conn, cursor

def reset_autoincrement(cursor, conn):
    # Fungsi untuk mengatur ulang ID setelah penghapusan
    cursor.execute("SELECT * FROM guru ORDER BY id_guru")
    rows = cursor.fetchall()
    
    # Buat tabel temporary
    cursor.execute("CREATE TABLE temp_guru AS SELECT * FROM guru")
    cursor.execute("DELETE FROM guru")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='guru'")
    
    # Masukkan kembali data dengan ID baru
    for row in rows:
        cursor.execute(
            "INSERT INTO guru (nama, nip, mata_pelajaran) VALUES (?, ?, ?)",
            (row[1], row[2], row[3])
        )
    
    # Hapus tabel temporary
    cursor.execute("DROP TABLE temp_guru")
    conn.commit()

def add_teacher(cursor, conn):
    clear_screen()
    print("\n=== TAMBAH GURU ===")
    
    while True:
        nama = input("Nama Guru : ").strip().upper()
        if not nama:
            print("Nama tidak boleh kosong!")
            continue
            
        try:
            nip = int(input("NIP : "))
            mata_pelajaran = input("Mata Pelajaran : ").strip().upper()
            
            cursor.execute(
                "INSERT INTO guru (nama, nip, mata_pelajaran) VALUES (?, ?, ?)",
                (nama, nip, mata_pelajaran)
            )
            conn.commit()
            print("\nData guru berhasil ditambahkan!")
            break
        except sqlite3.IntegrityError:
            print("NIP atau Nama sudah terdaftar!")
        except ValueError:
            print("NIP harus berupa angka!")
    
    input("\nTekan Enter untuk lanjut...")

def view_teachers(cursor):
    cursor.execute("SELECT * FROM guru ORDER BY id_guru")
    rows = cursor.fetchall()
    
    if rows:
        print("\n=== DAFTAR GURU ===")
        print(tabulate(rows, headers=["ID", "Nama", "NIP", "Mata Pelajaran"], tablefmt="grid"))
    else:
        print("\nData guru masih kosong!")
    
    input("\nTekan Enter untuk lanjut...")

def update_teacher(cursor, conn):
    view_teachers(cursor)
    
    try:
        id_guru = int(input("\nMasukkan ID Guru yang ingin diedit: "))
        cursor.execute("SELECT * FROM guru WHERE id_guru = ?", (id_guru,))
        guru = cursor.fetchone()
        
        if not guru:
            print("ID Guru tidak ditemukan!")
            return
            
        nama = input("Nama Guru baru (kosongkan jika tidak diubah): ").strip().upper() or guru[1]
        nip = input("NIP baru (kosongkan jika tidak diubah): ").strip()
        nip = int(nip) if nip else guru[2]
        mata_pelajaran = input("Mata Pelajaran baru (kosongkan jika tidak diubah): ").strip().upper() or guru[3]
        
        cursor.execute(
            "UPDATE guru SET nama=?, nip=?, mata_pelajaran=? WHERE id_guru=?",
            (nama, nip, mata_pelajaran, id_guru)
        )
        conn.commit()
        print("\nData guru berhasil diupdate!")
        
    except (ValueError, sqlite3.IntegrityError) as e:
        print(f"Terjadi kesalahan: {e}")
    
    input("\nTekan Enter untuk lanjut...")

def delete_teacher(cursor, conn):
    view_teachers(cursor)
    
    try:
        id_guru = int(input("\nMasukkan ID Guru yang ingin dihapus: "))
        cursor.execute("SELECT * FROM guru WHERE id_guru = ?", (id_guru,))
        
        if not cursor.fetchone():
            print("ID Guru tidak ditemukan!")
            return
            
        confirm = input("Yakin ingin menghapus? (y/n): ").lower()
        if confirm == 'y':
            cursor.execute("DELETE FROM guru WHERE id_guru = ?", (id_guru,))
            reset_autoincrement(cursor, conn)  # Reset ID setelah penghapusan
            print("\nData guru berhasil dihapus!")
    
    except ValueError:
        print("ID harus berupa angka!")
    
    input("\nTekan Enter untuk lanjut...")

def menu_guru():
    conn, cursor = connect_db()  # Misalnya ini menghubungkan ke DB
    
    while True:
        clear_screen()
        
        # Tampilan Header dengan warna
        print(warna_text("="*40, '1;34'))  # Biru terang
        print(warna_text("           === MENU GURU ===   ", '1;34'))  # Biru terang
        print(warna_text("="*40, '1;34'))  # Biru terang
        
        # Tampilan Pilihan Menu dengan warna
        print("\n" + warna_text("[1]", '1;32') + " Tambah Guru".ljust(25) + warna_text("[2]", '1;33') + " Lihat Guru".ljust(25))
        print(warna_text("[3]", '1;36') + " Update Guru".ljust(25) + warna_text("[4]", '1;31') + " Hapus Guru".ljust(25))
        print(warna_text("[0]", '1;35') + " Keluar".ljust(25))
        
        # Input Pilihan Menu
        menu = input("\nPilih menu (0-4): ")
        
        if menu == '1':
            add_teacher(cursor, conn)
        elif menu == '2':
            view_teachers(cursor)
        elif menu == '3':
            update_teacher(cursor, conn)
        elif menu == '4':
            delete_teacher(cursor, conn)
        elif menu == '0':
            print(warna_text("\nKeluar dari program...", '1;31'))  # Merah terang
            conn.close()
            break
        else:
            print(warna_text("\nMenu tidak valid!", '1;41'))  # Latar belakang merah dengan teks putih
            input("Tekan Enter untuk lanjut...")