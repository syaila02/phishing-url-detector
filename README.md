# PhishGuard — Phishing URL Detector (Defensive AI)

Proyek Ujian Akhir Semester (UAS) Mata Kuliah **Keamanan Informasi**  
**Judul:** Pengembangan Sistem Deteksi URL Phishing Menggunakan Algoritma Random Forest Berbasis Web  
**Topik:** Topik 1 — Defensive AI  

---

## 👥 Pembagian Tugas Kelompok

- **Anggota 1 — Machine Learning (STATUS: SELESAI ✅)**:
  - Pemeriksaan, pembersihan missing values & duplikat dataset LegitPhish (101.219 baris).
  - Ekstraksi 16 fitur leksikal & struktural URL tanpa data leakage.
  - Pelatihan model Random Forest Classifier (Akurasi: 99.95%, Phishing F1: 99.96%).
  - Evaluasi metrik, visualisasi confusion matrix, dan analisis risiko FP/FN.
  - Pembuatan interface prediksi modular (`src/prediction.py`) & prototype Streamlit.
- **Anggota 2 — Backend / Logika Sistem (STATUS: SIAP DIKERJAKAN ⏳)**:
  - Validasi format input URL (skema, regex, sanitasi input).
  - Integrasi fungsi `predict_url()` dari `src/prediction.py`.
  - Penanganan error handling dan logging.
- **Anggota 3 — Frontend / Aplikasi Web (STATUS: SIAP DIKERJAKAN ⏳)**:
  - Penyempurnaan tampilan antarmuka web Streamlit (`app/app.py`).
  - Pembuatan visualisasi status risiko, tips edukasi keamanan siber, dan penafian (disclaimer).

---

## 📁 Struktur Direktori Repository

```text
phishing-url-detector/
├── app/
│   └── app.py                      # Prototype frontend Streamlit (Anggota 1 / Anggota 3)
├── dataset/
│   ├── README.md                   # Dokumentasi LegitPhish Dataset
│   └── url_features_extracted1.csv # Dataset CSV (dibersihkan saat runtime)
├── src/
│   ├── inspect_dataset.py          # Script inspeksi dataset (Anggota 1)
│   ├── preprocessing.py            # Pembersihan data & train-test split (Anggota 1)
│   ├── feature_extraction.py       # Ekstraksi 16 fitur URL secara konsisten (Anggota 1)
│   ├── train_model.py              # Pelatihan RF & kalkulasi evaluasi (Anggota 1)
│   └── prediction.py               # Interface prediksi untuk Backend & Frontend (Handover Anggota 2)
├── models/
│   ├── README.md                   # Spesifikasi model & panduan pemuatan
│   ├── random_forest_phishing_model.joblib # Model Random Forest tersimpan
│   └── model_metadata.joblib       # Metadata & urutan fitur model
├── evaluation/
│   ├── README.md                   # Laporan detail metrik evaluasi
│   ├── confusion_matrix.png        # Plot visualisasi Confusion Matrix
│   ├── feature_importance.png      # Plot visualisasi Feature Importance
│   ├── evaluation_report.json      # Metadata evaluasi format JSON
│   └── evaluation_report.txt       # Ringkasan teks evaluasi & classification report
├── tests/
│   └── test_prediction.py          # Unit testing fungsi prediksi
├── requirements.txt                # Daftar dependensi Python
├── PANDUAN_PROYEK_PHISHING_URL_DETECTOR.md # Panduan komprehensif & handover tim
└── README.md                       # Dokumentasi utama proyek
```

---

## 🚀 Panduan Menjalankan Sistem (Windows PowerShell)

### 1. Menyiapkan Lingkungan Python
```powershell
cd "d:\IF XASY\SMT 5\KEAMANAN INFORMASI\uas\phishing-url-detector"
# Menggunakan virtual environment yang telah disediakan:
& ".\.venv\Scripts\Activate.ps1"
```

### 2. Memeriksa Dataset (Tugas Anggota 1)
```powershell
& ".\.venv\Scripts\python.exe" "src/inspect_dataset.py"
```

### 3. Melatih Ulang Model & Evaluasi
```powershell
& ".\.venv\Scripts\python.exe" "src/train_model.py"
```

### 4. Menjalankan Unit Testing
```powershell
& ".\.venv\Scripts\python.exe" "tests/test_prediction.py"
```

### 5. Menjalankan Aplikasi Web Streamlit
```powershell
& ".\.venv\Scripts\streamlit.exe" run "app/app.py"
```

---

## 🎯 Panduan Khusus Handover (Anggota 2 & Anggota 3)

### Untuk Anggota 2 (Backend / Logika Sistem)
Gunakan modul `src/prediction.py` langsung tanpa perlu memuat file model manual:
```python
from src.prediction import predict_url

# Contoh pemanggilan inferensi
hasil = predict_url("https://example.com")
print(hasil["prediction"])            # 'Phishing' atau 'Legitimate'
print(hasil["confidence"])            # float, e.g. 0.999
print(hasil["phishing_probability"])  # float probabilitas phishing
print(hasil["features"])              # 16 fitur yang diekstrak
```

### Untuk Anggota 3 (Frontend Web)
File `app/app.py` sudah menyediakan prototype kerja dengan alur input URL, tombol periksa, pembacaan hasil model nyata, tampilan probabilitas risiko, dan detail 16 fitur. Anggota 3 dapat menyempurnakan desain CSS, tipografi, serta menambahkan komponen edukasi keamanan.
