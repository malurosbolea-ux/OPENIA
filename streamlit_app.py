"""
OpinIA — Inteligencia de reputación online para e-commerce español
App interactiva: pega una reseña y la IA la analiza en tiempo real.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from PIL import Image
import os, json

st.set_page_config(page_title="OpinIA", page_icon="💬", layout="wide", initial_sidebar_state="expanded")

AZUL = "#5B9BD5"
AZUL_OSCURO = "#2E5F8A"
AZUL_CLARO = "#A8D1F0"
LAVANDA = "#B8A9D0"
ROSA = "#F2B5D4"
MELOCOTON = "#FFD4B8"
GRIS = "#7B8794"

HF_TOKEN = st.secrets.get("HF_TOKEN", None)
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def hf_query(model, payload):
    url = f"https://router.huggingface.co/hf-inference/models/{model}"
    r = requests.post(url, headers=HF_HEADERS, json=payload, timeout=60)
    if r.status_code == 503:
        st.warning("El modelo está cargando en HuggingFace, espera 20 segundos y vuelve a pulsar el botón.")
        return None
    if r.status_code != 200:
        st.error(f"Error {r.status_code}: {r.text[:200]}")
        return None
    return r.json()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Outfit:wght@300;400;500;600;700&display=swap');
    .main .block-container{padding-top:2rem;max-width:1100px}
    h1,h2,h3{font-family:'Outfit',sans-serif!important}
    .hero-title{font-family:'DM Serif Display',serif!important;font-size:3rem!important;color:#2E5F8A!important;margin-bottom:0!important}
    .hero-sub{font-size:1.15rem;color:#7B8794;font-weight:300;margin-top:4px}
    .metric-card{background:white;border-radius:16px;padding:24px;text-align:center;box-shadow:0 2px 12px rgba(0,0,0,0.04);border:1px solid #EEF2F7}
    .metric-number{font-family:'DM Serif Display',serif;font-size:2.4rem;color:#2E5F8A;line-height:1.2}
    .metric-label{font-size:.85rem;color:#7B8794;margin-top:4px}
    .section-tag{font-size:.8rem;font-weight:600;color:#5B9BD5;text-transform:uppercase;letter-spacing:2px;margin-bottom:4px}
    .result-box{background:white;border-radius:14px;padding:20px 24px;border:1px solid #EEF2F7;margin-bottom:12px;box-shadow:0 1px 8px rgba(0,0,0,0.03)}
    .quote-box{background:#F8F9FC;border-left:4px solid #5B9BD5;padding:14px 18px;border-radius:0 12px 12px 0;margin:10px 0;color:#4a5568}
    .tag{display:inline-block;padding:4px 12px;border-radius:20px;font-size:.8rem;font-weight:500;margin:2px}
    .tag-azul{background:rgba(91,155,213,0.12);color:#2E5F8A}
    .tag-rosa{background:rgba(242,181,212,0.2);color:#a0456e}
    div[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a3a5c 0%,#0d1f33 100%)}
    div[data-testid="stSidebar"] *{color:white!important}
    div[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,0.1)!important}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    logo_path = os.path.join(os.path.dirname(__file__), "OpinIA_Logo.png")
    if os.path.exists(logo_path):
        st.image(Image.open(logo_path), width=160)
    else:
        st.markdown("## 💬 OpinIA")
    st.markdown("---")
    pagina = st.radio("Navegación", ["Analizar reseña", "Clasificar por categorías", "Resultados PoC", "Sobre OpinIA"])
    st.markdown("---")
    st.markdown("<small style='color:rgba(255,255,255,0.35)'>María Luisa Ros Bolea<br>CEU San Pablo · 2026</small>", unsafe_allow_html=True)


# ── ANALIZAR RESEÑA ──
if pagina == "Analizar reseña":
    st.markdown('<p class="section-tag">Análisis de sentimiento</p>', unsafe_allow_html=True)
    st.markdown("## Pega una reseña y la IA la analiza al instante")
    st.markdown("Escribe o pega cualquier opinión de producto en español. El modelo **BERT multilingüe** detecta si es positiva, negativa o neutra.")
    st.markdown("")

    ejemplos = [
        "Este producto es increíble, lo mejor que he comprado en años. Funciona perfecto.",
        "Terrible, se rompió a los dos días. No lo recomiendo para nada. Dinero tirado.",
        "Funciona bien, nada especial pero cumple su función. Por el precio está correcto.",
        "La calidad es pésima, el plástico es muy fino y el envío tardó un mes.",
        "Excelente relación calidad-precio, muy contenta con la compra. Lo recomiendo.",
        "No me ha gustado nada, venía sin instrucciones y no funciona como dicen.",
    ]

    ejemplo_elegido = st.selectbox("Prueba un ejemplo o escribe tu propio texto abajo:", ejemplos)
    texto_usuario = st.text_area("Escribe la reseña aquí:", value=ejemplo_elegido, height=100, placeholder="Ej: Las zapatillas son cómodas pero la suela se despega al mes...")

    if st.button("🔍  Analizar sentimiento", type="primary", use_container_width=True):
        if not texto_usuario.strip():
            st.warning("Escribe o pega una reseña para analizar.")
        else:
            with st.spinner("Analizando con BERT multilingüe..."):
                data = hf_query("nlptown/bert-base-multilingual-uncased-sentiment", {"inputs": texto_usuario[:512]})

            if data and isinstance(data, list) and len(data) > 0:
                resultados = data[0] if isinstance(data[0], list) else data
                resultados = sorted(resultados, key=lambda x: x["score"], reverse=True)

                top_label = resultados[0]["label"]
                top_stars = int(top_label[0])

                score_neg = sum(r["score"] for r in resultados if int(r["label"][0]) <= 2)
                score_neu = sum(r["score"] for r in resultados if int(r["label"][0]) == 3)
                score_pos = sum(r["score"] for r in resultados if int(r["label"][0]) >= 4)

                if top_stars <= 2:
                    sentimiento, emoji, color = "NEGATIVO", "😠", "#C53030"
                    confianza = score_neg
                elif top_stars == 3:
                    sentimiento, emoji, color = "NEUTRO", "😐", "#7b6fa0"
                    confianza = score_neu
                else:
                    sentimiento, emoji, color = "POSITIVO", "😊", "#2B6CB0"
                    confianza = score_pos

                st.markdown("")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f'<div class="metric-card"><div style="font-size:2.5rem">{emoji}</div><div class="metric-number" style="color:{color}">{sentimiento}</div><div class="metric-label">Sentimiento detectado</div></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="metric-card"><div class="metric-number">{top_stars}★</div><div class="metric-label">Estrellas predichas</div></div>', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'<div class="metric-card"><div class="metric-number">{confianza*100:.0f}%</div><div class="metric-label">Confianza del modelo</div></div>', unsafe_allow_html=True)

                st.markdown("")
                st.markdown("**Desglose por estrellas:**")
                for r in sorted(resultados, key=lambda x: int(x["label"][0])):
                    n_s = int(r["label"][0])
                    pct = r["score"] * 100
                    bar_c = ROSA if n_s <= 2 else LAVANDA if n_s == 3 else AZUL
                    st.markdown(f'<div style="display:flex;align-items:center;gap:10px;margin:4px 0"><span style="min-width:50px;font-weight:600">{n_s}★</span><div style="flex:1;height:24px;background:#EEF2F7;border-radius:12px;overflow:hidden"><div style="width:{pct}%;height:100%;background:{bar_c};border-radius:12px"></div></div><span style="min-width:50px;font-size:.9rem">{pct:.1f}%</span></div>', unsafe_allow_html=True)

                st.markdown('<div class="quote-box" style="margin-top:16px">Modelo: <strong>nlptown/bert-base-multilingual-uncased-sentiment</strong> · La confianza muestra la probabilidad combinada del grupo de sentimiento (positivo = 4★+5★, negativo = 1★+2★).</div>', unsafe_allow_html=True)


# ── ZERO-SHOT ──
elif pagina == "Clasificar por categorías":
    st.markdown('<p class="section-tag">Clasificación zero-shot</p>', unsafe_allow_html=True)
    st.markdown("## Define tus categorías y la IA clasifica")
    st.markdown("Escribe una reseña y define las categorías que quieras. El modelo **BART** las asigna automáticamente **sin haber sido entrenado** para esas categorías.")
    st.markdown("")

    texto_zs = st.text_area("Reseña a clasificar:", value="El cable es demasiado corto, se calienta mucho y huele a plástico quemado. Muy peligroso.", height=100)
    st.markdown("**Categorías** (una por línea):")
    categorias_texto = st.text_area("cats", value="Problema de calidad del producto\nProblema con el envío o la entrega\nProducto peligroso o inseguro\nNo coincide con la descripción\nBuena relación calidad-precio\nProducto defectuoso o roto", height=150, label_visibility="collapsed")

    if st.button("🏷️  Clasificar", type="primary", use_container_width=True):
        categorias = [c.strip() for c in categorias_texto.strip().split("\n") if c.strip()]
        if not texto_zs.strip():
            st.warning("Escribe una reseña para clasificar.")
        elif len(categorias) < 2:
            st.warning("Necesitas al menos 2 categorías.")
        else:
            with st.spinner("Clasificando con BART (zero-shot)..."):
                payload = {
                    "inputs": texto_zs[:512],
                    "parameters": {"candidate_labels": categorias, "multi_label": True},
                }
                data = hf_query("facebook/bart-large-mnli", payload)

            if data and isinstance(data, dict) and "labels" in data:
                st.markdown("")
                st.markdown("**Resultado:**")
                for label, score in zip(data["labels"], data["scores"]):
                    pct = score * 100
                    if pct < 3:
                        continue
                    color = AZUL_OSCURO if pct > 80 else AZUL if pct > 50 else LAVANDA if pct > 30 else GRIS
                    st.markdown(f'<div style="display:flex;align-items:center;gap:12px;margin:6px 0"><div style="flex:1;max-width:500px;height:28px;background:#EEF2F7;border-radius:14px;overflow:hidden"><div style="width:{pct}%;height:100%;background:{color};border-radius:14px;display:flex;align-items:center;padding-left:12px"><span style="color:white;font-size:.8rem;font-weight:600">{pct:.0f}%</span></div></div><span style="font-size:.95rem">{label}</span></div>', unsafe_allow_html=True)

                st.markdown('<div class="quote-box" style="margin-top:16px">Puedes cambiar las categorías cuando quieras. El modelo no necesita reentrenamiento.</div>', unsafe_allow_html=True)
            elif data:
                st.error(f"Respuesta inesperada del modelo: {str(data)[:300]}")


# ── RESULTADOS ──
elif pagina == "Resultados PoC":
    st.markdown('<p class="section-tag">Prueba de concepto</p>', unsafe_allow_html=True)
    st.markdown("## Resultados sobre 210.000 reseñas")
    st.markdown("")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-number">210K</div><div class="metric-label">Reseñas analizadas</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-number">0.76</div><div class="metric-label">Mejor F1 (BERT)</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-number">6</div><div class="metric-label">Modelos evaluados</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><div class="metric-number">10</div><div class="metric-label">Técnicas de PLN</div></div>', unsafe_allow_html=True)

    st.markdown("")
    tab1, tab2, tab3 = st.tabs(["Comparativa de modelos", "Dataset", "Temas descubiertos"])

    with tab1:
        df_m = pd.DataFrame({"Modelo": ["BERT multilingüe", "DistilBERT fine-tuned", "LogReg + TF-IDF", "LogReg + BoW", "SVM + TF-IDF", "RF + TF-IDF"], "F1": [0.7593, 0.7150, 0.6808, 0.6744, 0.6706, 0.5828], "Tipo": ["Transformer", "Transformer", "Clásico", "Clásico", "Clásico", "Clásico"]})
        fig = go.Figure()
        fig.add_trace(go.Bar(y=df_m["Modelo"], x=df_m["F1"], orientation="h", marker_color=[AZUL_OSCURO if t == "Transformer" else LAVANDA for t in df_m["Tipo"]], text=[f"{v:.4f}" for v in df_m["F1"]], textposition="outside", textfont=dict(size=13, family="Outfit", color="#2E5F8A")))
        fig.update_layout(title="F1 Score (weighted)", title_font_size=16, font=dict(family="Outfit"), plot_bgcolor="white", xaxis=dict(range=[0, 0.88]), yaxis=dict(autorange="reversed"), margin=dict(l=10, r=80, t=50, b=30), height=340)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="quote-box">BERT supera a los modelos clásicos en 8 puntos de F1. La diferencia es especialmente notable en las reseñas neutras (3★).</div>', unsafe_allow_html=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig_s = px.bar(pd.DataFrame({"Estrellas": ["1★", "2★", "3★", "4★", "5★"], "Reseñas": [42000]*5, "Tipo": ["Negativo", "Negativo", "Neutro", "Positivo", "Positivo"]}), x="Estrellas", y="Reseñas", color="Tipo", color_discrete_map={"Negativo": ROSA, "Neutro": LAVANDA, "Positivo": AZUL}, title="Por estrellas")
            fig_s.update_layout(plot_bgcolor="white", font=dict(family="Outfit"), title_font_size=14, margin=dict(t=50, b=30))
            st.plotly_chart(fig_s, use_container_width=True)
        with c2:
            fig_p = px.pie(values=[84000, 42000, 84000], names=["Positivo", "Neutro", "Negativo"], color_discrete_sequence=[AZUL, LAVANDA, ROSA], title="Por sentimiento", hole=0.45)
            fig_p.update_layout(font=dict(family="Outfit"), title_font_size=14, margin=dict(t=50, b=30))
            st.plotly_chart(fig_p, use_container_width=True)

    with tab3:
        temas = [("Quejas generales", "demasiado, malo, pequeño, nunca", ROSA), ("Tamaño y estética", "grande, cómodo, color, aunque", LAVANDA), ("Envío y logística", "caja, material, tiempo, pedido", AZUL), ("Calidad-precio", "calidad, precio, funciona, genial", AZUL_OSCURO), ("Audio y sonido", "buena, mejor, sonido, esperaba", AZUL_CLARO), ("Satisfacción", "contento, fácil, relación, calidad", MELOCOTON), ("Experiencia", "perfectamente, perfecto, razón", LAVANDA), ("Regalos", "contenta, regalo, excelente, luz", ROSA)]
        c1, c2 = st.columns(2)
        for i, (nombre, palabras, color) in enumerate(temas):
            col = c1 if i % 2 == 0 else c2
            with col:
                st.markdown(f'<div class="result-box" style="border-left:4px solid {color}"><span style="color:{color};font-size:.8rem;font-weight:600">TEMA {i+1}</span><div style="font-weight:600;margin:4px 0">{nombre}</div><span style="font-size:.85rem;color:#7B8794">{palabras}</span></div>', unsafe_allow_html=True)


# ── SOBRE OPINIA ──
elif pagina == "Sobre OpinIA":
    st.markdown('<p class="section-tag">El producto</p>', unsafe_allow_html=True)
    st.markdown("## OpinIA convierte reseñas en decisiones de negocio")
    st.markdown("")
    ca, cb = st.columns(2)
    with ca:
        st.markdown("### El problema")
        st.markdown("Las marcas de e-commerce reciben **miles de reseñas al mes**. Leerlas manualmente es imposible. Las herramientas actuales solo muestran la media de estrellas.")
    with cb:
        st.markdown("### La solución")
        st.markdown("OpinIA usa **PLN avanzado** (BERT, BART, NER, LDA, FAISS) para analizar cada reseña automáticamente: sentimiento, categorías, marcas, temas y búsqueda semántica.")
    st.markdown("")
    st.markdown("### Tecnologías")
    st.markdown('<span class="tag tag-azul">BERT</span><span class="tag tag-azul">DistilBERT</span><span class="tag tag-rosa">BART</span><span class="tag tag-azul">NER</span><span class="tag tag-rosa">LDA</span><span class="tag tag-azul">Sentence-BERT</span><span class="tag tag-rosa">FAISS</span><span class="tag tag-azul">TF-IDF</span><span class="tag tag-azul">scikit-learn</span>', unsafe_allow_html=True)
    st.markdown("")
    st.markdown("### Planes")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric-card" style="border-top:4px solid #5B9BD5"><h4 style="color:#5B9BD5">Starter</h4><div class="metric-number">99€</div><div class="metric-label">/mes · Hasta 5.000 reseñas</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card" style="border-top:4px solid #B8A9D0"><h4 style="color:#7b6fa0">Growth</h4><div class="metric-number" style="color:#7b6fa0">299€</div><div class="metric-label">/mes · Hasta 50.000 reseñas</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card" style="border-top:4px solid #F2B5D4"><h4 style="color:#a0456e">Enterprise</h4><div class="metric-number" style="color:#a0456e">Custom</div><div class="metric-label">Volumen ilimitado</div></div>', unsafe_allow_html=True)
    st.markdown("")
    st.markdown("---")
    st.markdown('<p style="text-align:center;color:#7B8794;font-size:.9rem">María Luisa Ros Bolea · malurosbolea@gmail.com · <a href="https://www.linkedin.com/in/mar%C3%ADa-luisa-ros-bolea-400780160/">LinkedIn</a> · <a href="https://malurosbolea-ux.github.io/digital-strategy-portfolio/">Portfolio</a></p>', unsafe_allow_html=True)
