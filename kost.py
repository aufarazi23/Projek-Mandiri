import os
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import getpass
import datetime
os.system('cls')

konek = sqlite3.connect("kost.db")
cursor = konek.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS kamar(
    id_kamar INTEGER PRIMARY KEY AUTOINCREMENT,
    nomor_kamar TEXT NOT NULL,
    tipe_kamar TEXT NOT NULL,
    harga INTEGER NOT NULL,
    status TEXT NOT NULL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS penyewa(
    id_penyewa INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    no_hp TEXT NOT NULL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sewa(
    id_sewa INTEGER PRIMARY KEY AUTOINCREMENT,
    id_kamar INTEGER,
    id_penyewa INTEGER,
    tanggal_masuk TEXT NOT NULL,
    lama_sewa INTEGER NOT NULL,
    total_bayar INTEGER NOT NULL,
    FOREIGN KEY (id_kamar) REFERENCES kamar(id_kamar),
    FOREIGN KEY (id_penyewa) REFERENCES penyewa(id_penyewa)
)""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS login_tb(
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)""")

def menu_penyewa():
    os.system('cls')
    print("""
Selamat Datang di RaziKost
1. Lihat Kamar 
2. Sewa Kamar
3. Keluar
""")
    pilih_menu = int(input("Silahkan Pilih Menu : "))
    if pilih_menu == 1:
        os.system('cls')
        lihat_kamar('Penyewa')
    elif pilih_menu == 2:
        os.system('cls')
        sewa_kamar()
    else:
        os.system('cls')
        login()

def menu_admin():
    os.system('cls')
    print("""       --- Selamat Datang di RaziKost (Admin) ---
          
1. Lihat Kamar 
2. Lihat Penyewa
3. Tambah Kamar
4. Riwayat Sewa
5. Akhiri Sewa
6. Visualisasi Data
7. Keluar
""")
    pilih_menu = int(input("Silahkan Pilih Menu : "))
    if pilih_menu == 1:
        os.system('cls')
        lihat_kamar('Admin')
    elif pilih_menu == 2:
        os.system('cls')
        lihat_penyewa()
    elif pilih_menu == 3:
        os.system('cls')
        tambah_kamar("","","","Kosong")
    elif pilih_menu == 4:
        os.system('cls')
        transaksi_sewa()
    elif pilih_menu == 5:
        akhiri_sewa()
    elif pilih_menu == 6:
        menu_visualisasi()
    else:
        os.system('cls')
        login()

def new_user(user,password,role):
    os.system('cls')
    user = input("Masukkan Username Baru : ")
    password = input("Masukkan Password Baru : ")
    cursor.execute("""
        INSERT INTO login_tb(user,password,role)
        VALUES (?,?,?)
    """,(user,password,role))
    konek.commit()
    print("Username Berhasil Dibuat.")
    os.system('cls')

def tambah_kamar(nomor_kmr,tipe,harga,status):
    nomor_kmr = input("Masukkan Nomor Kamar : ")
    tipe = input("Masukkan Tipe Kamar : ")
    harga = int(input("Masukkan Harga Kamar : Rp."))
    cursor.execute("""
        INSERT INTO kamar(nomor_kamar,tipe_kamar,harga,status)
        VALUES (?,?,?,?)
    """,(nomor_kmr,tipe,harga,status))
    konek.commit()
    
def lihat_kamar(role):
    while True:
        cursor.execute("SELECT * FROM kamar")
        data = cursor.fetchall()
        os.system('cls')
        print(f"{'No':<5}{'Nomor Kamar':<15}{'Tipe Kamar':<15}{'Harga':<15}{'Status'}")
        print("-"*55)
        for i, row in enumerate(data,start=1):
            print(f"{i:<5}{row[1]:<15}{row[2]:<15}{row[3]:<15}{row[4]}")

        back = input("Kembali ke halaman menu (y/t)? ").lower()
        if back == 'y':
            if role == "Admin":
                menu_admin()
            else:
                menu_penyewa()
        else:
            break
        
def lihat_penyewa():
    os.system('cls')
    while True:
        cursor.execute("""
            SELECT 
                sewa.id_sewa,
                kamar.nomor_kamar,
                penyewa.nama,
                sewa.tanggal_masuk,
                sewa.lama_sewa,
                sewa.total_bayar,
                penyewa.id_penyewa,
                penyewa.no_hp
            FROM sewa
            JOIN kamar ON sewa.id_kamar = kamar.id_kamar
            JOIN penyewa ON sewa.id_penyewa = penyewa.id_penyewa
            WHERE kamar.status = 'Terisi'
        """)
        data = cursor.fetchall()
        os.system('cls')
        print("Daftar Penyewa: ")
        
        if len(data) == 0:
            print("Tidak ada penyewa aktif")
        else:
            print(f"{'No':<5}{'Nama':<15}{'Hp':<15}{'Kamar'}")
            print("-"*40)
            for i,row in enumerate(data,start=1):
                print(f"{i:<5}{row[2]:<15}{row[7]:<15}{row[1]}")

        back = input("Kembali ke halaman menu (y/t)? ").lower()
        if back == 'y':
            menu_admin()
        else:
            continue

def sewa_kamar():
    os.system('cls')
    while True :
        print("Daftar Kamar Tersedia")
        cursor.execute("SELECT * FROM kamar WHERE status='Kosong'")
        kamar_kosong = cursor.fetchall()
        for row in kamar_kosong:
            print(row)
        if not kamar_kosong:
            print("Kamar tidak tersedia")
            back = input("Kembali ke halaman menu (y/)? ").lower()
            if back == 'y':
                menu_penyewa()
            else:
                print("Tidak ada kamar!")
            return
        no_kamar = input("Masukkan nomor kamar yang mau disewa : ")
        nama_penyewa = input("Masukkan nama penyewa : ")
        hp = input("Masukkan nomor hp : ")

        cursor.execute("""
        INSERT INTO penyewa(nama,no_hp) 
        VALUES (?,?)""",(nama_penyewa,hp))
        konek.commit()

        id_penyewa = cursor.lastrowid
        lama_sewa = int(input("Lama sewa (bulan) : "))
        cursor.execute("SELECT harga FROM kamar WHERE id_kamar=?",(no_kamar))
        harga = cursor.fetchone()[0]
        tanggal_masuk = datetime.datetime.now().strftime("%Y-%m-%d")
        total = lama_sewa * harga
        print(f"Total Bayar  : {total}")

        cursor.execute("""
        INSERT INTO sewa(id_kamar,id_penyewa,tanggal_masuk,lama_sewa,total_bayar)
        VALUES (?,?,?,?,?)
        """,(no_kamar,id_penyewa,tanggal_masuk,lama_sewa,total))
        konek.commit()

        cursor.execute("UPDATE kamar SET status='Terisi' WHERE id_kamar=?",(no_kamar,))
        konek.commit()
        print("Sewa Berhasil")
        back = input("Kembali ke halaman menu (y/t)? ").lower()
        if back == 'y':
            menu_penyewa()
        else:
            continue
    

def transaksi_sewa():
    os.system('cls')
    while True:
        print("===== DATA TRANSAKSI SEWA KAMAR =====\n")

        cursor.execute("""
            SELECT 
                sewa.id_sewa,
                kamar.nomor_kamar,
                penyewa.nama,
                sewa.tanggal_masuk,
                sewa.lama_sewa,
                sewa.total_bayar
            FROM sewa
            JOIN kamar ON sewa.id_kamar = kamar.id_kamar
            JOIN penyewa ON sewa.id_penyewa = penyewa.id_penyewa
        """)

        data = cursor.fetchall()

        if len(data) == 0:
            print("Belum ada transaksi sewa")
        else:
            print(f"{'ID':<5}{'Kamar':<15}{'Penyewa':<15}{'Masuk':<15}{'Lama':<7}{'Total'}")
            print("-" * 65)
            for row in data:
                print(f"{row[0]:<5}{row[1]:<15}{row[2]:<15}{row[3]:<15}{row[4]:<7}{row[5]}")

        back = input("Kembali ke halaman menu (y/t)? ").lower()
        if back == 'y':
            menu_admin()
        else:
            continue

def akhiri_sewa():
    os.system('cls')
    while True:
        print("=== AKHIRI SEWA ===\n")

        cursor.execute("""
            SELECT 
                kamar.id_kamar,
                kamar.nomor_kamar,
                kamar.tipe_kamar,
                penyewa.nama
            FROM sewa
            JOIN kamar ON sewa.id_kamar = kamar.id_kamar
            JOIN penyewa ON sewa.id_penyewa = penyewa.id_penyewa
            WHERE kamar.status = 'Terisi'
        """)
        data = cursor.fetchall()

        if not data:
            print("Tidak ada kamar yang sedang disewa.")
            back = input("Kembali ke halaman menu (y/t)? ").lower()
            if back == 'y':
                menu_admin()
            else:
                continue

        print("Kamar yang sedang terisi:\n")
        for d in data:
            print(f"ID: {d[0]} | Kamar: {d[1]} | Tipe: {d[2]} | Penyewa: {d[3]}")

        id_kamar = int(input("\nMasukkan ID kamar yang mau diakhiri sewanya: "))

        cursor.execute(
            "UPDATE kamar SET status='Kosong' WHERE id_kamar=?",
            (id_kamar,)
        )
        konek.commit()

        print("Sewa berhasil diakhiri. Status kamar sekarang Kosong.")
        back = input("Kembali ke halaman menu (y/t)? ").lower()
        if back == 'y':
            menu_admin()
        else:
            continue

def menu_visualisasi():
    os.system('cls')
    print("""
=== VISUALISASI DATA KOST ===
1. Kamar Kosong vs Terisi
2. Pendapatan per Bulan
3. Tipe Kamar Paling Laku
4. Kembali
""")
    pilih = int(input("Pilih: "))

    if pilih == 1:
        visual_kamar_status()
    elif pilih == 2:
        visual_pendapatan_bulanan()
    elif pilih == 3:
        visual_tipe_kamar()
    else:
        menu_admin()

def visual_kamar_status():
    cursor.execute("""
        SELECT status, COUNT(*) 
        FROM kamar 
        GROUP BY status
    """)
    data = cursor.fetchall()

    if not data:
        print("Belum ada data kamar.")
        return

    status = [d[0] for d in data]
    jumlah = [d[1] for d in data]

    plt.figure()
    plt.pie(jumlah, labels=status, autopct='%1.1f%%', startangle=90)
    plt.title("Status Kamar Kost")
    plt.axis('equal')
    plt.show()

    pilih = input("Ingin melihat visualisasi yang lain? (y/t): ").lower()
    if pilih == 'y':
        menu_visualisasi()
    else:
        menu_admin()

def visual_pendapatan_bulanan():
    cursor.execute("""
        SELECT substr(tanggal_masuk,1,7) AS bulan,
               SUM(total_bayar)
        FROM sewa
        GROUP BY bulan
    """)
    data = cursor.fetchall()

    bulan = [d[0] for d in data]
    total = [d[1] for d in data]
    bulan_label = []
    for b in bulan:
        dt = datetime.datetime.strptime(b, "%Y-%m")
        bulan_label.append(dt.strftime("%B %Y"))

    plt.figure()
    plt.bar(bulan_label, total)
    plt.title("Pendapatan per Bulan")
    plt.xlabel("Bulan")
    plt.ylabel("Total Pendapatan")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    pilih = input("Ingin melihat visualisasi yang lain? (y/t): ").lower()
    if pilih == 'y':
        menu_visualisasi()
    else:
        menu_admin()


def visual_tipe_kamar():
    cursor.execute("""
        SELECT kamar.tipe_kamar, COUNT(sewa.id_sewa)
        FROM sewa
        JOIN kamar ON sewa.id_kamar = kamar.id_kamar
        GROUP BY kamar.tipe_kamar
    """)
    data = cursor.fetchall()

    tipe = [d[0] for d in data]
    jumlah = [d[1] for d in data]

    plt.figure()
    sns.barplot(x=tipe, y=jumlah)
    plt.title("Tipe Kamar Paling Laku")
    plt.xlabel("Tipe Kamar")
    plt.ylabel("Jumlah Disewa")
    plt.show()

    pilih = input("Ingin melihat visualisasi yang lain? (y/t): ").lower()
    if pilih == 'y':
        menu_visualisasi()
    else:
        menu_admin()

def login():
    while True:
        sign = input("Udah punya akun? (y/t)? ").lower()
        if sign == 'y':
            os.system('cls')
            user_login = input("Masukkan Username : ")
            pass_login = getpass.getpass("Masukkan Password : ")

            cursor.execute(" SELECT * FROM login_tb WHERE user=? AND password=?",(user_login,pass_login))
            login = cursor.fetchone()

            if login:
                role = login[3]
                if role == "Penyewa":
                    menu_penyewa()
                else:
                    menu_admin()
                break
            else:
                print("Username atau Password Salah!")

        elif sign == 't':
            new_user("", "", "Penyewa")
            input("Akun berhasil dibuat! Tekan Enter untuk login...")
            os.system('cls')

        else:
            print("Input nggak valid, ketik y atau t!")
login()
