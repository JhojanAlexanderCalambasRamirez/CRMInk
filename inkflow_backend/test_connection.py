import os
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:qChOZsjiSUKmzZoIIPjgYZtJnxsqZPtm@shinkansen.proxy.rlwy.net:33705/railway"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("✅ Conexión exitosa a PostgreSQL!")
        print(f"📊 Versión: {result.fetchone()[0]}")
        
        # Verificar si existe el schema inkflow
        result = conn.execute(text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'inkflow';"))
        if result.fetchone():
            print("✅ Schema 'inkflow' existe")
        else:
            print("❌ Schema 'inkflow' no existe - necesitamos crear las tablas")
            
except Exception as e:
    print(f"❌ Error de conexión: {e}")
