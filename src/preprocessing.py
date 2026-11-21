"""
Modul Preprocessing Data LegitPhish
Tugas: Anggota 1 (Machine Learning)
File: src/preprocessing.py
Deskripsi:
    Membersihkan missing value dan data duplikat,
    memisahkan fitur dan target (memastikan URL dan ClassLabel tidak bocor ke X),
    serta membagi data latih dan uji menggunakan stratified split.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split

DEFAULT_DATASET_PATH = os.path.join(
    os.path.dirname(__file__), "..", "dataset", "url_features_extracted1.csv"
)

# 16 fitur numerik URL yang sah digunakan untuk klasifikasi
FEATURE_COLUMNS = [
    "url_length",
    "has_ip_address",
    "dot_count",
    "https_flag",
    "url_entropy",
    "token_count",
    "subdomain_count",
    "query_param_count",
    "tld_length",
    "path_length",
    "has_hyphen_in_domain",
    "number_of_digits",
    "tld_popularity",
    "suspicious_file_extension",
    "domain_name_length",
    "percentage_numeric_chars",
]

TARGET_COLUMN = "ClassLabel"


def load_and_preprocess_data(file_path=DEFAULT_DATASET_PATH, test_size=0.2, random_state=42):
    """
    Memuat dan membersihkan dataset:
    1. Membaca dataset dari CSV.
    2. Menghapus baris dengan nilai target null (1 baris).
    3. Menghapus duplikasi baris penuh (346 baris) untuk mencegah data leakage.
    4. Memisahkan matriks fitur (X) dan target (y).
    5. Melakukan train_test_split dengan stratifikasi (stratify=y).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File dataset tidak ditemukan: {file_path}")

    print(f"[PREPROCESSING] Membaca dataset dari: {file_path}")
    df = pd.read_csv(file_path)
    initial_rows = len(df)
    print(f"[PREPROCESSING] Baris awal: {initial_rows:,}")

    # Hapus missing values pada target
    df = df.dropna(subset=[TARGET_COLUMN]).copy()
    rows_after_dropna = len(df)
    dropped_nulls = initial_rows - rows_after_dropna
    if dropped_nulls > 0:
        print(f"[PREPROCESSING] Dihapus {dropped_nulls} baris dengan label NaN.")

    # Hapus baris duplikat penuh untuk mencegah data leakage
    df = df.drop_duplicates().copy()
    rows_after_dedup = len(df)
    dropped_dups = rows_after_dropna - rows_after_dedup
    if dropped_dups > 0:
        print(f"[PREPROCESSING] Dihapus {dropped_dups:,} baris duplikat.")

    # Konversi ClassLabel ke integer (0 = Phishing, 1 = Legitimate)
    df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(int)

    # Validasi bahwa kolom URL tidak masuk ke X dan target tidak bocor
    assert "URL" not in FEATURE_COLUMNS, "KOLOM URL TIDAK BOLEH MASUK FITUR TRAINING!"
    assert TARGET_COLUMN not in FEATURE_COLUMNS, "KOLOM TARGET TIDAK BOLEH MASUK FITUR TRAINING!"

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()

    print(f"[PREPROCESSING] Total data bersih : {len(df):,} baris")
    print(f"[PREPROCESSING] Jumlah fitur (X)   : {X.shape[1]} kolom")
    print(f"[PREPROCESSING] Distribusi target   :")
    print(f"   - Phishing (0)   : {(y == 0).sum():,} baris ({(y == 0).mean()*100:.2f}%)")
    print(f"   - Legitimate (1) : {(y == 1).sum():,} baris ({(y == 1).mean()*100:.2f}%)")

    # Pembagian data training dan testing dengan Stratified Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    print(f"[PREPROCESSING] Data Training : {len(X_train):,} baris ({100 - test_size*100:.0f}%)")
    print(f"[PREPROCESSING] Data Testing  : {len(X_test):,} baris ({test_size*100:.0f}%)")

    return X_train, X_test, y_train, y_test, FEATURE_COLUMNS


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, feats = load_and_preprocess_data()
