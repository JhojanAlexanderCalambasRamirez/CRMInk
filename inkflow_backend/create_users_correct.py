from databases.dbconexion import engine
from sqlalchemy import text
from routers.router_auth import get_password_hash

def create_users_correct():
    print("🔄 Creando usuarios usando el tipo ENUM correcto...")
    
    with engine.connect() as conn:
        try:
            # Crear usuarios usando SQL directo con el tipo correcto user_role
            admin_password_hash = get_password_hash("admin123")
            tattooer_password_hash = get_password_hash("tattooer123")
            
            print(f"🔐 Admin hash: {admin_password_hash[:50]}...")
            print(f"🔐 Tattooer hash: {tattooer_password_hash[:50]}...")
            
            # Insertar admin@inkflow.com usando user_role
            result = conn.execute(text("""
                INSERT INTO inkflow.users (studio_id, email, password_hash, full_name, role, is_active)
                VALUES (1, 'admin@inkflow.com', :password, 'Administrador InkFlow', 'admin'::user_role, true)
                ON CONFLICT (email) DO UPDATE SET
                password_hash = EXCLUDED.password_hash,
                full_name = EXCLUDED.full_name,
                role = EXCLUDED.role
                RETURNING id;
            """), {"password": admin_password_hash})
            
            admin_id = result.scalar()
            print(f"✅ Usuario admin@inkflow.com creado/actualizado (ID: {admin_id})")
            
            # Insertar tattooer@inkflow.com usando user_role
            result = conn.execute(text("""
                INSERT INTO inkflow.users (studio_id, email, password_hash, full_name, role, is_active)
                VALUES (1, 'tattooer@inkflow.com', :password, 'Artista Demo', 'tattooer'::user_role, true)
                ON CONFLICT (email) DO UPDATE SET
                password_hash = EXCLUDED.password_hash,
                full_name = EXCLUDED.full_name,
                role = EXCLUDED.role
                RETURNING id;
            """), {"password": tattooer_password_hash})
            
            tattooer_id = result.scalar()
            print(f"✅ Usuario tattooer@inkflow.com creado/actualizado (ID: {tattooer_id})")
            
            conn.commit()
            print("🎉 Usuarios creados exitosamente!")
            
            # Verificar que se crearon
            result = conn.execute(text("""
                SELECT id, email, full_name, role 
                FROM inkflow.users 
                WHERE email IN ('admin@inkflow.com', 'tattooer@inkflow.com')
                ORDER BY email;
            """))
            
            users = result.fetchall()
            print("\n📋 Usuarios verificados:")
            for user in users:
                print(f"   - ID {user[0]}: {user[1]} ({user[2]}) - {user[3]}")
            
            print("\n🎯 Credenciales para login:")
            print("   admin@inkflow.com / admin123")
            print("   tattooer@inkflow.com / tattooer123")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            conn.rollback()
            return False

if __name__ == "__main__":
    create_users_correct()
