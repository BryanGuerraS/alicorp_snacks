### Importancion de librerias y funciones
import os
import streamlit as st
from dotenv import load_dotenv

from src import openai_services
from src import gemini_services
from src import vertexai_services

# Carga las variables de entorno
load_dotenv()

### Titulo de pestaña
st.set_page_config(page_title="Alicorp AI-Studio", page_icon="assets/alicorp_logo_corto_32x32.png", layout="wide")

# Sidebar para selección de modelo 
st.sidebar.image("assets/alicorp_logo_completo.png", width=150)
st.sidebar.title("Configuración")
provider = st.sidebar.radio(
    "Elige tu proveedor de IA:",
    ("OpenAI", "Gemini (Gratuito)", "Vertex AI (Créditos GCP)"),
    index=0, # Por defecto OpenAI
    help="Elige el motor de IA. Vertex AI usa tus créditos de GCP y puede generar imágenes."
)

# Seleccionar el servicio y verificar la API Key
IMAGE_GEN_AVAILABLE = False
if provider == "OpenAI":
    if not os.getenv("OPENAI_API_KEY"):
        st.error("No se encontró la clave de API de OpenAI. Por favor, añádela a tu archivo .env.")
        st.stop()
    service_module = openai_services
    generar_imagen = openai_services.generar_imagen_dalle
    IMAGE_GEN_AVAILABLE = True

elif provider == "Gemini (Gratuito)":
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("No se encontró la clave de API de Gemini. Por favor, añádela a tu archivo .env.")
        st.stop()
    service_module = gemini_services
    generar_imagen = gemini_services.generar_imagen_gemini # Esta función devuelve un error informativo
    IMAGE_GEN_AVAILABLE = False

elif provider == "Vertex AI (Créditos GCP)":
    if not os.getenv("GCP_PROJECT_ID"):
        st.error("No se encontró el GCP_PROJECT_ID. Por favor, añádelo a tu archivo .env.")
        st.stop()
    service_module = vertexai_services
    generar_imagen = vertexai_services.generar_imagen_vertex
    IMAGE_GEN_AVAILABLE = True

# Asignamos las funciones de texto del módulo seleccionado
generar_descripcion_producto = service_module.generar_descripcion_producto
analizar_feedback = service_module.analizar_feedback
generar_prompt_imagen = service_module.generar_prompt_imagen



