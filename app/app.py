"""
PhishGuard — Web-Based Phishing URL Detection System
Frontend Streamlit (Anggota 3)
Jalankan dari root project: streamlit run app/app.py
"""
import os
import sys

import streamlit as st

# --- Path backend ---
APP_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(APP_DIR)
for path in (APP_DIR, os.path.join(BASE_DIR, "src")):
    if path not in sys.path:
        sys.path.insert(0, path)

from prediction import get_model          # backend (Anggota 2)
import theme, components as ui, views     # frontend

st.set_page_config(
    page_title="PhishGuard — Phishing URL Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

PAGES = {
    "home": "Beranda",
    "scan": "URL Scanner",
    "eval": "Evaluasi Model",
    "guide": "Edukasi & Log",
}

# --- Session state ---
st.session_state.setdefault("nav", PAGES["home"])
st.session_state.setdefault("scan_history", [])
st.session_state.setdefault("last_result", None)
st.session_state.setdefault("bulk_df", None)
st.session_state.setdefault("url_input", "")


# --- Load model ---
@st.cache_resource
def load_model():
    return get_model()


try:
    load_model()
    model_ready = True
except Exception as err:
    model_ready = False
    st.error(f"Gagal memuat model Machine Learning: {err}")

# --- Tema (100% mengikuti pilihan di menu ⋮ -> Light / Dark) ---
palette = theme.get_palette(theme.is_dark())
theme.inject_css(palette)
palette = {**palette, "_pages": PAGES}

# --- Sidebar: panel info sesi & aktivitas terakhir ---
with st.sidebar:
    ui.brand()
    st.divider()

    hist = st.session_state.scan_history
    n_ph = sum(1 for h in hist if h["Hasil Prediksi"] == "Phishing")
    n_ok = sum(1 for h in hist if h["Hasil Prediksi"] == "Legitimate")
    st.markdown("**Ringkasan Sesi**")
    s1, s2, s3 = st.columns(3)
    s1.metric("Scan", len(hist))
    s2.metric("Phish", n_ph)
    s3.metric("Legit", n_ok)

    st.divider()
    st.markdown("**Aktivitas Terakhir**")
    if not hist:
        st.caption("Belum ada URL dipindai pada sesi ini.")
    else:
        for item in hist[:3]:
            badge = "🔴" if item["Hasil Prediksi"] == "Phishing" else "🟢"
            short_url = item["URL Sasaran"][:28] + ("..." if len(item["URL Sasaran"]) > 28 else "")
            st.caption(f"{badge} `{short_url}`\n**{item['Hasil Prediksi']}** ({item['Probabilitas Phishing']})")

    st.divider()
    status = "Aktif (Random Forest)" if model_ready else "Model gagal dimuat"
    st.caption(
        f"**Status Engine:** {status}\n\n"
        f"**Dataset Latih:** LegitPhish (100.872 URL)\n\n"
        f"**Mata Kuliah:** Keamanan Informasi\n\n"
        f"**Universitas Siliwangi**"
    )

# --- Navbar atas ---
with st.container(key="topnav"):
    c_brand, c1, c2, c3, c4, c_stat = st.columns([2.3, 1, 1.2, 1.3, 1.3, 1.4])
    with c_brand:
        ui.brand()
    for col, key in zip((c1, c2, c3, c4), ("home", "scan", "eval", "guide")):
        col.button(
            PAGES[key],
            key=f"nav_{key}",
            use_container_width=True,
            type="primary" if st.session_state.nav == PAGES[key] else "secondary",
            on_click=views.go_to,
            args=(PAGES[key],),
        )
    with c_stat:
        ui.status_pill(model_ready)

# --- Router ---
if not model_ready:
    st.stop()

page = st.session_state.nav
if page == PAGES["home"]:
    views.page_home(palette, PAGES)
elif page == PAGES["scan"]:
    views.page_scanner(palette)
elif page == PAGES["eval"]:
    views.page_eval(palette)
else:
    views.page_guide(palette)

ui.footer()