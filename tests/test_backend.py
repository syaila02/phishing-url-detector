
"""
Unit Testing Backend Phishing URL Detector
Tugas: Anggota 2 (Backend)
"""

import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src")
)

from backend import analyze_url, BackendPredictionError
from url_validator import URLValidationError


MOCK_RESULT = {
    "url": "https://example.com",
    "prediction": "Legitimate",
    "label": 1,
    "confidence": 0.99,
    "phishing_probability": 0.01,
    "legitimate_probability": 0.99,
    "features": {},
    "disclaimer": "Hasil merupakan prediksi model."
}


class TestBackend(unittest.TestCase):

    @patch("backend.predict_url")
    def test_valid_url(self, mock_predict):
        mock_predict.return_value = MOCK_RESULT

        result = analyze_url("https://example.com")

        self.assertEqual(result["prediction"], "Legitimate")
        mock_predict.assert_called_once_with("https://example.com")

    @patch("backend.predict_url")
    def test_url_without_scheme(self, mock_predict):
        mock_predict.return_value = MOCK_RESULT

        analyze_url("example.com")

        mock_predict.assert_called_once_with("example.com")

    def test_empty_url(self):
        with self.assertRaises(URLValidationError):
            analyze_url("")

    def test_invalid_url(self):
        with self.assertRaises(URLValidationError):
            analyze_url("ini-bukan-url")

    def test_url_too_long(self):
        long_url = "https://example.com/" + ("a" * 2050)

        with self.assertRaises(URLValidationError):
            analyze_url(long_url)

    def test_url_with_spaces(self):
        with self.assertRaises(URLValidationError):
            analyze_url("https://example.com/hello world")

    def test_invalid_port(self):
        with self.assertRaises(URLValidationError):
            analyze_url("https://example.com:99999")

    def test_ipv6_not_supported(self):
        with self.assertRaises(URLValidationError):
            analyze_url("http://[2001:db8::1]/")

    @patch("backend.predict_url")
    def test_model_not_found(self, mock_predict):
        mock_predict.side_effect = FileNotFoundError(
            "Model tidak ditemukan"
        )

        with self.assertRaises(BackendPredictionError):
            analyze_url("https://example.com")

    @patch("backend.predict_url")
    def test_prediction_error(self, mock_predict):
        mock_predict.side_effect = RuntimeError(
            "Terjadi kesalahan model"
        )

        with self.assertRaises(BackendPredictionError):
            analyze_url("https://example.com")

    @patch("backend.predict_url")
    def test_incomplete_prediction_result(self, mock_predict):
        mock_predict.return_value = {
            "prediction": "Legitimate"
        }

        with self.assertRaises(BackendPredictionError):
            analyze_url("https://example.com")


if __name__ == "__main__":
    unittest.main(verbosity=2)
