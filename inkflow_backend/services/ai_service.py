import os
import base64
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from databases.dbconexion import get_db
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from datetime import datetime
import uuid
from sqlalchemy import text
import json
load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")


# Inicialización del modelo IA
llm = ChatGoogleGenerativeAI(google_api_key= GOOGLE_API_KEY,model="gemini-2.5-pro", temperature=0.3)

# ========= 1. ANALIZAR TATUADORES =========
def analyze_tattooers(db: Session, studio_id: int):
    query = """
    SELECT 
        t.id, t.display_name, t.styles, t.hourly_rate, 
        COUNT(a.id) AS total_appointments,
        AVG(EXTRACT(EPOCH FROM (a.ends_at - a.starts_at)) / 3600) AS avg_duration_hours,
        COUNT(p.id) AS total_portfolio_images,
        AVG(pr.base_price) AS avg_base_price
    FROM inkflow.tattooers t
    LEFT JOIN inkflow.appointments a ON a.tattooer_id = t.id
    LEFT JOIN inkflow.portfolio_images p ON p.tattooer_id = t.id
    LEFT JOIN inkflow.pricing_rules pr ON pr.tattooer_id = t.id
    WHERE t.studio_id = :studio_id
    GROUP BY t.id, t.display_name, t.styles, t.hourly_rate;
    """

    results = db.execute(text(query), {"studio_id": studio_id}).fetchall()


    prompt = ChatPromptTemplate.from_template("""
    Analiza el rendimiento de los tatuadores con base en los siguientes datos:
    {data}
    Quiero un resumen con:
    - Promedio general de citas y duración.
    - Quién tiene más actividad.
    - Recomendaciones de optimización.
    """)

    response = llm.invoke(prompt.format(data=[dict(r._mapping) for r in results]))
    return response.content


# ========= 2. ANALIZAR CLIENTES =========
def analyze_clients(db: Session, studio_id: int):
    query = """
    SELECT 
        c.id, c.full_name, c.preferred_styles, COUNT(a.id) AS total_appointments,
        MIN(a.starts_at) AS first_visit, MAX(a.starts_at) AS last_visit
    FROM inkflow.clients c
    LEFT JOIN inkflow.appointments a ON a.client_id = c.id
    WHERE c.studio_id = :studio_id
    GROUP BY c.id, c.full_name, c.preferred_styles;
    """
    results = db.execute(text(query), {"studio_id": studio_id}).fetchall()

    prompt = ChatPromptTemplate.from_template("""
    Basándote en estos datos de clientes:
    {data}
    Genera:
    - Tendencias de estilos populares.
    - Clientes frecuentes y nuevos.
    - Sugerencias de marketing personalizadas.
    """)

    response = llm.invoke(prompt.format(data=[dict(r._mapping) for r in results]))
    return response.content


# ========= 3. ETIQUETAR IMAGEN =========
def label_image(db: Session, tattooer_id: int, studio_id: int, image_url: str, style_preference: str, color_scheme: str, body_area: str, size_label: str):
    prompt = ChatPromptTemplate.from_template("""
    Eres un modelo experto en análisis de tatuajes. 
    Analiza la imagen: {image_url}.
    Ten en cuenta el estilo preferido "{style_preference}" y el esquema de color "{color_scheme}".
    Devuelve etiquetas de estilo en formato lista JSON y un resumen breve.
    """)

    response = llm.invoke(prompt.format(
        image_url=image_url,
        style_preference=style_preference,
        color_scheme=color_scheme
    ))

    # Procesar etiquetas
    try:
        style_tags = eval(response.content) if "[" in response.content else [response.content]
    except:
        style_tags = [response.content.strip()]

    db.execute("""
        INSERT INTO inkflow.portfolio_images 
        (studio_id, tattooer_id, image_url, style_tags, body_area, size_label, uploaded_at)
        VALUES (:studio_id, :tattooer_id, :image_url, :style_tags, :body_area, :size_label, NOW())
    """, {
        "studio_id": studio_id,
        "tattooer_id": tattooer_id,
        "image_url": image_url,
        "style_tags": style_tags,
        "body_area": body_area,
        "size_label": size_label
    })
    db.commit()

    return {"message": "Imagen etiquetada y guardada exitosamente", "tags": style_tags}


# ========= 4. RECOMENDAR TATUADOR =========
def recommend_tattooer(db: Session, studio_id: int, style: str, budget: float):
    query = """
    SELECT 
        t.id, t.display_name, t.styles, pr.base_price, pr.per_cm2
    FROM inkflow.tattooers t
    JOIN inkflow.pricing_rules pr ON pr.tattooer_id = t.id
    WHERE t.studio_id = :studio_id;
    """
    results = db.execute(text(query), {"studio_id": studio_id}).fetchall()

    prompt = ChatPromptTemplate.from_template("""
    Basado en estos tatuadores:
    {data}
    Y considerando que el cliente busca estilo "{style}" y tiene un presupuesto de {budget},
    recomienda los mejores 3 tatuadores, ordenados por afinidad de estilo y costo estimado.
    """)

    response = llm.invoke(prompt.format(data=[dict(r._mapping) for r in results], style=style, budget=budget))
    return response.content

async def label_image_binary(db: Session, tattooer_id: int, studio_id: int, image, style_preference: str, color_scheme: str, body_area: str, size_label: str):
    image_bytes = await image.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    prompt = ChatPromptTemplate.from_template("""
    Eres un modelo experto en análisis de tatuajes. 
    Analiza la siguiente imagen en base64: {image_b64}
    Devuelve etiquetas de estilo en formato lista JSON y un resumen breve.
    """)

    response = llm.invoke(prompt.format(
        image_b64=image_b64,
        style_preference=style_preference,
        color_scheme=color_scheme
    ))

    try:
        style_tags = eval(response.content) if "[" in response.content else [response.content]
    except Exception:
        style_tags = [response.content.strip()]

    db.execute(
    text("""
        INSERT INTO inkflow.portfolio_images 
        (studio_id, tattooer_id, image_url, body_area, size_label, uploaded_at)
        VALUES (:studio_id, :tattooer_id, :image_url, :body_area, :size_label, NOW())
    """),
    {
        "studio_id": studio_id,
        "tattooer_id": tattooer_id,
        "image_url": image.filename,
        "body_area": body_area,
        "size_label": size_label
    }
)

    db.commit()

    return {
        "message": "Imagen analizada y guardada exitosamente",
        "tags": style_tags,
        "summary": response.content
    }

# =====================================================
# ========= NUEVO ENDPOINT: RECOMENDAR IDEA ============
# =====================================================
def recommend_idea(db: Session, style: str, color: str):
    prompt = ChatPromptTemplate.from_template("""
    Eres un artista experto en diseño de tatuajes. 
    Un cliente desea un tatuaje con el estilo "{style}" y colores "{color}".
    Describe una idea creativa para ese tatuaje, incluyendo:
    - Elementos visuales sugeridos
    - Zona del cuerpo recomendada
    - Tamaño aproximado
    - Significado artístico o simbólico
    """)
    
    response = llm.invoke(prompt.format(style=style, color=color))
    return {"idea": response.content.strip()}