import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="InkFlow CRM - Tatuador",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de la API
API_BASE_URL = "http://localhost:8000"

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
    
    def _make_request(self, endpoint, method="GET", data=None):
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, json=data)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except:
            return None
    
    def get_clients(self):
        return self._make_request("/api/clients/")
    
    def create_client(self, client_data):
        return self._make_request("/api/clients/", "POST", client_data)
    
    def get_appointments(self):
        return self._make_request("/api/appointments/")
    
    def get_design_categories(self):
        result = self._make_request("/api/designs/categories")
        return result.get('categories', []) if result else []
    
    def get_ai_idea(self, style, color):
        data = {"style": style, "color": color}
        result = self._make_request("/api/ai/recommend_idea", "POST", data)
        return result.get('idea', '') if result else "Error al generar idea"

def main():
    api_client = APIClient()
    
    # Sidebar para navegación
    with st.sidebar:
        st.title("🎨 InkFlow CRM")
        st.markdown("---")
        st.success("👋 Hola, Artista")
        st.caption("Tatuador Profesional")
        st.markdown("---")
        
        # Navegación
        page = st.selectbox(
            "Navegación",
            ["📊 Mi Dashboard", "👥 Mis Clientes", "📅 Mi Agenda", "🖼️ Mi Portfolio", "🎨 Diseños IA", "📊 Mis Analytics"]
        )
        
        st.markdown("---")
        st.caption("InkFlow CRM v1.0 - Tu espacio creativo")
    
    # Contenido según página seleccionada
    if page == "📊 Mi Dashboard":
        show_personal_dashboard(api_client)
    elif page == "👥 Mis Clientes":
        show_my_clients(api_client)
    elif page == "📅 Mi Agenda":
        show_my_appointments(api_client)
    elif page == "🖼️ Mi Portfolio":
        show_my_portfolio()
    elif page == "🎨 Diseños IA":
        show_ai_designs(api_client)
    elif page == "📊 Mis Analytics":
        show_personal_analytics()

