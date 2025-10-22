from databases.dbconexion import SessionLocal, engine
from databases.schemas import User
from sqlalchemy import text
from routers.router_auth import get_password_hash

def fix_passwords():
    print("🔧 Corrigiendo contraseñas...")
    
    db = SessionLocal()
    
    try:
        # Primero, verificar qué usuarios existen
        users = db.query(User).all()
        print("📋 Usuarios en la base de datos:")
        for user in users:
            print(f"   - {user.email} (ID: {user.id}, Rol: {user.role})")
        
        # Resetear contraseñas para todos los usuarios
        password_hash = get_password_hash("admin123")
        
        print(f"\\n🔄 Actualizando contraseñas a 'admin123'...")
        print(f"   Hash: {password_hash[:50]}...")
        
        # Actualizar usando SQL directo para evitar problemas de ENUM
        with engine.connect() as conn:
            # Actualizar todos los usuarios a la misma contraseña
            result = conn.execute(text("""
                UPDATE inkflow.users 
                SET password_hash = :password
                WHERE id IN (1, 2, 3, 4, 5, 6)
            """), {"password": password_hash})
            
            conn.commit()
            print(f"✅ {result.rowcount} usuarios actualizados")
        
        # Verificar los cambios
        print("\\n🔍 Verificando cambios...")
        updated_users = db.query(User).all()
        for user in updated_users:
            print(f"   - {user.email}: {user.password_hash[:30]}...")
        
        print("\\n🎯 Credenciales actualizadas:")
        print("   Todos los usuarios ahora usan: admin@inkmasters.com / admin123")
        print("   O: maria@inkmasters.com / admin123")
        print("   O: admin@urbanart.com / admin123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_passwords()
