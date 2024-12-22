import sqlite3
from tabulate import tabulate


def connect_database():
    """Menghubungkan ke database SQLite."""
    conn = sqlite3.connect("UAS.db")
    return conn


def display_students():
    """Menampilkan daftar siswa."""
    conn = connect_database()
    cursor = conn.cursor()
    # Mengambil semua data siswa
    cursor.execute("SELECT id, nama, nisn FROM siswa")
    siswa = cursor.fetchall()

    conn.close()

    print("\n=== Daftar Siswa ===")
    for s in siswa:
        print(f"{s[0]}. {s[1]} (NISN: {s[2]})")

    return siswa


def view_student_scores(nisn):
    """Menampilkan nilai siswa berdasarkan NISN."""
    conn = connect_database()
    cursor = conn.cursor()

    # Mengambil detail siswa
    cursor.execute("SELECT nama, nisn FROM siswa WHERE nisn = ?", (nisn,))
    student = cursor.fetchone()

    if not student:
        print("Siswa tidak ditemukan.")
        return

    nama, nisn = student

    # Mengambil nilai siswa
    cursor.execute("SELECT mapel, nilai FROM penilaian WHERE nisn = ?", (nisn,))
    scores = cursor.fetchall()

    conn.close()

    # Menampilkan nilai siswa
    print("\n=== Laporan Nilai ===")
    print(f"Nama        : {nama}")
    print(f"NISN        : {nisn}")
    print("\nMata Pelajaran dan Nilai:")
    print("-------------------------")

    total_score = 0
    for subject, score in scores:
        print(f"{subject:<15} : {score}")
        total_score += score

    average_score = total_score / len(scores) if scores else 0
    print("\n-------------------------")
    print(f"Total Nilai : {total_score}")
    print(f"Rata-rata   : {average_score:.2f}")
    print("========================\n")


if __name__ == "__main__":
    print("=== Sistem Laporan Nilai Siswa ===")

    while True:
        siswa = display_students()

        try:
            nisn = input(
                "\nMasukkan NISN siswa untuk melihat nilainya (atau 0 untuk keluar): "
            )
            if nisn == "0":
                print("Keluar dari sistem.")
                break

            nisn_list = [str(s[2]) for s in siswa]  # Mengambil NISN dari daftar siswa
            if nisn in nisn_list:
                view_student_scores(nisn)
            else:
                print("NISN siswa tidak valid.")
        except ValueError:
            print("Harap masukkan data yang valid.")
