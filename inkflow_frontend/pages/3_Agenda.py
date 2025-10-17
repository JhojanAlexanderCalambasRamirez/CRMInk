import streamlit as st
from services.session_state import is_authenticated

st.set_page_config(page_title="Agenda - InkFlow CRM", page_icon="📅")

if not is_authenticated():
    st.warning("🔐 Por favor inicia sesión para acceder a esta página")
    st.stop()

st.title("📅 Agenda de Citas")
st.info("""
Esta funcionalidad está en desarrollo. 
Próximamente podrás gestionar tu agenda de citas, ver disponibilidad 
y coordinar con tus clientes.
""")

st.subheader("🔄 Próximas Actualizaciones")
st.markdown("""
- 📋 **Visualización de calendario** semanal y mensual
- ⏰ **Gestión de disponibilidad** por tatuador  
- 🔔 **Recordatorios automáticos** para clientes
- 📊 **Métricas de productividad**
- 🔄 **Sincronización** con Google Calendar
""")

if st.button("🏠 Volver al Dashboard"):
    st.switch_page("app.py")
