"""Halaman-halaman PhishGuard."""
import os
from datetime import datetime

import pandas as pd
import streamlit as st

import components as ui
from prediction import predict_url

SAMPLES = [
    ("Legit · google.com", "https://www.google.com"),
    ("Legit · unsil.ac.id", "https://unsil.ac.id/"),
    ("Phish · IP + .sh", "http://117.205.108.72:37255/bin.sh"),
    ("Phish · godaddysites", "https://keraekken-loagginnusa.godaddysites.com/"),
]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVAL_PATH = os.path.join(BASE_DIR, "evaluation")


# ---------- callbacks ----------
def go_to(page: str):
    st.session_state.nav = page


def _set_sample(u: str):
    st.session_state.url_input = u
    st.session_state.pending_scan = True


def _quick_scan(pages: dict):
    st.session_state.url_input = st.session_state.get("quick_url", "").strip()
    st.session_state.pending_scan = True
    st.session_state.nav = pages["scan"]


def _quick_sample(u: str, pages: dict):
    st.session_state.url_input = u
    st.session_state.pending_scan = True
    st.session_state.nav = pages["scan"]


def _log(mode, url, pred, prob, conf):
    st.session_state.scan_history.insert(0, {
        "Waktu": datetime.now().strftime("%H:%M:%S"), "Mode": mode, "URL Sasaran": url,
        "Hasil Prediksi": pred, "Probabilitas Phishing": prob, "Confidence": conf,
    })


# =============================== BERANDA ===============================
def page_home(p, pages):
    ui.hero()
    ui.ticker()

    with st.container(border=True):
        ui.card_head("zap", "Quick Scan", "LOKAL · TANPA REQUEST")
        st.caption("Tempel URL, langsung diperiksa.")
        with st.form("quick_form"):
            a, b = st.columns([5, 1.3])
            a.text_input("URL", key="quick_url", label_visibility="collapsed",
                         placeholder="Contoh: https://contoh-website.com/login")
            b.form_submit_button("Scan", type="primary", use_container_width=True,
                                 on_click=_quick_scan, args=(pages,))
        st.caption("Atau coba contoh cepat:")
        cols = st.columns(len(SAMPLES))
        for col, (label, u) in zip(cols, SAMPLES):
            col.button(label, key=f"qs_{label}", use_container_width=True,
                       on_click=_quick_sample, args=(u, pages))

    st.write("")
    ui.stat_strip([("target", "99.95%", "Akurasi Pengujian"), ("grid", "16", "Fitur Leksikal"),
                   ("database", "100.872", "Data URL Latih"), ("eyeoff", "0", "Request ke Situs Target")])

    ui.section("01 · PENGANTAR", "Phishing URL: jebakan yang menyamar jadi situs resmi",
               "Pelajari cara penyerang menyamarkan tautan dan bagaimana PhishGuard membacanya.")
    a, b = st.columns([1.15, 1])
    with a:
        with st.container(border=True):
            ui.card_head("book", "Apa itu phishing URL?")
            st.markdown(
                "**Phishing URL** adalah tautan palsu yang dibuat menyerupai situs resmi (bank, e-commerce, "
                "instansi) untuk mencuri **kata sandi, PIN, OTP, atau data pribadi**.\n\n"
                "Penyerang biasanya menyamarkan tautan dengan alamat IP mentah, domain panjang penuh tanda hubung, "
                "subdomain berlapis, atau karakter acak. PhishGuard membaca pola-pola tersebut **hanya dari teks URL**."
            )
    with b:
        with st.container(border=True):
            ui.card_head("link", "Anatomi URL mencurigakan")
            ui.url_anatomy_static()

    ui.section("02 · KEUNGGULAN", "Mengapa PhishGuard?")
    ui.cards([
        ("zap", "Analisis 16 Fitur", "Panjang domain, entropi, IP langsung, ekstensi file, TLD, hyphen, dan fitur leksikal lainnya."),
        ("lock", "Zero-Visit & Aman", "Tidak ada HTTP request ke situs target, perangkat Anda aman dari skrip berbahaya dan pelacakan IP."),
        ("layers", "Random Forest 99.95%", "Ensemble 100 pohon keputusan dengan False Positive sangat rendah pada dataset LegitPhish."),
    ])

    ui.section("03 · ALUR KERJA", "Tiga langkah dari URL menjadi keputusan")
    ui.steps([
        ("1", "Input Tautan", "Tempel satu URL, atau banyak URL sekaligus di halaman Scanner."),
        ("2", "Ekstraksi & Prediksi", "Backend mengekstrak 16 fitur dan model menghitung probabilitas phishing."),
        ("3", "Laporan & Mitigasi", "Dapatkan skor keamanan (0–10), alasan teknis, dan langkah pencegahan."),
    ])

    with st.container(key="cta"):
        a, b, c = st.columns([3, 1.2, 1.4])
        with a:
            ui.cta_text("Punya tautan mencurigakan?", "Periksa sekarang, hasilnya keluar dalam hitungan detik.")
        b.button("Mulai Periksa URL", key="cta_scan", type="primary", use_container_width=True,
                 on_click=go_to, args=(pages["scan"],))
        c.button("Lihat Akurasi Model", key="cta_eval", use_container_width=True,
                 on_click=go_to, args=(pages["eval"],))


