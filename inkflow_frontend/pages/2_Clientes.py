import streamlit as st
from services.api_client import api_client
from services.session_state import is_authenticated

st.set_page_config(page_title="Clientes - InkFlow CRM", page_icon="👥")

if not is_authenticated():
    st.warning("🔐 Por favor inicia sesión para acceder a esta página")
    st.stop()

def show_clients():
    st.title("👥 Gestión de Clientes")
    st.markdown("---")
    
    # Crear nuevo cliente
    with st.expander("➕ Agregar Nuevo Cliente", expanded=True):
        with st.form("new_client_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Nombre Completo *", placeholder="Ej: Ana García")
                phone = st.text_input("Teléfono", placeholder="+57 300 123 4567")
                instagram = st.text_input("Instagram", placeholder="@usuario")
            
            with col2:
                preferred_styles = st.multiselect(
                    "Estilos Preferidos",
                    ["Minimalista", "Realismo", "Acuarela", "Japonés", "Tradicional", "Geométrico", "Blackwork"]
                )
                notes = st.text_area("Notas / Alergias / Condiciones", placeholder="Información importante sobre el cliente...")
            
            submitted = st.form_submit_button("💾 Guardar Cliente", use_container_width=True)
            
            if submitted:
                if not full_name:
                    st.error("❌ El nombre es obligatorio")
                else:
                    client_data = {
                        "full_name": full_name,
                        "phone": phone,
                        "instagram": instagram,
                        "preferred_styles": preferred_styles,
                        "notes": notes,
                        "studio_id": 1  # Demo
                    }
                    
                    if api_client.create_client(client_data):
                        st.success("✅ Cliente guardado exitosamente!")
                        st.rerun()
                    else:
                        st.error("❌ Error al guardar el cliente")
    
    # Lista de clientes
    st.markdown("## 📋 Lista de Clientes")
    
    clients = api_client.get_clients()
    
    if clients:
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("🔍 Buscar cliente", placeholder="Por nombre, teléfono...")
        with col2:
            filter_style = st.selectbox("Filtrar por estilo", ["Todos"] + ["Minimalista", "Realismo", "Acuarela", "Japonés"])
        
        # Mostrar clientes
        for i, client in enumerate(clients):
            # Aplicar filtros
            if search_term and search_term.lower() not in client.get("full_name", "").lower():
                continue
            if filter_style != "Todos" and filter_style not in client.get("preferred_styles", []):
                continue
                
            with st.container():
                st.markdown("---")
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.subheader(client.get("full_name", "Sin nombre"))
                    st.caption(f"📞 {client.get('phone', 'No tiene')} | 📷 {client.get('instagram', 'No tiene')}")
                    if client.get("notes"):
                        st.info(f"📝 {client.get('notes')}")
                
                with col2:
                    styles = client.get("preferred_styles", [])
                    if styles:
                        st.write("🎨 " + ", ".join(styles))
                    else:
                        st.write("🎨 Sin estilos definidos")
                
                with col3:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("👀", key=f"view_{i}"):
                            st.session_state.selected_client = client
                    with col_b:
                        if st.button("📅", key=f"appoint_{i}"):
                            st.info("Agendar cita para: " + client.get("full_name", ""))
    else:
        st.info("📝 No hay clientes registrados aún. Agrega el primero arriba.")
        
        # Datos de ejemplo para demo
        st.markdown("### 💡 Datos de Ejemplo (Demo)")
        sample_clients = [
            {"full_name": "Ana García", "phone": "+57 300 111 2233", "instagram": "@ana_tattoo", "preferred_styles": ["Minimalista", "Geométrico"]},
            {"full_name": "Carlos López", "phone": "+57 300 444 5566", "instagram": "@carlos_ink", "preferred_styles": ["Realismo", "Blackwork"]},
            {"full_name": "María Rodríguez", "phone": "+57 300 777 8899", "instagram": "@maria_art", "preferred_styles": ["Acuarela", "Japonés"]},
        ]
        
        for client in sample_clients:
            with st.container():
                st.markdown(f"**{client['full_name']}** - 📞 {client['phone']} - 🎨 {', '.join(client['preferred_styles'])}")

if __name__ == "__main__":
    show_clients()
