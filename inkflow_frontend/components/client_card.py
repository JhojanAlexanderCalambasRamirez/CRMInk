import streamlit as st

def client_card(client_data, key_suffix=""):
    """
    Componente reutilizable para mostrar tarjeta de cliente
    """
    with st.container():
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.subheader(client_data.get("full_name", "Sin nombre"))
            phone = client_data.get("phone", "No tiene")
            instagram = client_data.get("instagram", "No tiene")
            st.caption(f"📞 {phone} | 📷 {instagram}")
            
            notes = client_data.get("notes")
            if notes:
                st.info(f"📝 {notes}")
        
        with col2:
            styles = client_data.get("preferred_styles", [])
            if styles:
                st.write("🎨 " + ", ".join(styles))
            else:
                st.write("🎨 Sin estilos definidos")
        
        with col3:
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("👀", key=f"view_{key_suffix}"):
                    st.session_state.selected_client = client_data
            with col_b:
                if st.button("📅", key=f"appoint_{key_suffix}"):
                    st.session_state.client_to_appoint = client_data
