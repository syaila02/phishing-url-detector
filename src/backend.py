
"""
Modul Backend Deteksi URL Phishing
Tugas: Anggota 2 (Backend / Logika Sistem)

Deskripsi:
    Menghubungkan validasi URL dengan model Machine Learning
    untuk menghasilkan prediksi Phishing atau Legitimate.
"""

import logging
from typing import Any, Dict

from url_validator import validate_url
from prediction import predict_url


# Konfigurasi logging
logger = logging.getLogger(__name__)


class BackendPredictionError(RuntimeError):
    """Exception untuk kesalahan saat proses prediksi."""
    pass


def analyze_url(url: str) -> Dict[str, Any]:
    """
    Memvalidasi URL dan menjalankan prediksi phishing.

    Parameter:
        url (str): URL yang dimasukkan pengguna.

    Mengembalikan:
        dict: Hasil prediksi dari model Machine Learning.

    Raises:
        URLValidationError: Jika URL tidak valid.
        BackendPredictionError: Jika proses prediksi gagal.
    """

    # 1. Validasi URL
    clean_url = validate_url(url)

    # 2. Jalankan prediksi menggunakan model Anggota 1
    try:
        result = predict_url(clean_url)

    except FileNotFoundError as error:
        logger.exception("File model Machine Learning tidak ditemukan.")
        raise BackendPredictionError(
            "Model deteksi belum tersedia. Periksa file model pada folder models."
        ) from error

    except Exception as error:
        logger.exception("Terjadi kesalahan saat proses prediksi.")
        raise BackendPredictionError(
            "Terjadi kesalahan saat menganalisis URL. Silakan periksa sistem."
        ) from error

    # 3. Pastikan hasil prediksi memiliki struktur yang sesuai
    required_fields = {
        "url",
        "prediction",
        "label",
        "confidence",
        "phishing_probability",
        "legitimate_probability",
        "features",
        "disclaimer"
    }

    if not isinstance(result, dict):
        raise BackendPredictionError(
            "Format hasil prediksi tidak sesuai."
        )

    missing_fields = required_fields - result.keys()

    if missing_fields:
        logger.error(
            "Hasil prediksi kehilangan field: %s",
            missing_fields
        )
        raise BackendPredictionError(
            "Data hasil prediksi tidak lengkap."
        )

    # 4. Kembalikan hasil prediksi
    return result


if __name__ == "__main__":

    sample_url = "https://www.google.com"

    try:
        hasil = analyze_url(sample_url)

        print("=" * 55)
        print("       BACKEND PHISHING URL DETECTOR")
        print("=" * 55)

        print(f"URL                  : {hasil['url']}")
        print(f"Hasil Prediksi       : {hasil['prediction']}")
        print(f"Confidence           : {hasil['confidence'] * 100:.2f}%")
        print(
            f"Probabilitas Phishing: "
            f"{hasil['phishing_probability'] * 100:.2f}%"
        )
        print(
            f"Probabilitas Legitimate: "
            f"{hasil['legitimate_probability'] * 100:.2f}%"
        )

        print("\nDisclaimer:")
        print(hasil["disclaimer"])

    except ValueError as error:
        print(f"Validasi Gagal: {error}")

    except BackendPredictionError as error:
        print(f"Backend Error: {error}")
