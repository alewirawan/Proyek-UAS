def validasi_tanggal(tanggal_lahir_input):
    try:
        tahun, bulan, tanggal = tanggal_lahir_input.split('/')
        
        if len(tahun) != 4 or len(bulan) != 2 or len(tanggal) != 2:
            raise ValueError("Format tanggal salah. Gunakan format YYYY/MM/DD.")
        
        if not (1 <= int(bulan) <= 12):
            raise ValueError("Bulan harus antara 01 dan 12.")
        if not (1 <= int(tanggal) <= 31):
            raise ValueError("Tanggal harus antara 01 dan 31.")
        
        return f"{tahun}-{bulan}-{tanggal}"
    
    except ValueError as e:
        print(e)
        return None

def validasi_angkatan(angkatan_input):
    try:
        angkatan = int(angkatan_input)
        if len(str(angkatan)) != 4:
            raise ValueError("Angkatan harus berupa angka 4 digit.")
        if angkatan < 1900 or angkatan > 2100:
            raise ValueError("Angkatan tidak valid. Harus antara 1900 dan 2100.")
        return angkatan
    except ValueError as e:
        print(e)
        return None

def nisn_ai(cursor) :
    cursor.execute("SELECT MAX(id) FROM siswa")
    last_id = cursor.fetchone()[0]
    
    if last_id is None :
        last_id = 0
    
    nisn_auto = "241011"+ f"{last_id+1 :06d}"
    nisn = int(nisn_auto)
    return nisn

def validasi_input(cursor) :
    while True :
        nama_siswa = input("Masukkan Nama Siswa : ").strip().upper()
        if not nama_siswa :
            print("Nama Siswa Tidak Boleh Kosong !\n")
            continue        
        cursor.execute("SELECT COUNT(*) FROM siswa WHERE nama = ?", (nama_siswa,))
        if cursor.fetchone()[0] > 0 :
            print("Nama Sudah Terdaftar !")
        else :
            break
    
    while True :
        jk = input("Masukkan Jenis Kelamin (L/P) : ").upper()
        if jk not in ["L", "P"]:
            print("INPUT HARUS L ATAU P SAJA!")
        else :
            jk = 'Laki-Laki' if jk == "L" else 'Perempuan'
            break
    
    while True :
        tanggal_lahir_input = input("Masukkan Tanggal Lahir (YYYY/MM/DD) : ")
        tanggal_lahir = validasi_tanggal(tanggal_lahir_input)
        
        if tanggal_lahir :
            break
            
    while True :
        angkatan_input = input("Masukkan Angkatan (tahun) : ")
        angkatan = validasi_angkatan(angkatan_input)
        
        if angkatan is not None:
            break

    return nama_siswa, jk, tanggal_lahir, angkatan