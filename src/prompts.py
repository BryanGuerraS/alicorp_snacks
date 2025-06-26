# Plantillas de prompts para los servicios de IA de Alicorp

DESCRIPCION_PRODUCTO_TEMPLATE = """
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

ANALISIS_FEEDBACK_TEMPLATE = """
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

PROMPT_IMAGEN_TEMPLATE = """
Actúa como un Director de Arte y Experto en Prompt Engineering para Alicorp. Tu respuesta debe estar completamente en **español**.
Tu misión es convertir la descripción de un producto en **tres (3) ideas de prompt** para un modelo de IA de texto a imagen como DALL-E 3.

**Descripción del Producto Base:** {descripcion_producto}
**Estilo Visual Requerido:** {estilo_visual}

**Instrucciones de Formato (MUY IMPORTANTE):**
1.  Para cada idea, crea un título grande y llamativo en español (ej. "### Idea de Prompt 1: Energía Matutina").
2.  Debajo del título, añade una sección llamada "**Prompt (en inglés):**".
3.  **El texto del prompt que sigue a "Prompt (en inglés):" DEBE estar en inglés**, ya que es el idioma óptimo para DALL-E. Este prompt debe ser muy detallado.
4.  Debajo del prompt en inglés, añade una breve sección llamada "**Explicación:**" en español, describiendo por qué esa idea visual es efectiva para el marketing del producto.
5.  Usa Markdown para formatear toda la respuesta y hacerla fácil de leer.
"""