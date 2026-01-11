import os
os.system('cls')

data_nilai = (
    (range(81, 101), "A"),
    (range(61, 81), "B"),
    (range(41, 61), "C"),
    (range(21, 41), "D"),
    (range(0, 21), "E")
)

data_ipk = (
    ((3.51, 4.01), "Cumlaude"),
    ((3.00, 3.51), "Sangat Memuaskan"),
    ((0.00, 3.00), "Memuaskan")
)

data_bobot = {
    'A': {"bobot": 4.0},
    'B': {"bobot": 3.0},
    'C': {"bobot": 2.0},
    'D': {"bobot": 1.0},
    'E': {"bobot": 0.0},
}

prodi = {
    '04': {"studi": 'Informatika'},
    '19': {"studi": 'Informatika Medis'},
    '03': {"studi": 'Sistem Informasi'}
}

while True:
    npm = input("Masukkan NPM      : ")
    nama = input("Masukkan Nama     : ")

    print("\nKode Prodi:")
    for kode, kp in prodi.items():
        print(f"{kode} - {kp['studi']}")
        
    kd_prodi = input("Masukkan Kode Prodi       : ")
    mata_kuliah = int(input("\nMasukkan Jumlah Mata Kuliah        : "))

    matkul = []
    for i in range(1, mata_kuliah + 1):
        print(f"\n---  Mata Kuliah {i}  ---")
        nm_matkul = input("Nama Mata Kuliah : ")
        nil_ang = float(input("Nilai Angka    : "))
        jum_sks = int(input("SKS    : "))
        
        huruf = None
        for item, data in data_nilai:
            if nil_ang in item:
                huruf = data
                break

        hasil_bobot = (data_bobot[huruf]["bobot"])

        matkul.append({
        "nama": nm_matkul,
        "sks": jum_sks,
        "nilai_angka": nil_ang,
        "hrf": huruf,
        "hsl_bbt": hasil_bobot,
        "total": hasil_bobot * jum_sks
        })
    print("\n")
    print("="*50)
    print("             HASIL KONVERSI NILAI")
    print("="*50)
    print("NPM  :",npm)
    print("NAMA :",nama)
    if kd_prodi in prodi:
        prod = prodi[kd_prodi]
    print(f"PRODI   : {prod['studi']}")
    print("-"*50)
    print("\nDaftar Nilai:")
    print(f"Mata Kuliah               Nilai   SKS     Huruf   Bobot   Total")
    print("-"*63)
    for m in matkul:
        print(f"{m['nama']:<25} {m['nilai_angka']:<8} {m['sks']:<8} {m['hrf']:<7} {m['hsl_bbt']:<7} {m['total']:<8}")
    print("-"*63)

    total = sum(q['total'] for q in matkul)
    total_sks = sum(q['sks'] for q in matkul)
    ipk = total / total_sks

    prediket = None
    for w, e in data_ipk:
        if w[0] <= ipk < w[1]:
            prediket = e
            break
    print(f"IPK     : {ipk}")
    print(f"Predikat    : {prediket}")
    ulang = input("Ingin Input Mahasiswa Lagi? (y/n): ").lower()
    os.system('cls')
    if ulang != 'y':
        break






