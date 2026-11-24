"""Komponen UI PhishGuard."""
import html as _html
from urllib.parse import urlsplit

import altair as alt
import pandas as pd
import streamlit as st

ICONS = {
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M8 17v-4M13 17V8M18 17v-7"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "unlock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/>',
    "layers": '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "grid": '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5"/><path d="M3 12c0 1.7 4 3 9 3s9-1.3 9-3"/>',
    "eyeoff": '<path d="m2 2 20 20"/><path d="M6.7 6.7C3.9 8.4 2 12 2 12s3.5 7 10 7c1.9 0 3.6-.5 5-1.3"/><path d="M9.9 4.2A10 10 0 0 1 12 5c6.5 0 10 7 10 7a17 17 0 0 1-2.2 3.2"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/>',
    "minus": '<path d="M5 12h14"/>',
    "hash": '<path d="M4 9h16M4 15h16M10 3 8 21M16 3l-2 18"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/>',
    "tag": '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><circle cx="7" cy="7" r="1"/>',
    "alert": '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "flask": '<path d="M10 2v7.5L4 20a1 1 0 0 0 .9 1.5h14.2a1 1 0 0 0 .9-1.5L14 9.5V2"/><path d="M8.5 2h7"/>',
    "ruler": '<path d="M3 17 17 3l4 4L7 21z"/><path d="m7 13 2 2M10 10l2 2M13 7l2 2"/>',
    "binary": '<path d="M10 3H6v6h4zM18 15h-4v6h4zM14 3v6M6 15v6M18 3v6"/>',
}

LOGO_SVG = """
<svg width="{s}" height="{s}" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M32 4 8 13v17c0 15 10.2 26.4 24 30 13.8-3.6 24-15 24-30V13L32 4Z" fill="{fill}" fill-opacity="{fo}" stroke="{stroke}" stroke-width="3" stroke-linejoin="round"/>
  <path d="M21 32.5 29 40.5 44 24" stroke="{stroke}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

RADAR = """
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22d3ee" stop-opacity="0"/><stop offset="1" stop-color="#22d3ee" stop-opacity=".55"/></linearGradient></defs>
  <circle cx="120" cy="120" r="108" fill="rgba(2,12,40,.45)" stroke="rgba(103,232,249,.45)" stroke-width="1.5"/>
  <circle cx="120" cy="120" r="76" fill="none" stroke="rgba(103,232,249,.3)" stroke-width="1"/>
  <circle cx="120" cy="120" r="44" fill="none" stroke="rgba(103,232,249,.3)" stroke-width="1"/>
  <line x1="12" y1="120" x2="228" y2="120" stroke="rgba(103,232,249,.25)"/>
  <line x1="120" y1="12" x2="120" y2="228" stroke="rgba(103,232,249,.25)"/>
  <g class="sweep"><path d="M120 120 L120 12 A108 108 0 0 1 196 44 Z" fill="url(#sw)"/></g>
  <circle cx="176" cy="70" r="5" fill="#f87171"/><circle class="blip" cx="176" cy="70" r="5" fill="#f87171"/>
  <circle cx="72" cy="160" r="5" fill="#f87171"/><circle class="blip" cx="72" cy="160" r="5" fill="#f87171" style="animation-delay:.8s"/>
  <circle cx="160" cy="168" r="4" fill="#34d399"/><circle cx="88" cy="82" r="4" fill="#34d399"/>
  <path d="M120 100 100 108v13c0 11 7.6 19.8 20 22.5 12.4-2.7 20-11.5 20-22.5v-13L120 100Z" fill="rgba(255,255,255,.18)" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M111 121l6 6 12-12" stroke="#fff" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


def html(s: str) -> None:
    """Render HTML tanpa risiko jadi code-block akibat indentasi/baris kosong."""
    st.markdown("\n".join(l.strip() for l in s.splitlines() if l.strip()), unsafe_allow_html=True)


def esc(x) -> str:
    return _html.escape(str(x))


def icon(name: str, size: int = 20) -> str:
    return (f'<span class="ic" style="width:{size}px;height:{size}px"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS.get(name, "")}</svg></span>')


def logo(size=40, light=True) -> str:
    return LOGO_SVG.format(s=size, fill="#fff" if light else "#1d4ed8",
                           fo=".18" if light else ".12", stroke="#fff" if light else "#1d4ed8")


