from siswa import halaman_siswa

def main() :
    while True :
        print("Selamat Datang Di Aplikasi Pengolahan Data Siswa")
        print("1. Halaman Siswa")
        print("2. Halaman Guru")
        print("3. KELUAR")
        try :
            pilih = int(input("Silahkan Pilih Menu : "))
            if pilih == 1 :
                halaman_siswa()
            elif pilih == 2 :
                print("halaman_guru")
            elif pilih == 3 :
                print("Terima kasih!")
                break
            else :
                print("Pilihan tidak valid. Coba lagi.")
        except ValueError :
            print("Input harus berupa angka.")

main()