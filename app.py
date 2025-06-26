import os
from dotenv import load_dotenv
import streamlit as st
import openai

# Carga de variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Título de pestaña o Página
st.set_page_config(page_title="Alicorp AI-Studio", page_icon="assets/alicorp_logo_corto_32x32.png", layout="wide")

# Función para definir el prompt y la lógica de negocio
def generar_descripcion_producto(nombre_producto, ingredientes, beneficios, publico, tono):
    """
    Llama a la API de OpenAI para generar descripciones de producto.
    """
    try:
        prompt = f"""
        Actúa como un copywriter experto para Alicorp, especializado en productos de consumo masivo y snacks saludables.
        Tu tarea es generar tres (3) descripciones de producto creativas y atractivas para un nuevo lanzamiento.

        **Información del Producto:**
        - **Nombre:** {nombre_producto}
        - **Ingredientes Clave:** {ingredientes}
        - **Beneficios Principales:** {beneficios}
        - **Público Objetivo:** {publico}

        **Requerimientos:**
        1.  El tono de la comunicación debe ser: **{tono}**.
        2.  Genera tres variantes distintas:
            - **Variante 1 (Para E-commerce):** Una descripción detallada (2-3 párrafos), optimizada para SEO, mencionando los ingredientes y beneficios.
            - **Variante 2 (Para Redes Sociales - Instagram/Facebook):** Un copy corto y pegadizo (2-3 líneas), con un llamado a la acción claro y usando emojis relevantes.
            - **Variante 3 (Para Campañas de Email):** Un texto persuasivo y ligeramente más personal, enfocado en resolver una necesidad del público objetivo.
        3.  Formatea la respuesta usando Markdown para que sea fácil de leer, con títulos claros para cada variante.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini", # Más barato de openai
            messages=[
                {"role": "system", "content": "Eres un asistente de marketing de IA para Alicorp."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7, # Un poco de creatividad
            max_tokens=800
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error al conectar con la API de OpenAI: {e}"

# Interfaz de Usuario
st.image("assets/alicorp_logo_completo.png", width=150)
st.title("🚀 Alicorp AI-Studio") # h1
st.caption("Una herramienta de IA Generativa para acelerar tus lanzamientos")

# Usaremos columnas para un diseño más limpio
col1, col2 = st.columns([1, 1.5]) 

with col1:
    st.subheader("1. Ingresa los datos del producto") # h3
    nombre_producto = st.text_input("Nombre del Producto", "Barras de Energía 'Bryan Boost'")
    ingredientes = st.text_input("Ingredientes Clave", "Quinua, kiwicha, maca")
    beneficios = st.text_area("Beneficios Principales", "Fuente de energía natural, alto en fibra, sin azúcar añadida, ideal para media mañana.", height=70)
    publico = st.text_area("Público Objetivo", "Jóvenes profesionales y estudiantes universitarios (20-35 años) que buscan snacks saludables y prácticos.", height=70)
    
    tonos_disponibles = ["Moderno y Energético", "Confiable y Nutritivo", "Divertido y Juvenil", "Sofisticado y Premium"]
    tono = st.selectbox("Elige el tono de comunicación", tonos_disponibles)
    
    if st.button("✨ Generar Descripciones"):
        if not all([nombre_producto, ingredientes, beneficios, publico, tono]):
            st.warning("Por favor, completa todos los campos.")
        else:
            with st.spinner("Generando... Alimentamos ideas para un mañana mejor..."):
                descripcion_generada = generar_descripcion_producto(nombre_producto, ingredientes, beneficios, publico, tono)
                # Guardamos el resultado en el estado de la sesión para mostrarlo en la otra columna
                st.session_state['descripcion_generada'] = descripcion_generada

with col2:
    st.subheader("2. Resultados Generados por IA")
    if 'descripcion_generada' in st.session_state:
        st.markdown(st.session_state['descripcion_generada'])
    else:
        st.info("Aquí aparecerán las descripciones generadas por la IA.")

# Almacenar input y output en historial dentro de las carpetas