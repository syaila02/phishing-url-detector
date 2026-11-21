# Dokumentasi Model Machine Learning

Folder ini memuat model Machine Learning terlatih dan metadata fitur untuk sistem deteksi URL phishing.

## 1. File Model
- **`random_forest_phishing_model.joblib`**: Model scikit-learn `RandomForestClassifier` terlatih pada 80.697 data training.
- **`model_metadata.joblib`**: Metadata dictionary yang memuat nama fitur, urutan fitur, hyperparameter, dan skor evaluasi.

## 2. Spesifikasi Model
- **Algoritma:** Random Forest Classifier
- **Library:** `scikit-learn` & `joblib`
- **Hiperparameter:**
  - `n_estimators`: 100
  - `max_depth`: 25
  - `min_samples_split`: 5
  - `min_samples_leaf`: 2
  - `class_weight`: "balanced"
  - `random_state`: 42
  - `n_jobs`: -1

## 3. Cara Memuat Model di Python (Untuk Anggota 2 & 3)
```python
import joblib

# Muat model
model = joblib.load("models/random_forest_phishing_model.joblib")

# Muat metadata
metadata = joblib.load("models/model_metadata.joblib")
feature_names = metadata["feature_names"]

# Prediksi menggunakan DataFrame dengan kolom yang sesuai
# y_pred = model.predict(df_features[feature_names])
```

## 4. Urutan 16 Fitur Wajib
Model mengharapkan input 2D array atau DataFrame dengan urutan 16 kolom berikut:
1. `url_length` (int)
2. `has_ip_address` (int: 0 atau 1)
3. `dot_count` (int)
4. `https_flag` (int: 0 atau 1)
5. `url_entropy` (float)
6. `token_count` (int)
7. `subdomain_count` (int)
8. `query_param_count` (int)
9. `tld_length` (int)
10. `path_length` (int)
11. `has_hyphen_in_domain` (int: 0 atau 1)
12. `number_of_digits` (int)
13. `tld_popularity` (int: 0 atau 1)
14. `suspicious_file_extension` (int: 0 atau 1)
15. `domain_name_length` (int)
16. `percentage_numeric_chars` (float)
