"""Palet warna & CSS global PhishGuard. Nuansa Biru Elegan & Sinkron 100% dengan menu ⋮ -> Light / Dark."""
import streamlit as st

LIGHT = {
    "bg": "#eef4fc", "side": "#f7faff", "card": "#ffffff", "input": "#f0f5fc", "border": "#d4e1f5",
    "text": "#0b1936", "muted": "#4b6085", "accent": "#1d4ed8", "accent2": "#0284c7",
    "soft": "rgba(29,78,216,.09)", "shadow": "rgba(11,25,54,.06)",
    "danger": "#dc2626", "danger-bg": "#fef2f2", "danger-bd": "#fecaca",
    "safe": "#059669", "safe-bg": "#ecfdf5", "safe-bd": "#a7f3d0",
    "warn": "#d97706", "warn-bg": "#fffbeb",
    "chip-ok-bg": "#dcfce7", "chip-ok-fg": "#15803d",
    "chip-bad-bg": "#fee2e2", "chip-bad-fg": "#b91c1c",
    "chip-warn-bg": "#fef3c7", "chip-warn-fg": "#b45309",
    "chart-bg": "#ffffff", "track": "#dce7f7",
}
DARK = {
    "bg": "#081229", "side": "#0b1736", "card": "#0f2044", "input": "#091530", "border": "#1e3768",
    "text": "#eaf2ff", "muted": "#93afd9", "accent": "#38bdf8", "accent2": "#22d3ee",
    "soft": "rgba(56,189,248,.14)", "shadow": "rgba(2,8,23,.45)",
    "danger": "#f87171", "danger-bg": "rgba(239,68,68,.15)", "danger-bd": "#7f1d1d",
    "safe": "#34d399", "safe-bg": "rgba(16,185,129,.15)", "safe-bd": "#065f46",
    "warn": "#fbbf24", "warn-bg": "rgba(245,158,11,.14)",
    "chip-ok-bg": "rgba(16,185,129,.2)", "chip-ok-fg": "#34d399",
    "chip-bad-bg": "rgba(239,68,68,.2)", "chip-bad-fg": "#f87171",
    "chip-warn-bg": "rgba(245,158,11,.2)", "chip-warn-fg": "#fbbf24",
    "chart-bg": "#0f2044", "track": "#1e3768",
}


def is_dark() -> bool:
    try:
        return st.context.theme.type == "dark"
    except Exception:
        try:
            return st.get_option("theme.base") == "dark"
        except Exception:
            return False


def get_palette(dark: bool) -> dict:
    return DARK if dark else LIGHT


_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap');

/* ---------- Base ---------- */
.stApp, [data-testid="stAppViewContainer"] { background:var(--bg) !important; color:var(--text) !important; font-family:'Inter',sans-serif !important; }
[data-testid="stHeader"] { background:transparent !important; }
[data-testid="stDecoration"] { display:none; }
.block-container { max-width:1180px !important; padding-top:3.6rem !important; padding-bottom:3rem !important; }

/* Batasi pewarnaan heading & paragraf hanya di dalam .stApp agar tidak bocor ke dialog/modal sistem (Deploy/Settings) */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
  font-family:'Inter',sans-serif !important; color:var(--text) !important; letter-spacing:-.02em; font-weight:700;
}
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li,
.stApp label p { color:var(--text); }
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stCaptionContainer"] p { color:var(--muted) !important; }

[data-testid="stSidebar"] { background:var(--side) !important; border-right:1px solid var(--border) !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:var(--text); }

/* ---------- Navbar atas ---------- */
.st-key-topnav { background:var(--card); border:1px solid var(--border); border-radius:14px; padding:.5rem .9rem; margin-bottom:1.5rem; box-shadow:0 4px 14px var(--shadow); }
.st-key-topnav [data-testid="stHorizontalBlock"] { align-items:center; gap:.2rem; }
.st-key-topnav button { background:transparent !important; border:none !important; box-shadow:none !important; border-radius:9px !important;
  min-height:2.5rem !important; color:var(--muted) !important; font-weight:600 !important; transform:none !important; filter:none !important; }
