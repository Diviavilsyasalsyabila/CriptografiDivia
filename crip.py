# Import library yang dibutuhkan
import hashlib  # untuk membuat hash SHA-256
import json     # untuk menyimpan data ke file
import os       # untuk membersihkan layar
import getpass  # agar password tidak terlihat saat diketik

# Nama file tempat menyimpan data username dan password yang sudah di-hash
FILE_DATA = "data_pengguna.json"

# ==============================================
# PENGATURAN WARNA TEKS DI TERMINAL
# Kode warna ini membuat tampilan lebih menarik
# ==============================================
RESET   = "\033[0m"   # kembali ke warna normal
BOLD    = "\033[1m"   # teks tebal
DIM     = "\033[2m"   # teks redup

MERAH   = "\033[91m"  # warna merah
HIJAU   = "\033[92m"  # warna hijau
KUNING  = "\033[93m"  # warna kuning
BIRU    = "\033[94m"  # warna biru
MAGENTA = "\033[95m"  # warna ungu
CYAN    = "\033[96m"  # warna biru muda
PUTIH   = "\033[97m"  # warna putih

BG_BIRU  = "\033[44m"  # latar belakang biru
BG_HIJAU = "\033[42m"  # latar belakang hijau
BG_MERAH = "\033[41m"  # latar belakang merah
BG_HITAM = "\033[40m"  # latar belakang hitam


# ==============================================
# FUNGSI-FUNGSI TAMPILAN
# ==============================================

# Fungsi untuk membersihkan layar terminal
def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")

# Fungsi untuk mencetak garis pemisah
def cetak_garis(karakter="═", panjang=60, warna=CYAN):
    print(f"{warna}{karakter * panjang}{RESET}")

# Fungsi untuk menampilkan banner/judul program di bagian atas
def tampilkan_judul():
    bersihkan_layar()
    cetak_garis("═", 60, CYAN)
    print(f"{CYAN}║{RESET}{BG_BIRU}{BOLD}{PUTIH}{'🔐  SISTEM REGISTRASI & LOGIN AMAN':^58}{RESET}{CYAN}║{RESET}")
    print(f"{CYAN}║{RESET}{'':^58}{CYAN}║{RESET}")
    print(f"{CYAN}║{RESET}{BIRU}{'  Keamanan Password dengan Hash SHA-256':^58}{RESET}{CYAN}║{RESET}")
    cetak_garis("═", 60, CYAN)
    print()

# Fungsi untuk menampilkan pesan berhasil (warna hijau)
def tampilkan_sukses(pesan):
    print(f"\n  {BG_HIJAU}{BOLD} ✔  {RESET} {HIJAU}{BOLD}{pesan}{RESET}")

# Fungsi untuk menampilkan pesan error/gagal (warna merah)
def tampilkan_error(pesan):
    print(f"\n  {BG_MERAH}{BOLD} ✘  {RESET} {MERAH}{BOLD}{pesan}{RESET}")

# Fungsi untuk menampilkan pesan informasi biasa (warna cyan)
def tampilkan_info(pesan):
    print(f"\n  {CYAN}ℹ  {pesan}{RESET}")

# Fungsi untuk menunggu pengguna menekan Enter sebelum lanjut
def tunggu_enter():
    print(f"\n{DIM}  Tekan Enter untuk melanjutkan...{RESET}", end="")
    input()

# Fungsi untuk menampilkan kotak informasi berisi data penting
def tampilkan_kotak(judul, isi):
    cetak_garis("─", 56, KUNING)
    print(f"{KUNING}  {BOLD}{judul}{RESET}")
    cetak_garis("─", 56, KUNING)
    # Tampilkan setiap baris data dalam kotak
    for label, nilai in isi.items():
        print(f"  {KUNING}{label:<20}{RESET}: {PUTIH}{nilai}{RESET}")
    cetak_garis("─", 56, KUNING)


# ==============================================
# FUNGSI UNTUK MEMBACA DAN MENYIMPAN DATA
# ==============================================

# Fungsi untuk membaca data pengguna dari file JSON
# Jika file belum ada, kembalikan dictionary kosong
def baca_data():
    if not os.path.exists(FILE_DATA):
        return {}
    with open(FILE_DATA, "r") as f:
        return json.load(f)

