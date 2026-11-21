"""
Modul Prediksi URL Phishing (Interface untuk Anggota 2 & Anggota 3)
Tugas: Anggota 1 (Machine Learning)
File: src/prediction.py
Deskripsi:
    Menyediakan fungsi prediksi URL tunggal yang siap diimpor dan dipanggil
    oleh backend (Anggota 2) maupun antarmuka Streamlit (Anggota 3).
"""

import os
from typing import Any, Dict
import joblib
import pandas as pd

from feature_extraction import FEATURE_NAMES, extract_features, extract_features_df

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "random_forest_phishing_model.joblib")
METADATA_PATH = os.path.join(BASE_DIR, "models", "model_metadata.joblib")

# Cache model agar tidak dibaca ulang dari disk setiap kali prediksi dipanggil
_CACHED_MODEL = None
_CACHED_METADATA = None


def get_model():
    """Memuat model Random Forest dan metadata dari file joblib (dengan in-memory caching)."""
    global _CACHED_MODEL, _CACHED_METADATA
    if _CACHED_MODEL is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file tidak ditemukan di {MODEL_PATH}. Jalankan src/train_model.py terlebih dahulu.")
        _CACHED_MODEL = joblib.load(MODEL_PATH)
        if os.path.exists(METADATA_PATH):
            _CACHED_METADATA = joblib.load(METADATA_PATH)
    return _CACHED_MODEL, _CACHED_METADATA


def predict_url(url: str) -> Dict[str, Any]:
    """
    Menerima 1 string URL dan menghasilkan prediksi deteksi phishing.

    Parameter:
        url (str): String URL yang ingin dianalisis (contoh: "https://google.com").

    Mengembalikan Dictionary:
        {
            "url": str,
            "prediction": str,            # "Phishing" atau "Legitimate"
            "label": int,                 # 0 untuk Phishing, 1 untuk Legitimate
            "confidence": float,          # Skor keyakinan prediksi (0.0 - 1.0)
            "phishing_probability": float,# Probabilitas URL tergolong Phishing (0.0 - 1.0)
            "legitimate_probability": float, # Probabilitas URL tergolong Legitimate (0.0 - 1.0)
            "features": dict,             # Nilai 16 fitur yang diekstrak dari URL
            "disclaimer": str             # Pesan peringatan batas kemampuan model ML
        }
    """
    if not url or not isinstance(url, str) or not url.strip():
        raise ValueError("Input URL tidak boleh kosong atau hanya berupa spasi.")

    clean_url = url.strip()

    # 1. Ekstraksi 16 fitur URL secara konsisten
    features_dict = extract_features(clean_url)
    features_df = pd.DataFrame([features_dict])[FEATURE_NAMES]

    # 2. Muat model
    model, _ = get_model()

    # 3. Prediksi label dan probabilitas
    pred_label = int(model.predict(features_df)[0])
    prob_array = model.predict_proba(features_df)[0]
    
    # Class 0: Phishing, Class 1: Legitimate
    prob_phishing = float(prob_array[0])
    prob_legitimate = float(prob_array[1])

    is_legitimate = (pred_label == 1)
    label_text = "Legitimate" if is_legitimate else "Phishing"
    confidence = prob_legitimate if is_legitimate else prob_phishing

    return {
        "url": clean_url,
        "prediction": label_text,
        "label": pred_label,
        "confidence": confidence,
        "phishing_probability": prob_phishing,
        "legitimate_probability": prob_legitimate,
        "features": features_dict,
        "disclaimer": "Hasil klasifikasi merupakan prediksi model Machine Learning berdasarkan karakteristik teks URL, bukan jaminan mutlak keamanan sistem.",
    }


if __name__ == "__main__":
    sample_urls = [
        "https://www.google.com",
        "http://myglobaltech.in/",
        "http://117.205.108.72:37255/bin.sh",
        "https://keraekken-loagginnusa.godaddysites.com/",
    ]
    print("=" * 60)
    print("       PENGUJIAN FUNGSI PREDIKSI (src/prediction.py)")
    print("=" * 60)
    for u in sample_urls:
        res = predict_url(u)
        print(f"\nURL        : {res['url']}")
        print(f"Hasil      : [{res['prediction']}] (Label: {res['label']})")
        print(f"Confidence : {res['confidence']*100:.2f}% (Phishing: {res['phishing_probability']*100:.1f}%, Legitimate: {res['legitimate_probability']*100:.1f}%)")
