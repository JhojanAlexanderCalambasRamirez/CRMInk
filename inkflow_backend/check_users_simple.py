from databases.dbconexion import SessionLocal
from databases.schemas import User

def check_users():
    db = SessionLocal()
    
    try:
        print("🔍 Verificando usuarios en la base de datos...")
        
        users = db.query(User).all()
        
        if not users:
            print("❌ No hay usuarios en la base de datos")
            return False
        
        print(f"📊 Total de usuarios: {len(users)}")
        
        for user in users:
            print(f"\n👤 Usuario ID: {user.id}")
            print(f"   Email: {user.email}")
            print(f"   Nombre: {user.full_name}")
            print(f"   Rol: {user.role}")
            print(f"   Studio ID: {user.studio_id}")
            print(f"   Activo: {user.is_active}")
            print(f"   Hash: {user.password_hash[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    check_users()
