import sqlite3

def connect_database():
    """Menghubungkan ke database SQLite."""
    conn = sqlite3.connect("UAS.db")
    return conn

def display_students():
    """Menampilkan daftar siswa."""
    conn = connect_database()
    cursor = conn.cursor()

    # Mengambil semua data siswa
    cursor.execute("SELECT id, name, class FROM students")
    students = cursor.fetchall()

    conn.close()

    print("\n=== Daftar Siswa ===")
    for student in students:
        print(f"{student[0]}. {student[1]} (Kelas: {student[2]})")

    return students

def view_student_scores(student_id):
    """Menampilkan nilai siswa berdasarkan ID."""
    conn = connect_database()
    cursor = conn.cursor()

    # Mengambil detail siswa
    cursor.execute("SELECT name, class FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    
    if not student:
        print("Siswa tidak ditemukan.")
        return

    name, student_class = student

    # Mengambil nilai siswa
    cursor.execute("SELECT subject, score FROM scores WHERE student_id = ?", (student_id,))
    scores = cursor.fetchall()

    conn.close()

    # Menampilkan nilai siswa
    print("\n=== Laporan Nilai ===")
    print(f"Nama        : {name}")
    print(f"Kelas       : {student_class}")
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
        students = display_students()
        
        try:
            student_id = int(input("\nMasukkan ID siswa untuk melihat nilainya (atau 0 untuk keluar): "))
            if student_id == 0:
                print("Keluar dari sistem.")
                break

            student_ids = [student[0] for student in students]
            if student_id in student_ids:
                view_student_scores(student_id)
            else:
                print("ID siswa tidak valid.")
        except ValueError:
            print("Harap masukkan angka yang valid.")