def page_header(ic: str, title: str, caption: str) -> None:
    html(f'<div class="pg-pagehead"><div class="ico">{icon(ic, 22)}</div><h2>{title}</h2></div>')
    st.caption(caption)
    st.write("")


def section(eyebrow: str, title: str, sub: str = "") -> None:
    sp = f'<div class="sp">{sub}</div>' if sub else ""
    html(f'<div class="sec"><div class="eyebrow">{eyebrow}</div><div class="sh">{title}</div>{sp}</div>')


def card_head(ic: str, title: str, tag: str = "") -> None:
    t = f'<span class="ch-tag">{tag}</span>' if tag else ""
    html(f'<div class="ch"><span class="ch-ic">{icon(ic, 17)}</span><span class="ch-t">{title}</span>{t}</div>')


def chip(text: str, kind: str = "ok") -> str:
    return f'<span class="chip {kind}">{text}</span>'


def val(x) -> str:
    return f'<span class="info-v">{x}</span>'


def info_rows(rows) -> None:
    html("".join(f'<div class="info-row"><span class="info-k">{k}</span>{v}</div>' for k, v in rows))


# ---------- Navbar ----------
def brand() -> None:
    html(f"""
    <div class="nav-brand">{logo(34, light=False)}
      <div><div class="n">PhishGuard</div><div class="t">URL THREAT DETECTION</div></div>
    </div>
    """)


def status_pill(ready: bool) -> None:
    html(f'<div class="status-pill {"" if ready else "off"}"><i></i>{"Engine aktif" if ready else "Model gagal dimuat"}</div>')


def footer() -> None:
    html('<div class="foot">PhishGuard · Keamanan Informasi · Universitas Siliwangi — analisis berbasis teks URL, tanpa mengunjungi situs target.</div>')


# ---------- Beranda ----------
def hero() -> None:
    html(f"""
    <div class="hero">
      <div class="hero-main">
        <div class="hero-badge"><span class="dot"></span> DEFENSIVE AI · KEAMANAN INFORMASI</div>
        <h1>Deteksi tautan phishing <span class="hl">sebelum Anda mengkliknya.</span></h1>
        <p><strong>PhishGuard</strong> adalah aplikasi web berbasis <em>Machine Learning (Random Forest)</em> yang menganalisis
        struktur dan karakteristik teks URL secara instan, aman, dan tanpa membuka situs tujuan.</p>
        <div class="hero-meta"><span>Random Forest</span><span>16 Fitur Leksikal</span><span>Zero-Visit</span></div>
      </div>
      <div class="hero-art">
        {RADAR}
        <div class="fchip c1"><i></i>paypal-secure.xyz → PHISHING</div>
        <div class="fchip c2"><i></i>unsil.ac.id → LEGITIMATE</div>
      </div>
    </div>
    """)


def ticker() -> None:
    items = [
        ("bad", "http://117.205.108.72/bin.sh"), ("ok", "https://www.google.com"),
        ("bad", "paypal-secure-login.xyz/verify.exe"), ("ok", "https://unsil.ac.id"),
        ("bad", "bca-klikbca-verifikasi.top/login"), ("ok", "https://www.wikipedia.org"),
        ("bad", "http://free-gift-claim.click/a8f3k2"), ("ok", "https://github.com"),
    ]
    chips = "".join(f'<span class="tk {k}"><i></i>{esc(t)}</span>' for k, t in items)
    html(f'<div class="ticker"><div class="ticker-track">{chips}{chips}</div></div>')
    st.caption("Ilustrasi contoh URL yang dianalisis. Bukan hasil prediksi aktual.")


def stat_strip(items) -> None:
    html('<div class="grid4">' + "".join(
        f'<div class="stat"><div class="ic-box">{icon(i, 20)}</div><div><div class="v">{v}</div><div class="l">{l}</div></div></div>'
        for i, v, l in items) + "</div>")


def cards(items, cols=3) -> None:
    html(f'<div class="grid{cols}">' + "".join(
        f'<div class="fcard"><div class="ico">{icon(i, 20)}</div><div class="t">{t}</div><div class="d">{d}</div></div>'
        for i, t, d in items) + "</div>")


