import os
from dotenv import load_dotenv
import streamlit as st
import openai

# Carga de variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Título de pestaña o Página
st.set_page_config(page_title="Alicorp AI-Studio", page_icon="assets/alicorp_logo_corto_32x32.png", layout="wide")

### Funciones de Negocio o módulos

# Función del prompt que genera la descripción del producto
def generar_descripcion_producto(nombre_producto, ingredientes, beneficios, publico, tono):
    # Llama a la API de OpenAI para generar descripciones de producto.
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
            - **1. E-commerce:** Una descripción detallada (1 párrafo), optimizada para SEO, mencionando los ingredientes y beneficios.
            - **2. Redes Sociales - Instagram/Facebook/etc:** Un copy corto y pegadizo (2-3 líneas), con un llamado a la acción claro y usando emojis relevantes.
            - **3. Campañas de Email:** Un texto persuasivo y ligeramente más personal, enfocado en resolver una necesidad del público objetivo.
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

# Función del prompt que analiza el feedback
def analizar_feedback(comentarios):
    # Usa la IA para resumir y analizar comentarios de clientes.
    try:
        prompt = f"""
        Actúa como un Analista de Datos especializado en feedback de clientes para Alicorp.
        Tu tarea es analizar el siguiente bloque de comentarios de usuarios sobre un nuevo producto.

        **Comentarios de Usuarios:**
        ---
        {comentarios}
        ---

        **Análisis Requerido:**
        Realiza un análisis conciso y presenta los resultados en formato Markdown. Cubre los siguientes puntos:
        1.  **Sentimiento General:** Resume el sentimiento predominante (ej. "Mayormente Positivo", "Mixto con críticas constructivas").
        2.  **Temas Positivos Recurrentes:** Lista los 3 aspectos que más gustaron a los clientes (ej. Sabor, Textura, Empaque).
        3.  **Áreas de Mejora:** Lista las 3 críticas o sugerencias más comunes.
        4.  **Cita Destacada:** Extrae una cita textual (positiva o negativa) que resuma bien una opinión popular.
        """
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente de análisis de datos para Alicorp."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3, # Menos creativo
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al conectar con la API de OpenAI: {e}"
    
### Interfaz de Usuario | Streamlit
st.image("assets/alicorp_logo_completo.png", width=150)
st.title("🚀 Alicorp AI-Studio") # h1
st.caption("Una herramienta de IA Generativa para acelerar tus lanzamientos")

tab1, tab2 = st.tabs(["✍️ Generador de Contenido", "📊 Analizador de Feedback"])

with tab1:
    # col1: Menú para ingresar datos
    # col_div: Columna usada como espaciado
    # col2: Menú para mostrar los resultados
    col1, col_div, col2 = st.columns([1, 0.05, 1.5]) 

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
    with col_div:
        st.markdown(
            """<div style='height: 100%; border-left: 1px solid #ccc;'></div>""",
            unsafe_allow_html=True
        )

    with col2:
        st.subheader("2. Resultados Generados por IA")
        if 'descripcion_generada' in st.session_state:
            st.markdown(st.session_state['descripcion_generada'])
        else:
            st.info("Aquí aparecerán las descripciones generadas por la IA.")

with tab2:
    # col1: Menú para ingresar datos
    # col_div: Columna usada como espaciado
    # col2: Menú para mostrar los resultados

    st.header("📊 Análisis de Feedback de Clientes")
    
    # Creamos las dos columnas, manteniendo la proporción para consistencia
    col1, col_div, col2 = st.columns([1, 0.05, 1.5])

    with col1:
        st.subheader("1. Ingresa los comentarios")
        
        sample_comments = """
        - "Me encantó el sabor de la barra Andean Boost, no es muy dulce y se siente natural. ¡Perfecta para la oficina!"
        - "La textura es increíble, crocante pero no dura. El empaque es práctico pero un poco difícil de abrir a veces."
        - "Buen producto, aunque me pareció un poco caro para el tamaño que tiene. Quizás un pack de 3 sería mejor."
        - "¡La mejor barra que he probado! La compré en el marketplace y llegó al día siguiente. Súper recomendada."
        - "El sabor a cacao es muy ligero, me gustaría que fuera más intenso. Por lo demás, todo bien."
        """
        # Aumentamos un poco la altura para que se vea mejor en la columna
        comentarios = st.text_area("Pega los comentarios de tus clientes aquí:", sample_comments, height=350)

        if st.button("📈 Analizar Feedback"):
            if not comentarios.strip(): # Usamos .strip() para evitar que espacios en blanco cuenten como input
                st.warning("Por favor, ingresa algunos comentarios para analizar.")
            else:
                with st.spinner("Analizando opiniones..."):
                    analisis_resultado = analizar_feedback(comentarios)
                    st.session_state['analisis_resultado'] = analisis_resultado
    with col_div:
        st.markdown(
            """<div style='height: 100%; border-left: 1px solid #ccc;'></div>""",
            unsafe_allow_html=True
        )

    with col2:
        st.subheader("2. Resultados del Análisis")
        
        if 'analisis_resultado' in st.session_state:
            # Mostramos el resultado que se generó y guardó desde la columna izquierda
            st.markdown(st.session_state['analisis_resultado'])
        else:
            st.info("Aquí aparecerá el análisis generado por la IA.")

# Posibles mejoras
# Almacenar input y output en historial dentro de las carpetas