"""
PhishGuard — Phishing URL Detector
Antarmuka Web Deteksi URL Phishing Berbasis Machine Learning
File: app/app.py
Deskripsi:
    Aplikasi web Streamlit teroptimasi untuk demonstrasi sistem deteksi URL phishing.
    Menggunakan tata letak responsif, kartu panel modular, dan palet warna profesional.
"""

import sys
import os
import streamlit as st

# Hubungkan direktori src/ agar modul prediksi dan ekstraksi fitur dapat diimpor
SRC_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from prediction import predict_url, get_model


# 1. Konfigurasi Halaman (Wide Layout dengan Pembatas Lebar Maksimal)
st.set_page_config(
    page_title="PhishGuard — Phishing URL Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inisialisasi Model Menggunakan Cache Streamlit
@st.cache_resource
def load_model_instance():
    return get_model()

try:
    load_model_instance()
    is_model_ready = True
except Exception as err:
    is_model_ready = False
    st.error(f"Gagal memuat model Machine Learning: {err}")

# 3. Kustomisasi Styling CSS (Navy, Slate, Teal, & Card System)
st.markdown(
    """
    <style>
    /* Optimasi Lebar Kontainer Utama untuk Layar Laptop */
    .block-container {
        max-width: 1080px !important;
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Hero Banner yang Ringkas & Elegan */
    .hero-banner {
        background: linear-gradient(135deg, #0f2744 0%, #1e3a5f 60%, #0d9488 100%);
        border-radius: 12px;
        padding: 1.25rem 1.6rem;
        color: #ffffff;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 15px rgba(15, 39, 68, 0.15);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .hero-badge-wrap {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 0.35rem;
    }
    .hero-badge {
        background-color: rgba(14, 165, 233, 0.25);
        color: #38bdf8;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.2rem 0.65rem;
        border-radius: 16px;
        letter-spacing: 0.6px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        display: inline-block;
    }
    .hero-title {
        font-size: 1.75rem;
        font-weight: 800;
        color: #ffffff !important;
        margin: 0 0 0.25rem 0;
        letter-spacing: -0.5px;
    }
    .hero-desc {
        font-size: 0.92rem;
        color: #e2e8f0 !important;
        margin: 0;
        line-height: 1.45;
    }

    /* Kartu Panel Modular */
    .panel-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    @media (prefers-color-scheme: dark) {
        .panel-card {
            background: #1e293b;
            border-color: #334155;
            color: #f8fafc;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
        }
    }

    /* Kartu Hasil Deteksi */
    .result-alert-phishing {
        background: rgba(239, 68, 68, 0.08);
        border: 1.5px solid #ef4444;
        border-radius: 10px;
        padding: 1.1rem 1.35rem;
        margin-bottom: 1rem;
    }
    .result-alert-legitimate {
        background: rgba(16, 185, 129, 0.08);
        border: 1.5px solid #10b981;
        border-radius: 10px;
        padding: 1.1rem 1.35rem;
        margin-bottom: 1rem;
    }
    .result-title-phishing {
        color: #dc2626;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .result-title-legitimate {
        color: #059669;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .result-text {
        font-size: 0.92rem;
        margin: 0;
        line-height: 1.5;
        opacity: 0.95;
    }

    /* Disclaimer Box */
    .disclaimer-card {
        background: rgba(14, 165, 233, 0.05);
        border-left: 4px solid #0284c7;
        border-radius: 4px 8px 8px 4px;
        padding: 0.85rem 1.1rem;
        font-size: 0.84rem;
        line-height: 1.5;
        margin-top: 1rem;
    }

    /* Penyesuaian Tombol CTA */
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #ffffff;
        font-weight: 600;
        font-size: 0.95rem;
        height: 2.85rem;
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0369a1 0%, #075985 100%);
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.45);
        color: #ffffff;
    }

    /* Metric Box Kustom */
    .metric-badge {
        padding: 0.75rem 1rem;
        border-radius: 8px;
        background: rgba(241, 245, 249, 0.6);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    @media (prefers-color-scheme: dark) {
        .metric-badge {
            background: rgba(15, 23, 42, 0.4);
            border-color: #334155;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 4. Hero Banner Ringkas
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-badge-wrap">
            <span class="hero-badge">DEFENSIVE AI • SISTEM DETEKSI DINI</span>
        </div>
        <h1 class="hero-title">🛡️ PhishGuard — Phishing URL Detector</h1>
        <p class="hero-desc">
            Sistem analisis defensif berbasis Machine Learning untuk mengidentifikasi indikasi ancaman URL phishing 
            melalui 16 karakteristik leksikal dan struktural tanpa membuka koneksi ke situs tujuan.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 5. Panel Input URL & Pilihan Sampel
st.markdown("#### 🔍 Pemeriksaan URL")

# Layout 2 Baris Bersih: Baris 1 Input URL & Contoh, Baris 2 Tombol Periksa
col_url, col_sample = st.columns([3.2, 1.3])

with col_sample:
    pilihan_sampel = st.selectbox(
        "Pilih Contoh URL:",
        options=[
            "Ketik URL Sendiri...",
            "https://www.google.com",
            "http://myglobaltech.in/",
            "http://117.205.108.72:37255/bin.sh",
            "https://keraekken-loagginnusa.godaddysites.com/"
        ],
        help="Gunakan URL contoh dari dataset untuk demonstrasi cepat."
    )

default_text = "" if pilihan_sampel == "Ketik URL Sendiri..." else pilihan_sampel

with col_url:
    url_target = st.text_input(
        "URL Sasaran:",
        value=default_text,
        placeholder="https://example.com/login atau www.domain.com",
        help="Masukkan alamat web lengkap atau tanpa protokol."
    )

col_action, col_info_tip = st.columns([1.5, 3])
with col_action:
    btn_periksa = st.button("🚀 Analisis Keamanan URL", type="primary", use_container_width=True)

with col_info_tip:
    st.caption("🔒 Analisis dilakukan murni pada teks URL (offline & aman). Tidak ada HTTP request ke server target.")

# 6. Logika Eksekusi Prediksi & Area Hasil Analisis
if btn_periksa:
    if not url_target.strip():
        st.warning("⚠️ Mohon masukkan URL terlebih dahulu sebelum menekan tombol analisis.")
    else:
        try:
            with st.spinner("Mengekstrak fitur leksikal dan menghitung probabilitas model..."):
                hasil = predict_url(url_target)

            st.write("")
            st.markdown("#### 📊 Hasil Analisis Sistem")

            is_phishing = (hasil["prediction"] == "Phishing")

            # Panel Utama Hasil Prediksi
            if is_phishing:
                st.markdown(
                    f"""
                    <div class="result-alert-phishing">
                        <div class="result-title-phishing">🚨 Terindikasi URL Phishing</div>
                        <p class="result-text">
                            Model mendeteksi anomali pada karakteristik teks URL ini yang menyerupai pola penipuan, pemalsuan identitas, atau distribusi konten berbahaya.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="result-alert-legitimate">
                        <div class="result-title-legitimate">✅ Diprediksi URL Legitimate (Aman)</div>
                        <p class="result-text">
                            Karakteristik struktur dan leksikal URL ini konsisten dengan pola situs web yang sah dan tidak memperlihatkan indikasi khas penipuan phishing.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Ringkasan 3 Metrik Utama
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric(
                    label="Status Klasifikasi",
                    value=hasil["prediction"],
                    delta="- Berisiko" if is_phishing else "+ Terverifikasi"
                )
            with col_m2:
                st.metric(
                    label="Tingkat Keyakinan Model",
                    value=f"{hasil['confidence'] * 100:.2f}%"
                )
            with col_m3:
                st.metric(
                    label="Probabilitas Phishing",
                    value=f"{hasil['phishing_probability'] * 100:.2f}%"
                )

            # Indikator Visual Skor Risiko
            st.markdown("<small style='font-weight:600;'>Estimasi Skor Risiko Phishing:</small>", unsafe_allow_html=True)
            st.progress(float(hasil["phishing_probability"]))

            # Panel Rincian 16 Fitur URL
            with st.expander("📋 Rincian 16 Karakteristik Fitur URL yang Dianalisis", expanded=False):
                st.caption("Nilai 16 parameter leksikal dan struktural yang diekstrak oleh model:")
                f = hasil["features"]
                
                f_col1, f_col2, f_col3, f_col4 = st.columns(4)
                with f_col1:
                    st.metric("Panjang URL", f"{f['url_length']} ch")
                    st.metric("Host Alamat IP", "Ya" if f['has_ip_address'] else "Tidak")
                    st.metric("Jumlah Titik (.)", f"{f['dot_count']}")
                    st.metric("Protokol HTTPS", "Ya" if f['https_flag'] else "Tidak")

                with f_col2:
                    st.metric("Entropi Shannon", f"{f['url_entropy']:.3f}")
                    st.metric("Jumlah Token", f"{f['token_count']}")
                    st.metric("Tingkat Subdomain", f"{f['subdomain_count']}")
                    st.metric("Query Parameters", f"{f['query_param_count']}")

                with f_col3:
                    st.metric("Panjang TLD", f"{f['tld_length']} ch")
                    st.metric("Panjang Path", f"{f['path_length']} ch")
                    st.metric("Hyphen (-) Domain", "Ya" if f['has_hyphen_in_domain'] else "Tidak")
                    st.metric("Jumlah Angka", f"{f['number_of_digits']}")

                with f_col4:
                    st.metric("Popularitas TLD", "Populer" if f['tld_popularity'] else "Rendah")
                    st.metric("Ekstensi Bahaya", "Ya" if f['suspicious_file_extension'] else "Tidak")
                    st.metric("Panjang Domain", f"{f['domain_name_length']} ch")
                    st.metric("Kerapatan Angka", f"{f['percentage_numeric_chars']:.1f}%")

            # Penafian Keamanan Wajib
            st.markdown(
                f"""
                <div class="disclaimer-card">
                    <strong>🛡️ Catatan Keamanan & Penafian (Security Disclaimer):</strong><br>
                    {hasil['disclaimer']}<br>
                    <em>Hasil klasifikasi merupakan estimasi probabilitas model statistik dan bukan merupakan jaminan mutlak keamanan suatu situs web. Selalu terapkan kewaspadaan sebelum memasukkan kredensial pribadi.</em>
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses URL: {e}")

# 7. Sidebar Ramping & Informatif
with st.sidebar:
    st.markdown("### 🛡️ PhishGuard System")
    st.markdown(
        """
        Sistem pertahanan siber berbasis **Defensive AI** untuk klasifikasi URL phishing secara cepat dan presisi.
        """
    )
    st.divider()

    st.markdown("##### ⚙️ Arsitektur Model")
    st.markdown("- **Model:** Random Forest (100 Trees)")
    st.markdown("- **Dataset:** LegitPhish Dataset")
    st.markdown("- **Fitur:** 16 Fitur Leksikal & Struktural")

    st.divider()

    st.markdown("##### 📈 Hasil Evaluasi Aktual (Test Set)")
    st.markdown("- **Akurasi Total:** `99.95%`")
    st.markdown("- **Phishing Precision:** `99.93%`")
    st.markdown("- **Phishing Recall:** `99.98%`")
    st.markdown("- **Phishing F1-Score:** `99.96%`")
    st.markdown("- **Legitimate F1-Score:** `99.93%`")

    st.divider()
    st.caption("Keamanan Informasi • Topik 1 (Defensive AI)")
