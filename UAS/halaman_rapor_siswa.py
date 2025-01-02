import sqlite3
from tabulate import tabulate


def warna_teks(teks, kode_warna):
    return f"\033[{kode_warna}m{teks}\033[0m"


def hubungkan_database():
    return sqlite3.connect("UAS.db")


def tampilkan_daftar_siswa():
    koneksi = hubungkan_database()
    kursor = koneksi.cursor()
    kursor.execute("SELECT id, nama, nisn FROM siswa")
    daftar_siswa = kursor.fetchall()
    koneksi.close()

    print(warna_teks("\n=== Daftar Siswa ===", "1;36"))
    headers = [
        warna_teks("No", "1;33"),
        warna_teks("Nama", "1;33"),
        warna_teks("NISN", "1;33"),
    ]
    data_siswa = [
        [
            warna_teks(str(s[0]), "1;37"),
            warna_teks(s[1], "1;37"),
            warna_teks(str(s[2]), "1;37"),
        ]
        for s in daftar_siswa
    ]
    print(tabulate(data_siswa, headers=headers, tablefmt="double_grid"))
    return daftar_siswa


def lihat_nilai_siswa(nisn):
    koneksi = hubungkan_database()
    kursor = koneksi.cursor()
    kursor.execute("SELECT nama, nisn FROM siswa WHERE nisn = ?", (nisn,))
    siswa = kursor.fetchone()

    if not siswa:
        print(warna_teks("Data siswa tidak ditemukan.", "1;31"))
        return

    nama, nisn = siswa
    kursor.execute("SELECT mapel, nilai FROM penilaian WHERE nisn = ?", (nisn,))
    nilai_siswa = kursor.fetchall()
    koneksi.close()

    print(warna_teks("\n=== Laporan Nilai Siswa ===", "1;35"))
    print(warna_teks(f"Nama Siswa: {nama}", "1;37"))
    print(warna_teks(f"NISN: {nisn}", "1;37"))

    if not nilai_siswa:
        print(warna_teks("\nBelum ada data nilai untuk siswa ini.", "1;33"))
        return

    print(warna_teks("\nDaftar Nilai:", "1;32"))
    headers = [warna_teks("Mata Pelajaran", "1;33"), warna_teks("Nilai", "1;33")]
    table_color = [
        [warna_teks(mapel, "1;37"), warna_teks(str(nilai), "1;37")]
        for mapel, nilai in nilai_siswa
    ]
    print(tabulate(table_color, headers=headers, tablefmt="double_grid"))

    total_nilai = sum(nilai for _, nilai in nilai_siswa)
    rata_rata = total_nilai / len(nilai_siswa)

    print(warna_teks("\nRingkasan Nilai:", "1;35"))
    print(warna_teks(f"Total Nilai    : {total_nilai}", "1;37"))
    print(warna_teks(f"Rata-rata      : {rata_rata:.2f}", "1;37"))
    print(warna_teks("=" * 40, "1;36"))


def menu_rapor():
    print(warna_teks("=" * 40, "1;36"))
    print(warna_teks("SISTEM INFORMASI NILAI SISWA", "1;35"))
    print(warna_teks("=" * 40, "1;36"))

    while True:
        try:
            daftar_siswa = tampilkan_daftar_siswa()
            nisn = input(warna_teks("\nMasukkan NISN siswa (0 untuk keluar): ", "1;32"))
            if nisn == "0":
                print(
                    warna_teks("\nTerima kasih telah menggunakan sistem ini.", "1;33")
                )
                break

            nisn_terdaftar = [str(s[2]) for s in daftar_siswa]
            if nisn in nisn_terdaftar:
                lihat_nilai_siswa(nisn)
            else:
                print(warna_teks("NISN tidak terdaftar dalam sistem.", "1;31"))

        except ValueError as e:
            print(warna_teks(f"Terjadi kesalahan: {str(e)}", "1;31"))
            print(warna_teks("Mohon masukkan data yang valid.", "1;33"))
        except Exception as e:
            print(warna_teks(f"Terjadi kesalahan sistem: {str(e)}", "1;31"))
            print(warna_teks("Silakan coba lagi.", "1;33"))
