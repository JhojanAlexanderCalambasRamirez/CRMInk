import streamlit as st
from services.api_client import api_client
from services.session_state import init_session_state

# Configuración de página
st.set_page_config(
    page_title="Login - InkFlow CRM",
    page_icon="🔐",
    layout="centered"
)

init_session_state()

def show_login():
    st.title("🔐 InkFlow CRM - Login")
    st.markdown("---")
    
    # Si ya está autenticado, redirigir al dashboard
    if st.session_state.get("token"):
        st.success("✅ Ya estás autenticado")
        if st.button("Ir al Dashboard"):
            st.switch_page("app.py")
        return
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="tu@email.com")
        password = st.text_input("🔒 Contraseña", type="password", placeholder="Tu contraseña")
        
        submitted = st.form_submit_button("🚀 Iniciar Sesión", use_container_width=True)
        
        if submitted:
            if not email or not password:
                st.error("❌ Por favor completa todos los campos")
                return
            
            with st.spinner("Verificando credenciales..."):
                if api_client.login(email, password):
                    st.success("✅ ¡Login exitoso!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas o error de conexión")
    
    # Información de demo
    with st.expander("💡 Información para Pruebas"):
        st.markdown("""
        **Para probar la aplicación:**
        
        - **Email:** cualquier email válido
        - **Contraseña:** cualquier contraseña
        
        **Nota:** El sistema está en modo demo, por lo que cualquier credencial funcionará.
        
        **Backend requerido:**
        - Asegúrate de que el backend esté ejecutándose en `http://localhost:8000`
        - Puedes ver la documentación en `http://localhost:8000/docs`
        """)

if __name__ == "__main__":
    show_login()
