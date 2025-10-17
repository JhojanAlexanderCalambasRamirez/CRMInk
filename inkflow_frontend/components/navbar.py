# components/navbar.py
import streamlit as st

def render_navbar():
    cols = st.columns([1,4,1])
    with cols[0]:
        # st.image("assets/logo.png", width=60)  # <- comenta o elimina esta línea
        st.markdown("### 🧠 InkFlow")  # texto temporal
        st.markdown("<h1 style='margin:0;'>FindInk — Dashboard</h1>", unsafe_allow_html=True)
    with cols[1]:
        if st.session_state.get("user"):
            st.write(f"👋 {st.session_state.user.get('name')}")
            if st.button("Cerrar sesión"):
                st.session_state.token = None
                st.session_state.user = None
                st.session_state.api_client = None
                st.experimental_rerun()