def steps(items) -> None:
    html('<div class="grid3">' + "".join(
        f'<div class="step"><div class="n">LANGKAH {n}</div><div class="t">{t}</div><div class="d">{d}</div></div>'
        for n, t, d in items) + "</div>")


def checklist(items) -> None:
    html("".join(f'<div class="check"><div class="b">{icon("check", 13)}</div><div><div class="t">{t}</div><div class="d">{d}</div></div></div>'
                 for t, d in items))


def cta_text(title: str, desc: str) -> None:
    html(f'<div class="cta-t">{title}</div><div class="cta-d">{desc}</div>')


def url_anatomy_static() -> None:
    html("""
    <div class="pg-url">
      <span class="seg bad">http://</span><span class="seg warn">paypal-secure-login</span><span class="seg ok">.</span><span class="seg warn">xyz</span><span class="seg ok">/</span><span class="seg bad">verify.exe</span>
    </div>
    <div class="legend"><span><i style="background:var(--danger)"></i>Berbahaya</span><span><i style="background:var(--warn)"></i>Mencurigakan</span><span><i style="background:var(--muted)"></i>Netral</span></div>
    """)
    st.caption("Contoh ilustrasi: tanpa HTTPS, banyak tanda hubung, TLD tidak umum, dan ekstensi file berbahaya. Bukan hasil prediksi aktual.")


# ---------- Hasil deteksi ----------
def gauge(p: dict, score: float, is_phish: bool) -> str:
    color = p["danger"] if is_phish else p["safe"]
    pct = max(0.0, min(score, 10.0)) * 10
    return f"""
    <svg viewBox="0 0 200 125" xmlns="http://www.w3.org/2000/svg">
      <path d="M20 105 A80 80 0 0 1 180 105" pathLength="100" fill="none" stroke="{p['track']}" stroke-width="14" stroke-linecap="round"/>
      <path class="g-fill" d="M20 105 A80 80 0 0 1 180 105" pathLength="100" fill="none" stroke="{color}" stroke-width="14" stroke-linecap="round" stroke-dasharray="{pct:.1f} 100"/>
      <text x="100" y="92" text-anchor="middle" font-size="36" font-weight="800" fill="{p['text']}" font-family="JetBrains Mono, monospace">{score}</text>
      <text x="100" y="112" text-anchor="middle" font-size="10" font-weight="700" fill="{p['muted']}">SAFETY SCORE / 10</text>
    </svg>"""


def verdict(p: dict, is_phish: bool, url: str, score: float) -> None:
    if is_phish:
        kind, ic, title, sub = "danger", "alert", "PHISHING", "Terindikasi"
        desc = "URL diprediksi memiliki karakteristik phishing. Pola struktur dan karakternya menyerupai tautan penipuan berdasarkan model Random Forest."
    else:
        kind, ic, title, sub = "safe", "shield", "LEGITIMATE", "Tidak terindikasi"
        desc = "URL diprediksi sebagai legitimate oleh model. Struktur leksikalnya konsisten dengan situs sah, namun tetap waspada."
    html(f"""
    <div class="verdict {kind}">
      <div class="v-ic">{icon(ic, 28)}</div>
      <div>
        <div class="v-tag">HASIL DETEKSI</div>
        <div class="v-title">{title}</div>
        <div class="v-sub">{sub}</div>
        <div class="v-url"><strong>URL:</strong> {esc(url)}</div>
        <div class="v-desc">{desc}</div>
      </div>
      <div class="v-gauge">{gauge(p, score, is_phish)}</div>
    </div>
    """)


def kpis(p: dict, prob: float, conf: float, score: float, is_phish: bool) -> None:
    color = p["danger"] if is_phish else p["safe"]
    html(f"""
    <div class="grid3" style="margin-bottom:1rem;">
      <div class="mcard"><div class="l">SAFETY SCORE</div><div class="v">{score} <span style="font-size:.9rem;color:{p['muted']}">/ 10</span></div>
        <div class="n">Semakin tinggi semakin aman</div></div>
      <div class="mcard"><div class="l">PROBABILITAS PHISHING</div><div class="v">{prob*100:.2f}%</div>
        <div class="pbar"><div style="width:{prob*100:.1f}%;background:{color};"></div></div></div>
      <div class="mcard"><div class="l">CONFIDENCE MODEL</div><div class="v">{conf*100:.2f}%</div>
        <div class="pbar"><div style="width:{conf*100:.1f}%;background:{p['accent']};"></div></div></div>
    </div>
    """)


