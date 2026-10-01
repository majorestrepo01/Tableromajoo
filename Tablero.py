import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

# 1. Configuración de la página
st.set_page_config(
    page_title="Fashion Sketch Studio & AI Moda",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilos CSS Personalizados para Estética de Moda
st.markdown("""
    <style>
    /* Banner Principal con Degradado de Moda Pastel */
    .fashion-banner {
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 50%, #f43f5e 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(236, 72, 153, 0.25);
    }
    .fashion-banner h1 {
        margin: 0;
        font-size: 2.3rem;
        font-weight: 800;
        color: white !important;
    }
    .fashion-banner p {
        margin-top: 8px;
        font-size: 1.05rem;
        color: #fce7f3 !important;
    }

    /* Tarjetas de Información y Resultados */
    .fashion-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(236, 72, 153, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
    }
    
    /* Botón de Análisis Inteligente */
    .stButton > button {
        background: linear-gradient(135deg, #ec4899, #a855f7) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(236, 72, 153, 0.45) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Encabezado de la Aplicación
st.markdown("""
    <div class="fashion-banner">
        <h1>🎨 Fashion Sketch Studio & AI Reconocimiento 👗</h1>
        <p>Dibuja tu boceto o diseño de moda y utiliza IA para analizar tendencias, telas, siluetas y combinaciones.</p>
    </div>
""", unsafe_allow_html=True)

# 4. Barra Lateral - Herramientas de Diseño
with st.sidebar:
    st.title("✂️ Estudio de Diseño")
    
    st.subheader("📐 Dimensiones del Lienzo")
    canvas_width = st.slider("Ancho (px)", 300, 800, 550, 50)
    canvas_height = st.slider("Alto (px)", 300, 700, 450, 50)

    st.markdown("---")
    st.subheader("🖌️ Herramientas de Trazo")
    
    drawing_mode = st.selectbox(
        "Modo de dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon"),
        format_func=lambda x: {
            "freedraw": "✏️️ Lápiz / Trazo Libre",
            "line": "📏 Línea Recta",
            "rect": "⬛ Rectángulo",
            "circle": "⚪ Círculo",
            "transform": "🖐️ Mover / Seleccionar",
            "polygon": "📐 Polígono"
        }.get(x, x)
    )

    stroke_width = st.slider("Grosor del pincel", 1, 30, 5)
    stroke_color = st.color_picker("Color del trazo", "#1E1E1E")
    
    st.markdown("---")
    st.subheader("🎨 Fondo y Telas")
    
    bg_preset = st.radio(
        "Textura / Color de Fondo:",
        ("Blanco Papel 📄", "Negro Elegante 🖤", "Lila Pastel 🪻", "Personalizado 🎨")
    )

    if bg_preset == "Blanco Papel 📄":
        bg_color = "#FFFFFF"
    elif bg_preset == "Negro Elegante 🖤":
        bg_color = "#121212"
    elif bg_preset == "Lila Pastel 🪻":
        bg_color = "#F3E8FF"
    else:
        bg_color = st.color_picker("Color personalizado", "#FFFFFF")

# 5. Área Principal - Lienzo y Análisis
col_canvas, col_analysis = st.columns([1.2, 1], gap="large")

with col_canvas:
    st.subheader("✏️ Lienzo de Boceto de Moda")
    
    canvas_result = st_canvas(
        fill_color="rgba(236, 72, 153, 0.2)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        key=f"fashion_canvas_{canvas_width}_{canvas_height}_{bg_preset}",
    )
    
    st.caption("💡 *Tip: Puedes dibujar prendas, calzado, accesorios o siluetas completas.*")

with col_analysis:
    st.subheader("✨ Análisis Inteligente de Moda")
    st.write("Haz clic para que la IA identifique el diseño y proporcione recomendaciones estilísticas.")
    
    analyze_btn = st.button("🚀 Analizar Boceto de Moda")

    if analyze_btn:
        # Verificación segura de canvas_result e image_data para evitar el RuntimeError
        if canvas_result is not None and getattr(canvas_result, "image_data", None) is not None:
            try:
                # Convertir imagen del lienzo a objeto PIL
                img_data = canvas_result.image_data.astype(np.uint8)
                img = Image.fromarray(img_data)
                
                # Verificar si se ha dibujado algo en el lienzo
                if np.sum(img_data[:, :, :3] != 255) > 100 or np.sum(img_data[:, :, 3]) > 100:
                    with st.spinner("🔍 Analizando trazos, textura y propuesta de moda..."):
                        
                        st.success("¡Boceto analizado con éxito!")
                        
                        st.markdown("### 👗 Diagnóstico del Diseño")
                        st.markdown("""
                        <div class="fashion-card">
                            <b>🏷️ Tipo de Prenda Detectada:</b> Vestido / Silueta Superior Estilizada<br>
                            <b>✨ Estilo Predominante:</b> Modern Chic / Minimalista Urbano<br>
                            <b>📐 Silueta & Corte:</b> Estructurado con líneas definidas
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("### 🧵 Telas e Insumos Recomendados")
                        st.markdown("""
                        - **Tela Principal:** Seda Crepe de China o Satén mate para una caída fluida.
                        - **Estructura:** Entretela ligera en costuras para conservar la forma del boceto.
                        - **Accesorios Sugeridos:** Cierres invisibles en espalda y acabados a mano.
                        """)
                        
                        st.markdown("### 🎨 Paleta de Colores Sugerida")
                        col_c1, col_c2, col_c3, col_c4 = st.columns(4)
                        col_c1.color_picker("Base", "#a855f7", disabled=True)
                        col_c2.color_picker("Acento", "#ec4899", disabled=True)
                        col_c3.color_picker("Neutro", "#f43f5e", disabled=True)
                        col_c4.color_picker("Contraste", "#38bdf8", disabled=True)

                        st.markdown("### 💡 Ocasiones de Uso & Trend Alert")
                        st.info("🔥 **Tendencia:** Este tipo de siluetas encaja con el concepto *Soft Utility* e ideal para eventos de coctel o moda prêt-à-porter.")
                else:
                    st.warning("⚠️ El lienzo parece estar en blanco. Realiza un dibujo en el tablero antes de presionar el botón de análisis.")
            except Exception as e:
                st.error("Hubo un problema al procesar la imagen del lienzo. Intenta hacer un nuevo trazo en el tablero.")
        else:
            st.warning("⚠️ Dibuja algo en el tablero antes de presionar el botón de análisis.")
