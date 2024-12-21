from halaman_siswa import menu_siswa
from halaman_nilai import menu_nilai

def main() :
    while True :
        print("Selamat Datang Di Aplikasi Pengolahan Data Siswa")
        print("1. Halaman Siswa")
        print("2. Halaman Guru")
        print("3. Halaman Penilaian")
        print("4. Halaman Raport Siswa")
        print("0. KELUAR")
        try :
            pilih = int(input("Silahkan Pilih Menu : "))
            if pilih == 1 :
                menu_siswa()
            elif pilih == 2 :
                print("halaman_guru")
            elif pilih == 3 :
                menu_nilai()
            elif pilih == 4 :
                print("halaman_rapor_siswa")
            elif pilih == 0 :
                print("Terimakasih !")
                break
            else :
                print("Pilihan tidak valid. Coba lagi !")
        except ValueError :
            print("Input harus berupa angka !")

main()