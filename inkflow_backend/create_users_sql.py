from databases.dbconexion import engine
from sqlalchemy import text
from routers.router_auth import get_password_hash

def create_users_sql():
    print("🔄 Creando usuarios usando SQL directo...")
    
    with engine.connect() as conn:
        try:
            # Crear usuarios usando SQL directo para evitar problemas de tipo
            admin_password_hash = get_password_hash("admin123")
            tattooer_password_hash = get_password_hash("tattooer123")
            
            # Insertar admin@inkflow.com
            conn.execute(text("""
                INSERT INTO inkflow.users (studio_id, email, password_hash, full_name, role, is_active)
                VALUES (1, 'admin@inkflow.com', :password, 'Administrador InkFlow', 'admin'::userrole, true)
                ON CONFLICT (email) DO UPDATE SET
                password_hash = EXCLUDED.password_hash,
                full_name = EXCLUDED.full_name,
                role = EXCLUDED.role;
            """), {"password": admin_password_hash})
            
            # Insertar tattooer@inkflow.com
            conn.execute(text("""
                INSERT INTO inkflow.users (studio_id, email, password_hash, full_name, role, is_active)
                VALUES (1, 'tattooer@inkflow.com', :password, 'Artista Demo', 'tattooer'::userrole, true)
                ON CONFLICT (email) DO UPDATE SET
                password_hash = EXCLUDED.password_hash,
                full_name = EXCLUDED.full_name,
                role = EXCLUDED.role;
            """), {"password": tattooer_password_hash})
            
            conn.commit()
            print("✅ Usuarios creados/actualizados exitosamente!")
            
            # Verificar que se crearon
            result = conn.execute(text("""
                SELECT id, email, full_name, role 
                FROM inkflow.users 
                WHERE email IN ('admin@inkflow.com', 'tattooer@inkflow.com');
            """))
            
            users = result.fetchall()
            print("📋 Usuarios verificados:")
            for user in users:
                print(f"   - {user[1]} ({user[2]}) - {user[3]}")
            
            print("\n🎯 Credenciales para login:")
            print("   admin@inkflow.com / admin123")
            print("   tattooer@inkflow.com / tattooer123")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            conn.rollback()
            return False

if __name__ == "__main__":
    create_users_sql()
