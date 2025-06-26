import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.prompts import (
    DESCRIPCION_PRODUCTO_TEMPLATE,
    ANALISIS_FEEDBACK_TEMPLATE,
    PROMPT_IMAGEN_TEMPLATE
)

# Carga de variables y configuración de la API de Gemini
load_dotenv()

try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    print(f"Error configurando la API de Gemini. Asegúrate de que GOOGLE_API_KEY esté en tu .env: {e}")

# Seleccionamos el modelo de Gemini. 'flash' es rápido y muy capaz para estas tareas.
MODEL_NAME = "gemini-1.5-flash-latest"

def generar_descripcion_producto(nombre_producto, ingredientes, beneficios, publico, tono):
    try:
        # Gemini maneja las instrucciones del sistema en la inicialización del modelo
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction="Actúa como un copywriter experto para Alicorp, especializado en productos de consumo masivo y snacks saludables."
        )
        prompt = DESCRIPCION_PRODUCTO_TEMPLATE.format(
            nombre_producto=nombre_producto,
            ingredientes=ingredientes,
            beneficios=beneficios,
            publico=publico,
            tono=tono
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al conectar con la API de Gemini: {e}"

def analizar_feedback(comentarios):
    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction="Actúa como un Analista de Datos especializado en feedback de clientes para Alicorp."
        )
        prompt = ANALISIS_FEEDBACK_TEMPLATE.format(comentarios=comentarios)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al conectar con la API de Gemini: {e}"

def generar_prompt_imagen(descripcion_producto, estilo_visual):
    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction="Actúa como un Director de Arte y Experto en Prompt Engineering para Alicorp. Tu respuesta debe estar completamente en español."
        )
        prompt = PROMPT_IMAGEN_TEMPLATE.format(
            descripcion_producto=descripcion_producto,
            estilo_visual=estilo_visual
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al conectar con la API de Gemini: {e}"

# La API de Google Generative AI (gratuita) no tiene un endpoint de generación de imágenes
def generar_imagen_gemini(prompt_detallado, quality="standard", size="1024x1024"):
    return "Error: La generación de imágenes no está disponible con la API de Gemini en esta configuración. Por favor, usa OpenAI (DALL-E) para esta función."