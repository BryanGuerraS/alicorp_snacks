# 🚀 Alicorp AI-Studio

**Alicorp AI-Studio** es una aplicación web de IA Generativa diseñada para acelerar los procesos de lanzamiento de nuevos productos en Alicorp. Esta herramienta aborda los cuellos de botella clave en la creación de contenido de marketing y el análisis de feedback de clientes, permitiendo a los equipos comerciales y de marketing ser más ágiles, creativos y basados en datos.

---

## ✨ Features Clave

La aplicación está organizada en tres módulos principales, con la flexibilidad de usar diferentes proveedores de IA:

### ✍️ Generador de Contenido:
- Crea automáticamente descripciones de producto optimizadas para distintos canales (E-commerce, Redes Sociales, Email Marketing).
- Permite personalizar el tono de la comunicación para alinearse con la estrategia de marca.

### 📊 Analizador de Feedback:
- Procesa y resume grandes volúmenes de comentarios de clientes en segundos.
- Extrae el sentimiento general, temas positivos, áreas de mejora y citas destacadas para obtener insights accionables.

### 🎨 Arte Promocional:
- **Ideación de Prompts**: Actúa como un director de arte virtual, sugiriendo prompts detallados para la creación de imágenes.
- **Generación de Imágenes**: Crea material visual de alta calidad y listo para usar en campañas, utilizando modelos de última generación como DALL·E 3 (OpenAI) y Imagen 2 (Google Cloud Vertex AI).

---

## 🛠️ Tech Stack & Arquitectura

La solución está construida con un enfoque en la modularidad y escalabilidad, utilizando herramientas modernas y prácticas recomendadas.

- **Frontend**: Streamlit  
- **Backend & Lógica**: Python  
- **Proveedores de IA**:  
  - OpenAI (GPT-4o-mini, DALL·E 3)  
  - Google AI Studio (Gemini 1.5 Flash - Capa gratuita)  
  - Google Cloud Vertex AI (Gemini 1.5 Flash & Imagen 2 - Usando créditos de GCP)  
- **Gestión de Dependencias**: `pip` y `virtualenv`

---

## 📁 Estructura del Proyecto

```console
├── src/
│ ├── openai_services.py 	# Lógica para interactuar con la API de OpenAI
│ ├── gemini_services.py 	# Lógica para la API gratuita de Google AI Studio
│ ├── vertexai_services.py 	# Lógica para la API empresarial de Vertex AI
│ └── prompts.py 		# Centraliza todas las plantillas de prompts
├── assets/ 			# Logos e imágenes estáticas
├── outputs/ 			# Carpeta para las imágenes generadas por Vertex AI
├── .env.example 		# Plantilla para las variables de entorno
├── app.py 			# Script principal de la aplicación Streamlit (UI)
├── requirements.txt 		# Dependencias del proyecto
└── README.md 			# Esta guía
```

---

## 🚀 Cómo Ejecutar el Proyecto

### 1. Prerrequisitos
- Python 3.9+
- Git
- (Opcional para Vertex AI) Google Cloud SDK (`gcloud CLI`) instalado

---

### 2. Clonar el Repositorio

```console
git clone https://github.com/tu-usuario/alicorp_snacks.git
cd alicorp_snacks
```

### 3. Configurar el Entorno Virtual
```console
# Crear el entorno virtual
python -m venv venv

# Activar el entorno
# En Windows:
.\venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 4. Instalar Dependencias
```console
pip install -r requirements.txt
```

### 5. Configurar Credenciales
```console
# Clave de API de OpenAI
OPENAI_API_KEY="sk-..."

# Clave de API de Google AI Studio (para el modo gratuito de Gemini)
GOOGLE_API_KEY="AIzaSy..."

# ID del Proyecto de Google Cloud (para Vertex AI)
GCP_PROJECT_ID="tu-proyecto-id-aqui"

# Región de Google Cloud (opcional, por defecto us-central1)
GCP_REGION="us-central1"
```

### 6. Autenticación para Vertex AI (Opcional)
```console
gcloud auth application-default login
```
Esto abrirá el navegador para iniciar sesión y permitir el uso de Vertex AI desde tu entorno local.

7. ¡Ejecutar la Aplicación!
```console
streamlit run app.py
```
La aplicación se abrirá automáticamente en tu navegador web.