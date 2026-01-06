Aplikasi ini merupakan aplikasi web berbasis Flask yang berfungsi untuk mengekstraksi teks dari gambar menggunakan teknologi Optical Character Recognition (OCR). Proses pengenalan teks dilakukan dengan bantuan Tesseract OCR dan didukung oleh teknik preprocessing citra menggunakan OpenCV untuk meningkatkan akurasi hasil pembacaan teks.

1️⃣ Import Library
import pytesseract
from PIL import Image
import cv2
import os
from datetime import datetime
from flask import Flask, render_template, request


Library yang digunakan memiliki fungsi sebagai berikut:
pytesseract: antarmuka Python untuk Tesseract OCR
PIL (Image): mengelola format gambar
OpenCV (cv2): melakukan preprocessing citra
os: mengelola file dan direktori
datetime: mencatat waktu proses OCR
Flask: framework web
render_template: menampilkan halaman HTML
request: menerima data upload dari pengguna

2️⃣ Konfigurasi Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

os.environ["TESSDATA_PREFIX"] = (
    r"C:\Program Files\Tesseract-OCR\tessdata"
)


Bagian ini digunakan untuk menentukan lokasi engine Tesseract OCR dan data bahasa pada sistem operasi Windows. Konfigurasi ini penting agar Python dapat memanggil Tesseract dengan benar saat proses OCR dijalankan.

3️⃣ Konfigurasi Flask
app = Flask(__name__)
UPLOAD_FOLDER = "Image"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


Aplikasi Flask dikonfigurasi agar file gambar yang diunggah pengguna disimpan ke dalam folder Image sebelum diproses lebih lanjut.

4️⃣ Preprocessing Citra
def preprocess_image(path):


Tahap preprocessing bertujuan untuk meningkatkan kualitas citra sehingga teks lebih mudah dikenali oleh OCR.

a. Membaca dan memperbesar gambar
img = cv2.imread(path)


Gambar dibaca menggunakan OpenCV. Jika ukuran gambar terlalu kecil, gambar akan diperbesar agar detail teks lebih jelas.

b. Konversi ke grayscale dan reduksi noise
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)


Grayscale menghilangkan informasi warna

Gaussian Blur mengurangi noise pada gambar

c. Thresholding Otsu
_, thresh = cv2.threshold(
    gray, 0, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)


Metode ini mengubah gambar menjadi hitam-putih secara otomatis sehingga kontras antara teks dan latar belakang menjadi lebih jelas.

5️⃣ Proses OCR
def proses_ocr(path):


Pada tahap ini, gambar hasil preprocessing dikirim ke Tesseract OCR untuk diekstraksi teksnya.

teks = pytesseract.image_to_string(
    img,
    lang="ind",
    config="--oem 3 --psm 3"
)


Bahasa OCR yang digunakan adalah Bahasa Indonesia

Engine OCR menggunakan model LSTM modern

Mode segmentasi halaman diatur otomatis

6️⃣ Penyimpanan Hasil OCR
def simpan_hasil(nama_file, teks):


Hasil OCR disimpan ke dalam file teks hasil_ocr.txt beserta:

Nama file gambar

Waktu proses OCR

Isi teks hasil ekstraksi

Fitur ini berfungsi sebagai histori pemrosesan OCR.

7️⃣ Routing Aplikasi Flask
a. Halaman utama (/)
@app.route("/", methods=["GET", "POST"])


Halaman ini digunakan untuk:

Upload gambar

Menjalankan proses OCR

Menampilkan hasil teks ke pengguna

b. Halaman histori (/history)
@app.route("/history")


Menampilkan seluruh riwayat hasil OCR yang pernah diproses dalam aplikasi.

8️⃣ Menjalankan Aplikasi
if __name__ == "__main__":
    app.run(debug=True)


Aplikasi dijalankan pada server lokal dan dapat diakses melalui browser.
