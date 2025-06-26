import os
import openai
from dotenv import load_dotenv
from src.prompts import (
    DESCRIPCION_PRODUCTO_TEMPLATE,
    ANALISIS_FEEDBACK_TEMPLATE,
    PROMPT_IMAGEN_TEMPLATE
)

# Carga de variables de entorno y configuración de la API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generar_descripcion_producto(nombre_producto, ingredientes, beneficios, publico, tono):
    try:
        prompt = DESCRIPCION_PRODUCTO_TEMPLATE.format(
            nombre_producto=nombre_producto,
            ingredientes=ingredientes,
            beneficios=beneficios,
            publico=publico,
            tono=tono
        )
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente de marketing de IA para Alicorp."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al conectar con la API de OpenAI: {e}"

def analizar_feedback(comentarios):
    try:
        prompt = ANALISIS_FEEDBACK_TEMPLATE.format(comentarios=comentarios)
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente de análisis de datos para Alicorp."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al conectar con la API de OpenAI: {e}"

def generar_prompt_imagen(descripcion_producto, estilo_visual):
    try:
        prompt = PROMPT_IMAGEN_TEMPLATE.format(
            descripcion_producto=descripcion_producto,
            estilo_visual=estilo_visual
        )
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente de dirección de arte bilingüe para Alicorp. Respondes en español pero creas prompts técnicos en inglés."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al conectar con la API de OpenAI: {e}"

def generar_imagen_dalle(prompt_detallado, quality="standard", size="1024x1024"):
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt_detallado,
            n=1,
            size=size,
            quality=quality,
        )
        return response.data[0].url
    except Exception as e:
        print(f"Error en DALL-E: {e}")
        
        if isinstance(e, openai.BadRequestError):
            return f"Error: Tu solicitud fue rechazada por el sistema de seguridad de OpenAI. Intenta con un prompt más simple. Detalles: {e}"
        return f"Error al generar la imagen con DALL-E: {e}"