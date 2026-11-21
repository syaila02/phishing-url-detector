"""
Modul Ekstraksi Fitur URL
Tugas: Anggota 1 (Machine Learning) & Integrasi Anggota 2 (Backend)
File: src/feature_extraction.py
Deskripsi:
    Mengekstrak 16 karakteristik leksikal dan struktural dari sebuah string URL
    agar konsisten 100% dengan format fitur dataset LegitPhish saat training.
"""

import math
import os
import re
from collections import Counter
from urllib.parse import urlparse
import pandas as pd

# Daftar 16 fitur dengan urutan yang sama persis seperti dataset
FEATURE_NAMES = [
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

POPULAR_TLDS = {"com", "org", "net", "edu", "gov"}
SUSPICIOUS_EXTENSIONS = {".exe", ".zip", ".bin", ".apk", ".cmd", ".js", ".1exe"}
IPV4_PATTERN = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?::\d+)?$")


def calculate_entropy(text: str) -> float:
    """Menghitung Shannon Entropy dari teks URL."""
    if not text:
        return 0.0
    length = len(text)
    counts = Counter(text)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())


def extract_features(url: str) -> dict:
    """
    Mengekstrak 16 fitur dari sebuah URL string.
    Mengembalikan dictionary dengan key sesuai FEATURE_NAMES.
    """
    clean_url = str(url).strip()
    if not clean_url:
        raise ValueError("URL tidak boleh kosong.")

    # Jika URL tidak memiliki skema (misal 'example.com'), tambahkan 'http://' untuk parsing
    parse_target = clean_url
    if not clean_url.startswith(("http://", "https://", "ftp://")):
        parse_target = "http://" + clean_url

    parsed = urlparse(parse_target)
    netloc = parsed.netloc or ""
    host = netloc.split(":")[0]  # buang port jika ada
    path = parsed.path or ""

    # 1. url_length
    url_length = len(clean_url)

    # 2. has_ip_address
    has_ip = 1 if bool(IPV4_PATTERN.match(netloc) or IPV4_PATTERN.match(host)) else 0

    # 3. dot_count
    dot_count = clean_url.count(".")

    # 4. https_flag
    https_flag = 1 if clean_url.lower().startswith("https://") else 0

    # 5. url_entropy
    url_entropy = calculate_entropy(clean_url)

    # 6. token_count: sum(len(part.split('.')) for part in clean_url.split('/'))
    token_count = sum(len(part.split(".")) for part in clean_url.split("/"))

    # Domain parsing untuk subdomain, domain_name, tld
    host_parts = host.split(".") if host else []
    if len(host_parts) >= 2:
        tld = host_parts[-1].lower()
        domain_name = host_parts[-2]
        subdomain_count = max(0, len(host_parts) - 2)
    elif len(host_parts) == 1:
        tld = host_parts[0].lower()
        domain_name = host_parts[0]
        subdomain_count = 0
    else:
        tld = ""
        domain_name = ""
        subdomain_count = 0

    # 7. subdomain_count
    # (dihitung di atas)

    # 8. query_param_count
    query_param_count = (clean_url.count("&") + 1) if clean_url.count("&") > 0 else 1

    # 9. tld_length
    tld_length = len(tld)

    # 10. path_length
    path_length = len(path)

    # 11. has_hyphen_in_domain
    has_hyphen_in_domain = 1 if ("-" in host or "-" in domain_name) else 0

    # 12. number_of_digits
    number_of_digits = sum(c.isdigit() for c in clean_url)

    # 13. tld_popularity
    tld_popularity = 1 if tld in POPULAR_TLDS else 0

    # 14. suspicious_file_extension
    _, ext = os.path.splitext(path)
    suspicious_file_extension = 1 if ext.lower() in SUSPICIOUS_EXTENSIONS else 0

    # 15. domain_name_length
    domain_name_length = len(domain_name)

    # 16. percentage_numeric_chars
    percentage_numeric_chars = (number_of_digits / url_length * 100.0) if url_length > 0 else 0.0

    features = {
        "url_length": int(url_length),
        "has_ip_address": int(has_ip),
        "dot_count": int(dot_count),
        "https_flag": int(https_flag),
        "url_entropy": float(url_entropy),
        "token_count": int(token_count),
        "subdomain_count": int(subdomain_count),
        "query_param_count": int(query_param_count),
        "tld_length": int(tld_length),
        "path_length": int(path_length),
        "has_hyphen_in_domain": int(has_hyphen_in_domain),
        "number_of_digits": int(number_of_digits),
        "tld_popularity": int(tld_popularity),
        "suspicious_file_extension": int(suspicious_file_extension),
        "domain_name_length": int(domain_name_length),
        "percentage_numeric_chars": float(percentage_numeric_chars),
    }

    return features


def extract_features_df(url: str) -> pd.DataFrame:
    """
    Mengekstrak fitur dari URL dan mengembalikan DataFrame 1 baris
    dengan kolom dan urutan yang tepat untuk diinput ke model ML.
    """
    feat_dict = extract_features(url)
    return pd.DataFrame([feat_dict])[FEATURE_NAMES]


if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "http://paypal-security-update.com/login.php?cmd=login&token=123",
        "http://117.205.108.72:37255/bin.sh",
    ]
    for u in test_urls:
        print(f"\nURL: {u}")
        df_feat = extract_features_df(u)
        print(df_feat.to_dict(orient="records")[0])