# =============================== SCANNER ===============================
def _run_single_scan(url: str):
    url = (url or "").strip()
    st.session_state.last_result = None
    if not url:
        st.warning("**Input kosong.** Masukkan alamat URL terlebih dahulu sebelum menekan **Scan URL**.", icon="⚠️")
        return
    if any(ch.isspace() for ch in url):
        st.warning("**Format tidak valid.** URL tidak boleh mengandung spasi. Contoh: `https://contoh.com/login`", icon="⚠️")
        return
    try:
        with st.spinner("Mengekstrak 16 fitur leksikal dan memprediksi tingkat risiko..."):
            hasil = predict_url(url)
        _log("Tunggal", url, hasil["prediction"],
             f"{hasil['phishing_probability']*100:.2f}%", f"{hasil['confidence']*100:.2f}%")
        st.session_state.last_result = {"url": url, "hasil": hasil}
    except ValueError as e:
        st.warning(f"**Format input tidak valid:** {e}", icon="⚠️")
    except Exception as e:
        st.error(f"**Kesalahan sistem:** gagal memproses URL ({e}).")


def _render_result(p, url, hasil):
    is_phish = hasil["prediction"] == "Phishing"
    prob = float(hasil["phishing_probability"])
    conf = float(hasil["confidence"])
    score = round((1.0 - prob) * 10, 1)
    f = hasil["features"]

    ui.verdict(p, is_phish, url, score)
    ui.kpis(p, prob, conf, score, is_phish)
    ui.pipeline()

    c_an, c_why = st.columns([1.15, 1])
    with c_an:
        with st.container(border=True):
            ui.card_head("link", "Anatomi URL yang dipindai")
            ui.url_anatomy_live(url, f)
    with c_why:
        with st.container(border=True):
            ui.card_head("search", "Mengapa hasilnya begini?")
            ui.reasons(f)

    c_ind, c_tech = st.columns(2)
    with c_ind:
        with st.container(border=True):
            ui.card_head("shield", "Security Indicators")
            ui.info_rows([
                ("Protokol Enkripsi", ui.chip("HTTPS Aktif") if f["https_flag"] else ui.chip("Non-HTTPS", "bad")),
                ("Identitas Host", ui.chip("Alamat IP Langsung", "bad") if f["has_ip_address"] else ui.chip("Nama Domain")),
                ("Ekstensi File", ui.chip("Ekstensi Berisiko", "bad") if f["suspicious_file_extension"] else ui.chip("Tidak Ada")),
                ("Hyphen (-) Domain", ui.chip("Ada Hyphen", "warn") if f["has_hyphen_in_domain"] else ui.chip("Bersih")),
                ("Reputasi TLD", ui.chip("TLD Populer") if f["tld_popularity"] else ui.chip("TLD Tidak Umum", "warn")),
            ])
    with c_tech:
        with st.container(border=True):
            ui.card_head("hash", "Technical Details")
            ui.info_rows([
                ("Panjang Total URL", ui.val(f"{f['url_length']} chars")),
                ("Panjang Domain", ui.val(f"{f['domain_name_length']} chars")),
                ("Shannon Entropy", ui.val(f"{f['url_entropy']:.4f}")),
                ("Subdomain / Titik", ui.val(f"{f['subdomain_count']} sub / {f['dot_count']} dot")),
                ("Digit Angka (Rasio)", ui.val(f"{f['number_of_digits']} ({f['percentage_numeric_chars']:.1f}%)")),
            ])

    c_rec, c_chart = st.columns([1.1, 1.4])
    with c_rec:
        with st.container(border=True):
            ui.card_head("shield", "Rekomendasi Tindakan")
            if is_phish:
                st.markdown(
                    "- **Jangan buka** tautan ini di browser utama.\n"
                    "- **Jangan masukkan** kata sandi, PIN, NIK, atau OTP.\n"
                    "- **Verifikasi** dengan mengetik alamat resmi instansi secara manual.\n"
                    "- **Laporkan** pesan pengirim sebagai spam/phishing."
                )
            else:
                st.markdown(
                    "- **Periksa ejaan domain** untuk menghindari *typosquatting*.\n"
                    "- **Pastikan ikon gembok HTTPS** aktif sebelum login.\n"
                    "- **Waspada unduhan** `.exe`, `.apk`, `.sh` dari sumber tak dikenal."
                )
    with c_chart:
        with st.container(border=True):
            ui.card_head("chart", "Komponen Struktural URL")
            st.altair_chart(ui.structure_chart(p, f, is_phish), use_container_width=True)

    with st.expander("Rincian lengkap 16 fitur ekstraksi"):
        ui.feature_tiles(f)

    ui.disclaimer(hasil.get("disclaimer", ""))


