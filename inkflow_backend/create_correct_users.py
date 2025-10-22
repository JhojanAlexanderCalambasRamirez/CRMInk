from databases.dbconexion import SessionLocal
from databases.schemas import User, Studio
from routers.router_auth import get_password_hash

def create_correct_users():
    db = SessionLocal()
    
    try:
        print("🔄 Creando usuarios con emails correctos...")
        
        # Verificar si existe el studio
        studio = db.query(Studio).filter(Studio.id == 1).first()
        if not studio:
            studio = Studio(name="InkFlow Studio", description="Studio principal")
            db.add(studio)
            db.commit()
            db.refresh(studio)
            print(f"✅ Studio creado: {studio.name}")
        
        # Crear usuario admin@inkflow.com
        admin_user = db.query(User).filter(User.email == "admin@inkflow.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@inkflow.com",
                full_name="Administrador InkFlow",
                password_hash=get_password_hash("admin123"),
                role="admin",
                studio_id=studio.id
            )
            db.add(admin_user)
            print("✅ Usuario admin@inkflow.com creado")
        else:
            print("✅ Usuario admin@inkflow.com ya existe")
        
        # Crear usuario tattooer@inkflow.com
        tattooer_user = db.query(User).filter(User.email == "tattooer@inkflow.com").first()
        if not tattooer_user:
            tattooer_user = User(
                email="tattooer@inkflow.com",
                full_name="Artista Demo",
                password_hash=get_password_hash("tattooer123"),
                role="tattooer", 
                studio_id=studio.id
            )
            db.add(tattooer_user)
            print("✅ Usuario tattooer@inkflow.com creado")
        else:
            print("✅ Usuario tattooer@inkflow.com ya existe")
        
        db.commit()
        print("🎉 Usuarios creados exitosamente!")
        
        # Mostrar los usuarios creados
        print("\n📧 Usuarios disponibles para login:")
        print("   admin@inkflow.com / admin123")
        print("   tattooer@inkflow.com / tattooer123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_correct_users()