# Fungsi untuk menyimpan data pengguna ke file JSON
def simpan_data(data):
    with open(FILE_DATA, "w") as f:
        json.dump(data, f, indent=4)

# Fungsi untuk mengubah password menjadi hash SHA-256
# SHA-256 mengubah password menjadi kode unik sepanjang 64 karakter
# Proses ini tidak bisa dibalik, sehingga password asli tidak bisa diketahui
def buat_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ==============================================
# FITUR 1: REGISTRASI PENGGUNA BARU
# ==============================================
def registrasi():
    tampilkan_judul()
    print(f"  {MAGENTA}{BOLD}╔══════════════════════════════╗")
    print(f"  ║   📋  REGISTRASI PENGGUNA   ║")
    print(f"  ╚══════════════════════════════╝{RESET}\n")

    # Baca data yang sudah ada
    data = baca_data()

    print(f"  {PUTIH}Masukkan data akun baru kamu:{RESET}\n")

    # Minta input username
    username = input(f"  {CYAN}➤  Username   : {RESET}").strip()

    # Cek apakah username kosong
    if not username:
        tampilkan_error("Username tidak boleh kosong!")
        tunggu_enter()
        return

    # Cek apakah username sudah dipakai orang lain
    if username in data:
        tampilkan_error(f"Username '{username}' sudah dipakai! Coba nama lain.")
        tunggu_enter()
        return

    # Minta input password (tidak terlihat saat diketik)
    print(f"  {CYAN}➤  Password   : {RESET}", end="", flush=True)
    password = getpass.getpass(prompt="")

    # Cek apakah password kosong
    if not password:
        tampilkan_error("Password tidak boleh kosong!")
        tunggu_enter()
        return

    # Minta konfirmasi password agar tidak salah ketik
    print(f"  {CYAN}➤  Konfirmasi : {RESET}", end="", flush=True)
    konfirmasi = getpass.getpass(prompt="")

    # Cek apakah password dan konfirmasi sama
    if password != konfirmasi:
        tampilkan_error("Password dan konfirmasi tidak sama!")
        tunggu_enter()
        return

    # Ubah password menjadi hash SHA-256 sebelum disimpan
    hash_password = buat_hash(password)

    # Simpan username dan hash password ke dalam data
    data[username] = {"hash_password": hash_password}
    simpan_data(data)

    # Tampilkan hasil registrasi
    print()
    tampilkan_kotak("✔  REGISTRASI BERHASIL", {
        "Username"     : username,
        "Hash SHA-256" : hash_password[:32] + "...",
        "Hash Lengkap" : hash_password,
    })

    tampilkan_sukses(f"Akun '{username}' berhasil dibuat dan disimpan!")
    tunggu_enter()


# ==============================================
# FITUR 2: LOGIN PENGGUNA
# ==============================================
def login():
    tampilkan_judul()
    print(f"  {BIRU}{BOLD}╔══════════════════════════════╗")
    print(f"  ║     🔑  LOGIN PENGGUNA      ║")
    print(f"  ╚══════════════════════════════╝{RESET}\n")

    # Baca data pengguna yang sudah tersimpan
    data = baca_data()

    # Jika belum ada pengguna sama sekali, arahkan untuk registrasi dulu
    if not data:
        tampilkan_info("Belum ada pengguna terdaftar. Silakan registrasi dulu.")
        tunggu_enter()
        return

    print(f"  {PUTIH}Masukkan data login kamu:{RESET}\n")

    # Minta input username
    username = input(f"  {CYAN}➤  Username   : {RESET}").strip()

    # Cek apakah username ada di data
    if username not in data:
        tampilkan_error(f"Username '{username}' tidak ditemukan!")
        tunggu_enter()
        return

    # Minta input password
    print(f"  {CYAN}➤  Password   : {RESET}", end="", flush=True)
    password = getpass.getpass(prompt="")

    # Hash password yang baru saja diketik
    hash_dari_input = buat_hash(password)

    # Ambil hash password yang sudah tersimpan di file
    hash_tersimpan = data[username]["hash_password"]

    # Bandingkan kedua hash tersebut
    # Jika sama berarti password benar, jika beda berarti salah
    print()
    tampilkan_kotak("🔍  VERIFIKASI PASSWORD", {
        "Username"       : username,
        "Hash Input"     : hash_dari_input[:32] + "...",
        "Hash Tersimpan" : hash_tersimpan[:32] + "...",
        "Cocok?"         : "✔  YA" if hash_dari_input == hash_tersimpan else "✘  TIDAK",
    })

    if hash_dari_input == hash_tersimpan:
        print(f"\n  {BG_HIJAU}{BOLD}{'  ✔  LOGIN BERHASIL! Selamat datang, ' + username + '!  ':^54}{RESET}")
    else:
        print(f"\n  {BG_MERAH}{BOLD}{'  ✘  LOGIN GAGAL! Password yang kamu masukkan salah.  ':^54}{RESET}")

    tunggu_enter()