def _single_tab(p):
    pending = st.session_state.pop("pending_scan", None)

    with st.container(border=True):
        ui.card_head("search", "Pemeriksaan URL tunggal", "LOKAL · TANPA REQUEST")
        with st.form("scan_form"):
            c_in, c_btn = st.columns([5, 1.3])
            url = c_in.text_input("URL", key="url_input", label_visibility="collapsed",
                                  placeholder="Contoh: https://contoh-website.com/login")
            submit = c_btn.form_submit_button("Scan URL", type="primary", use_container_width=True)
        st.caption("Coba contoh cepat (langsung dipindai):")
        cols = st.columns(len(SAMPLES))
        for col, (label, u) in zip(cols, SAMPLES):
            col.button(label, key=f"smp_{label}", use_container_width=True, on_click=_set_sample, args=(u,))
        st.caption("Analisis dilakukan lokal pada teks URL tanpa membuka koneksi ke server tujuan.")

    if submit:
        _run_single_scan(url)
    elif pending:
        _run_single_scan(st.session_state.get("url_input", ""))

    res = st.session_state.get("last_result")
    if res:
        st.write("")
        _render_result(p, res["url"], res["hasil"])


def _bulk_tab(p):
    sample_bulk = "\n".join(u for _, u in SAMPLES)
    with st.container(border=True):
        ui.card_head("list", "Pemindaian massal", "1 BARIS = 1 URL")
        bulk_text = st.text_area("Daftar URL", value=sample_bulk, height=150, label_visibility="collapsed")
        go = st.button("Mulai Bulk Scan", type="primary")

    if go:
        lines = [l.strip() for l in bulk_text.splitlines() if l.strip()]
        if not lines:
            st.warning("Daftar URL masih kosong.", icon="⚠️")
            st.session_state.bulk_df = None
        else:
            rows, prog = [], st.progress(0, text="Memindai...")
            for i, u in enumerate(lines):
                try:
                    r = predict_url(u)
                    pred = r["prediction"]
                    pp, cf = f"{r['phishing_probability']*100:.2f}%", f"{r['confidence']*100:.2f}%"
                    ket = "Terindikasi Phishing" if pred == "Phishing" else "Tidak Terindikasi Phishing"
                except Exception as e:
                    pred, pp, cf, ket = "Invalid / Error", "-", "-", str(e)
                rows.append({"No": i + 1, "URL Sasaran": u, "Hasil Prediksi": pred,
                             "Probabilitas Phishing": pp, "Confidence": cf, "Keterangan": ket})
                _log("Massal", u, pred, pp, cf)
                prog.progress((i + 1) / len(lines), text=f"Memindai {i+1}/{len(lines)}")
            prog.empty()
            st.session_state.bulk_df = pd.DataFrame(rows)

    df = st.session_state.get("bulk_df")
    if df is not None:
        st.write("")
        n_ph = int((df["Hasil Prediksi"] == "Phishing").sum())
        n_ok = int((df["Hasil Prediksi"] == "Legitimate").sum())
        n_er = int((df["Hasil Prediksi"] == "Invalid / Error").sum())
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Total Dipindai", len(df))
        b2.metric("Terindikasi Phishing", n_ph)
        b3.metric("Diprediksi Legitimate", n_ok)
        b4.metric("Invalid / Error", n_er)
        ui.split_bar(p, n_ph, n_ok, n_er)

        filt = st.selectbox("Filter hasil", ["Semua", "Phishing", "Legitimate", "Invalid / Error"])
        view = df if filt == "Semua" else df[df["Hasil Prediksi"] == filt]
        st.dataframe(view, use_container_width=True, hide_index=True)
        st.download_button("Unduh Laporan Audit (.CSV)", df.to_csv(index=False).encode("utf-8"),
                           file_name=f"phishguard_audit_{datetime.now():%Y%m%d_%H%M%S}.csv", mime="text/csv")


