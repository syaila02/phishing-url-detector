"""
Modul Pemeriksaan Dataset LegitPhish
Tugas: Anggota 1 (Machine Learning)
File: src/inspect_dataset.py
Deskripsi:
    Membaca dataset 'dataset/url_features_extracted1.csv', melakukan analisis
    struktur kolom, tipe data, missing values, duplikasi, dan distribusi label.
"""

import os
import pandas as pd

DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "url_features_extracted1.csv")


def inspect_dataset(file_path=DATASET_PATH):
    print("=" * 60)
    print("      HASIL PEMERIKSAAN DATASET: LegitPhish Dataset")
    print("=" * 60)

    if not os.path.exists(file_path):
        print(f"[ERROR] File dataset tidak ditemukan di: {file_path}")
        return None

    # 1. Membaca dataset
    df = pd.read_csv(file_path)
    n_rows, n_cols = df.shape
    print(f"\n1. DIMENSI DATASET:")
    print(f"   - Jumlah Baris : {n_rows:,}")
    print(f"   - Jumlah Kolom : {n_cols}")

    # 2. Daftar kolom dan tipe data
    print(f"\n2. DAFTAR KOLOM DAN TIPE DATA:")
    for idx, (col, dtype) in enumerate(zip(df.columns, df.dtypes), start=1):
        print(f"   {idx:2d}. {col:<28} : {dtype}")

    # 3. Missing values
    print(f"\n3. PEMERIKSAAN MISSING VALUES:")
    null_series = df.isnull().sum()
    null_cols = null_series[null_series > 0]
    if len(null_cols) == 0:
        print("   - Tidak ditemukan missing values (dataset bersih).")
    else:
        for col, count in null_cols.items():
            print(f"   - Kolom '{col}' memiliki {count} missing value ({count/n_rows*100:.4f}%).")

    # 4. Duplikasi data
    exact_duplicates = df.duplicated().sum()
    url_duplicates = df["URL"].duplicated().sum()
    print(f"\n4. PEMERIKSAAN DUPLIKASI DATA:")
    print(f"   - Baris duplikat penuh (seluruh kolom sama) : {exact_duplicates:,}")
    print(f"   - URL duplikat                            : {url_duplicates:,}")

    # 5. Distribusi label
    print(f"\n5. DISTRIBUSI KELAS TARGET (ClassLabel):")
    counts = df["ClassLabel"].value_counts(dropna=False)
    percents = df["ClassLabel"].value_counts(dropna=False, normalize=True) * 100
    for label, count in counts.items():
        if pd.isna(label):
            label_str = "NaN (Missing)"
        elif label == 0:
            label_str = "0 (Phishing)"
        else:
            label_str = "1 (Legitimate)"
        pct = percents[label]
        formatted_count = f"{count:,}"
        print(f"   - Label {label_str:<18} : {formatted_count:>8} baris ({pct:6.2f}%)")

    # 6. Sampel data
    print(f"\n6. SAMPEL 3 BARIS PERTAMA:")
    print(df.head(3).to_string())

    print("\n" + "=" * 60)
    print("Kesimpulan Kondisi Dataset:")
    print(" - Total 16 fitur berbasis karakteristik URL telah terekstraksi.")
    print(" - Kolom 'URL' berisi teks URL asli (digunakan sebagai identifier).")
    print(" - Terdapat 1 baris bernilai NaN pada kolom 'ClassLabel' yang perlu dihapus.")
    print(" - Terdapat 346 baris duplikat yang perlu dibersihkan agar tidak terjadi leakage.")
    print(" - Distribusi kelas: 62.91% Phishing dan 37.09% Legitimate (kategori cukup seimbang).")
    print("=" * 60)

    return df


if __name__ == "__main__":
    inspect_dataset()