.st-key-topnav button p { color:inherit !important; font-size:.88rem !important; font-weight:600 !important; }
.st-key-topnav button:hover { background:var(--soft) !important; color:var(--text) !important; }
.st-key-topnav [data-testid="stBaseButton-primary"] { background:var(--soft) !important; color:var(--accent) !important; box-shadow:inset 0 -2px 0 var(--accent) !important; border-radius:9px 9px 4px 4px !important; }
.st-key-topnav [data-testid="stBaseButton-primary"]:hover { color:var(--accent) !important; }
.nav-brand { display:flex; align-items:center; gap:.6rem; }
.nav-brand .n { font-weight:800; font-size:1.12rem; letter-spacing:-.02em; color:var(--text); line-height:1.1; }
.nav-brand .t { font-size:.62rem; color:var(--muted); font-weight:600; letter-spacing:.1em; }
.status-pill { display:flex; align-items:center; justify-content:flex-end; gap:.45rem; font-size:.76rem; font-weight:600; color:var(--muted); white-space:nowrap; }
.status-pill i { width:8px; height:8px; border-radius:50%; background:var(--safe); box-shadow:0 0 0 3px var(--safe-bg); }
.status-pill.off i { background:var(--danger); box-shadow:0 0 0 3px var(--danger-bg); }

/* ---------- Ikon ---------- */
.ic { display:inline-flex; flex:none; }
.ic svg { width:100%; height:100%; }

/* ---------- Cards ---------- */
.stApp [data-testid="stVerticalBlockBorderWrapper"] { background:var(--card) !important; border:1px solid var(--border) !important; border-radius:16px !important; box-shadow:0 4px 14px var(--shadow) !important; transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease; }
.stApp [data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: var(--accent) !important; }
.stApp [data-testid="stForm"] { border:none !important; padding:0 !important; background:transparent !important; }
.stApp [data-testid="stExpander"] { border:1px solid var(--border) !important; border-radius:14px !important; background:var(--card) !important; }
.ch { display:flex; align-items:center; gap:.6rem; margin-bottom:.85rem; }
.ch-ic { width:32px; height:32px; border-radius:9px; background:var(--soft); color:var(--accent); display:grid; place-items:center; }
.ch-ic .ic { width:17px; height:17px; }
.ch-t { font-weight:700; font-size:.98rem; color:var(--text); }
.ch-tag { margin-left:auto; font-family:'JetBrains Mono',monospace; font-size:.66rem; font-weight:700; letter-spacing:.06em; color:var(--muted); border:1px solid var(--border); border-radius:6px; padding:.18rem .5rem; }

/* ---------- Input ---------- */
.stApp .stTextInput input, .stApp .stTextArea textarea, .stApp div[data-baseweb="select"] > div { background:var(--input) !important; color:var(--text) !important;
  border:1px solid var(--border) !important; border-radius:10px !important; font-family:'JetBrains Mono',monospace !important; font-size:.88rem !important; }
.stApp .stTextInput input { height:2.9rem; }
.stApp .stTextInput input:focus, .stApp .stTextArea textarea:focus { border-color:var(--accent) !important; box-shadow:0 0 0 3px var(--soft) !important; }
ul[data-baseweb="menu"] { background:var(--card) !important; border:1px solid var(--border) !important; }
ul[data-baseweb="menu"] li { color:var(--text) !important; }

/* ---------- Tombol ---------- */
.stApp [data-testid="stBaseButton-primary"], .stApp [data-testid="stBaseButton-primaryFormSubmit"] {
  background:var(--accent) !important; color:#fff !important; border:none !important; border-radius:10px !important; font-weight:600 !important;
  min-height:2.9rem !important; box-shadow:0 4px 12px var(--shadow) !important; transition:all .15s ease !important; }
