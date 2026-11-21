"""
Modul Pelatihan dan Evaluasi Model Random Forest
Tugas: Anggota 1 (Machine Learning)
File: src/train_model.py
Deskripsi:
    1. Melatih model Random Forest Classifier pada data training.
    2. Menghitung metrik evaluasi nyata (Accuracy, Precision, Recall, F1-Score, Confusion Matrix).
    3. Menganalisis False Positive (FP) dan False Negative (FN).
    4. Menyimpan plot confusion matrix dan feature importance ke folder evaluation/.
    5. Menyimpan model terlatih dan metadata fitur ke folder models/ menggunakan Joblib.
"""

import json
import os
import time
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from preprocessing import FEATURE_COLUMNS, load_and_preprocess_data

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
EVALUATION_DIR = os.path.join(BASE_DIR, "evaluation")

MODEL_FILE = os.path.join(MODELS_DIR, "random_forest_phishing_model.joblib")
METADATA_FILE = os.path.join(MODELS_DIR, "model_metadata.joblib")
CONFUSION_MATRIX_PLOT = os.path.join(EVALUATION_DIR, "confusion_matrix.png")
FEATURE_IMPORTANCE_PLOT = os.path.join(EVALUATION_DIR, "feature_importance.png")
REPORT_JSON = os.path.join(EVALUATION_DIR, "evaluation_report.json")
REPORT_TXT = os.path.join(EVALUATION_DIR, "evaluation_report.txt")


