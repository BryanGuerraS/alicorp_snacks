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

# Función que genera el prompt para la imagen
def generar_prompt_imagen(descripcion_producto, estilo_visual):
    # Usa la IA para generar prompts detallados para modelos de generación de imágenes.
    try:
        prompt = f"""
        Actúa como un Director de Arte y Experto en Prompt Engineering para Alicorp. Tu respuesta debe estar completamente en **español**.
        Tu misión es convertir la descripción de un producto en **tres (3) ideas de prompt** para un modelo de IA de texto a imagen como DALL-E 3.

        **Descripción del Producto Base:**{descripcion_producto}
        **Estilo Visual Requerido:**{estilo_visual}

        **Instrucciones de Formato (MUY IMPORTANTE):**
        1.  Para cada idea, crea un título grande y llamativo en español (ej. "### Idea de Prompt 1: Energía Matutina").
        2.  Debajo del título, añade una sección llamada "**Prompt (en inglés):**".
        3.  **El texto del prompt que sigue a "Prompt (en inglés):" DEBE estar en inglés**, ya que es el idioma óptimo para DALL-E. Este prompt debe ser muy detallado.
        4.  Debajo del prompt en inglés, añade una breve sección llamada "**Explicación:**" en español, describiendo por qué esa idea visual es efectiva para el marketing del producto.
        5.  Usa Markdown para formatear toda la respuesta y hacerla fácil de leer.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente de dirección de arte bilingüe para Alicorp. Respondes en español pero creas prompts técnicos en inglés."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8, # Más creatividad para las imágenes
            max_tokens=1000
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error al conectar con la API de OpenAI: {e}"
    
# Función que genera la imagen con dall-e
def generar_imagen_dalle(prompt_detallado, quality="standard", size="1024x1024"):
    # Llama a la API de DALL-E 3 de OpenAI para generar una imagen.
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt_detallado,
            n=1,  # Generamos una sola imagen por llamada
            size=size, # DALL-E 3 soporta "1024x1024", "1792x1024", o "1024x1792"
            quality=quality, # "standard" o "hd"
        )
        # La API devuelve un objeto, la URL de la imagen está dentro
        image_url = response.data[0].url
        return image_url
    except openai.BadRequestError as e:
        # Esto es útil para capturar cuando el prompt es rechazado por el filtro de seguridad
        st.error(f"Error: Tu solicitud fue rechazada por el sistema de seguridad de OpenAI. Intenta con un prompt más simple. Detalles: {e}")
        return None
    except Exception as e:
        st.error(f"Error al generar la imagen con DALL-E: {e}")
        return None

### Interfaz de Usuario | Streamlit
st.image("assets/alicorp_logo_completo.png", width=150)
st.title("🚀 Alicorp AI-Studio") # h1
st.caption("Una herramienta de IA Generativa para acelerar tus lanzamientos")

tab1, tab2, tab3 = st.tabs(["✍️ Generador de Contenido", "📊 Analizador de Feedback", "🎨 Arte Promocional"])

with tab1:
    # col1: Menú para ingresar datos
    # col_div: Columna usada como espaciado
    # col2: Menú para mostrar los resultados
    st.header("Generador de Descripciones de Producto")
    col1, col_div, col2 = st.columns([1, 0.05, 1.5]) 

    with col1:
        st.subheader("1. Ingresa los datos del producto") # h3
        nombre_producto = st.text_input("Nombre del Producto", "Barras de Energía 'Bryan Boost'")
        ingredientes = st.text_input("Ingredientes Clave", "Quinua, kiwicha, maca")
        beneficios = st.text_area("Beneficios Principales", "Fuente de energía natural, alto en fibra, sin azúcar añadida, ideal para media mañana.", height=70)
        publico = st.text_area("Público Objetivo", "Jóvenes profesionales y estudiantes universitarios (20-35 años) que buscan snacks saludables y prácticos.", height=70)
        
        tonos_disponibles = ["Moderno y Energético", "Confiable y Nutritivo", "Divertido y Juvenil", "Sofisticado y Premium"]
        tono = st.selectbox("Elige el tono de comunicación", tonos_disponibles)
        
        if st.button("✨ Generar Descripciones", key="btn_generar"):
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
    # col1_fb: Menú para ingresar datos
    # col_div_fb: Columna usada como espaciado
    # col2_fb: Menú para mostrar los resultados
    st.header("📊 Análisis de Feedback de Clientes")
    col1_fb, col_div_fb, col2_fb = st.columns([1, 0.05, 1.5])

    with col1_fb:
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
    with col_div_fb:
        st.markdown(
            """<div style='height: 100%; border-left: 1px solid #ccc;'></div>""",
            unsafe_allow_html=True
        )

    with col2_fb:
        st.subheader("2. Resultados del Análisis")
        
        if 'analisis_resultado' in st.session_state:
            # Mostramos el resultado que se generó y guardó desde la columna izquierda
            st.markdown(st.session_state['analisis_resultado'])
        else:
            st.info("Aquí aparecerá el análisis generado por la IA.")

with tab3:
    st.header("Ideación de Imágenes Promocionales")
    st.markdown("Genera ideas y prompts para crear imágenes de producto impactantes.")
    
    col1_img, col_img_fb, col2_img = st.columns([1, 0.05, 1.5])

    with col1_img:
        st.subheader("Paso 1: Describe tu producto y visión (Opcional)")
        descripcion_para_imagen = st.text_area(
            "Describe brevemente el producto o la escena que quieres visualizar", 
            "Una barra energética llamada 'Andean Boost', hecha con quinua y cacao. Quiero que se vea saludable, natural y perfecta para una pausa en el trabajo.",
            height=150
        )
        
        estilos_visuales = ["Fotografía Publicitaria (Hiperrealista)", "Estilo de Vida (Lifestyle)", "Ilustración Digital Plana", "Plano Cenital (Flat Lay)"]
        estilo_visual = st.selectbox("Elige un estilo visual", estilos_visuales)

        # Mejoramos el prompt de imagen a usar
        if st.button("🎨 Optimizar Prompts de Imagen"):
            if not descripcion_para_imagen.strip():
                st.warning("Por favor, describe el producto o la escena.")
            else:
                with st.spinner("Optimizando prompt..."):
                    prompt_resultado = generar_prompt_imagen(descripcion_para_imagen, estilo_visual)
                    st.session_state['prompt_resultado'] = prompt_resultado

        # Mostramos los prompts generados aquí mismo en la columna izquierda
        if 'prompt_resultado' in st.session_state:
            st.markdown("---")
            st.write("#### Ideas de Prompt generadas:")
            st.info("Copia uno de estos prompts (o parte de ellos) en el Paso 2.", icon="👇")
            st.markdown(st.session_state['prompt_resultado'])

        st.markdown("---")
        st.subheader("Paso 2: Crea tu imagen")
        prompt_final_para_dalle = st.text_area(
            "Pega o escribe aquí el prompt final para DALL-E 3", 
            height=150,
            key="prompt_final"
        )

        # Opciones avanzadas para el usuario
        col_quality, col_size = st.columns(2)
        with col_quality:
            quality = st.selectbox("Calidad", ("standard", "hd"), help="HD crea imágenes con más detalle, pero puede tardar más y tiene un costo mayor.")
        with col_size:
            size = st.selectbox("Tamaño", ("1024x1024", "1792x1024", "1024x1792"))
            
        if st.button("🖼️ Crear Imagen", type="primary"):
            if not prompt_final_para_dalle.strip():
                st.warning("Por favor, ingresa un prompt para generar la imagen.")
            else:
                # La generación de imágenes puede tardar, el spinner es crucial
                with st.spinner("Generando arte promocional..."):
                    imagen_url = generar_imagen_dalle(prompt_final_para_dalle, quality, size)
                    if imagen_url:
                        st.session_state['imagen_generada_url'] = imagen_url
                        # Limpiamos el resultado del prompt de texto para no confundir
                        if 'prompt_resultado' in st.session_state:
                            del st.session_state['prompt_resultado']

    with col_div_fb:
        st.markdown(
            """<div style='height: 100%; border-left: 1px solid #ccc;'></div>""",
            unsafe_allow_html=True
        )

    with col2_img:
        st.subheader("Resultado Visual")

        if 'imagen_generada_url' in st.session_state:
            st.image(st.session_state['imagen_generada_url'], caption="Imagen generada por DALL-E 3")
            st.success("¡Imagen generada con éxito!")
        else:
            st.info("Aquí aparecerá la imagen promocional generada por la IA.")

# Posibles mejoras
# Almacenar input y output en historial dentro de las carpetas