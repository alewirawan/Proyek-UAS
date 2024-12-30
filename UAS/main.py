import os
from time import sleep

# Import halaman
from halaman_siswa import menu_siswa
from halaman_guru import menu_guru
from halaman_nilai import menu_nilai
from halaman_rapor_siswa import menu_rapor

# Kode untuk warna
def warna_teks(teks, kode_warna):
    return f"\033[{kode_warna}m{teks}\033[0m"

# Fungsi untuk membersihkan layar 
def bersihkan_layar():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

# Fungsi banner
def banner():
    print(warna_teks("=" * 66, '1;36'))  
    print(warna_teks("||                 SELAMAT DATANG DI SISTEM                     ||", '1;36'))
    print(warna_teks("||               APLIKASI PENGOLAHAN DATA SISWA                 ||", '1;36'))
    print(warna_teks("||                                                              ||", '1;36'))
    print(warna_teks("||   dibuat oleh:                                               ||", '1;36'))
    print(warna_teks("||   [1]Alejandro Wirawan        [4]M Mahesa                    ||", '1;36'))
    print(warna_teks("||   [2]Dion Enrico Aritonang    [5]Ratih Nawang Wulan          ||", '1;36'))
    print(warna_teks("||   [3]Holip Patullah                                          ||", '1;36'))
    print(warna_teks("=" * 66, '1;36'))  

# Fungsi untuk menampilkan menu utama
def tampilan_menu():
    print(warna_teks("|----------------------------------------------------|", '1;33'))  
    print(warna_teks("|----------------------------------------------------|", '1;33'))  
    print(warna_teks("| [1] Halaman Siswa                                  |", '1;33')) 
    print(warna_teks("| [2] Halaman Guru                                   |", '1;33')) 
    print(warna_teks("| [3] Halaman Penilaian                              |", '1;33'))  
    print(warna_teks("| [4] Halaman Rapor Siswa                            |", '1;33')) 
    print(warna_teks("| [0] Keluar                                         |", '1;33'))  
    print(warna_teks("|----------------------------------------------------|", '1;33'))  

# Fungsi untuk animasi loading
def animasi_load():
    print("\nMemuat", end="")
    titik = 3
    jeda = 0.5
    for _ in range(titik):
        print(".", end="", flush=True)
        sleep(jeda)
    print("\n")

def main():
    while True:
        bersihkan_layar()
        banner()
        tampilan_menu()
        try:
            pilih = input(warna_teks("Silahkan Pilih Menu 0-4]: ", '1;32'))  

            if pilih in ["0", "1", "2", "3", "4"]:
                animasi_load()
                if pilih == "1":
                    menu_siswa()
                elif pilih == "2":
                    menu_guru()
                elif pilih == "3":
                    menu_nilai()
                elif pilih == "4":
                    menu_rapor()
                elif pilih == "0":
                    bersihkan_layar()
                    print(warna_teks("Terima kasih sudah menggunakan sistem ini!", '1;35'))  
                    sleep(2)
                    break
            else:
                print(warna_teks("Pilihan tidak valid! Silahkan pilih menu 0-4!", '1;31'))
                sleep(2)
        except ValueError:
            print(warna_teks("Input harus berupa angka!", '1;31'))
            sleep(2)

if __name__ == "__main__":
    main()