def page_scanner(p):
    ui.page_header("search", "URL Threat Scanner",
                   "Periksa satu URL secara mendalam atau lakukan pemindaian massal untuk banyak tautan sekaligus.")
    t1, t2 = st.tabs(["Pemeriksaan Tunggal", "Pemindaian Massal"])
    with t1:
        st.write("")
        _single_tab(p)
    with t2:
        st.write("")
        _bulk_tab(p)


# =============================== EVALUASI ===============================
def page_eval(p):
    ui.page_header("chart", "Evaluasi & Performa Model",
                   "Hasil pengujian Random Forest pada 20.175 sampel uji dari dataset LegitPhish (100.872 URL).")
    ui.metric_grid([
        ("AKURASI PENGUJIAN", "99.95%", 99.95, "Prediksi benar dari seluruh sampel uji"),
        ("PHISHING PRECISION", "99.93%", 99.93, "Dari yang ditandai phishing, berapa yang benar"),
        ("PHISHING RECALL", "99.98%", 99.98, "Dari semua phishing, berapa yang tertangkap"),
        ("PHISHING F1-SCORE", "99.96%", 99.96, "Harmonisasi precision & recall"),
    ])

    st.write("")
    a, b = st.columns(2)
    with a:
        with st.container(border=True):
            ui.card_head("grid", "Confusion Matrix", "TEST SET")
            ui.confusion_grid(12697, 2, 9, 7467)
            st.caption("Hanya 11 kesalahan prediksi dari 20.175 sampel uji (2 FP + 9 FN).")
    with b:
        with st.container(border=True):
            ui.card_head("chart", "Feature Importance", "16 PARAMETER")
            fi = os.path.join(EVAL_PATH, "feature_importance.png")
            if os.path.exists(fi):
                st.image(fi, caption="Kontribusi fitur dalam klasifikasi Random Forest", use_container_width=True)
            else:
                st.info("File `evaluation/feature_importance.png` belum tersedia.")

    ui.section("RINGKASAN", "Tentang model")
    ui.cards([
        ("layers", "Algoritma", "Random Forest, ensemble 100 Decision Trees."),
        ("flask", "Data Uji", "20.175 sampel uji dari total 100.872 URL bersih (LegitPhish)."),
        ("grid", "Fitur", "16 fitur leksikal numerik/boolean hasil ekstraksi teks URL."),
    ])

    cm = os.path.join(EVAL_PATH, "confusion_matrix.png")
    if os.path.exists(cm):
        st.write("")
        with st.expander("Lihat gambar confusion matrix asli dari Anggota 1"):
            st.image(cm, use_container_width=True)


