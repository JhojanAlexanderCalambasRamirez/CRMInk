import requests
import streamlit as st
from typing import Optional, Dict, Any
import json

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if st.session_state.get("token"):
            headers["Authorization"] = f"Bearer {st.session_state.token}"
        return headers
    
    def login(self, email: str, password: str) -> bool:
        """Autenticar usuario"""
        try:
            # Usando OAuth2PasswordRequestForm format
            form_data = {
                "username": email,
                "password": password
            }
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                data=form_data
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.token = data.get("access_token")
                # Para demo, creamos un usuario simulado
                st.session_state.user = {
                    "email": email,
                    "full_name": "Usuario Demo",
                    "role": "tattooer"
                }
                return True
            return False
        except requests.exceptions.ConnectionError:
            st.error("❌ No se puede conectar al servidor. Verifica que el backend esté ejecutándose.")
            return False
    
    def get_clients(self) -> Optional[list]:
        """Obtener lista de clientes"""
        try:
            response = requests.get(
                f"{self.base_url}/api/clients/",
                headers=self._get_headers()
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.ConnectionError:
            st.error("❌ Error de conexión con el servidor")
            return None
    
    def create_client(self, client_data: Dict[str, Any]) -> bool:
        """Crear nuevo cliente"""
        try:
            response = requests.post(
                f"{self.base_url}/api/clients/",
                json=client_data,
                headers=self._get_headers()
            )
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            st.error("❌ Error de conexión con el servidor")
            return False
    
    def get_design_categories(self) -> Optional[list]:
        """Obtener categorías de diseños"""
        try:
            response = requests.get(
                f"{self.base_url}/api/designs/categories",
                headers=self._get_headers()
            )
            if response.status_code == 200:
                return response.json().get("categories", [])
            return None
        except requests.exceptions.ConnectionError:
            st.error("❌ Error de conexión con el servidor")
            return None
    
    def match_designs(self, preferences: Dict[str, Any]) -> Optional[list]:
        """Buscar diseños que coincidan con preferencias"""
        try:
            response = requests.get(
                f"{self.base_url}/api/designs/match",
                params=preferences,
                headers=self._get_headers()
            )
            if response.status_code == 200:
                return response.json().get("designs", [])
            return None
        except requests.exceptions.ConnectionError:
            st.error("❌ Error de conexión con el servidor")
            return None
    
    def generate_design(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Generar diseño con IA"""
        try:
            response = requests.post(
                f"{self.base_url}/api/ai/generate-design",
                json={"prompt": prompt},
                headers=self._get_headers()
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.ConnectionError:
            st.error("❌ Error de conexión con el servidor")
            return None
    
    def create_appointment(self, appointment_data: Dict[str, Any]) -> bool:
        """Crear nueva cita"""
        try:
            response = requests.post(
                f"{self.base_url}/api/appointments/",
                json=appointment_data,
                headers=self._get_headers()
            )
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            st.error("❌ Error de conexión con el servidor")
            return False

# Instancia global del cliente API
api_client = APIClient()