.stApp [data-testid="stBaseButton-primary"]:hover, .stApp [data-testid="stBaseButton-primaryFormSubmit"]:hover { filter:brightness(1.1); transform:translateY(-1px); }
.stApp [data-testid="stBaseButton-primary"] p, .stApp [data-testid="stBaseButton-primaryFormSubmit"] p { color:#fff !important; }
.stApp [data-testid="stBaseButton-secondary"], .stApp [data-testid="stBaseButton-secondaryFormSubmit"], .stApp .stDownloadButton > button {
  background:var(--card) !important; color:var(--text) !important; border:1px solid var(--border) !important; border-radius:10px !important; font-weight:600 !important; min-height:2.6rem; }
.stApp [data-testid="stBaseButton-secondary"]:hover, .stApp .stDownloadButton > button:hover { border-color:var(--accent) !important; color:var(--accent) !important; }
.stApp [data-testid="stBaseButton-secondary"] p, .stApp .stDownloadButton p { color:inherit !important; }

/* ---------- Tabs ---------- */
.stApp .stTabs [data-baseweb="tab-list"] { gap:4px; border-bottom:1px solid var(--border); }
.stApp .stTabs [data-baseweb="tab"] { border-radius:8px 8px 0 0; font-weight:600; }
.stApp .stTabs [data-baseweb="tab"] p { color:var(--muted); }
.stApp .stTabs [aria-selected="true"] p { color:var(--accent) !important; }

[data-testid="stMetricValue"] { font-family:'JetBrains Mono',monospace !important; font-weight:800 !important; color:var(--text) !important; }
[data-testid="stMetricLabel"] p { color:var(--muted) !important; font-weight:600 !important; }

/* ---------- Animasi ---------- */
@keyframes spin { to { transform:rotate(360deg); } }
@keyframes pulse { 0%{transform:scale(1);opacity:1} 70%{transform:scale(2.4);opacity:0} 100%{opacity:0} }
@keyframes floaty { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
@keyframes fadeup { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:none} }
@keyframes draw { from { stroke-dasharray:0 100; } }
@keyframes blink { 50% { opacity:.25; } }
@keyframes marquee { to { transform:translateX(-50%); } }

/* ---------- Hero ---------- */
.hero { position:relative; overflow:hidden; border-radius:22px; padding:2.7rem 2.7rem; margin-bottom:1.2rem; display:grid; grid-template-columns:1.3fr .9fr; gap:1.5rem; align-items:center; animation:fadeup .5s ease;
  background:radial-gradient(800px 340px at 100% -10%, rgba(56,189,248,.28), transparent 60%), linear-gradient(135deg,#0b1736 0%,#11295c 55%,#0b3f64 100%); box-shadow:0 16px 36px rgba(10,26,63,.25); border:1px solid rgba(56,189,248,.22); }
.hero::before { content:""; position:absolute; inset:0; opacity:.45; background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px); background-size:34px 34px; }
.hero * { color:#fff !important; position:relative; z-index:1; }
.hero-badge { display:inline-flex; align-items:center; gap:.5rem; background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.28); font-size:.7rem; font-weight:700; padding:.35rem .9rem; border-radius:999px; letter-spacing:.09em; margin-bottom:1rem; }
.hero-badge .dot { width:8px; height:8px; border-radius:50%; background:#34d399; animation:blink 1.4s infinite; }
.hero h1 { font-size:2.55rem; font-weight:800; line-height:1.12; margin:0 0 .9rem; padding:0; letter-spacing:-.03em; }
.hero .hl { color:#7dd3fc !important; }
.hero p { color:#cfe3ff !important; font-size:1rem; line-height:1.7; max-width:600px; margin:0 0 1.1rem; }
.hero-meta { display:flex; gap:.5rem; flex-wrap:wrap; }
.hero-meta span { background:rgba(255,255,255,.09); border:1px solid rgba(255,255,255,.2); padding:.3rem .8rem; border-radius:8px; font-size:.76rem; font-weight:600; }
.hero-art { position:relative; display:flex; justify-content:center; }
.hero-art svg { width:100%; max-width:300px; height:auto; }
.sweep { transform-origin:120px 120px; animation:spin 4.5s linear infinite; }
.blip { transform-origin:center; transform-box:fill-box; animation:pulse 2.2s infinite; }
.fchip { position:absolute; font-family:'JetBrains Mono',monospace; font-size:.68rem; font-weight:700; padding:.4rem .7rem; border-radius:8px; backdrop-filter:blur(6px); animation:floaty 4s ease-in-out infinite; white-space:nowrap; display:flex; align-items:center; gap:.4rem; }
.fchip i { width:7px; height:7px; border-radius:50%; display:inline-block; }
.fchip.c1 { top:6%; left:-4%; background:rgba(220,38,38,.28); border:1px solid rgba(248,113,113,.7); } .fchip.c1 i { background:#f87171; }
.fchip.c2 { bottom:8%; right:-2%; background:rgba(5,150,105,.28); border:1px solid rgba(52,211,153,.7); animation-delay:1.3s; } .fchip.c2 i { background:#34d399; }

/* ---------- Ticker ---------- */
.ticker { overflow:hidden; border:1px solid var(--border); border-radius:12px; background:var(--card); padding:.6rem 0; margin:0 0 1.2rem;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent); mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent); }
.ticker-track { display:flex; gap:.6rem; width:max-content; animation:marquee 40s linear infinite; }
.ticker:hover .ticker-track { animation-play-state:paused; }
.tk { display:flex; align-items:center; gap:.45rem; font-family:'JetBrains Mono',monospace; font-size:.74rem; font-weight:600; padding:.3rem .75rem; border-radius:8px; white-space:nowrap; }
.tk i { width:7px; height:7px; border-radius:50%; }
.tk.bad { background:var(--chip-bad-bg); color:var(--chip-bad-fg); } .tk.bad i { background:var(--danger); }
.tk.ok { background:var(--chip-ok-bg); color:var(--chip-ok-fg); } .tk.ok i { background:var(--safe); }

/* ---------- Section & page header ---------- */
.sec { margin:2.2rem 0 1rem; animation:fadeup .4s ease; }
.eyebrow { font-family:'JetBrains Mono',monospace; font-size:.68rem; font-weight:700; letter-spacing:.14em; color:var(--accent); margin-bottom:.3rem; }
.sh { font-weight:800; font-size:1.55rem; letter-spacing:-.025em; color:var(--text); line-height:1.2; }
.sp { color:var(--muted); font-size:.92rem; margin-top:.3rem; max-width:680px; line-height:1.6; }
.pg-pagehead { display:flex; align-items:center; gap:.85rem; margin-bottom:.2rem; animation:fadeup .35s ease; }
.pg-pagehead .ico { width:44px; height:44px; border-radius:12px; display:grid; place-items:center; background:var(--soft); color:var(--accent); }
.pg-pagehead .ico .ic { width:22px; height:22px; }
.pg-pagehead h2 { margin:0; padding:0; font-weight:800; font-size:1.7rem; }

/* ---------- Grid & kartu ---------- */
.grid2 { display:grid; grid-template-columns:repeat(2,1fr); gap:1rem; }
.grid3 { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; }
.grid4 { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; }
@media (max-width:860px) { .grid3,.grid4 { grid-template-columns:1fr 1fr; } .hero { grid-template-columns:1fr; } .hero-art { display:none; } .hero h1 { font-size:2rem; } }
@media (max-width:560px) { .grid2,.grid3,.grid4 { grid-template-columns:1fr; } }

.fcard { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:1.3rem; height:100%; box-shadow:0 4px 14px var(--shadow); transition:border-color .15s ease, box-shadow .15s ease; }
.fcard:hover { border-color:var(--accent); box-shadow:0 8px 22px var(--shadow); }
.fcard .ico { width:40px; height:40px; border-radius:10px; display:grid; place-items:center; background:var(--soft); color:var(--accent); margin-bottom:.8rem; }
.fcard .ico .ic { width:20px; height:20px; }
.fcard .t { font-weight:700; font-size:1rem; color:var(--text); margin-bottom:.3rem; }
.fcard .d { color:var(--muted); font-size:.86rem; line-height:1.6; }
.fcard .d code { background:var(--soft); color:var(--accent); padding:.05rem .35rem; border-radius:5px; font-size:.8rem; }

.stat { display:flex; align-items:center; gap:.9rem; background:var(--card); border:1px solid var(--border); border-radius:16px; padding:1rem 1.1rem; box-shadow:0 4px 14px var(--shadow); }
.stat .ic-box { width:42px; height:42px; flex:none; border-radius:10px; display:grid; place-items:center; background:var(--soft); color:var(--accent); }
.stat .ic-box .ic { width:20px; height:20px; }
.stat .v { font-family:'JetBrains Mono',monospace; font-weight:800; font-size:1.45rem; line-height:1.1; color:var(--text); }
.stat .l { font-size:.76rem; color:var(--muted); font-weight:600; margin-top:.1rem; }

.step { position:relative; background:var(--card); border:1px solid var(--border); border-radius:16px; padding:1.3rem; box-shadow:0 4px 14px var(--shadow); height:100%; transition: transform 0.18s ease, border-color 0.18s ease; }
.step:hover { transform: translateY(-3px); border-color: var(--accent); }
.step:not(:last-child)::after { content:""; position:absolute; right:-.9rem; top:50%; width:.8rem; height:2px; background:var(--border); }
.step .n { font-family:'JetBrains Mono',monospace; font-weight:800; font-size:.8rem; color:var(--accent); background:var(--soft); display:inline-block; padding:.2rem .6rem; border-radius:6px; margin-bottom:.7rem; }
.step .t { font-weight:700; color:var(--text); margin-bottom:.25rem; }
.step .d { color:var(--muted); font-size:.86rem; line-height:1.55; }
@media (max-width:860px) { .step::after { display:none; } }

.mcard { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:1.1rem 1.2rem; box-shadow:0 4px 14px var(--shadow); transition: transform 0.18s ease, border-color 0.18s ease; }
.mcard:hover { transform: translateY(-2px); border-color: var(--accent); }
.mcard .l { font-size:.72rem; color:var(--muted); font-weight:700; letter-spacing:.06em; }
.mcard .v { font-family:'JetBrains Mono',monospace; font-weight:800; font-size:1.65rem; color:var(--text); margin:.2rem 0 .5rem; }
.mcard .bar { height:6px; border-radius:999px; background:var(--track); overflow:hidden; }
.mcard .bar > div { height:100%; border-radius:999px; background:var(--accent); }
.mcard .n { font-size:.74rem; color:var(--muted); margin-top:.4rem; }

/* ---------- CTA ---------- */
.st-key-cta { background:linear-gradient(135deg,#0b1736,#11295c); border-radius:18px; padding:1.5rem 1.8rem; margin-top:2.2rem; box-shadow:0 12px 30px rgba(10,26,63,.22); }
.st-key-cta [data-testid="stHorizontalBlock"] { align-items:center; }
.cta-t { font-weight:800; font-size:1.35rem; letter-spacing:-.02em; color:#fff; }
.cta-d { color:#bcd3f5; font-size:.9rem; margin-top:.2rem; }
.st-key-cta [data-testid="stBaseButton-primary"] { background:#fff !important; box-shadow:none !important; }
.st-key-cta [data-testid="stBaseButton-primary"] p { color:#0b1736 !important; }
.st-key-cta [data-testid="stBaseButton-secondary"] { background:transparent !important; border:1px solid rgba(255,255,255,.35) !important; }
.st-key-cta [data-testid="stBaseButton-secondary"] p { color:#fff !important; }

/* ---------- Anatomi URL ---------- */
.pg-url { font-family:'JetBrains Mono',monospace; font-size:.9rem; background:var(--input); border:1px solid var(--border); border-radius:12px; padding:1rem 1.1rem; word-break:break-all; line-height:2.1; }
.seg { padding:.12rem .35rem; border-radius:5px; font-weight:700; }
.seg.bad { background:var(--danger-bg); color:var(--danger); } .seg.warn { background:var(--warn-bg); color:var(--warn); }
.seg.ok { color:var(--muted); font-weight:500; } .seg.good { background:var(--safe-bg); color:var(--safe); }
.legend { display:flex; gap:1rem; flex-wrap:wrap; margin-top:.6rem; font-size:.74rem; color:var(--muted); font-weight:600; }
.legend i { display:inline-block; width:10px; height:10px; border-radius:3px; margin-right:.3rem; vertical-align:-1px; }

/* ---------- Verdict ---------- */
.verdict { border-radius:18px; padding:1.5rem 1.7rem; margin-bottom:1rem; display:grid; grid-template-columns:auto 1fr auto; gap:1.2rem; align-items:center; animation:fadeup .4s ease; }
.verdict.danger { background:var(--danger-bg); border:1px solid var(--danger-bd); border-left:6px solid var(--danger); }
.verdict.safe { background:var(--safe-bg); border:1px solid var(--safe-bd); border-left:6px solid var(--safe); }
.v-ic { width:56px; height:56px; border-radius:16px; display:grid; place-items:center; color:#fff; }
.v-ic .ic { width:28px; height:28px; }
.verdict.danger .v-ic { background:var(--danger); } .verdict.safe .v-ic { background:var(--safe); }
.v-tag { font-family:'JetBrains Mono',monospace; font-size:.68rem; font-weight:700; letter-spacing:.14em; color:var(--muted); }
.v-title { font-size:2rem; font-weight:800; letter-spacing:-.03em; line-height:1.1; margin:.2rem 0 .1rem; }
.verdict.danger .v-title { color:var(--danger); } .verdict.safe .v-title { color:var(--safe); }
.v-sub { font-weight:700; font-size:.98rem; color:var(--text); margin-bottom:.5rem; }
.v-url { font-family:'JetBrains Mono',monospace; font-size:.78rem; word-break:break-all; margin-bottom:.4rem; color:var(--muted); }
.v-desc { font-size:.9rem; line-height:1.6; color:var(--text); max-width:620px; }
.v-gauge svg { width:200px; height:auto; }
.g-fill { animation:draw 1s ease-out; }
@media (max-width:760px) { .verdict { grid-template-columns:1fr; } .v-gauge { text-align:center; } }

/* ---------- Pipeline ---------- */
.pipe { display:flex; align-items:center; gap:.5rem; margin:.2rem 0 1rem; flex-wrap:wrap; }
.pstep { flex:1; min-width:150px; display:flex; align-items:center; gap:.6rem; background:var(--card); border:1px solid var(--border); border-radius:12px; padding:.6rem .85rem; font-size:.8rem; font-weight:700; color:var(--text); }
.pstep .ck { width:24px; height:24px; border-radius:50%; background:var(--chip-ok-bg); color:var(--chip-ok-fg); display:grid; place-items:center; flex:none; }
.pstep .ck .ic { width:13px; height:13px; }
.pstep small { display:block; color:var(--muted); font-weight:500; font-size:.7rem; }
.parrow { color:var(--border); font-weight:800; }

/* ---------- Info rows, chip, alasan ---------- */
.info-row { display:flex; justify-content:space-between; align-items:center; padding:.6rem 0; border-bottom:1px solid var(--border); font-size:.86rem; gap:.6rem; }
.info-row:last-child { border-bottom:none; }
.info-k { color:var(--muted); font-weight:500; }
.info-v { font-family:'JetBrains Mono',monospace; font-weight:700; font-size:.82rem; color:var(--text); }
.chip { padding:.2rem .65rem; border-radius:6px; font-size:.72rem; font-weight:700; white-space:nowrap; }
.chip.ok { background:var(--chip-ok-bg); color:var(--chip-ok-fg); } .chip.bad { background:var(--chip-bad-bg); color:var(--chip-bad-fg); } .chip.warn { background:var(--chip-warn-bg); color:var(--chip-warn-fg); }
.reason { display:flex; gap:.7rem; align-items:flex-start; padding:.65rem .85rem; border-radius:10px; margin-bottom:.45rem; font-size:.86rem; line-height:1.5; color:var(--text); }
.reason .ri { flex:none; margin-top:.1rem; } .reason .ri .ic { width:17px; height:17px; }
.reason.danger { background:var(--danger-bg); } .reason.danger .ri { color:var(--danger); }
.reason.warn { background:var(--warn-bg); } .reason.warn .ri { color:var(--warn); }
.reason.ok { background:var(--safe-bg); } .reason.ok .ri { color:var(--safe); }

.pbar { height:7px; border-radius:999px; background:var(--track); overflow:hidden; margin:.35rem 0 .2rem; }
.pbar > div { height:100%; border-radius:999px; }
.ftile { background:var(--input); border:1px solid var(--border); border-radius:12px; padding:.7rem .85rem; }
.ftile .k { font-size:.68rem; color:var(--muted); font-weight:700; letter-spacing:.04em; }
.ftile .v { font-family:'JetBrains Mono',monospace; font-weight:800; font-size:1rem; color:var(--text); margin-top:.15rem; }

.cm { display:grid; grid-template-columns:auto 1fr 1fr; gap:6px; font-size:.82rem; align-items:stretch; }
.cm .h { color:var(--muted); font-weight:700; display:flex; align-items:center; justify-content:center; padding:.3rem; text-align:center; }
.cm .c { border-radius:12px; padding:1.1rem .6rem; text-align:center; font-family:'JetBrains Mono',monospace; font-weight:800; font-size:1.35rem; }
.cm .c small { display:block; font-family:'Inter'; font-weight:600; font-size:.7rem; opacity:.85; margin-top:.2rem; }
.cm .good { background:var(--safe-bg); color:var(--safe); } .cm .miss { background:var(--danger-bg); color:var(--danger); }
.sbar { display:flex; height:12px; border-radius:999px; overflow:hidden; background:var(--track); margin:.4rem 0 .3rem; }

.check { display:flex; gap:.8rem; align-items:flex-start; padding:.75rem 0; border-bottom:1px solid var(--border); }
.check:last-child { border-bottom:none; }
.check .b { width:24px; height:24px; flex:none; border-radius:7px; display:grid; place-items:center; background:var(--chip-ok-bg); color:var(--chip-ok-fg); }
.check .b .ic { width:13px; height:13px; }
.check .t { font-weight:700; color:var(--text); font-size:.92rem; } .check .d { color:var(--muted); font-size:.83rem; line-height:1.5; }

.disclaimer { background:var(--input); border:1px solid var(--border); border-left:4px solid var(--accent); border-radius:12px; padding:1rem 1.2rem; font-size:.82rem; color:var(--muted); line-height:1.65; margin-top:1rem; }
.disclaimer strong { color:var(--text); }
.foot { text-align:center; color:var(--muted); font-size:.75rem; margin-top:2.2rem; }
"""


def inject_css(p: dict) -> None:
    dynamic_vars = ";".join(
        f"--{k}:light-dark({LIGHT[k]},{DARK[k]})"
        for k in LIGHT
    )
    st.markdown(f"<style>:root{{{dynamic_vars}}}{_CSS}</style>", unsafe_allow_html=True)