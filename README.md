<div align="center">
  <img src="OpinIA_Logo.png" alt="Logo de OpinIA" width="250"/>
</div>

# OpinIA — Inteligencia de reputación online para e-commerce español

Dashboard interactivo de la prueba de concepto (PoC) de **OpinIA**, un sistema de análisis automatizado de reseñas de productos usando Procesamiento del Lenguaje Natural (PLN).

**Práctica de PLN · Máster en Big Data e IA · CEU San Pablo · 2026**

## Demo en vivo

👉 **[Abrir la app en Streamlit](https://opinia-demo.streamlit.app)**

## ¿Qué es OpinIA?

OpinIA procesa automáticamente reseñas de e-commerce con PLN avanzado:

- **Análisis de sentimiento** con BERT multilingüe (F1: 0.76)
- **Clasificación zero-shot** con BART (categorías personalizadas sin reentrenamiento)
- **Extracción de entidades** (NER) para detectar marcas
- **Descubrimiento de temas** con LDA (no supervisado)
- **Búsqueda semántica** con Sentence-BERT + FAISS

## Estructura del repositorio

```
opinia-demo/
├── streamlit_app.py        # App principal
├── OpinIA_Logo.png         # Logo del proyecto
├── requirements.txt        # Dependencias
├── .streamlit/
│   └── config.toml         # Tema visual
└── README.md
```

## Autora

**María Luisa Ros Bolea**

- [LinkedIn](https://www.linkedin.com/in/mar%C3%ADa-luisa-ros-bolea-400780160/)
- [Portfolio](https://malurosbolea-ux.github.io/digital-strategy-portfolio/)
- malurosbolea@gmail.com
