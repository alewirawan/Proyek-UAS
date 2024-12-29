import sqlite3
from tabulate import tabulate


def hubungkan_database():
    """Menghubungkan ke database SQLite."""
    koneksi = sqlite3.connect("UAS.db")
    return koneksi


def tampilkan_daftar_siswa():
    """Menampilkan daftar seluruh siswa."""
    koneksi = hubungkan_database()
    kursor = koneksi.cursor()

    # Mengambil semua data siswa
    kursor.execute("SELECT id, nama, nisn FROM siswa")
    daftar_siswa = kursor.fetchall()

    koneksi.close()

    print("\n=== Daftar Siswa ===")
    # Menggunakan tabulate untuk tampilan yang lebih rapi
    headers = ["No", "Nama", "NISN"]
    data_siswa = [[s[0], s[1], s[2]] for s in daftar_siswa]
    print(tabulate(data_siswa, headers=headers, tablefmt="grid"))

    return daftar_siswa


def lihat_nilai_siswa(nisn):
    """Menampilkan nilai siswa berdasarkan NISN."""
    koneksi = hubungkan_database()
    kursor = koneksi.cursor()

    # Mengambil detail siswa
    kursor.execute("SELECT nama, nisn FROM siswa WHERE nisn = ?", (nisn,))
    siswa = kursor.fetchone()

    if not siswa:
        print("Data siswa tidak ditemukan.")
        return

    nama, nisn = siswa

    # Mengambil nilai siswa
    kursor.execute("SELECT mapel, nilai FROM penilaian WHERE nisn = ?", (nisn,))
    nilai_siswa = kursor.fetchall()

    koneksi.close()

    # Menampilkan nilai siswa dengan format yang lebih rapi
    print("\n=== Laporan Nilai Siswa ===")
    print(f"Nama Siswa: {nama}")
    print(f"NISN: {nisn}")

    if not nilai_siswa:
        print("\nBelum ada data nilai untuk siswa ini.")
        return

    print("\nDaftar Nilai:")
    headers = ["Mata Pelajaran", "Nilai"]
    print(tabulate(nilai_siswa, headers=headers, tablefmt="grid"))

    # Menghitung statistik nilai
    total_nilai = sum(nilai for _, nilai in nilai_siswa)
    rata_rata = total_nilai / len(nilai_siswa)

    print("\nRingkasan Nilai:")
    print(f"Total Nilai    : {total_nilai}")
    print(f"Rata-rata      : {rata_rata:.2f}")
    print("=" * 40 + "\n")


def menu_rapor():
    print("=" * 40)
    print("SISTEM INFORMASI NILAI SISWA")
    print("=" * 40)

    while True:
        try:
            daftar_siswa = tampilkan_daftar_siswa()
            nisn = input("\nMasukkan NISN siswa (0 untuk keluar): ")
            if nisn == "0":
                print("\nTerima kasih telah menggunakan sistem ini.")
                break

            # Memeriksa apakah NISN valid
            nisn_terdaftar = [str(s[2]) for s in daftar_siswa]
            if nisn in nisn_terdaftar:
                lihat_nilai_siswa(nisn)
            else:
                print("NISN tidak terdaftar dalam sistem.")

        except ValueError as e:
            print(f"Terjadi kesalahan: {str(e)}")
            print("Mohon masukkan data yang valid.")
        except Exception as e:
            print(f"Terjadi kesalahan sistem: {str(e)}")
            print("Silakan coba lagi.")
