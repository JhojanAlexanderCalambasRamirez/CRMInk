import streamlit as st
from services.session_state import is_authenticated

st.set_page_config(page_title="Portafolio - InkFlow CRM", page_icon="🖼️")

if not is_authenticated():
    st.warning("🔐 Por favor inicia sesión para acceder a esta página")
    st.stop()

st.title("🖼️ Mi Portafolio")
st.info("""
Esta funcionalidad está en desarrollo. 
Próximamente podrás gestionar tu portafolio profesional, 
subir imágenes y organizar tus trabajos por categorías.
""")

st.subheader("🎨 Próximas Funcionalidades")
st.markdown("""
- 📸 **Subida de imágenes** con previsualización
- 🏷️ **Etiquetado automático** por estilo y ubicación
- 📂 **Organización** por categorías y estilos
- 🌐 **Galería pública** para mostrar a clientes
- 📊 **Análisis de engagement** por diseño
- 🤖 **IA para sugerir** tags y categorías
""")

if st.button("🏠 Volver al Dashboard"):
    st.switch_page("app.py")