def show_personal_dashboard(api_client):
    st.title("🎨 Mi Dashboard - InkFlow")
    st.info("Bienvenido a tu espacio de trabajo personal")
    
    # Obtener datos de la API (modo demo si no hay conexión)
    appointments = api_client.get_appointments() or []
    clients = api_client.get_clients() or []
    
    # Filtrar citas confirmadas para métricas
    confirmed_appointments = [apt for apt in appointments if apt.get('status') == 'confirmed']
    monthly_count = len(confirmed_appointments) if confirmed_appointments else 8
    
    # Métricas personales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Citas Este Mes", monthly_count, "+2", delta_color="normal")
    
    with col2:
        st.metric("Satisfacción Cliente", "94%", "+3%", delta_color="normal")
    
    with col3:
        st.metric("Visitas Portfolio", "156", "+24", delta_color="normal")
    
    with col4:
        st.metric("Ingresos Mensuales", "$1,200", "+$180", delta_color="normal")
    
    # Próximas citas
    st.subheader("📅 Mis Próximas Citas")
    
    if appointments:
        for apt in appointments[:5]:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    client_name = f"Cliente #{apt.get('client_id', 'N/A')}"
                    st.write(f"**{client_name}**")
                    st.write(f"🕐 {apt.get('starts_at', 'Fecha no disponible')}")
                    st.write(f"📝 {apt.get('notes', 'Sin notas')}")
                with col2:
                    duration = apt.get('duration', 120)
                    st.write(f"⏱️ {duration} min")
                    st.write(f"🎨 {apt.get('style', 'Estilo no especificado')}")
                with col3:
                    status = apt.get('status', 'pending')
                    color = "🟢" if status == 'confirmed' else "🟡" if status == 'pending' else "🔴"
                    st.write(f"{color} {status}")
                st.markdown("---")
    else:
        st.info("No tienes citas programadas")
        # Datos de ejemplo para demo
        sample_appointments = [
            {"client_id": 1, "starts_at": "2024-03-20 10:00", "notes": "Tatuaje minimalista en brazo", "style": "Minimalista", "status": "confirmed"},
            {"client_id": 2, "starts_at": "2024-03-21 14:00", "notes": "Retoque de tatuaje anterior", "style": "Realismo", "status": "pending"},
            {"client_id": 3, "starts_at": "2024-03-22 16:00", "notes": "Nuevo diseño geométrico", "style": "Geométrico", "status": "confirmed"},
        ]
        
        for apt in sample_appointments:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**Cliente #{apt['client_id']}**")
                    st.write(f"🕐 {apt['starts_at']}")
                    st.write(f"📝 {apt['notes']}")
                with col2:
                    st.write(f"⏱️ 120 min")
                    st.write(f"🎨 {apt['style']}")
                with col3:
                    color = "🟢" if apt['status'] == 'confirmed' else "🟡"
                    st.write(f"{color} {apt['status']}")
                st.markdown("---")
    
    # Acciones rápidas
    st.subheader("🚀 Acciones Rápidas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 Agendar Nueva Cita", use_container_width=True):
            st.info("📍 Funcionalidad de agendamiento - Próximamente")
    
    with col2:
        if st.button("👥 Agregar Cliente", use_container_width=True):
            st.info("📍 Funcionalidad de clientes - Próximamente")
    
    with col3:
        if st.button("🖼️ Actualizar Portfolio", use_container_width=True):
            st.info("📍 Funcionalidad de portfolio - Próximamente")
    
    # Estadísticas rápidas
    st.subheader("📈 Resumen Rápido")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Citas por Estilo**")
        style_data = pd.DataFrame({
            'Estilo': ['Minimalista', 'Realismo', 'Acuarela', 'Geométrico'],
            'Citas': [8, 5, 3, 2]
        })
        fig = px.bar(style_data, x='Estilo', y='Citas', color='Estilo')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.info("**Ingresos Mensuales**")
        income_data = pd.DataFrame({
            'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
            'Ingresos': [800, 950, 1200, 1100, 1300, 1400]
        })
        fig = px.line(income_data, x='Mes', y='Ingresos', markers=True)
        st.plotly_chart(fig, use_container_width=True)

