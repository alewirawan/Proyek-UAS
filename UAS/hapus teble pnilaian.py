import sqlite3

def delete_penilaian_table():
    try:
        # Membuka koneksi ke database
        conn = sqlite3.connect('UAS.db')
        cursor = conn.cursor()
        
        # Perintah untuk menghapus tabel
        cursor.execute("DROP TABLE IF EXISTS penilaian;")
        conn.commit()
        
        print("Tabel 'penilaian' berhasil dihapus (jika ada).")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()

# Memanggil fungsi untuk menghapus tabel
delete_penilaian_table()
