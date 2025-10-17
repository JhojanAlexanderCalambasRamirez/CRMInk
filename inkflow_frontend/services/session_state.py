import streamlit as st

def init_session_state():
    """Inicializa el estado de la sesión"""
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user" not in st.session_state:
        st.session_state.user = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

def clear_session():
    """Limpia la sesión (logout)"""
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.current_page = "Dashboard"

def is_authenticated():
    """Verifica si el usuario está autenticado"""
    return st.session_state.token is not None

def get_user_role():
    """Obtiene el rol del usuario actual"""
    return st.session_state.user.get("role") if st.session_state.user else None
