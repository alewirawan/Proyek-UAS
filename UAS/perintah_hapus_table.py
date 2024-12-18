import sqlite3

def drop_table():
    conn = sqlite3.connect("UAS.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS penilaian")
        conn.commit()
        print("Tabel 'penilaian' berhasil dihapus.")
    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        conn.close()

# Panggil fungsi untuk menghapus tabel
drop_table()
