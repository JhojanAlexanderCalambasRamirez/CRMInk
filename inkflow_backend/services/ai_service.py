import os
import base64
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from databases.dbconexion import get_db
from langchain.prompts import ChatPromptTemplate
from datetime import datetime
import uuid
from sqlalchemy import text
import json
load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# ========= CONFIGURACIÓN MEJORADA DEL MODELO IA =========
def get_llm():
    """Inicializar el modelo solo cuando se necesite y con configuración correcta"""
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "tu_api_key_de_google_ai_aqui":
        print("⚠️  GEMINI_API_KEY no configurada o inválida - usando modo demo")
        return None
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        # Configuración corregida para usar API key directamente
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",  # Modelo más estable
            google_api_key=GOOGLE_API_KEY,
            temperature=0.3
        )
        # Probar la conexión con una consulta simple
        test_response = llm.invoke("Responde 'OK' si estás funcionando")
        if "OK" in test_response.content:
            print("✅ IA conectada correctamente")
            return llm
        else:
            print("⚠️  IA respondió pero no como se esperaba")
            return None
    except Exception as e:
        print(f"❌ Error inicializando modelo IA: {e}")
        return None

# ========= 4. RECOMENDAR IDEA (MEJORADO) =========
def recommend_idea(db: Session, style: str, color: str):
    llm = get_llm()
    if not llm:
        # Modo demo - respuestas predefinidas
        demo_responses = {
            "minimalista": f"💡 Idea para estilo {style} en {color}: Diseño de líneas simples y elegantes. Sugiero un patrón geométrico abstracto en el antebrazo, tamaño mediano (10-15cm). Perfecto para quien busca elegancia discreta.",
            "realismo": f"💡 Idea para estilo {style} en {color}: Retrato detallado con sombras realistas. Considera un animal en escala de grises con texturas de piel/pelo muy detalladas, ideal para el muslo o espalda.",
            "acuarela": f"💡 Idea para estilo {style} en {color}: Efectos de pintura difuminada. Flores con colores {color} que parezcan pintadas a mano, con bordes suaves y transiciones de color fluidas.",
            "japonés": f"💡 Idea para estilo {style} en {color}: Diseño tradicional con líneas gruesas. Un dragón o koi fish con colores {color} vibrantes, ideal para el brazo completo o espalda.",
            "geométrico": f"💡 Idea para estilo {style} en {color}: Patrones simétricos y precisos. Mandala con formas {color} interconectadas, perfecto para pecho o hombro.",
            "tribal": f"💡 Idea para estilo {style} en {color}: Líneas negras gruesas con patrones culturales. Diseño maorí o polinesio con significado espiritual."
        }
        
        response = demo_responses.get(style.lower(), 
            f"💡 Idea para estilo {style} en {color}: Diseño creativo que combina elementos modernos con técnicas tradicionales. Zona recomendada: brazo o pierna. Tamaño: mediano.")
        
        return {"idea": response + " [Modo Demo - Conecta una API key de Google AI para ideas personalizadas]"}

    try:
        prompt = ChatPromptTemplate.from_template("""
        Eres un artista experto en diseño de tatuajes. 
        Un cliente desea un tatuaje con el estilo "{style}" y colores "{color}".
        Describe una idea creativa para ese tatuaje, incluyendo:
        - Elementos visuales sugeridos
        - Zona del cuerpo recomendada
        - Tamaño aproximado
        - Significado artístico o simbólico
        
        Responde en español y sé específico pero conciso.
        """)
        
        response = llm.invoke(prompt.format(style=style, color=color))
        return {"idea": response.content.strip()}
    except Exception as e:
        return {"idea": f"Error generando idea: {str(e)}"}

# ========= FUNCIONES DE ANÁLISIS (MODO DEMO) =========
def analyze_tattooers(db: Session, studio_id: int):
    """Análisis de tatuadores en modo demo"""
    return {"message": "Análisis de tatuadores - Modo Demo", 
            "recommendations": "Conecta una API key válida para análisis con IA"}

def analyze_clients(db: Session, studio_id: int):
    """Análisis de clientes en modo demo"""
    return {"message": "Análisis de clientes - Modo Demo",
            "insights": "Conecta una API key válida para insights con IA"}

async def label_image_binary(db: Session, tattooer_id: int, studio_id: int, image, style_preference: str, color_scheme: str, body_area: str, size_label: str):
    """Etiquetado de imágenes en modo demo"""
    return {
        "message": "Análisis de imagen - Modo Demo",
        "tags": [style_preference, color_scheme, "demo-tag"],
        "summary": "Conecta una API key válida para análisis de imágenes con IA"
    }