def train_and_evaluate():
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(EVALUATION_DIR, exist_ok=True)

    print("=" * 65)
    print("      MEMULAI PELATIHAN MODEL RANDOM FOREST CLASSIFIER")
    print("=" * 65)

    # 1. Preprocessing data
    X_train, X_test, y_train, y_test, feature_names = load_and_preprocess_data()

    # 2. Inisialisasi model dengan hiperparameter terjustifikasi
    # - n_estimators=100 : Jumlah pohon keputusan ideal untuk stabilitas ensemble voting.
    # - max_depth=25     : Membatasi kedalaman pohon untuk mencegah overfitting dan menjaga efisiensi memori.
    # - min_samples_split=5 : Mencegah split pada kelompok data yang terlalu kecil/spesifik.
    # - min_samples_leaf=2  : Memastikan setiap daun memiliki minimal 2 sampel untuk generalisasi.
    # - class_weight='balanced' : Memberi bobot seimbang pada kelas 0 (Phishing) dan 1 (Legitimate).
    # - random_state=42  : Memastikan eksperimen 100% dapat direproduksi secara konsisten.
    # - n_jobs=-1        : Memanfaatkan seluruh inti CPU yang tersedia untuk mempercepat training.
    rf_params = {
        "n_estimators": 100,
        "max_depth": 25,
        "min_samples_split": 5,
        "min_samples_leaf": 2,
        "class_weight": "balanced",
        "random_state": 42,
        "n_jobs": -1,
    }

    print("\n[TRAINING] Konfigurasi Hiperparameter:")
    for k, v in rf_params.items():
        print(f"   - {k:<18} : {v}")

    model = RandomForestClassifier(**rf_params)

    # 3. Training
    start_time = time.time()
    print("\n[TRAINING] Sedang melatih model...")
    model.fit(X_train, y_train)
    training_duration = time.time() - start_time
    print(f"[TRAINING] Pelatihan selesai dalam {training_duration:.2f} detik.")

    # 4. Prediksi pada data uji (X_test)
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)

    # 5. Perhitungan Metrik Evaluasi Nyata
    acc = float(accuracy_score(y_test, y_pred))
    
    # Metrik untuk kelas 0 (Phishing)
    prec_phish = float(precision_score(y_test, y_pred, pos_label=0))
    rec_phish = float(recall_score(y_test, y_pred, pos_label=0))
    f1_phish = float(f1_score(y_test, y_pred, pos_label=0))

    # Metrik untuk kelas 1 (Legitimate)
    prec_legit = float(precision_score(y_test, y_pred, pos_label=1))
    rec_legit = float(recall_score(y_test, y_pred, pos_label=1))
    f1_legit = float(f1_score(y_test, y_pred, pos_label=1))

    # Macro & Weighted Average
    macro_f1 = float(f1_score(y_test, y_pred, average="macro"))
    weighted_f1 = float(f1_score(y_test, y_pred, average="weighted"))

    # Confusion Matrix:
    # y_true vs y_pred
    # baris 0 = True Phishing, baris 1 = True Legitimate
    # kolom 0 = Pred Phishing, kolom 1 = Pred Legitimate
    cm = confusion_matrix(y_test, y_pred)
    tn = int(cm[0, 0])  # True Phishing (prediksi Phishing, aktual Phishing)
    fp = int(cm[0, 1])  # False Legitimate (aktual Phishing, salah diprediksi Legitimate)
    fn = int(cm[1, 0])  # False Phishing (aktual Legitimate, salah diprediksi Phishing)
    tp = int(cm[1, 1])  # True Legitimate (prediksi Legitimate, aktual Legitimate)

    print("\n" + "=" * 65)
    print("                     HASIL EVALUASI MODEL")
    print("=" * 65)
    print(f"Accuracy                 : {acc * 100:.2f}%")
    print("\nDetail Metrik Per Kelas:")
    print(f"  [Kelas 0 - Phishing]   : Precision = {prec_phish*100:.2f}%, Recall = {rec_phish*100:.2f}%, F1 = {f1_phish*100:.2f}%")
    print(f"  [Kelas 1 - Legitimate] : Precision = {prec_legit*100:.2f}%, Recall = {rec_legit*100:.2f}%, F1 = {f1_legit*100:.2f}%")
    print(f"  Macro F1-Score         : {macro_f1 * 100:.2f}%")
    print(f"  Weighted F1-Score      : {weighted_f1 * 100:.2f}%")

    print("\nConfusion Matrix:")
    print(f"                      Prediksi Phishing (0)    Prediksi Legitimate (1)")
    print(f"  Aktual Phishing (0)       {tn:>8,} (TN)               {fp:>8,} (FP)")
    print(f"  Aktual Legitimate (1)     {fn:>8,} (FN)               {tp:>8,} (TP)")

    # 6. Analisis False Positive dan False Negative
    print("\n" + "-" * 65)
    print("ANALISIS KESALAHAN KLASIFIKASI (SECURITY IMPACT ANALYSIS):")
    print(f"1. False Legitimate (Phishing lolos sebagai Aman / FP terhadap Legitimate): {fp:,} kasus ({fp/len(y_test)*100:.2f}%)")
    print("   -> Dampak Keamanan: SANGAT KRITIS. URL phishing yang lolos dapat menipu pengguna")
    print("      untuk memasukkan kredensial atau mengunduh malware.")
    print(f"2. False Phishing (Legitimate terblokir sebagai Phishing / FN terhadap Legitimate): {fn:,} kasus ({fn/len(y_test)*100:.2f}%)")
    print("   -> Dampak Pengguna: Mengakibatkan *false alarm* atau ketidaknyamanan,")
    print("      namun secara keamanan jauh lebih aman dibanding phishing yang lolos.")
    print("-" * 65)

    # 7. Simpan Visualisasi Confusion Matrix
    plt.figure(figsize=(6, 5))
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title("Confusion Matrix - Random Forest URL Detector", fontsize=12, pad=12)
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ["Phishing (0)", "Legitimate (1)"])
    plt.yticks(tick_marks, ["Phishing (0)", "Legitimate (1)"])

    # Nilai di dalam cell
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            val = f"{cm[i, j]:,}"
            plt.text(
                j,
                i,
                val,
                ha="center",
                va="center",
                color="white" if cm[i, j] > thresh else "black",
                fontsize=11,
                fontweight="bold",
            )

    plt.ylabel("Label Aktual", fontsize=11)
    plt.xlabel("Label Prediksi", fontsize=11)
    plt.tight_layout()
    plt.savefig(CONFUSION_MATRIX_PLOT, dpi=300)
    plt.close()
    print(f"\n[EVALUASI] Plot Confusion Matrix tersimpan di: {CONFUSION_MATRIX_PLOT}")

    # 8. Analisis dan Plot Feature Importance
    importances = model.feature_importances_
    feat_imp_df = pd.DataFrame(
        {"Fitur": feature_names, "Importance": importances}
    ).sort_values("Importance", ascending=True)

    plt.figure(figsize=(9, 6))
    plt.barh(feat_imp_df["Fitur"], feat_imp_df["Importance"], color="#2b5c8f")
    plt.title("Tingkat Kepentingan Fitur (Feature Importance) - Random Forest", fontsize=12)
    plt.xlabel("Skor Kepentingan (Gini Importance)", fontsize=11)
    plt.tight_layout()
    plt.savefig(FEATURE_IMPORTANCE_PLOT, dpi=300)
    plt.close()
    print(f"[EVALUASI] Plot Feature Importance tersimpan di: {FEATURE_IMPORTANCE_PLOT}")

    # 9. Simpan Model & Metadata Menggunakan Joblib
    joblib.dump(model, MODEL_FILE)
    print(f"\n[MODEL] Model Random Forest tersimpan di: {MODEL_FILE}")

    metadata = {
        "model_name": "RandomForestClassifier",
        "algorithm": "Random Forest",
        "parameters": rf_params,
        "feature_names": feature_names,
        "n_features": len(feature_names),
        "target_mapping": {0: "Phishing", 1: "Legitimate"},
        "training_samples": len(X_train),
        "testing_samples": len(X_test),
        "metrics": {
            "accuracy": acc,
            "phishing": {"precision": prec_phish, "recall": rec_phish, "f1_score": f1_phish},
            "legitimate": {"precision": prec_legit, "recall": rec_legit, "f1_score": f1_legit},
            "macro_f1": macro_f1,
            "weighted_f1": weighted_f1,
            "confusion_matrix": {
                "tn": tn,
                "fp": fp,
                "fn": fn,
                "tp": tp,
            },
        },
        "feature_importances": dict(zip(feat_imp_df["Fitur"], feat_imp_df["Importance"])),
    }
    joblib.dump(metadata, METADATA_FILE)
    print(f"[MODEL] Metadata fitur dan evaluasi tersimpan di: {METADATA_FILE}")

    # 10. Simpan Laporan Evaluasi dalam JSON dan TXT
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    with open(REPORT_TXT, "w", encoding="utf-8") as f:
        f.write("LAPORAN EVALUASI MODEL RANDOM FOREST - PHISHING URL DETECTOR\n")
        f.write("=" * 65 + "\n\n")
        f.write(f"Waktu Pelatihan    : {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Durasi Pelatihan   : {training_duration:.2f} detik\n")
        f.write(f"Jumlah Data Train  : {len(X_train):,} baris\n")
        f.write(f"Jumlah Data Test   : {len(X_test):,} baris\n\n")
        f.write("METRIK EVALUASI:\n")
        f.write(f"- Akurasi                : {acc*100:.2f}%\n")
        f.write(f"- Phishing (0) Precision : {prec_phish*100:.2f}%\n")
        f.write(f"- Phishing (0) Recall    : {rec_phish*100:.2f}%\n")
        f.write(f"- Phishing (0) F1-Score  : {f1_phish*100:.2f}%\n")
        f.write(f"- Legitimate (1) Precision: {prec_legit*100:.2f}%\n")
        f.write(f"- Legitimate (1) Recall : {rec_legit*100:.2f}%\n")
        f.write(f"- Legitimate (1) F1-Score: {f1_legit*100:.2f}%\n")
        f.write(f"- Macro F1-Score         : {macro_f1*100:.2f}%\n")
        f.write(f"- Weighted F1-Score      : {weighted_f1*100:.2f}%\n\n")
        f.write("CONFUSION MATRIX:\n")
        f.write(f"- True Phishing (TN)   : {tn:,}\n")
        f.write(f"- False Legitimate (FP): {fp:,}\n")
        f.write(f"- False Phishing (FN)  : {fn:,}\n")
        f.write(f"- True Legitimate (TP) : {tp:,}\n\n")
        f.write("SKL CLASSIFICATION REPORT:\n")
        f.write(classification_report(y_test, y_pred, target_names=["Phishing (0)", "Legitimate (1)"]))

    print(f"[EVALUASI] Laporan evaluasi tersimpan di: {REPORT_TXT}")
    print("=" * 65)


if __name__ == "__main__":
    train_and_evaluate()
