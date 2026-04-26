"""
OpinIA — Inteligencia de reputación online para e-commerce español
Dashboard interactivo con los resultados de la PoC
Autora: María Luisa Ros Bolea | CEU San Pablo | 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="OpinIA — Demo",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta OpinIA
AZUL = "#5B9BD5"
AZUL_OSCURO = "#2E5F8A"
AZUL_CLARO = "#A8D1F0"
LAVANDA = "#B8A9D0"
ROSA = "#F2B5D4"
MELOCOTON = "#FFD4B8"
GRIS = "#7B8794"
BLANCO = "#FAFCFF"

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Outfit:wght@300;400;500;600;700&display=swap');

    .main .block-container { padding-top: 2rem; max-width: 1100px; }

    h1, h2, h3 { font-family: 'Outfit', sans-serif !important; }

    .hero-title {
        font-family: 'DM Serif Display', serif !important;
        font-size: 3.5rem !important;
        color: #2E5F8A !important;
        margin-bottom: 0 !important;
        line-height: 1.1 !important;
    }

    .hero-sub {
        font-size: 1.2rem;
        color: #7B8794;
        font-weight: 300;
        margin-top: 8px;
    }

    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        border: 1px solid #EEF2F7;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); }

    .metric-number {
        font-family: 'DM Serif Display', serif;
        font-size: 2.6rem;
        color: #2E5F8A;
        line-height: 1.2;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #7B8794;
        margin-top: 4px;
    }

    .section-header {
        font-size: 0.85rem;
        font-weight: 600;
        color: #5B9BD5;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 4px;
    }

    .quote-box {
        background: #F8F9FC;
        border-left: 4px solid #5B9BD5;
        padding: 16px 20px;
        border-radius: 0 12px 12px 0;
        margin: 12px 0;
        font-style: italic;
        color: #4a5568;
    }

    .result-card {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #EEF2F7;
        margin-bottom: 8px;
    }

    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 2px;
    }
    .tag-azul { background: rgba(91,155,213,0.12); color: #2E5F8A; }
    .tag-rosa { background: rgba(242,181,212,0.2); color: #a0456e; }
    .tag-lavanda { background: rgba(184,169,208,0.2); color: #5e4f7a; }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a3a5c 0%, #0d1f33 100%);
    }
    div[data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSidebar"] .stRadio label { color: rgba(255,255,255,0.8) !important; }
    div[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }

    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 20px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    logo_path = os.path.join(os.path.dirname(__file__), "OpinIA_Logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, width=180)
    else:
        st.markdown("## 💬 OpinIA")

    st.markdown("---")

    pagina = st.radio(
        "Navegación",
        ["Inicio", "Dataset", "Modelos", "Zero-shot", "Búsqueda semántica",
         "Temas LDA", "Negocio"],
        index=0,
    )

    st.markdown("---")
    st.markdown(
        "<small style='color:rgba(255,255,255,0.4)'>María Luisa Ros Bolea<br>"
        "CEU San Pablo · 2026</small>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# PAGINA: INICIO
# ─────────────────────────────────────────────
if pagina == "Inicio":
    st.markdown('<p class="hero-title">OpinIA</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">'
        "Inteligencia de reputación online para e-commerce español"
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown("")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-number">210K</div>'
            '<div class="metric-label">Reseñas analizadas</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-number">0.76</div>'
            '<div class="metric-label">F1 Score (BERT)</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-number">10</div>'
            '<div class="metric-label">Técnicas de PLN</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-number">87%</div>'
            '<div class="metric-label">Similitud semántica</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown("")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<p class="section-header">El problema</p>', unsafe_allow_html=True)
        st.markdown(
            "Las marcas de e-commerce reciben **miles de reseñas al mes**. "
            "Leerlas manualmente es imposible y las herramientas actuales solo "
            "muestran la media de estrellas, que no dice *por qué* el cliente "
            "está contento o enfadado."
        )
    with col_b:
        st.markdown('<p class="section-header">La solución</p>', unsafe_allow_html=True)
        st.markdown(
            "OpinIA procesa cada reseña con **PLN avanzado**: detecta sentimiento, "
            "extrae categorías de queja, identifica marcas, descubre temas "
            "emergentes y permite buscar por significado en milisegundos."
        )

    st.markdown("")
    st.markdown(
        '<div style="display:flex;gap:6px;flex-wrap:wrap">'
        '<span class="tag tag-azul">Análisis de sentimiento</span>'
        '<span class="tag tag-azul">BERT multilingüe</span>'
        '<span class="tag tag-lavanda">Zero-shot</span>'
        '<span class="tag tag-lavanda">NER</span>'
        '<span class="tag tag-rosa">LDA Topics</span>'
        '<span class="tag tag-rosa">FAISS</span>'
        '<span class="tag tag-azul">Fine-tuning</span>'
        '<span class="tag tag-lavanda">Sentence-BERT</span>'
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# PAGINA: DATASET
# ─────────────────────────────────────────────
elif pagina == "Dataset":
    st.markdown('<p class="section-header">Los datos</p>', unsafe_allow_html=True)
    st.markdown("## 210.000 reseñas reales en español")
    st.markdown(
        "Amazon Reviews Multi · Perfectamente balanceado · 42.000 reseñas por estrella"
    )

    st.markdown("")

    # Distribución de estrellas
    col1, col2 = st.columns(2)

    with col1:
        df_stars = pd.DataFrame({
            "Estrellas": ["1★", "2★", "3★", "4★", "5★"],
            "Reseñas": [42000, 42000, 42000, 42000, 42000],
            "Color": ["Negativo", "Negativo", "Neutro", "Positivo", "Positivo"],
        })
        fig_stars = px.bar(
            df_stars, x="Estrellas", y="Reseñas", color="Color",
            color_discrete_map={"Negativo": ROSA, "Neutro": LAVANDA, "Positivo": AZUL},
            title="Distribución de puntuaciones",
        )
        fig_stars.update_layout(
            showlegend=True, plot_bgcolor="white",
            font=dict(family="Outfit"), title_font_size=16,
            yaxis_title="", xaxis_title="",
            margin=dict(t=50, b=30),
        )
        st.plotly_chart(fig_stars, use_container_width=True)

    with col2:
        df_sent = pd.DataFrame({
            "Sentimiento": ["Positivo (4-5★)", "Neutro (3★)", "Negativo (1-2★)"],
            "Reseñas": [84000, 42000, 84000],
            "Porcentaje": ["40%", "20%", "40%"],
        })
        fig_sent = px.pie(
            df_sent, values="Reseñas", names="Sentimiento",
            color="Sentimiento",
            color_discrete_map={
                "Positivo (4-5★)": AZUL,
                "Neutro (3★)": LAVANDA,
                "Negativo (1-2★)": ROSA,
            },
            title="Distribución de sentimiento",
            hole=0.45,
        )
        fig_sent.update_layout(
            font=dict(family="Outfit"), title_font_size=16,
            margin=dict(t=50, b=30),
        )
        fig_sent.update_traces(textinfo="label+percent", textfont_size=12)
        st.plotly_chart(fig_sent, use_container_width=True)

    st.markdown(
        '<div class="quote-box">'
        "El dataset está perfectamente balanceado (42K por estrella), lo que permite "
        "evaluar los modelos sin sesgos. Las reseñas negativas tienden a ser más "
        "largas: cuando un cliente está enfadado, escribe más."
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# PAGINA: MODELOS
# ─────────────────────────────────────────────
elif pagina == "Modelos":
    st.markdown('<p class="section-header">Resultados</p>', unsafe_allow_html=True)
    st.markdown("## 6 modelos evaluados, un ganador claro")

    df_modelos = pd.DataFrame({
        "Modelo": [
            "BERT multilingüe", "DistilBERT fine-tuned", "LogReg + TF-IDF",
            "LogReg + BoW", "SVM + TF-IDF", "RF + TF-IDF",
        ],
        "F1 Score": [0.7593, 0.7150, 0.6808, 0.6744, 0.6706, 0.5828],
        "Accuracy": [0.7595, 0.7185, 0.7057, 0.6942, 0.6979, 0.6550],
        "Tiempo (s)": [281.9, 148.6, 16.8, 21.2, 8.0, 104.7],
        "Tipo": [
            "Transformer", "Transformer", "Clásico",
            "Clásico", "Clásico", "Clásico",
        ],
    })

    # Gráfico comparativo principal
    fig_comp = go.Figure()

    colors = [AZUL_OSCURO if t == "Transformer" else LAVANDA for t in df_modelos["Tipo"]]

    fig_comp.add_trace(go.Bar(
        y=df_modelos["Modelo"],
        x=df_modelos["F1 Score"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:.4f}" for v in df_modelos["F1 Score"]],
        textposition="outside",
        textfont=dict(size=13, family="Outfit", color="#2E5F8A"),
    ))

    fig_comp.update_layout(
        title="Comparativa de modelos — F1 Score (weighted)",
        title_font_size=16,
        font=dict(family="Outfit"),
        plot_bgcolor="white",
        xaxis=dict(range=[0, 0.88], title="F1 Score"),
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=80, t=50, b=40),
        height=380,
    )

    st.plotly_chart(fig_comp, use_container_width=True)

    # Métricas detalladas
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-number" style="color:#2E5F8A">0.7593</div>'
            '<div class="metric-label">Mejor F1 — BERT multilingüe</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-number" style="color:#B8A9D0">0.5828</div>'
            '<div class="metric-label">Peor F1 — Random Forest</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-number" style="color:#5B9BD5">+8 pts</div>'
            '<div class="metric-label">Mejora Transformer vs Clásico</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")

    # Detalle por clase
    st.markdown("### Rendimiento por clase de sentimiento")

    df_clases = pd.DataFrame({
        "Clase": ["Negativo", "Neutro", "Positivo"] * 2,
        "Modelo": ["BERT multilingüe"] * 3 + ["LogReg + TF-IDF"] * 3,
        "Recall": [0.83, 0.50, 0.86, 0.80, 0.22, 0.83],
    })

    fig_clases = px.bar(
        df_clases, x="Clase", y="Recall", color="Modelo", barmode="group",
        color_discrete_map={
            "BERT multilingüe": AZUL_OSCURO,
            "LogReg + TF-IDF": LAVANDA,
        },
        title="Recall por clase: BERT vs mejor modelo clásico",
    )
    fig_clases.update_layout(
        plot_bgcolor="white", font=dict(family="Outfit"),
        title_font_size=16, yaxis=dict(range=[0, 1], title="Recall"),
        margin=dict(t=50, b=30), height=350,
    )
    st.plotly_chart(fig_clases, use_container_width=True)

    st.markdown(
        '<div class="quote-box">'
        "La diferencia clave está en la clase neutra: BERT alcanza un 50% de recall "
        "frente al 22% de LogReg. Los modelos clásicos no entienden la ambigüedad de "
        "las reseñas de 3 estrellas porque solo cuentan palabras sin captar el contexto."
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# PAGINA: ZERO-SHOT
# ─────────────────────────────────────────────
elif pagina == "Zero-shot":
    st.markdown('<p class="section-header">Clasificación zero-shot</p>', unsafe_allow_html=True)
    st.markdown("## El cliente define las categorías, el modelo las detecta")

    st.markdown(
        "El modelo **BART** (Facebook) clasifica reseñas en categorías "
        "**que nunca ha visto** durante su entrenamiento. No necesita ejemplos "
        "previos ni reentrenamiento."
    )

    st.markdown("")

    # Ejemplos reales del notebook
    ejemplos_zs = [
        {
            "texto": "Muy lenta y se queda pillada en casi todos los juegos, compré dos unidades y las dos igual...",
            "categorias": [
                ("Producto defectuoso o roto", 0.99),
                ("Problema de calidad del producto", 0.97),
                ("No coincide con la descripción", 0.89),
            ],
        },
        {
            "texto": "El cable es demasiado corto y no llega al enchufe. Para el precio que tiene esperaba mucho más...",
            "categorias": [
                ("Problema de calidad del producto", 0.96),
                ("No coincide con la descripción", 0.91),
                ("Producto defectuoso o roto", 0.54),
            ],
        },
        {
            "texto": "Llegó un mes después de la fecha prometida y con la caja aplastada...",
            "categorias": [
                ("Problema con el envío o la entrega", 0.98),
                ("Problema de calidad del producto", 0.62),
                ("No coincide con la descripción", 0.41),
            ],
        },
    ]

    for i, ej in enumerate(ejemplos_zs):
        st.markdown(
            f'<div class="quote-box">"{ej["texto"]}"</div>',
            unsafe_allow_html=True,
        )
        for cat, score in ej["categorias"]:
            pct = int(score * 100)
            color = AZUL_OSCURO if score > 0.9 else AZUL if score > 0.7 else LAVANDA
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:12px;margin:4px 0 4px 20px">'
                f'<div style="flex:1;max-width:400px;height:22px;background:#EEF2F7;'
                f'border-radius:11px;overflow:hidden">'
                f'<div style="width:{pct}%;height:100%;background:{color};'
                f'border-radius:11px"></div></div>'
                f'<span style="font-size:0.9rem;min-width:240px">{cat} '
                f'<strong>{pct}%</strong></span></div>',
                unsafe_allow_html=True,
            )
        st.markdown("")

    st.markdown(
        '<div class="quote-box">'
        "El cliente puede crear nuevas categorías en cualquier momento sin depender "
        "de nosotros para reentrenar el modelo. Eso es escalabilidad real."
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# PAGINA: BUSQUEDA SEMANTICA
# ─────────────────────────────────────────────
elif pagina == "Búsqueda semántica":
    st.markdown('<p class="section-header">Búsqueda semántica</p>', unsafe_allow_html=True)
    st.markdown("## Busca por significado, no por palabras")
    st.markdown(
        "El sistema convierte cada reseña en un vector numérico que representa su "
        "significado. Así encuentra reseñas relevantes **aunque no compartan las mismas "
        "palabras** que la consulta."
    )

    st.markdown("")

    consultas_demo = {
        "el producto se rompió muy rápido": [
            (0.87, "2★", "Se ha roto muy rápido, llevaba un mes usándola..."),
            (0.73, "1★", "Fatal, el producto llegó roto y sin protección..."),
            (0.73, "2★", "Mala calidad, se rompió un enganche al mes de comprarla..."),
        ],
        "excelente regalo para niños": [
            (0.85, "5★", "Perfecto como regalo para mi sobrina, le encantó..."),
            (0.79, "5★", "Lo compré para el cumpleaños de mi hijo y fue un acierto..."),
            (0.74, "4★", "Bonito para regalar, buena presentación y calidad..."),
        ],
        "la calidad del sonido es horrible": [
            (0.84, "1★", "El sonido es malísimo, se escucha muy bajo y distorsionado..."),
            (0.78, "2★", "Calidad de audio pésima, no merece la pena para música..."),
            (0.71, "2★", "Esperaba mucho mejor sonido por este precio..."),
        ],
        "envío rápido y bien embalado": [
            (0.82, "5★", "Llegó al día siguiente y muy bien empaquetado..."),
            (0.76, "5★", "Rapidez de envío y protección del paquete impecables..."),
            (0.71, "4★", "Buen embalaje, llegó en perfectas condiciones..."),
        ],
    }

    consulta_elegida = st.selectbox(
        "Elige una consulta de ejemplo:",
        list(consultas_demo.keys()),
    )

    st.markdown(
        f'<div style="background:#EEF2F7;border:1px solid {AZUL};border-radius:12px;'
        f'padding:16px 20px;margin:16px 0">'
        f'<span style="color:{AZUL};font-size:0.85rem">🔍 Consulta</span>'
        f'<p style="font-size:1.15rem;font-weight:500;margin-top:4px">'
        f'"{consulta_elegida}"</p></div>',
        unsafe_allow_html=True,
    )

    resultados = consultas_demo[consulta_elegida]
    for sim, stars, texto in resultados:
        star_color = "#C53030" if "1" in stars or "2" in stars else "#2B6CB0"
        border_color = AZUL_OSCURO if sim > 0.8 else AZUL if sim > 0.7 else LAVANDA
        st.markdown(
            f'<div class="result-card" style="border-left:3px solid {border_color}; '
            f'display:flex;justify-content:space-between;align-items:center">'
            f'<div><span style="color:{star_color};font-weight:600">{stars}</span> '
            f'{texto}</div>'
            f'<span style="color:{border_color};font-weight:700;min-width:80px;'
            f'text-align:right">{int(sim*100)}% sim</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown(
        '<div class="quote-box">'
        "Sentence-BERT + FAISS · 5.000 reseñas indexadas · Búsqueda en menos de 5ms"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# PAGINA: TEMAS LDA
# ─────────────────────────────────────────────
elif pagina == "Temas LDA":
    st.markdown('<p class="section-header">Descubrimiento de temas</p>', unsafe_allow_html=True)
    st.markdown("## LDA descubre lo que el cliente ni sabía que estaba pasando")
    st.markdown(
        "El algoritmo analiza las 210.000 reseñas y agrupa automáticamente las "
        "palabras que tienden a aparecer juntas. El resultado son **8 temas** que "
        "cubren los principales asuntos que mencionan los clientes."
    )

    st.markdown("")

    temas = [
        {"nombre": "Quejas generales", "palabras": "demasiado, malo, pequeño, nunca, tampoco, funda, hace, vez", "color": ROSA},
        {"nombre": "Tamaño y estética", "palabras": "grande, cómodo, solo, ver, aunque, color, cargo, parece", "color": LAVANDA},
        {"nombre": "Envío y logística", "palabras": "caja, material, tiempo, llegado, batería, día, libro, pedido", "color": AZUL},
        {"nombre": "Calidad-precio", "palabras": "calidad, precio, funciona, genial, bonito, punto, genial", "color": AZUL_OSCURO},
        {"nombre": "Audio y superación", "palabras": "buena, mejor, esperaba, sonido, bastante, tener, fácil", "color": AZUL_CLARO},
        {"nombre": "Satisfacción y recomendación", "palabras": "contento, fácil, bastante, relación, calidad, práctico", "color": MELOCOTON},
        {"nombre": "Experiencia de compra", "palabras": "perfectamente, hacer, perfecto, razón, siempre, adecuado", "color": LAVANDA},
        {"nombre": "Regalos y experiencias", "palabras": "contenta, regalo, excelente, tiempo, encantado, luz", "color": ROSA},
    ]

    col1, col2 = st.columns(2)
    for i, tema in enumerate(temas):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(
                f'<div class="metric-card" style="text-align:left;margin-bottom:12px;'
                f'border-left:4px solid {tema["color"]}">'
                f'<span style="color:{tema["color"]};font-size:0.8rem;font-weight:600">'
                f'TEMA {i+1}</span>'
                f'<h4 style="margin:6px 0;font-size:1.05rem">{tema["nombre"]}</h4>'
                f'<p style="font-size:0.85rem;color:#7B8794">{tema["palabras"]}</p>'
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="quote-box">'
        "Estos temas emergen de forma no supervisada. El cliente puede descubrir "
        "tendencias que ni siquiera sabía que existían en sus datos."
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# PAGINA: NEGOCIO
# ─────────────────────────────────────────────
elif pagina == "Negocio":
    st.markdown('<p class="section-header">Modelo de negocio</p>', unsafe_allow_html=True)
    st.markdown("## SaaS con suscripción mensual")

    st.markdown("")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            '<div class="metric-card" style="border-top:4px solid #5B9BD5">'
            '<h4 style="color:#5B9BD5;margin-bottom:8px">Starter</h4>'
            '<div class="metric-number">99€</div>'
            '<div class="metric-label">/mes</div>'
            '<p style="margin-top:16px;font-size:0.85rem;color:#7B8794">'
            "Hasta 5.000 reseñas<br>Sentimiento + categorías<br>Dashboard básico</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="metric-card" style="border-top:4px solid #B8A9D0;'
            'background:linear-gradient(to bottom, rgba(184,169,208,0.06), white)">'
            '<h4 style="color:#7b6fa0;margin-bottom:8px">Growth</h4>'
            '<div class="metric-number" style="color:#7b6fa0">299€</div>'
            '<div class="metric-label">/mes</div>'
            '<p style="margin-top:16px;font-size:0.85rem;color:#7B8794">'
            "Hasta 50.000 reseñas<br>+ NER + Topics + Búsqueda<br>API + Alertas</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="metric-card" style="border-top:4px solid #F2B5D4">'
            '<h4 style="color:#a0456e;margin-bottom:8px">Enterprise</h4>'
            '<div class="metric-number" style="color:#a0456e">Custom</div>'
            '<div class="metric-label">&nbsp;</div>'
            '<p style="margin-top:16px;font-size:0.85rem;color:#7B8794">'
            "Volumen ilimitado<br>Fine-tuning personalizado<br>Integración dedicada</p>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown("### Hoja de ruta")

    r1, r2, r3, r4 = st.columns(4)
    pasos = [
        ("Q2 2026", "MVP", "API REST + Dashboard Streamlit"),
        ("Q3 2026", "Pilotos", "3-5 retailers españoles"),
        ("Q4 2026", "Lanzamiento", "Producto SaaS público"),
        ("2027", "Escala", "Multiidioma + Integraciones"),
    ]
    for col, (periodo, titulo, desc) in zip([r1, r2, r3, r4], pasos):
        with col:
            st.markdown(
                f'<div class="metric-card" style="padding:16px">'
                f'<span style="color:{AZUL};font-weight:600;font-size:0.85rem">'
                f"{periodo}</span>"
                f'<h4 style="margin:6px 0">{titulo}</h4>'
                f'<p style="font-size:0.82rem;color:#7B8794">{desc}</p></div>',
                unsafe_allow_html=True,
            )

    st.markdown("")
    st.markdown(
        '<div class="quote-box">'
        "E-commerce en España: 72.000M€ (2023). Cualquier retailer con presencia "
        "online necesita entender la voz de su cliente. La tecnología ya funciona "
        "— solo falta construir el producto."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown("---")
    st.markdown(
        '<p style="text-align:center;color:#7B8794;font-size:0.9rem">'
        "OpinIA · María Luisa Ros Bolea · malurosbolea@gmail.com · "
        '<a href="https://www.linkedin.com/in/mar%C3%ADa-luisa-ros-bolea-400780160/">'
        "LinkedIn</a> · "
        '<a href="https://malurosbolea-ux.github.io/digital-strategy-portfolio/">'
        "Portfolio</a></p>",
        unsafe_allow_html=True,
    )
