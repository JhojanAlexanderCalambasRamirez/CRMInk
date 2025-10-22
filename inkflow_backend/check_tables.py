from databases.dbconexion import engine
from sqlalchemy import text

def check_tables():
    print("🔍 Verificando tablas en la base de datos...")
    
    with engine.connect() as conn:
        # Verificar tablas en el schema inkflow
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'inkflow'
            ORDER BY table_name;
        """))
        
        tables = [row[0] for row in result]
        
        if tables:
            print("✅ Tablas encontradas en schema 'inkflow':")
            for table in tables:
                print(f"   - {table}")
        else:
            print("❌ No se encontraron tablas en el schema 'inkflow'")
            return False
        
        # Verificar conteo de registros en cada tabla
        print("\n📊 Conteo de registros por tabla:")
        for table in tables:
            try:
                count_result = conn.execute(text(f"SELECT COUNT(*) FROM inkflow.{table}"))
                count = count_result.scalar()
                print(f"   - {table}: {count} registros")
            except Exception as e:
                print(f"   - {table}: Error al contar - {e}")
    
    return True

if __name__ == "__main__":
    check_tables()
