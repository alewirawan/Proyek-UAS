import os
from time import sleep

#import halaman
from halaman_siswa import menu_siswa
from halaman_guru import menu_guru
from halaman_nilai import menu_nilai
from halaman_rapor_siswa import menu_rapor


# Perintah untuk membersihkan layar 
def bersihkan_layar():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def banner():
    print("\033[1;36m")  # cyan
    print("=" * 66)
    print("||                 SELAMAT DATANG DI SISTEM                     ||")
    print("||               APLIKASI PENGOLAHAN DATA SISWA                 ||")
    print("||                                                              ||")
    print("||   dibuat oleh:                                               ||")
    print("||   [1]Alejandro Wirawan        [4]M Mahesa                    ||")
    print("||   [2]Dion Enrico Aritonang    [5]Ratih Nawang Wulan          ||")
    print("||   [3]Holip Patullah                                          ||")
    print("=" * 66)
    print("\033[0m")  # reset


def tampilan_menu():
    print("\033[1;33m")  # kuning
    print("|----------------------------------------------------|")
    print("|                      MENU UTAMA                    |")
    print("|----------------------------------------------------|")
    print("| [1] Halaman                                        |")
    print("| [2] Halaman Guru                                   |")
    print("| [3] Halaman Penilaian                              |")
    print("| [4] Halaman Rapor Siswa                            |")
    print("| [0] Keluar                                         |")
    print("|----------------------------------------------------|")
    print("\033[0m") #reset


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
            pilih = input("\033[1;32mSilahkan Pilih Menu 0-4]: \033[0m")

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
                    print(
                        "\033[1;35mTerima kasih sudah menggunakan sistem ini !\033[0m"
                    )
                    sleep(2)
                    break
            else:
                print("\033[1;31mPilihan tidak valid! Silahkan pilih menu 0-4!\033[0m")
                sleep(2)
        except ValueError:
            print("\033[1;31mInput harus berupa angka!\033[0m")
            sleep(2)

if __name__ == "__main__":
    main()