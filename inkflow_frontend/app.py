import streamlit as st
from services.session_state import init_session_state
from components.sidebar import show_sidebar

# Configuración de la página
st.set_page_config(
    page_title="InkFlow CRM AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estado de sesión
init_session_state()

# Mostrar sidebar
show_sidebar()

# Página principal
def main():
    st.title("🎨 InkFlow CRM AI - Dashboard")
    st.markdown("---")
    
    if not st.session_state.get("token"):
        st.warning("⚠️ Por favor inicia sesión para acceder al sistema")
        st.page_link("pages/1_Login.py", label="Ir al Login", icon="🔐")
        return
    
    # Dashboard principal
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Clientes Registrados", "15", "+3")
    
    with col2:
        st.metric("Citas Esta Semana", "8", "+2")
    
    with col3:
        st.metric("Diseños Generados", "24", "+7")
    
    with col4:
        st.metric("Ingresos", "$1,240", "+12%")
    
    st.markdown("### Acciones Rápidas")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("👥 Gestionar Clientes", use_container_width=True):
            st.switch_page("pages/2_Clientes.py")
    
    with col2:
        if st.button("📅 Ver Agenda", use_container_width=True):
            st.switch_page("pages/3_Agenda.py")
    
    with col3:
        if st.button("🖼️ Mi Portafolio", use_container_width=True):
            st.switch_page("pages/4_Portafolio.py")
    
    with col4:
        if st.button("🎨 Galería", use_container_width=True):
            st.switch_page("pages/5_Galeria_Disenos.py")
    
    # Últimas actividades
    st.markdown("### 📊 Actividad Reciente")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Próximas Citas")
        st.info("""
        - **Hoy 3:00 PM** - Ana García (Tattoo minimalista)
        - **Mañana 10:00 AM** - Carlos López (Retoque)
        - **Mañana 2:00 PM** - María Rodríguez (Diseño nuevo)
        """)
    
    with col2:
        st.subheader("Clientes Recientes")
        st.success("""
        - **Laura Martínez** - Estilo: Acuarela
        - **David Hernández** - Estilo: Realismo  
        - **Sofía Castro** - Estilo: Minimalista
        """)

if __name__ == "__main__":
    main()
