from halaman_siswa import menu_siswa
from halaman_nilai import menu_nilai
from halaman_guru import menu_guru


def main() :
    while True :
        print("Selamat Datang Di Aplikasi Pengolahan Data Siswa")
        print("="*50)
        print("1. Halaman Siswa")
        print("2. Halaman Guru")
        print("3. Halaman Penilaian")
        print("4. Halaman Raport Siswa")
        print("0. KELUAR")
        print("="*50)
        try :
            pilih = int(input("Silahkan Pilih Menu : "))
            if pilih == 1 :
                menu_siswa()
            elif pilih == 2 :
                menu_guru()
            elif pilih == 3 :
                menu_nilai()
            elif pilih == 4 :
                print("halaman_rapor_siswa")
            elif pilih == 0 :
                print("Terima kasih !")
                break
            else :
                print("Pilihan tidak valid. Coba lagi !")
        except ValueError :
            print("Input harus berupa angka !")

main()