### Interfaz de Usuario | Streamlit ###
st.title("🚀 Alicorp AI-Studio") # h1
st.markdown(f"""<div style='font-size:18px; color:#6c757d'>
                    Una herramienta de IA Generativa para acelerar tus lanzamientos | IA: <b>{provider}</b>
                </div>""", unsafe_allow_html=True)

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
                with st.spinner(f"Generando con {provider}... Alimentamos ideas para un mañana mejor..."):
                    descripcion_generada = generar_descripcion_producto(nombre_producto, ingredientes, beneficios, publico, tono)
                    st.session_state['descripcion_generada'] = descripcion_generada # Guardamos el resultado en el estado de la sesión para mostrarlo en la otra columna
    with col_div:
        st.markdown("""<div style='height: 100%; border-left: 1px solid #ccc;'></div>""", unsafe_allow_html=True)

    with col2:
        st.subheader(f"2. Resultados Generados por {provider}")
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
        - "Me encantó el sabor de la barra Bryan Boost, no es muy dulce y se siente natural. ¡Perfecta para la oficina!"
        - "La textura es increíble, crocante pero no dura. El empaque es práctico pero un poco difícil de abrir a veces."
        - "Buen producto, aunque me pareció un poco caro para el tamaño que tiene. Quizás un pack de 3 sería mejor."
        - "¡La mejor barra que he probado! La compré en el marketplace y llegó al día siguiente. Súper recomendada."
        - "El sabor a cacao es muy ligero, me gustaría que fuera más intenso. Por lo demás, todo bien."
        """
        comentarios = st.text_area("Pega los comentarios de tus clientes aquí:", sample_comments, height=350)

        if st.button("📈 Analizar Feedback"):
            if not comentarios.strip(): # Usamos .strip() para evitar que espacios en blanco cuenten como input
                st.warning("Por favor, ingresa algunos comentarios para analizar.")
            else:
                with st.spinner(f"Analizando opiniones con {provider}..."):
                    analisis_resultado = analizar_feedback(comentarios)
                    st.session_state['analisis_resultado'] = analisis_resultado
    with col_div_fb:
        st.markdown("""<div style='height: 100%; border-left: 1px solid #ccc;'></div>""", unsafe_allow_html=True)

    with col2_fb:
        st.subheader("2. Resultados del Análisis")
        
        if 'analisis_resultado' in st.session_state:
            # Mostramos el resultado que se generó y guardó desde la columna izquierda
            st.markdown(st.session_state['analisis_resultado'])
        else:
            st.info("Aquí aparecerá el análisis generado por la IA.")

with tab3:
    st.header("Creación de Imágenes Promocionales")
    st.markdown("Genera ideas y prompts para crear imágenes de productos impactantes.")
    
    col1_img, col_img_fb, col2_img = st.columns([1, 0.05, 1.5])

    with col1_img:
        st.subheader("Paso 1: Describe tu producto y visión")
        descripcion_para_imagen = st.text_area(
            "Describe brevemente el producto o la escena que quieres visualizar", 
            "Una barra energética llamada 'Bryan Boost', hecha con quinua y cacao. Quiero que se vea saludable, natural y perfecta para una pausa en el trabajo.",
            height=150
        )
        
        estilos_visuales = ["Fotografía Publicitaria (Hiperrealista)", "Estilo de Vida (Lifestyle)", "Ilustración Digital Plana", "Plano Cenital (Flat Lay)"]
        estilo_visual = st.selectbox("Elige un estilo visual", estilos_visuales)

        # Mejoramos el prompt de imagen a usar
        if st.button("🎨 Optimizar Prompts de Imagen"):
            if not descripcion_para_imagen.strip():
                st.warning("Por favor, describe el producto o la escena.")
            else:
                with st.spinner(f"Optimizando prompt con {provider}..."):
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

        if not IMAGE_GEN_AVAILABLE:
            st.warning(f"La generación de imágenes no está disponible para {provider}. Por favor, cambia a OpenAI o Vertex AI.")

        prompt_final = st.text_area("Pega o escribe aquí el prompt final para la imagen", height=150, key="prompt_final", disabled=not IMAGE_GEN_AVAILABLE)

        # En Vertex AI, los parámetros son complejos, así que los deshabilitamos para simplificar la UI.
        st.info("Nota: Los controles de calidad y tamaño solo aplican a OpenAI.", icon="ℹ️")
        col_quality, col_size = st.columns(2)
        with col_quality:
            quality = st.selectbox("Calidad", ("standard", "hd"), disabled=(provider != "OpenAI"))
        with col_size:
            size = st.selectbox("Tamaño", ("1024x1024", "1792x1024", "1024x1792"), disabled=(provider != "OpenAI"))
        
        if st.button("🖼️ Crear Imagen", type="primary", disabled=not IMAGE_GEN_AVAILABLE):
            if not prompt_final.strip():
                st.warning("Por favor, ingresa un prompt para generar la imagen.")
            else:
                with st.spinner(f"Generando arte promocional con {provider}... ¡Esto puede tardar un minuto!"):
                    resultado_imagen = generar_imagen(prompt_final, quality, size)
                    if resultado_imagen:
                        # Si el resultado es una URL de OpenAI
                        if resultado_imagen.startswith('http'):
                            st.session_state['imagen_generada'] = resultado_imagen
                            st.session_state['imagen_tipo'] = 'url'
                        # Si es una ruta local de Vertex AI
                        elif os.path.exists(resultado_imagen):
                            st.session_state['imagen_generada'] = resultado_imagen
                            st.session_state['imagen_tipo'] = 'local'
                        # Si es un mensaje de error
                        else:
                            st.error(resultado_imagen)
                        
                        if 'prompt_resultado' in st.session_state:
                            del st.session_state['prompt_resultado']

    with col_div_fb:
        st.markdown("""<div style='height: 100%; border-left: 1px solid #ccc;'></div>""", unsafe_allow_html=True)

    with col2_img:
        st.subheader("Resultado Visual")

        if 'imagen_generada' in st.session_state:
            image_path_or_url = st.session_state['imagen_generada']
            st.image(image_path_or_url, caption=f"Imagen generada por {provider}")
            st.success("¡Imagen generada con éxito!")

            # Ofrecer descarga para imágenes locales
            if st.session_state.get('imagen_tipo') == 'local':
                with open(image_path_or_url, "rb") as file:
                    st.download_button(
                        label="Descargar Imagen",
                        data=file,
                        file_name=os.path.basename(image_path_or_url),
                        mime="image/png"
                    )
        else:
            st.info("Aquí aparecerá la imagen promocional generada por la IA.")