def pipeline() -> None:
    steps_ = [("Input URL", "Divalidasi"), ("Ekstraksi", "16 fitur leksikal"), ("Random Forest", "100 pohon keputusan"), ("Verdict", "Skor & rekomendasi")]
    parts = []
    for i, (t, s) in enumerate(steps_):
        parts.append(f'<div class="pstep"><span class="ck">{icon("check", 13)}</span><div>{t}<small>{s}</small></div></div>')
        if i < len(steps_) - 1:
            parts.append('<span class="parrow">›</span>')
    html('<div class="pipe">' + "".join(parts) + "</div>")


def url_anatomy_live(url: str, f: dict) -> None:
    try:
        u = urlsplit(url if "://" in url else "//" + url)
    except ValueError:
        html(f'<div class="pg-url">{esc(url)}</div>')
        return
    segs = []
    if u.scheme:
        segs.append((f"{u.scheme}://", "good" if u.scheme == "https" else "bad"))
    host_kind = "bad" if f.get("has_ip_address") else ("warn" if (f.get("has_hyphen_in_domain") or not f.get("tld_popularity")) else "ok")
    segs.append((u.netloc, host_kind))
    if u.path:
        segs.append((u.path, "bad" if f.get("suspicious_file_extension") else "ok"))
    if u.query:
        segs.append(("?" + u.query, "ok"))
    if u.fragment:
        segs.append(("#" + u.fragment, "ok"))
    body = "".join(f'<span class="seg {k}">{esc(t)}</span>' for t, k in segs)
    html(f"""
    <div class="pg-url">{body}</div>
    <div class="legend"><span><i style="background:var(--danger)"></i>Berbahaya</span><span><i style="background:var(--warn)"></i>Mencurigakan</span>
    <span><i style="background:var(--safe)"></i>Aman</span><span><i style="background:var(--muted)"></i>Netral</span></div>
    """)


def build_reasons(f: dict):
    """Sinyal heuristik dari fitur ekstraksi (penjelasan pendukung; keputusan tetap dari model)."""
    r = []
    if f["has_ip_address"]:
        r.append(("danger", "globe", "URL memakai <b>alamat IP langsung</b> alih-alih nama domain."))
    if f["suspicious_file_extension"]:
        r.append(("danger", "file", "Terdapat <b>ekstensi file berisiko</b> (mis. .exe, .sh, .apk)."))
    if not f["https_flag"]:
        r.append(("warn", "unlock", "Tidak memakai <b>HTTPS</b>, data rentan disadap."))
    if f["has_hyphen_in_domain"]:
        r.append(("warn", "minus", "Domain mengandung <b>tanda hubung (-)</b>, pola umum peniruan merek."))
    if not f["tld_popularity"]:
        r.append(("warn", "tag", "<b>TLD tidak umum</b> / jarang dipakai situs resmi."))
    if f["subdomain_count"] >= 3:
        r.append(("warn", "layers", f"Subdomain berlebih (<b>{f['subdomain_count']}</b> level)."))
    if f["url_entropy"] > 4.5:
        r.append(("warn", "hash", f"Entropi karakter tinggi (<b>{f['url_entropy']:.2f}</b>), indikasi string acak."))
    if f["url_length"] > 75:
        r.append(("warn", "ruler", f"URL sangat panjang (<b>{f['url_length']}</b> karakter)."))
    if f["percentage_numeric_chars"] > 20:
        r.append(("warn", "binary", f"Proporsi angka tinggi (<b>{f['percentage_numeric_chars']:.1f}%</b>)."))
    if not r:
        r.append(("ok", "check", "Tidak ada sinyal struktural mencurigakan yang menonjol."))
    return r


def reasons(f: dict) -> None:
    html("".join(f'<div class="reason {lvl}"><span class="ri">{icon(ic, 17)}</span><span>{txt}</span></div>'
                 for lvl, ic, txt in build_reasons(f)))


