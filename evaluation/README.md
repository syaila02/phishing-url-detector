# Laporan Hasil Evaluasi Model Machine Learning

Hasil evaluasi di bawah ini berasal dari eksperimen nyata yang dijalankan menggunakan script `src/train_model.py` pada 20.175 data uji (20% test set dari LegitPhish dataset bersih).

## 1. Ringkasan Metrik Performa

| Metrik | Skor / Nilai |
|:---|:---:|
| **Accuracy** | **99.95%** |
| **Phishing Precision (Kelas 0)** | **99.93%** |
| **Phishing Recall (Kelas 0)** | **99.98%** |
| **Phishing F1-Score (Kelas 0)** | **99.96%** |
| **Legitimate Precision (Kelas 1)** | **99.97%** |
| **Legitimate Recall (Kelas 1)** | **99.88%** |
| **Legitimate F1-Score (Kelas 1)** | **99.93%** |
| **Macro F1-Score** | **99.94%** |
| **Weighted F1-Score** | **99.95%** |

## 2. Confusion Matrix

| Label Aktual \ Prediksi | Prediksi Phishing (0) | Prediksi Legitimate (1) | Total Aktual |
|:---|:---:|:---:|:---:|
| **Aktual Phishing (0)** | **12.697** *(True Phishing / TN)* | **2** *(False Legitimate / FP)* | 12.699 |
| **Aktual Legitimate (1)** | **9** *(False Phishing / FN)* | **7.467** *(True Legitimate / TP)* | 7.476 |
| **Total Prediksi** | 12.706 | 7.469 | 20.175 |

- Visualisasi Confusion Matrix tersimpan di: `evaluation/confusion_matrix.png`
- Visualisasi Feature Importance tersimpan di: `evaluation/feature_importance.png`
- Data mentah JSON: `evaluation/evaluation_report.json`
- Laporan teks lengkap: `evaluation/evaluation_report.txt`

## 3. Analisis False Positive dan False Negative (Konteks Keamanan Informasi)

Dalam sistem pertahanan siber (*Defensive AI*), kedua jenis kesalahan memiliki konsekuensi yang berbeda:

1. **False Legitimate / False Positive terhadap Kelas 1 (2 kasus / 0,01%)**:
   - **Kondisi:** URL sebenarnya adalah **Phishing**, namun model memprediksinya sebagai **Legitimate**.
   - **Dampak Keamanan:** **SANGAT BERBAHAYA (Kritis)**. Pengguna dapat terkecoh dan memasukkan data kredensial, kata sandi, atau mengunduh malware karena sistem menyatakan URL tersebut sah. 
   - **Pencapaian Model:** Model Random Forest berhasil meminimalkan celah ini hingga hanya 2 URL phishing yang lolos dari 12.699 sampel uji (Recall Phishing mencapai 99,98%).

2. **False Phishing / False Negative terhadap Kelas 1 (9 kasus / 0,04%)**:
   - **Kondisi:** URL sebenarnya adalah **Legitimate**, namun model memprediksinya sebagai **Phishing**.
   - **Dampak Keamanan:** **Rendah hingga Sedang (Operasional)**. Pengguna mengalami *false alarm* dan mungkin tidak dapat langsung mengakses situs web yang sah. Namun, kesalahan ini tidak mengakibatkan kompromi data atau pencurian akun.

## 4. Analisis Kontribusi Fitur (Feature Importance)
Berdasarkan perhitungan Mean Decrease in Impurity (Gini Importance), 6 fitur dengan pengaruh terbesar adalah:
1. `path_length` (39,11%): Panjang jalur direktori/path URL menjadi pembeda kuat antara halaman phishing dan situs asli.
2. `token_count` (15,46%): Banyaknya segmentasi pemisah kata dalam URL.
3. `https_flag` (13,21%): Masih banyaknya domain serangan phishing tanpa sertifikat TLS atau menggunakan protokol tidak aman.
4. `number_of_digits` (10,36%): Jumlah angka yang tinggi akibat penyisipan IP address atau hash acak.
5. `percentage_numeric_chars` (9,33%): Kerapatan karakter numerik di dalam string URL.
6. `dot_count` (4,21%): Frekuensi titik pemisah domain dan subdomain.
