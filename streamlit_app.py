"""
OpinIA — Inteligencia de reputación online para e-commerce español
App interactiva con diseño premium.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from PIL import Image
import os

st.set_page_config(page_title="OpinIA", page_icon="💬", layout="wide", initial_sidebar_state="expanded")

AZUL = "#5B9BD5"
AZUL_OSCURO = "#2E5F8A"
AZUL_DEEP = "#1a3a5c"
AZUL_CLARO = "#A8D1F0"
LAVANDA = "#B8A9D0"
ROSA = "#F2B5D4"
MELOCOTON = "#FFD4B8"
GRIS = "#7B8794"

HF_TOKEN = st.secrets.get("HF_TOKEN", None)
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def hf_query(model, payload):
    url = f"https://router.huggingface.co/hf-inference/models/{model}"
    try:
        r = requests.post(url, headers=HF_HEADERS, json=payload, timeout=120)
    except requests.exceptions.ReadTimeout:
        st.warning("⏳ El modelo está tardando en cargar. Espera 30 segundos y vuelve a pulsar.")
        return None
    except Exception:
        st.warning("⚠️ Error de conexión. Inténtalo de nuevo en unos segundos.")
        return None
    if r.status_code == 503:
        st.warning("⏳ El modelo se está iniciando en HuggingFace. Espera 20 segundos y vuelve a pulsar.")
        return None
    if r.status_code != 200:
        st.error(f"Error {r.status_code}")
        return None
    return r.json()

# ─── CSS PREMIUM ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600;700&display=swap');

    .main .block-container { padding-top: 1.5rem; max-width: 1100px; }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; font-weight: 700 !important; }

    /* Hero gradient title */
    .hero-title {
        font-family: 'DM Serif Display', serif !important;
        font-size: 3.2rem !important;
        background: linear-gradient(135deg, #2E5F8A 0%, #5B9BD5 50%, #B8A9D0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0 !important;
        line-height: 1.1 !important;
    }

    .hero-sub {
        font-size: 1.1rem;
        color: #7B8794;
        font-weight: 300;
        margin-top: 6px;
    }

    /* Glass cards */
    .glass-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,255,0.9) 100%);
        border-radius: 20px;
        padding: 28px;
        text-align: center;
        border: 1px solid rgba(91,155,213,0.12);
        box-shadow: 0 4px 24px rgba(46,95,138,0.06), 0 1px 4px rgba(0,0,0,0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(46,95,138,0.1), 0 2px 8px rgba(0,0,0,0.04);
    }

    .metric-big {
        font-family: 'DM Serif Display', serif;
        font-size: 2.6rem;
        line-height: 1.2;
        background: linear-gradient(135deg, #2E5F8A 0%, #5B9BD5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .metric-label {
        font-size: 0.82rem;
        color: #7B8794;
        margin-top: 6px;
        font-weight: 500;
        letter-spacing: 0.3px;
    }

    /* Section tag */
    .section-tag {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        color: white;
        text-transform: uppercase;
        letter-spacing: 3px;
        background: linear-gradient(135deg, #2E5F8A 0%, #5B9BD5 100%);
        padding: 6px 16px;
        border-radius: 20px;
        margin-bottom: 8px;
    }

    /* Result cards */
    .result-card {
        background: white;
        border-radius: 16px;
        padding: 20px 24px;
        border: 1px solid rgba(0,0,0,0.04);
        margin-bottom: 10px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.03);
    }

    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #f0f4ff 0%, #f8f0ff 100%);
        border-left: 4px solid #5B9BD5;
        padding: 16px 20px;
        border-radius: 0 14px 14px 0;
        margin: 12px 0;
        color: #4a5568;
        font-size: 0.92rem;
    }

    /* Sentiment result */
    .sentiment-result {
        background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(248,250,255,0.95) 100%);
        border-radius: 20px;
        padding: 32px;
        border: 1px solid rgba(91,155,213,0.1);
        box-shadow: 0 4px 20px rgba(46,95,138,0.06);
        text-align: center;
    }

    .emoji-big { font-size: 3.5rem; margin-bottom: 8px; }

    .sentiment-label {
        font-family: 'DM Serif Display', serif;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: 1px;
    }

    /* Tags */
    .pill {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 3px;
        letter-spacing: 0.3px;
    }
    .pill-azul { background: rgba(91,155,213,0.1); color: #2E5F8A; border: 1px solid rgba(91,155,213,0.2); }
    .pill-rosa { background: rgba(242,181,212,0.15); color: #a0456e; border: 1px solid rgba(242,181,212,0.25); }
    .pill-lavanda { background: rgba(184,169,208,0.15); color: #5e4f7a; border: 1px solid rgba(184,169,208,0.25); }

    /* Progress bars */
    .bar-track {
        width: 100%;
        height: 26px;
        background: #f0f2f5;
        border-radius: 13px;
        overflow: hidden;
        margin: 3px 0;
    }
    .bar-fill {
        height: 100%;
        border-radius: 13px;
        display: flex;
        align-items: center;
        padding-left: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        color: white;
        transition: width 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }

    /* Sidebar */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a3a5c 0%, #0f2440 50%, #0a1628 100%) !important;
    }
    div[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
    div[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; }
    div[data-testid="stSidebar"] .stRadio label:hover { color: white !important; }

    /* Category input styling */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1px solid rgba(91,155,213,0.2) !important;
        font-size: 0.95rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #5B9BD5 !important;
        box-shadow: 0 0 0 3px rgba(91,155,213,0.1) !important;
    }

    /* Button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2E5F8A 0%, #5B9BD5 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        padding: 12px 24px !important;
        font-size: 1rem !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(46,95,138,0.25) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 4px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }

    /* Divider */
    .gradient-divider {
        height: 3px;
        background: linear-gradient(90deg, #2E5F8A 0%, #5B9BD5 30%, #B8A9D0 60%, #F2B5D4 100%);
        border-radius: 2px;
        margin: 24px 0;
        opacity: 0.5;
    }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───
with st.sidebar:
    logo_path = os.path.join(os.path.dirname(__file__), "OpinIA_Logo.png")
    if os.path.exists(logo_path):
        st.image(Image.open(logo_path), width=150)
    else:
        st.markdown("## 💬 OpinIA")
    st.markdown('<div style="height:4px;background:linear-gradient(90deg,#5B9BD5,#B8A9D0,#F2B5D4);border-radius:2px;margin:8px 0 16px"></div>', unsafe_allow_html=True)
    pagina = st.radio("", ["🔍 Analizar reseña", "🏷️ Clasificar por categorías", "📊 Resultados PoC", "💡 Sobre OpinIA"])
    st.markdown("---")
    st.markdown("<small style='color:rgba(255,255,255,0.3)'>María Luisa Ros Bolea<br>CEU San Pablo · 2026<br><br>Práctica PLN<br>Máster Big Data e IA</small>", unsafe_allow_html=True)


# ─── ANALIZAR RESEÑA ───
if pagina == "🔍 Analizar reseña":
    st.markdown('<span class="section-tag">Análisis de sentimiento</span>', unsafe_allow_html=True)
    st.markdown("## Pega una reseña y la IA la analiza")
    st.markdown("Escribe cualquier opinión en español. **BERT multilingüe** (110M parámetros) detecta el sentimiento al instante.")
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    ejemplos = [
        "Este producto es increíble, lo mejor que he comprado en años. Funciona perfecto.",
        "Terrible, se rompió a los dos días. No lo recomiendo para nada. Dinero tirado.",
        "Funciona bien, nada especial pero cumple su función. Por el precio está correcto.",
        "La calidad es pésima, el plástico es muy fino y el envío tardó un mes.",
        "Excelente relación calidad-precio, muy contenta con la compra. Lo recomiendo.",
        "No me ha gustado nada, venía sin instrucciones y no funciona como dicen.",
    ]

    ejemplo_elegido = st.selectbox("Elige un ejemplo o escribe tu texto abajo:", ejemplos)
    texto_usuario = st.text_area("Tu reseña:", value=ejemplo_elegido, height=100, placeholder="Ej: Las zapatillas son cómodas pero la suela se despega al mes...")

    if st.button("🔍  Analizar sentimiento", type="primary", use_container_width=True):
        if not texto_usuario.strip():
            st.warning("Escribe o pega una reseña.")
        else:
            with st.spinner("Analizando..."):
                data = hf_query("nlptown/bert-base-multilingual-uncased-sentiment", {"inputs": texto_usuario[:512]})

            if data and isinstance(data, list) and len(data) > 0:
                resultados = data[0] if isinstance(data[0], list) else data
                resultados = sorted(resultados, key=lambda x: x["score"], reverse=True)

                top_stars = int(resultados[0]["label"][0])
                score_neg = sum(r["score"] for r in resultados if int(r["label"][0]) <= 2)
                score_neu = sum(r["score"] for r in resultados if int(r["label"][0]) == 3)
                score_pos = sum(r["score"] for r in resultados if int(r["label"][0]) >= 4)

                if top_stars <= 2:
                    sentimiento, emoji, color, grad = "NEGATIVO", "😠", "#C53030", "linear-gradient(135deg, #fff5f5 0%, #fef2f2 100%)"
                    confianza = score_neg
                elif top_stars == 3:
                    sentimiento, emoji, color, grad = "NEUTRO", "😐", "#7b6fa0", "linear-gradient(135deg, #f8f5ff 0%, #f3f0ff 100%)"
                    confianza = score_neu
                else:
                    sentimiento, emoji, color, grad = "POSITIVO", "😊", "#2B6CB0", "linear-gradient(135deg, #f0f7ff 0%, #ebf4ff 100%)"
                    confianza = score_pos

                st.markdown("")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f'<div class="sentiment-result" style="background:{grad};border-color:{color}20"><div class="emoji-big">{emoji}</div><div class="sentiment-label" style="color:{color}">{sentimiento}</div><div class="metric-label">Sentimiento detectado</div></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="glass-card"><div class="metric-big">{top_stars}★</div><div class="metric-label">Estrellas predichas</div></div>', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'<div class="glass-card"><div class="metric-big">{confianza*100:.0f}%</div><div class="metric-label">Confianza</div></div>', unsafe_allow_html=True)

                st.markdown("")
                st.markdown("##### Desglose por estrellas")
                for r in sorted(resultados, key=lambda x: int(x["label"][0])):
                    n_s = int(r["label"][0])
                    pct = r["score"] * 100
                    bar_c = f"linear-gradient(90deg, #e8a0b8, {ROSA})" if n_s <= 2 else f"linear-gradient(90deg, #9b8ec0, {LAVANDA})" if n_s == 3 else f"linear-gradient(90deg, #3a7cc0, {AZUL})"
                    st.markdown(f'<div style="display:flex;align-items:center;gap:12px;margin:5px 0"><span style="min-width:40px;font-weight:700;color:{AZUL_OSCURO}">{n_s}★</span><div class="bar-track"><div class="bar-fill" style="width:{max(pct,2)}%;background:{bar_c}">{pct:.1f}%</div></div></div>', unsafe_allow_html=True)

                st.markdown('<div class="info-box">Modelo: <strong>nlptown/bert-base-multilingual-uncased-sentiment</strong> · La confianza suma las probabilidades del grupo (positivo = 4★+5★).</div>', unsafe_allow_html=True)


# ─── ZERO-SHOT ───
elif pagina == "🏷️ Clasificar por categorías":
    st.markdown('<span class="section-tag">Clasificación zero-shot</span>', unsafe_allow_html=True)
    st.markdown("## Define tus categorías y la IA clasifica")
    st.markdown("El modelo asigna automáticamente categorías **sin haber sido entrenado** para ellas. Puedes cambiarlas cuando quieras.")
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    texto_zs = st.text_area("Reseña a clasificar:", value="El cable es demasiado corto, se calienta mucho y huele a plástico quemado. Muy peligroso.", height=100)
    st.markdown("**Categorías** (una por línea, edítalas libremente):")
    categorias_texto = st.text_area("cats", value="Problema de calidad del producto\nProblema con el envío o la entrega\nProducto peligroso o inseguro\nNo coincide con la descripción\nBuena relación calidad-precio\nProducto defectuoso o roto", height=150, label_visibility="collapsed")

    if st.button("🏷️  Clasificar", type="primary", use_container_width=True):
        categorias = [c.strip() for c in categorias_texto.strip().split("\n") if c.strip()]
        if not texto_zs.strip():
            st.warning("Escribe una reseña.")
        elif len(categorias) < 2:
            st.warning("Necesitas al menos 2 categorías.")
        else:
            with st.spinner("Clasificando..."):
                payload = {"inputs": texto_zs[:512], "parameters": {"candidate_labels": categorias, "multi_label": True}}
                data = hf_query("MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli", payload)

            if data and isinstance(data, list):
                data = {"labels": [d["label"] for d in data], "scores": [d["score"] for d in data]}
            if data and isinstance(data, dict) and "labels" in data:
                st.markdown("")
                st.markdown("##### Resultado")
                colors_zs = [
                    "linear-gradient(90deg, #1a3a5c, #2E5F8A)",
                    "linear-gradient(90deg, #2E5F8A, #5B9BD5)",
                    "linear-gradient(90deg, #7b6fa0, #B8A9D0)",
                    "linear-gradient(90deg, #c47da0, #F2B5D4)",
                    "linear-gradient(90deg, #d4a574, #FFD4B8)",
                    "linear-gradient(90deg, #5a6570, #7B8794)",
                ]
                for i, (label, score) in enumerate(zip(data["labels"], data["scores"])):
                    pct = score * 100
                    if pct < 3:
                        continue
                    grad = colors_zs[i % len(colors_zs)]
                    st.markdown(f'<div class="result-card" style="display:flex;align-items:center;gap:16px"><div style="flex:1"><div style="font-weight:600;margin-bottom:6px;color:#1a1a2e">{label}</div><div class="bar-track" style="height:22px"><div class="bar-fill" style="width:{max(pct,3)}%;background:{grad};font-size:0.75rem">{pct:.0f}%</div></div></div></div>', unsafe_allow_html=True)

                st.markdown('<div class="info-box">Puedes cambiar las categorías libremente. El modelo entiende la relación semántica entre el texto y cada categoría sin necesitar reentrenamiento.</div>', unsafe_allow_html=True)
            elif data:
                st.error(f"Respuesta inesperada: {str(data)[:200]}")


# ─── RESULTADOS ───
elif pagina == "📊 Resultados PoC":
    st.markdown('<span class="section-tag">Prueba de concepto</span>', unsafe_allow_html=True)
    st.markdown("## Resultados sobre 210.000 reseñas")
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    metrics = [("210K", "Reseñas analizadas"), ("0.76", "Mejor F1 (BERT)"), ("6", "Modelos evaluados"), ("10", "Técnicas PLN")]
    for col, (num, label) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(f'<div class="glass-card"><div class="metric-big">{num}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("")
    tab1, tab2, tab3 = st.tabs(["📊 Comparativa", "📁 Dataset", "💬 Temas"])

    with tab1:
        df_m = pd.DataFrame({"Modelo": ["BERT multilingüe", "DistilBERT fine-tuned", "LogReg + TF-IDF", "LogReg + BoW", "SVM + TF-IDF", "RF + TF-IDF"], "F1": [0.7593, 0.7150, 0.6808, 0.6744, 0.6706, 0.5828], "Tipo": ["Transformer", "Transformer", "Clásico", "Clásico", "Clásico", "Clásico"]})
        fig = go.Figure()
        fig.add_trace(go.Bar(y=df_m["Modelo"], x=df_m["F1"], orientation="h", marker_color=[AZUL_OSCURO if t == "Transformer" else LAVANDA for t in df_m["Tipo"]], text=[f"{v:.4f}" for v in df_m["F1"]], textposition="outside", textfont=dict(size=13, family="Inter", color=AZUL_OSCURO)))
        fig.update_layout(title="F1 Score (weighted)", title_font=dict(size=16, family="Inter"), font=dict(family="Inter"), plot_bgcolor="white", paper_bgcolor="white", xaxis=dict(range=[0, 0.88], gridcolor="#f0f2f5"), yaxis=dict(autorange="reversed"), margin=dict(l=10, r=80, t=50, b=30), height=340)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="info-box">BERT supera a los clásicos en <strong>8 puntos de F1</strong>. La diferencia es especialmente notable en las reseñas neutras (3★), donde el recall pasa del 20% al 50%.</div>', unsafe_allow_html=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig_s = px.bar(pd.DataFrame({"Estrellas": ["1★", "2★", "3★", "4★", "5★"], "Reseñas": [42000]*5, "Tipo": ["Negativo", "Negativo", "Neutro", "Positivo", "Positivo"]}), x="Estrellas", y="Reseñas", color="Tipo", color_discrete_map={"Negativo": ROSA, "Neutro": LAVANDA, "Positivo": AZUL}, title="Distribución por estrellas")
            fig_s.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(family="Inter"), title_font_size=14, margin=dict(t=50, b=30))
            st.plotly_chart(fig_s, use_container_width=True)
        with c2:
            fig_p = px.pie(values=[84000, 42000, 84000], names=["Positivo (4-5★)", "Neutro (3★)", "Negativo (1-2★)"], color_discrete_sequence=[AZUL, LAVANDA, ROSA], title="Distribución de sentimiento", hole=0.45)
            fig_p.update_layout(font=dict(family="Inter"), title_font_size=14, margin=dict(t=50, b=30), paper_bgcolor="white")
            st.plotly_chart(fig_p, use_container_width=True)
        st.markdown('<div class="info-box">Dataset perfectamente balanceado (42K por estrella). Las reseñas negativas son más largas: cuando un cliente está enfadado, escribe más.</div>', unsafe_allow_html=True)

    with tab3:
        temas = [("Quejas", "demasiado, malo, pequeño, nunca", ROSA, "😤"), ("Estética", "grande, cómodo, color, aunque", LAVANDA, "🎨"), ("Envío", "caja, material, tiempo, pedido", AZUL, "📦"), ("Calidad-precio", "calidad, precio, funciona, genial", AZUL_OSCURO, "💰"), ("Audio", "buena, mejor, sonido, esperaba", AZUL_CLARO, "🎵"), ("Satisfacción", "contento, fácil, relación", MELOCOTON, "😊"), ("Experiencia", "perfectamente, perfecto, razón", LAVANDA, "✨"), ("Regalos", "contenta, regalo, excelente", ROSA, "🎁")]
        c1, c2 = st.columns(2)
        for i, (nombre, palabras, color, icon) in enumerate(temas):
            col = c1 if i % 2 == 0 else c2
            with col:
                st.markdown(f'<div class="result-card" style="border-left:4px solid {color}"><div style="display:flex;align-items:center;gap:10px"><span style="font-size:1.4rem">{icon}</span><div><span style="color:{color};font-size:0.75rem;font-weight:700;letter-spacing:1px">TEMA {i+1}</span><div style="font-weight:600;margin:2px 0;color:#1a1a2e">{nombre}</div><span style="font-size:0.82rem;color:#7B8794">{palabras}</span></div></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">8 temas descubiertos automáticamente con LDA, sin definir categorías a priori.</div>', unsafe_allow_html=True)


# ─── SOBRE OPINIA ───
elif pagina == "💡 Sobre OpinIA":
    st.markdown('<p class="hero-title">OpinIA</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Inteligencia de reputación online para e-commerce español</p>', unsafe_allow_html=True)
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    ca, cb = st.columns(2)
    with ca:
        st.markdown("#### 🔴 El problema")
        st.markdown("Las marcas reciben **miles de reseñas al mes**. Leerlas a mano es imposible. La media de estrellas no dice *por qué* el cliente está contento o enfadado.")
    with cb:
        st.markdown("#### 🟢 La solución")
        st.markdown("OpinIA usa **PLN avanzado** para analizar cada reseña: detecta sentimiento, extrae categorías, identifica marcas, descubre temas y permite buscar por significado.")

    st.markdown("")
    st.markdown("#### Tecnologías")
    st.markdown(
        '<span class="pill pill-azul">BERT</span>'
        '<span class="pill pill-azul">DistilBERT</span>'
        '<span class="pill pill-rosa">BART</span>'
        '<span class="pill pill-lavanda">NER</span>'
        '<span class="pill pill-rosa">LDA</span>'
        '<span class="pill pill-azul">Sentence-BERT</span>'
        '<span class="pill pill-lavanda">FAISS</span>'
        '<span class="pill pill-azul">TF-IDF</span>'
        '<span class="pill pill-rosa">scikit-learn</span>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    st.markdown("#### Planes")
    c1, c2, c3 = st.columns(3)
    planes = [
        ("Starter", "99€", "/mes · 5K reseñas", AZUL, f"linear-gradient(135deg, {AZUL}10 0%, white 100%)"),
        ("Growth", "299€", "/mes · 50K reseñas", LAVANDA, f"linear-gradient(135deg, {LAVANDA}15 0%, white 100%)"),
        ("Enterprise", "Custom", "Volumen ilimitado", ROSA, f"linear-gradient(135deg, {ROSA}15 0%, white 100%)"),
    ]
    for col, (name, price, desc, color, bg) in zip([c1, c2, c3], planes):
        with col:
            st.markdown(f'<div class="glass-card" style="border-top:4px solid {color};background:{bg}"><h4 style="color:{color};margin:0 0 8px;font-size:0.95rem">{name}</h4><div class="metric-big" style="background:none;-webkit-text-fill-color:{color}">{price}</div><div class="metric-label">{desc}</div></div>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown("---")
    st.markdown('<p style="text-align:center;color:#7B8794;font-size:0.85rem">María Luisa Ros Bolea · malurosbolea@gmail.com · <a href="https://www.linkedin.com/in/mar%C3%ADa-luisa-ros-bolea-400780160/" style="color:#5B9BD5">LinkedIn</a> · <a href="https://malurosbolea-ux.github.io/digital-strategy-portfolio/" style="color:#5B9BD5">Portfolio</a></p>', unsafe_allow_html=True)
