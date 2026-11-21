"""
Unit Testing untuk Modul Prediksi URL Phishing
Tugas: Pengujian Anggota 1 & Anggota 2
File: tests/test_prediction.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from prediction import predict_url
from feature_extraction import extract_features, FEATURE_NAMES


class TestPhishingDetector(unittest.TestCase):

    def test_feature_extraction_keys(self):
        url = "https://example.com/test?a=1"
        features = extract_features(url)
        self.assertEqual(len(features), len(FEATURE_NAMES))
        for key in FEATURE_NAMES:
            self.assertIn(key, features)

    def test_empty_url_validation(self):
        with self.assertRaises(ValueError):
            predict_url("")

        with self.assertRaises(ValueError):
            predict_url("   ")

    def test_valid_prediction_structure(self):
        url = "https://www.google.com"
        result = predict_url(url)
        self.assertIn("url", result)
        self.assertIn("prediction", result)
        self.assertIn("label", result)
        self.assertIn("confidence", result)
        self.assertIn("phishing_probability", result)
        self.assertIn("legitimate_probability", result)
        self.assertIn("features", result)
        self.assertIn("disclaimer", result)
        self.assertIn(result["prediction"], ["Phishing", "Legitimate"])
        self.assertIn(result["label"], [0, 1])
        self.assertAlmostEqual(result["phishing_probability"] + result["legitimate_probability"], 1.0, places=4)


if __name__ == "__main__":
    unittest.main()
