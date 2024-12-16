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