def structure_chart(p: dict, f: dict, is_phish: bool):
    df = pd.DataFrame({
        "Parameter": ["Panjang URL", "Panjang Domain", "Panjang Path", "Jumlah Angka", "Jumlah Token", "Jumlah Titik"],
        "Nilai": [f["url_length"], f["domain_name_length"], f["path_length"],
                  f["number_of_digits"], f["token_count"], f["dot_count"]],
    })
    return (
        alt.Chart(df)
        .mark_bar(cornerRadiusEnd=5, color=p["danger"] if is_phish else p["accent"])
        .encode(
            x=alt.X("Nilai:Q", title=None, axis=alt.Axis(labelColor=p["muted"], gridColor=p["border"], domain=False)),
            y=alt.Y("Parameter:N", sort="-x", title=None, axis=alt.Axis(labelColor=p["text"], domain=False, ticks=False)),
            tooltip=["Parameter", "Nilai"],
        )
        .properties(height=200, background=p["chart_bg"])
        .configure_view(strokeWidth=0)
    )


FEATURE_LABELS = [
    ("url_length", "PANJANG URL"), ("domain_name_length", "PANJANG DOMAIN"), ("path_length", "PANJANG PATH"),
    ("tld_length", "PANJANG TLD"), ("token_count", "JUMLAH TOKEN"), ("dot_count", "JUMLAH TITIK"),
    ("subdomain_count", "SUBDOMAIN"), ("query_param_count", "QUERY PARAMS"), ("number_of_digits", "JUMLAH ANGKA"),
    ("percentage_numeric_chars", "RASIO ANGKA (%)"), ("url_entropy", "ENTROPI URL"), ("https_flag", "HTTPS"),
    ("has_ip_address", "IP LANGSUNG"), ("suspicious_file_extension", "EKSTENSI RISIKO"),
    ("has_hyphen_in_domain", "HYPHEN DOMAIN"), ("tld_popularity", "TLD POPULER"),
]


def feature_tiles(f: dict) -> None:
    def fmt(v):
        if isinstance(v, bool):
            return "Ya" if v else "Tidak"
        if isinstance(v, float):
            return f"{v:.3f}"
        return str(v)
    html('<div class="grid4">' + "".join(
        f'<div class="ftile"><div class="k">{lbl}</div><div class="v">{fmt(f.get(k, "-"))}</div></div>'
        for k, lbl in FEATURE_LABELS) + "</div>")


def disclaimer(text: str) -> None:
    html(f"""
    <div class="disclaimer"><strong>Catatan Penafian Keamanan:</strong><br>{esc(text)}
    Hasil merupakan prediksi model Machine Learning berdasarkan teks URL dan bukan jaminan mutlak
    bahwa suatu situs 100% aman atau berbahaya.</div>
    """)


# ---------- Evaluasi & Log ----------
def metric_grid(items) -> None:
    html('<div class="grid4">' + "".join(
        f'<div class="mcard"><div class="l">{l}</div><div class="v">{v}</div>'
        f'<div class="bar"><div style="width:{pct}%"></div></div><div class="n">{n}</div></div>'
        for l, v, pct, n in items) + "</div>")


def confusion_grid(tn, fp, fn, tp) -> None:
    html(f"""
    <div class="cm">
      <div></div><div class="h">Prediksi<br>Legitimate</div><div class="h">Prediksi<br>Phishing</div>
      <div class="h">Aktual<br>Legitimate</div>
      <div class="c good">{tn:,}<small>True Negative</small></div>
      <div class="c miss">{fp:,}<small>False Positive</small></div>
      <div class="h">Aktual<br>Phishing</div>
      <div class="c miss">{fn:,}<small>False Negative</small></div>
      <div class="c good">{tp:,}<small>True Positive</small></div>
    </div>
    """)


def split_bar(p: dict, phish: int, legit: int, err: int) -> None:
    total = max(phish + legit + err, 1)
    html(f"""
    <div class="sbar">
      <div style="width:{phish/total*100:.1f}%;background:{p['danger']}"></div>
      <div style="width:{legit/total*100:.1f}%;background:{p['safe']}"></div>
      <div style="width:{err/total*100:.1f}%;background:{p['warn']}"></div>
    </div>
    <div class="legend"><span><i style="background:{p['danger']}"></i>Phishing {phish}</span>
    <span><i style="background:{p['safe']}"></i>Legitimate {legit}</span><span><i style="background:{p['warn']}"></i>Error {err}</span></div>
    """)