from databases.dbconexion import engine
from sqlalchemy import text

def fix_enum_issue():
    print("🔧 Corrigiendo problema de tipos ENUM...")
    
    with engine.connect() as conn:
        try:
            # Verificar los tipos ENUM existentes
            result = conn.execute(text("""
                SELECT typname, enumlabel 
                FROM pg_enum 
                JOIN pg_type ON pg_enum.enumtypid = pg_type.oid 
                WHERE typname LIKE '%user%' OR typname LIKE '%role%';
            """))
            
            enums = result.fetchall()
            print("📋 ENUMs existentes en la base de datos:")
            for enum in enums:
                print(f"   - {enum[0]}: {enum[1]}")
            
            # Verificar si existe userrole enum
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT 1 FROM pg_type WHERE typname = 'userrole'
                );
            """))
            userrole_exists = result.scalar()
            
            if userrole_exists:
                print("✅ ENUM 'userrole' existe en la base de datos")
            else:
                print("❌ ENUM 'userrole' NO existe en la base de datos")
                # Crear el ENUM si no existe
                conn.execute(text("CREATE TYPE userrole AS ENUM ('admin', 'tattooer', 'client');"))
                conn.commit()
                print("✅ ENUM 'userrole' creado")
            
            # Verificar la columna role de la tabla users
            result = conn.execute(text("""
                SELECT column_name, data_type, udt_name
                FROM information_schema.columns 
                WHERE table_schema = 'inkflow' 
                AND table_name = 'users' 
                AND column_name = 'role';
            """))
            
            column_info = result.fetchone()
            if column_info:
                print(f"📊 Columna 'role': {column_info}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

if __name__ == "__main__":
    fix_enum_issue()
