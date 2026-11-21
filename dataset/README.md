# Dokumentasi Dataset: LegitPhish

## 1. Informasi Sumber
- **Nama Dataset:** LegitPhish: A large-scale annotated dataset for URL-based phishing detection
- **Penerbit / Sumber:** Mendeley Data & ScienceDirect (*Data in Brief*, PMCID: PMC12538017)
- **DOI / Link:** [https://data.mendeley.com/datasets/hx4m73v2sf/2](https://data.mendeley.com/datasets/hx4m73v2sf/2)
- **Penulis:** Rachana S. Potpelwar, Uday V. Kulkarni, Jaishri M. Waghmare
- **File CSV:** `url_features_extracted1.csv`

## 2. Struktur Data Mentah
- **Jumlah Baris Mentah:** 101.219 baris
- **Jumlah Kolom:** 18 kolom (1 URL string, 16 fitur numerik, 1 target `ClassLabel`)
- **Missing Value:** 1 baris bernilai `NaN` pada kolom target `ClassLabel` (baris indeks ke-65118).
- **Duplikasi:** 346 baris duplikat penuh.

## 3. Data Setelah Preprocessing
- **Total Data Bersih:** 100.872 baris
- **Distribusi Kelas:**
  - Label `0` (Phishing)   : 63.492 baris (62,94%) — bersumber dari URLhaus & PhishTank
  - Label `1` (Legitimate) : 37.380 baris (37,06%) — bersumber dari Google Search API, Wikipedia, Stack Overflow
- **Pembagian Data:**
  - Data Training : 80.697 baris (80%)
  - Data Testing  : 20.175 baris (20%)
  - Metode: `StratifiedShuffleSplit` (`stratify=y`, `random_state=42`)

## 4. Daftar 16 Fitur Leksikal & Struktural URL
1. `url_length`: Panjang total karakter string URL.
2. `has_ip_address`: Bernilai 1 jika host berupa alamat IP numerik (IPv4), 0 jika nama domain.
3. `dot_count`: Jumlah karakter titik (`.`) dalam URL.
4. `https_flag`: Bernilai 1 jika menggunakan protokol HTTPS, 0 jika HTTP.
5. `url_entropy`: Nilai entropi Shannon mengukur keacakan karakter teks URL.
6. `token_count`: Jumlah token/potongan kata hasil pemisahan URL.
7. `subdomain_count`: Jumlah level subdomain sebelum nama domain utama.
8. `query_param_count`: Jumlah parameter query (pemisah `&`).
9. `tld_length`: Panjang karakter Top-Level Domain (TLD).
10. `path_length`: Panjang karakter string path URL.
11. `has_hyphen_in_domain`: Bernilai 1 jika ada tanda hubung (`-`) pada domain, 0 jika tidak.
12. `number_of_digits`: Jumlah karakter angka numerik (0–9) dalam URL.
13. `tld_popularity`: Bernilai 1 jika TLD populer (`.com`, `.org`, `.net`, `.edu`, `.gov`), 0 jika lainnya.
14. `suspicious_file_extension`: Bernilai 1 jika path memiliki ekstensi berbahaya (`.exe`, `.zip`, `.bin`, `.apk`, dll.).
15. `domain_name_length`: Panjang karakter nama domain utama.
16. `percentage_numeric_chars`: Persentase karakter angka terhadap total panjang URL.