# =============================== EDUKASI & LOG ===============================
def page_guide(p):
    ui.page_header("book", "Edukasi Phishing & Log Sesi",
                   "Pelajari ciri tautan berbahaya dan pantau seluruh aktivitas pemindaian selama sesi.")
    ui.cards([
        ("globe", "1. Alamat IP Langsung", "Situs resmi memakai domain terdaftar (mis. <code>unsil.ac.id</code>), penyerang sering memakai IP mentah (<code>http://117.205.108.72/...</code>)."),
        ("minus", "2. Tanda Hubung & Subdomain Berlebih", "Contoh: <code>login-verifikasi-keamanan-akun.com</code> untuk meniru merek resmi."),
        ("hash", "3. Entropi Acak & Ekstensi Bahaya", "Kombinasi huruf-angka acak atau tautan ke file eksekusi seperti <code>.sh</code> dan <code>.exe</code>."),
        ("unlock", "4. Tanpa HTTPS", "Halaman login di <code>http://</code> tanpa SSL/TLS rentan terhadap penyadapan data."),
    ], cols=2)

    ui.section("PANDUAN CEPAT", "Cek 5 detik sebelum mengklik")
    with st.container(border=True):
        ui.checklist([
            ("Lihat domain utamanya", "Baca bagian sebelum tanda / pertama. Waspadai ejaan yang dimirip-miripkan."),
            ("Perhatikan protokol", "Halaman login wajib HTTPS. HTTP biasa berarti data tidak terenkripsi."),
            ("Curigai desakan", "Pesan 'akun diblokir' atau 'hadiah kedaluwarsa' adalah taktik tekanan."),
            ("Jangan unduh file asing", "Ekstensi .exe, .apk, dan .sh dari tautan tak dikenal sangat berisiko."),
            ("Tempel ke PhishGuard", "Periksa tautan di halaman Scanner sebelum membukanya."),
        ])

    ui.section("FAQ", "Pertanyaan yang sering muncul")
    with st.expander("Apakah PhishGuard membuka tautan yang saya periksa?"):
        st.write("Tidak. Analisis hanya membaca teks URL, tidak ada koneksi ke situs tujuan.")
    with st.expander("Seberapa akurat hasilnya?"):
        st.write("Akurasi pengujian 99.95% pada 20.175 sampel uji. Tetap berupa prediksi model, bukan jaminan mutlak.")
    with st.expander("Mengapa URL aman bisa terdeteksi phishing, atau sebaliknya?"):
        st.write("Model hanya melihat pola teks URL. Tautan yang strukturnya tidak biasa bisa salah klasifikasi, jadi tetap gunakan kewaspadaan.")
    with st.expander("Bagaimana mengganti tema gelap/terang?"):
        st.write("Buka menu ⋮ di pojok kanan atas, pilih Settings, lalu Theme.")

    ui.section("LOG SESI", "Riwayat pemeriksaan")
    with st.container(border=True):
        ui.card_head("clock", "Riwayat pemeriksaan", "SESI BERJALAN")
        hist = st.session_state.scan_history
        if not hist:
            st.info(f"Belum ada URL diperiksa. Buka halaman **{p['_pages']['scan']}** untuk memulai.")
        else:
            h = pd.DataFrame(hist)
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Pemindaian", len(h))
            m2.metric("Terindikasi Phishing", int((h["Hasil Prediksi"] == "Phishing").sum()))
            m3.metric("Legitimate", int((h["Hasil Prediksi"] == "Legitimate").sum()))
            st.dataframe(h, use_container_width=True, hide_index=True)
            d1, d2, _ = st.columns([1.2, 1.2, 3])
            d1.download_button("Unduh Log (.CSV)", h.to_csv(index=False).encode("utf-8"),
                               file_name=f"phishguard_log_{datetime.now():%Y%m%d_%H%M%S}.csv", mime="text/csv",
                               use_container_width=True)
            if d2.button("Bersihkan Log Sesi", use_container_width=True):
                st.session_state.scan_history = []
                st.rerun()