def show_my_clients(api_client):
    st.title("👥 Mis Clientes")
    st.info("Gestión de tu base de clientes personal")
    
    # Formulario para nuevo cliente
    with st.expander("➕ Agregar Nuevo Cliente", expanded=True):
        with st.form("new_client_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Nombre Completo *", placeholder="Ej: Ana García López")
                phone = st.text_input("Teléfono", placeholder="+57 300 123 4567")
                email = st.text_input("Email", placeholder="cliente@email.com")
            
            with col2:
                instagram = st.text_input("Instagram", placeholder="@usuario")
                preferred_styles = st.multiselect(
                    "Estilos Preferidos",
                    ["Minimalista", "Realismo", "Acuarela", "Japonés", "Tradicional", "Geométrico", "Blackwork", "Acuarela"]
                )
                birth_date = st.date_input("Fecha de Nacimiento")
            
            notes = st.text_area("Notas / Alergias / Condiciones médicas", 
                               placeholder="Información importante sobre el cliente...")
            
            submitted = st.form_submit_button("💾 Guardar Cliente", use_container_width=True)
            
            if submitted:
                if not full_name:
                    st.error("❌ El nombre es obligatorio")
                else:
                    client_data = {
                        "full_name": full_name,
                        "phone": phone,
                        "email": email,
                        "instagram": instagram,
                        "preferred_styles": preferred_styles,
                        "notes": notes,
                        "birth_date": birth_date.isoformat() if birth_date else None,
                        "studio_id": 1
                    }
                    
                    if api_client.create_client(client_data):
                        st.success("✅ Cliente guardado exitosamente!")
                        st.rerun()
                    else:
                        st.error("❌ Error al guardar el cliente")
    
    # Lista de clientes
    st.markdown("## 📋 Lista de Clientes")
    
    clients = api_client.get_clients()
    
    if not clients:
        st.info("📝 No hay clientes registrados aún. Agrega el primero arriba.")
        
        # Datos de ejemplo para demo
        st.markdown("### 💡 Datos de Ejemplo (Demo)")
        sample_clients = [
            {"id": 1, "full_name": "Ana García", "phone": "+57 300 111 2233", "instagram": "@ana_tattoo", "preferred_styles": ["Minimalista", "Geométrico"], "notes": "Prefiere colores negros"},
            {"id": 2, "full_name": "Carlos López", "phone": "+57 300 444 5566", "instagram": "@carlos_ink", "preferred_styles": ["Realismo", "Blackwork"], "notes": "Alérgico a látex"},
            {"id": 3, "full_name": "María Rodríguez", "phone": "+57 300 777 8899", "instagram": "@maria_art", "preferred_styles": ["Acuarela", "Japonés"], "notes": ""},
        ]
        clients = sample_clients
    
    if clients:
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("🔍 Buscar cliente", placeholder="Por nombre, teléfono...")
        with col2:
            filter_style = st.selectbox("Filtrar por estilo", ["Todos"] + ["Minimalista", "Realismo", "Acuarela", "Japonés"])
        
        # Mostrar clientes
        for client in clients:
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
                    st.caption(f"📞 {client.get('phone', 'No tiene')} | 📧 {client.get('email', 'No tiene')} | 📷 {client.get('instagram', 'No tiene')}")
                    if client.get("notes"):
                        st.info(f"📝 {client.get('notes')}")
                
                with col2:
                    styles = client.get("preferred_styles", [])
                    if styles:
                        st.write("🎨 " + ", ".join(styles))
                    else:
                        st.write("🎨 Sin estilos definidos")
                    
                    if client.get("birth_date"):
                        st.write(f"🎂 {client.get('birth_date')}")
                
                with col3:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("👀", key=f"view_{client.get('id')}"):
                            st.session_state.selected_client = client
                    with col_b:
                        if st.button("📅", key=f"appoint_{client.get('id')}"):
                            st.info(f"Agendar cita para: {client.get('full_name', '')}")

def show_my_appointments(api_client):
    st.title("📅 Mi Agenda Personal")
    st.info("Organiza y gestiona todas tus citas")
    
    # Vista de calendario simple
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader("🗓️ Vista Semanal")
    with col2:
        week_start = st.date_input("Inicio de semana", datetime.now().date())
    with col3:
        if st.button("📅 Nueva Cita", use_container_width=True):
            st.info("Funcionalidad de nueva cita en desarrollo")
    
    # Lista de citas
    appointments = api_client.get_appointments()
    
    if not appointments:
        st.info("📅 No hay citas programadas para esta semana.")
        
        # Datos de ejemplo para demo
        st.markdown("### 💡 Citas de Ejemplo (Demo)")
        sample_appointments = [
            {"id": 1, "client_id": 1, "starts_at": "2024-03-20 10:00", "ends_at": "2024-03-20 12:00", "style": "Minimalista", "status": "confirmed", "notes": "Tatuaje de líneas finas en muñeca"},
            {"id": 2, "client_id": 2, "starts_at": "2024-03-21 14:00", "ends_at": "2024-03-21 16:00", "style": "Realismo", "status": "pending", "notes": "Retoque de retrato"},
            {"id": 3, "client_id": 3, "starts_at": "2024-03-22 11:00", "ends_at": "2024-03-22 14:00", "style": "Geométrico", "status": "confirmed", "notes": "Diseño simétrico en espalda"},
        ]
        appointments = sample_appointments
    
    if appointments:
        for apt in appointments:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**Cita #{apt.get('id')}**")
                    st.write(f"👤 Cliente ID: {apt.get('client_id')}")
                    st.write(f"🕐 {apt.get('starts_at')} - {apt.get('ends_at')}")
                    st.write(f"📝 {apt.get('notes', 'Sin notas')}")
                with col2:
                    st.write(f"🎨 {apt.get('style', 'Estilo no especificado')}")
                    duration = "120 min"  # Calcular duración
                    st.write(f"⏱️ {duration}")
                with col3:
                    status = apt.get('status', 'pending')
                    if status == 'confirmed':
                        st.success("✅ Confirmada")
                    elif status == 'pending':
                        st.warning("⏳ Pendiente")
                    else:
                        st.error("❌ Cancelada")
                    
                    if st.button("📋 Detalles", key=f"details_{apt.get('id')}"):
                        st.write(f"**Detalles completos de la cita:**")
                        st.json(apt)
                st.markdown("---")
    
    # Estadísticas de agenda
    st.subheader("📊 Estadísticas de Agenda")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_appointments = len(appointments)
        st.metric("Citas Totales", total_appointments)
    
    with col2:
        confirmed_count = len([apt for apt in appointments if apt.get('status') == 'confirmed'])
        st.metric("Confirmadas", confirmed_count)
    
    with col3:
        pending_count = len([apt for apt in appointments if apt.get('status') == 'pending'])
        st.metric("Pendientes", pending_count)
    
    with col4:
        cancellation_rate = "5%"
        st.metric("Tasa Cancelación", cancellation_rate)