# ==============================================
# FITUR 3: LIHAT DAFTAR SEMUA PENGGUNA
# ==============================================
def lihat_pengguna():
    tampilkan_judul()
    print(f"  {KUNING}{BOLD}╔═══════════════════════════════════╗")
    print(f"  ║  📂  DAFTAR PENGGUNA TERDAFTAR  ║")
    print(f"  ╚═══════════════════════════════════╝{RESET}\n")

    # Baca semua data pengguna
    data = baca_data()

    # Jika data kosong, tampilkan pesan
    if not data:
        tampilkan_info("Belum ada pengguna yang terdaftar.")
        tunggu_enter()
        return

    # Tampilkan data dalam bentuk tabel
    cetak_garis("─", 60, KUNING)
    print(f"  {KUNING}{BOLD}{'No':<5}{'Username':<20}{'Hash SHA-256 (sebagian)'}{RESET}")
    cetak_garis("─", 60, KUNING)

    # Loop untuk menampilkan setiap pengguna satu per satu
    nomor = 1
    for username, info in data.items():
        # Tampilkan hanya 30 karakter pertama dari hash agar tidak terlalu panjang
        hash_pendek = info["hash_password"][:30] + "..."
        print(f"  {PUTIH}{nomor:<5}{CYAN}{username:<20}{DIM}{hash_pendek}{RESET}")
        nomor += 1

    cetak_garis("─", 60, KUNING)
    print(f"\n  Total pengguna terdaftar: {HIJAU}{BOLD}{len(data)}{RESET}")
    tunggu_enter()


# ==============================================
# MENU UTAMA PROGRAM
# ==============================================
def menu_utama():
    # Loop agar program terus berjalan sampai pengguna memilih keluar
    while True:
        tampilkan_judul()
        print(f"  {PUTIH}{BOLD}Silakan pilih menu:{RESET}\n")
        print(f"  {BG_HITAM} {HIJAU} 1 {RESET}  {HIJAU}Registrasi Pengguna Baru{RESET}")
        print(f"  {BG_HITAM} {BIRU} 2 {RESET}  {BIRU}Login Pengguna{RESET}")
        print(f"  {BG_HITAM} {KUNING} 3 {RESET}  {KUNING}Lihat Daftar Pengguna{RESET}")
        print(f"  {BG_HITAM} {MERAH} 0 {RESET}  {MERAH}Keluar{RESET}")
        print()
        cetak_garis("─", 60, DIM)

        # Minta pengguna memasukkan pilihan
        pilihan = input(f"\n  {CYAN}➤  Pilihan kamu [0-3]: {RESET}").strip()

        # Jalankan fungsi sesuai pilihan
        if pilihan == "1":
            registrasi()
        elif pilihan == "2":
            login()
        elif pilihan == "3":
            lihat_pengguna()
        elif pilihan == "0":
            tampilkan_judul()
            print(f"  {HIJAU}{BOLD}Terima kasih! Sampai jumpa lagi 👋{RESET}\n")
            cetak_garis("═", 60, CYAN)
            break  # keluar dari loop, program selesai
        else:
            tampilkan_error("Pilihan tidak valid! Masukkan angka 0, 1, 2, atau 3.")
            tunggu_enter()


# ==============================================
# PROGRAM MULAI DI SINI
# ==============================================
if __name__ == "__main__":
    menu_utama()
