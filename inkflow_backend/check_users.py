from databases.dbconexion import SessionLocal
from databases.schemas import User
from routers.router_auth import verify_password

def check_users():
    db = SessionLocal()
    
    try:
        print("🔍 Verificando usuarios en la base de datos...")
        
        users = db.query(User).all()
        
        if not users:
            print("❌ No hay usuarios en la base de datos")
            return False
        
        for user in users:
            print(f"\n👤 Usuario: {user.email}")
            print(f"   Nombre: {user.full_name}")
            print(f"   Rol: {user.role}")
            print(f"   Hash: {user.password_hash}")
            print(f"   Activo: {user.is_active}")
            
            # Probar contraseña
            test_passwords = ["admin123", "tattooer123", "demo"]
            for pwd in test_passwords:
                if verify_password(pwd, user.password_hash):
                    print(f"   ✅ Contraseña correcta: '{pwd}'")
                    break
            else:
                print(f"   ❌ Ninguna contraseña de prueba funciona")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    check_users()
