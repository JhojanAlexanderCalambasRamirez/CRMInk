import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_backend():
    print("🔍 Diagnóstico del Backend...")
    
    try:
        # Verificar imports
        from databases.dbconexion import engine, SessionLocal
        from sqlalchemy import text
        print("✅ Conexión a BD: OK")
        
        from databases import schemas
        print("✅ Schemas: OK")
        
        from routers import router_auth, router_clients, router_appointments
        print("✅ Routers: OK")
        
        from config import settings
        print("✅ Config: OK")
        
        # Verificar que podemos conectar a la BD (corregido)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión a PostgreSQL: OK")
        
        print("🎉 Backend listo para iniciar!")
        return True
        
    except Exception as e:
        print(f"❌ Error en el backend: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_backend()