def show_my_portfolio():
    st.title("🖼️ Mi Portfolio")
    st.info("Muestra tu trabajo y atrae nuevos clientes")
    
    # Subir nuevo trabajo
    with st.expander("📤 Subir Nuevo Trabajo", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            work_title = st.text_input("Título del trabajo", placeholder="Ej: Dragón Japonés en Espalda")
            client_name = st.text_input("Nombre del cliente", placeholder="Ej: Carlos Martínez")
            work_date = st.date_input("Fecha del trabajo", datetime.now().date())
            work_style = st.selectbox("Estilo", ["Minimalista", "Realismo", "Acuarela", "Japonés", "Tradicional", "Geométrico"])
        
        with col2:
            body_part = st.selectbox("Parte del cuerpo", ["Brazo", "Espalda", "Pecho", "Pierna", "Muñeca", "Cuello", "Otro"])
            hours_taken = st.number_input("Horas tomadas", min_value=1, max_value=20, value=3)
            price = st.number_input("Precio ($)", min_value=50, max_value=2000, value=300)
            upload_photo = st.file_uploader("Subir foto", type=['png', 'jpg', 'jpeg'])
        
        description = st.text_area("Descripción del trabajo", placeholder="Describe el proceso, inspiración, técnicas utilizadas...")
        
        if st.button("💾 Publicar en Portfolio", use_container_width=True):
            if upload_photo:
                st.success("✅ Trabajo publicado exitosamente en tu portfolio!")
            else:
                st.error("❌ Por favor sube una foto del trabajo")
    
    # Galería de trabajos
    st.subheader("🎨 Mi Galería de Trabajos")
    
    # Trabajos de ejemplo
    portfolio_works = [
        {
            "title": "Dragón Japonés", 
            "client": "Ana García", 
            "style": "Japonés", 
            "body_part": "Espalda completa",
            "hours": 8,
            "price": "$800",
            "date": "2024-02-15",
            "image": "https://via.placeholder.com/300x300/4A90E2/FFFFFF?text=Dragón+Japonés"
        },
        {
            "title": "Flor de Loto Acuarela", 
            "client": "María López", 
            "style": "Acuarela", 
            "body_part": "Muslo",
            "hours": 4,
            "price": "$400",
            "date": "2024-02-10",
            "image": "https://via.placeholder.com/300x300/50E3C2/FFFFFF?text=Flor+Acuarela"
        },
        {
            "title": "Geometría Sagrada", 
            "client": "Carlos Ruiz", 
            "style": "Geométrico", 
            "body_part": "Pecho",
            "hours": 6,
            "price": "$600",
            "date": "2024-02-05",
            "image": "https://via.placeholder.com/300x300/B8E986/FFFFFF?text=Geometría"
        },
        {
            "title": "Retrato Realista", 
            "client": "Laura Martínez", 
            "style": "Realismo", 
            "body_part": "Brazo",
            "hours": 10,
            "price": "$1200",
            "date": "2024-01-28",
            "image": "https://via.placeholder.com/300x300/9013FE/FFFFFF?text=Retrato"
        },
    ]
    
    # Mostrar galería en grid
    cols = st.columns(2)
    for idx, work in enumerate(portfolio_works):
        with cols[idx % 2]:
            with st.container():
                st.image(work["image"], use_column_width=True)
                st.write(f"**{work['title']}**")
                st.write(f"👤 {work['client']}")
                st.write(f"🎨 {work['style']} | 🕐 {work['hours']}h | 💰 {work['price']}")
                st.write(f"📍 {work['body_part']} | 📅 {work['date']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✏️ Editar", key=f"edit_{idx}"):
                        st.info(f"Editando: {work['title']}")
                with col2:
                    if st.button("🗑️ Eliminar", key=f"delete_{idx}"):
                        st.warning(f"¿Eliminar {work['title']}?")
                
                st.markdown("---")
    
    # Estadísticas del portfolio
    st.subheader("📊 Estadísticas del Portfolio")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Trabajos Publicados", "24")
    
    with col2:
        st.metric("Visitas Totales", "1,245")
    
    with col3:
        st.metric("Me gusta", "189")
    
    with col4:
        st.metric("Tasa Conversión", "12%")

def show_ai_designs(api_client):
    st.title("🎨 Asistente de IA para Diseños")
    st.info("Genera ideas creativas y personalizadas con inteligencia artificial")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💡 Generar Idea de Diseño")
        
        with st.form("ai_design_form"):
            style = st.selectbox(
                "Estilo de tatuaje",
                ["Minimalista", "Realismo", "Acuarela", "Japonés", "Geométrico", "Tribal", "Tradicional", "Blackwork"]
            )
            
            color = st.selectbox(
                "Esquema de color",
                ["Negro", "Color", "Negro y Gris", "Colores vibrantes", "Pasteles", "Acuarela", "Monocromático"]
            )
            
            theme = st.text_input("Tema o concepto", placeholder="Ej: naturaleza, protección, familia, libertad...")
            
            placement = st.selectbox(
                "Ubicación en el cuerpo",
                ["Brazo", "Espalda", "Pecho", "Pierna", "Muñeca", "Cuello", "Manos", "Costillas"]
            )
            
            size = st.select_slider(
                "Tamaño",
                options=["Pequeño", "Mediano", "Grande", "Muy Grande"]
            )
            
            submitted = st.form_submit_button("🤖 Generar Idea con IA", use_container_width=True)
            
            if submitted:
                with st.spinner("🤖 Generando idea creativa..."):
                    # Combinar inputs para el prompt
                    prompt = f"{style} style, {color} colors"
                    if theme:
                        prompt += f", theme: {theme}"
                    prompt += f", placement: {placement}, size: {size}"
                    
                    idea = api_client.get_ai_idea(style, color)
                    
                    if idea and not idea.startswith("Error"):
                        st.success("✅ ¡Idea generada exitosamente!")
                        
                        st.markdown("### 🎨 Concepto Generado")
                        st.info(f"**Estilo:** {style} | **Colores:** {color} | **Ubicación:** {placement}")
                        
                        st.markdown("#### 💡 Descripción del Diseño:")
                        st.write(idea)
                        
                        st.markdown("#### 🎯 Recomendaciones Técnicas:")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Tiempo estimado:** 2-3 horas")
                            st.write("**Nivel de dificultad:** Medio")
                            st.write("**Técnicas recomendadas:** Línea fina, sombreado suave")
                        with col2:
                            st.write("**Preparación piel:** Limpieza profunda")
                            st.write("**Cuidados posteriores:** 2 semanas")
                            st.write("**Precio estimado:** $300-500")
                        
                        # Acciones
                        st.markdown("---")
                        st.subheader("📝 ¿Te gusta esta idea?")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("💾 Guardar Concepto", use_container_width=True):
                                st.success("Concepto guardado en tus ideas!")
                        with col2:
                            if st.button("🔄 Generar Variación", use_container_width=True):
                                st.rerun()
                        with col3:
                            if st.button("📅 Agendar Cita", use_container_width=True):
                                st.info("Redirigiendo a agenda...")
                    
                    else:
                        st.error("❌ Error al generar el diseño. Intenta nuevamente.")
                        
                        # Idea de ejemplo para demo
                        st.info("💡 **Idea de ejemplo (modo demo):**")
                        example_ideas = {
                            "Minimalista": "Líneas geométricas finas que forman un patrón de mandala en el brazo, usando solo negro para un look limpio y moderno.",
                            "Realismo": "Retrato detallado con sombras profundas y highlights, capturando texturas de piel y expresiones realistas.",
                            "Acuarela": "Efectos de pintura difuminada con colores vibrantes que simulan acuarela, sin líneas definidas.",
                            "Japonés": "Dragón tradicional con escamas detalladas, nubes y olas, usando líneas gruesas y colores primarios."
                        }
                        st.write(example_ideas.get(style, "Diseño creativo que combina elementos únicos con tu estilo preferido."))
    
    with col2:
        st.subheader("📚 Catálogo de Estilos")
        
        categories = api_client.get_design_categories()
        if not categories:
            categories = [
                {"style_name": "Minimalista", "characteristics": "Líneas simples, diseños limpios, mucho espacio negativo"},
                {"style_name": "Realismo", "characteristics": "Detalle fotográfico, sombras realistas, texturas"},
                {"style_name": "Acuarela", "characteristics": "Efectos de pintura, difuminados, sin líneas negras"},
                {"style_name": "Japonés", "characteristics": "Tradicional, líneas gruesas, motivos simbólicos"},
                {"style_name": "Geométrico", "characteristics": "Formas perfectas, patrones, simetría"},
            ]
        
        for category in categories:
            with st.expander(f"🎨 {category.get('style_name', 'Categoría')}"):
                st.write(category.get('characteristics', 'Sin descripción'))
                
                # Información adicional por estilo
                style_info = {
                    "Minimalista": "Ideal para primeros tatuajes, curación rápida, look moderno",
                    "Realismo": "Requiere múltiples sesiones, técnica avanzada, resultados impactantes",
                    "Acuarela": "Efecto artístico, colores vibrantes, necesita retoques periódicos",
                    "Japonés": "Tradición centenaria, llenado completo, significado cultural",
                    "Geométrico": "Precisión matemática, diseño simétrico, look contemporáneo"
                }
                st.info(style_info.get(category.get('style_name', '')))
        
        st.markdown("---")
        st.subheader("🎓 Tips de Diseño")
        
        tips = [
            "💡 **Considera la anatomía**: Los diseños deben fluir con las curvas del cuerpo",
            "🎨 **Paleta de colores**: Limita a 3-4 colores principales para cohesión",
            "📏 **Escala adecuada**: Los detalles finos se pierden en áreas muy pequeñas",
            "⏱️ **Tiempo realista**: Calcula 1-2 horas por palma de mano de área",
            "🔍 **Ubicación estratégica**: Considera visibilidad y dolor al elegir ubicación"
        ]
        
        for tip in tips:
            st.write(tip)

def show_personal_analytics():
    st.title("📊 Mis Analytics")
    st.info("Mide tu rendimiento y crecimiento como artista")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Ingresos Totales", "$8,450", "+12%")
    
    with col2:
        st.metric("Clientes este Año", "45", "+8")
    
    with col3:
        st.metric("Tasa de Retención", "78%", "+5%")
    
    with col4:
        st.metric("Satisfacción", "4.8/5", "+0.2")
    
    # Gráficos de analytics
    st.subheader("📈 Rendimiento Mensual")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Citas por Mes**")
        monthly_data = pd.DataFrame({
            'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
            'Citas': [6, 8, 12, 10, 15, 8]
        })
        fig = px.line(monthly_data, x='Mes', y='Citas', markers=True,
                     title="Evolución de Citas Mensuales")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.info("**Estilos Más Solicitados**")
        styles_data = pd.DataFrame({
            'Estilo': ['Minimalista', 'Realismo', 'Acuarela', 'Geométrico', 'Japonés'],
            'Solicitudes': [8, 5, 3, 2, 1]
        })
        fig = px.bar(styles_data, x='Estilo', y='Solicitudes', 
                    color='Solicitudes', title="Popularidad de Estilos")
        st.plotly_chart(fig, use_container_width=True)
    
    # Métricas de engagement
    st.subheader("🎯 Engagement con Clientes")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Clientes Recurrentes", "15", "+3")
    
    with col2:
        st.metric("Referidos por Clientes", "12", "+2")
    
    with col3:
        st.metric("Reseñas Positivas", "23", "+4")
    
    # Análisis de rentabilidad
    st.subheader("💰 Análisis de Rentabilidad")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Ingresos por Estilo**")
        revenue_data = pd.DataFrame({
            'Estilo': ['Realismo', 'Japonés', 'Acuarela', 'Minimalista', 'Geométrico'],
            'Ingreso Promedio': [800, 600, 450, 300, 350]
        })
        fig = px.bar(revenue_data, x='Estilo', y='Ingreso Promedio',
                    color='Ingreso Promedio', title="Ingreso Promedio por Estilo")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.info("**Eficiencia de Tiempo**")
        efficiency_data = pd.DataFrame({
            'Estilo': ['Minimalista', 'Geométrico', 'Acuarela', 'Japonés', 'Realismo'],
            'Horas por Trabajo': [2, 3, 4, 6, 8],
            'Ingreso por Hora': [150, 117, 113, 100, 100]
        })
        fig = px.scatter(efficiency_data, x='Horas por Trabajo', y='Ingreso por Hora',
                        size='Ingreso por Hora', color='Estilo',
                        title="Eficiencia: Ingreso vs Tiempo")
        st.plotly_chart(fig, use_container_width=True)
    
    # Metas y objetivos
    st.subheader("🎯 Mis Metas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Meta Ingresos Mensuales", "$1,500", "$1,200", delta_color="normal")
        st.progress(1200/1500)
    
    with col2:
        st.metric("Meta Clientes Mensuales", "10", "8", delta_color="normal")
        st.progress(8/10)
    
    with col3:
        st.metric("Meta Portfolio", "30 trabajos", "24 trabajos", delta_color="normal")
        st.progress(24/30)
    
    # Recomendaciones
    st.subheader("💡 Recomendaciones para Crecer")
    
    recommendations = [
        "🎨 **Desarrolla tu estilo signature**: Los clientes buscan artistas con estilo único",
        "📱 **Activa tus redes sociales**: Postea regularmente en Instagram y TikTok",
        "⭐ **Solicita reseñas**: Pide a clientes satisfechos que dejen reseñas",
        "🔄 **Crea un proceso claro**: Desde consulta hasta cuidado posterior",
        "📚 **Continúa aprendiendo**: Toma cursos de nuevas técnicas y estilos"
    ]
    
    for rec in recommendations:
        st.write(rec)

if __name__ == "__main__":
    main()
