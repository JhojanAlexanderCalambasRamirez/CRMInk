import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Verificando variables de entorno...")
print(f"DATABASE_URL: {'✅' if os.getenv('DATABASE_URL') else '❌ No encontrada'}")
print(f"SECRET_KEY: {'✅' if os.getenv('SECRET_KEY') else '❌ No encontrada'}")
print(f"GEMINI_API_KEY: {'✅' if os.getenv('GEMINI_API_KEY') else '❌ No encontrada (modo demo)'}")

if not os.getenv('GEMINI_API_KEY'):
    print("\n💡 Para habilitar IA completa, agrega al .env:")
    print("GEMINI_API_KEY=tu_api_key_de_google_ai_aqui")
