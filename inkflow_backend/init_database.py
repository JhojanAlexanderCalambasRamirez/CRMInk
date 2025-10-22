from databases.dbconexion import engine, Base
from databases import schemas
from sqlalchemy import text

def init_db():
    print("🔄 Creando tablas en la base de datos...")
    
    # Crear el schema si no existe
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS inkflow;"))
        conn.commit()
        print("✅ Schema 'inkflow' creado/verificado")
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    print("✅ Todas las tablas creadas exitosamente!")
    
    print("🎉 Base de datos inicializada correctamente")

if __name__ == "__main__":
    init_db()
