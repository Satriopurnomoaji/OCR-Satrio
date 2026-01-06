import pytesseract
from PIL import Image
import cv2
import os
from datetime import datetime
from flask import Flask, render_template, request

# ===============================
# KONFIGURASI TESSERACT
# ===============================
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

os.environ["TESSDATA_PREFIX"] = (
    r"C:\Program Files\Tesseract-OCR\tessdata"
)

# ===============================
# FLASK CONFIG
# ===============================
app = Flask(__name__)
UPLOAD_FOLDER = "Image"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ===============================
# PREPROCESSING
# ===============================
def preprocess_image(path):
    img = cv2.imread(path)

    h, w = img.shape[:2]
    if max(h, w) < 1000:
        scale = 1000 / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return Image.fromarray(thresh)

# ===============================
# OCR PROCESS
# ===============================
def proses_ocr(path):
    img = preprocess_image(path)
    teks = pytesseract.image_to_string(
        img,
        lang="ind",
        config="--oem 3 --psm 3"
    )
    return teks.strip()

# ===============================
# SAVE HISTORY
# ===============================
def simpan_hasil(nama_file, teks):
    with open("hasil_ocr.txt", "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 50 + "\n")
        f.write(f"Waktu : {datetime.now()}\n")
        f.write(f"File  : {nama_file}\n")
        f.write("-" * 50 + "\n")
        f.write(teks + "\n")

# ===============================
# ROUTES
# ===============================
@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None

    if request.method == "POST":
        file = request.files["gambar"]
        if file:
            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)

            hasil = proses_ocr(path)
            simpan_hasil(file.filename, hasil)

    return render_template("index.html", hasil=hasil)

@app.route("/history")
def history():
    if os.path.exists("hasil_ocr.txt"):
        with open("hasil_ocr.txt", "r", encoding="utf-8") as f:
            histori = f.read()
    else:
        histori = "Belum ada histori OCR."

    return render_template("history.html", histori=histori)

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    app.run(debug=True)