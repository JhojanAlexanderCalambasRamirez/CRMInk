import streamlit as st
from services.session_state import clear_session, is_authenticated

def show_sidebar():
    with st.sidebar:
        st.title("🎨 InkFlow CRM")
        st.markdown("---")
        
        if is_authenticated():
            user = st.session_state.user
            st.success(f"👋 Hola, {user.get('full_name', 'Usuario')}")
            st.caption(f"Rol: {user.get('role', 'N/A')}")
            st.markdown("---")
        
        # Navegación
        st.subheader("Navegación")
        
        if st.button("🏠 Dashboard", use_container_width=True):
            if "app.py" in st.session_state.get("page_script", ""):
                st.rerun()
            else:
                st.switch_page("app.py")
        
        if st.button("👥 Clientes", use_container_width=True):
            st.switch_page("pages/2_Clientes.py")
        
        if st.button("📅 Agenda", use_container_width=True):
            st.switch_page("pages/3_Agenda.py")
        
        if st.button("🖼️ Portafolio", use_container_width=True):
            st.switch_page("pages/4_Portafolio.py")
        
        if st.button("🎨 Galería de Diseños", use_container_width=True):
            st.switch_page("pages/5_Galeria_Disenos.py")
        
        if st.button("🤖 Asistente IA", use_container_width=True):
            st.switch_page("pages/6_Asistente_IA.py")
        
        st.markdown("---")
        
        # Sesión
        if is_authenticated():
            if st.button("🚪 Cerrar Sesión", use_container_width=True):
                clear_session()
                st.rerun()
        else:
            if st.button("🔐 Iniciar Sesión", use_container_width=True):
                st.switch_page("pages/1_Login.py")
        
        st.markdown("---")
        st.caption("v1.0 - InkFlow CRM AI")
        
        # Estado del backend
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                st.success("✅ Backend conectado")
            else:
                st.warning("⚠️ Backend con problemas")
        except:
            st.error("❌ Backend no disponible")
