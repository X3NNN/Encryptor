# Aplikasi Cipher

Ini adalah aplikasi cipher berbasis web yang memungkinkan pengguna untuk mengenkripsi dan mendekripsi teks menggunakan berbagai metode cipher. Aplikasi ini dibangun dengan Python Flask untuk backend dan HTML/CSS/JavaScript untuk frontend.

## Fitur

1. Beberapa metode cipher:
   - Cipher Vigenère
   - Cipher Vigenère Auto-Key
   - Cipher Playfair
   - Cipher Hill
   - Super Enkripsi (kombinasi cipher Vigenère dan Transposisi)

2. Fungsi enkripsi dan dekripsi
3. Unggah file untuk memproses teks panjang
4. Unduh hasil sebagai file teks
5. Antarmuka web yang ramah pengguna

## Teknologi yang Digunakan

- Backend:
  - Python 3.x
  - Flask (Kerangka kerja web)
  - NumPy (untuk operasi matematika dalam Cipher Hill)

- Frontend:
  - HTML5
  - CSS3
  - JavaScript (ES6+)

## Cara Menjalankan Program

1. Pastikan Anda telah menginstal Python 3.x di sistem Anda.

2. Klon repositori ini:
git clone https://github.com/username-anda/Encryptor.git
cd Encryptor

3. Instal dependensi yang diperlukan:
pip install flask numpy werkzeug

4. Jalankan aplikasi Flask:
python enkriptor.py atau bisa langsung klik enkriptor.py untuk menjalankan

5. Buka browser web dan akses `http://localhost:5000` untuk menggunakan aplikasi.

## Penggunaan

1. Masukkan teks yang ingin Anda enkripsi atau dekripsi di kolom "Teks".
2. Masukkan kunci enkripsi/dekripsi di kolom "Kunci".
3. Pilih metode cipher dari menu dropdown.
4. Pilih apakah Anda ingin mengenkripsi atau mendekripsi teks.
5. Klik "Proses" untuk melakukan operasi.
6. Hasil akan ditampilkan di halaman.
7. Anda dapat mengunduh hasil sebagai file teks dengan mengklik "Unduh Hasil".
8. Untuk memproses teks dari file, gunakan tombol "Unggah" di samping area teks.


