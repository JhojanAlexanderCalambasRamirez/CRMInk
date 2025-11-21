import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Findink CRM Global",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Sidebar para navegación
    with st.sidebar:
        st.title("👑 Findink CRM")
        st.markdown("---")
        st.success("🔓 Modo Demo - CRM Global")
        st.caption("Sistema de gestión multi-tenant")
        st.markdown("---")
        
        # Navegación
        page = st.selectbox(
            "Navegación",
            ["📊 Dashboard Sistema", "👥 CRMs Activos", "📈 Analytics Mercado", "💰 Facturación", "⚙️ Configuración"]
        )
        
        st.markdown("---")
        st.caption("Findink CRM v1.0 - Sistema Global")
    
    # Contenido según página seleccionada
    if page == "📊 Dashboard Sistema":
        show_system_dashboard()
    elif page == "👥 CRMs Activos":
        show_active_crms()
    elif page == "📈 Analytics Mercado":
        show_market_analytics()
    elif page == "💰 Facturación":
        show_billing()
    elif page == "⚙️ Configuración":
        show_system_config()

def show_system_dashboard():
    st.title("📊 Dashboard Sistema - Findink CRM")
    st.info("Vista global de todos los CRMs activos en la plataforma")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("CRMs Activos", "24", "+3", delta_color="normal")
    
    with col2:
        st.metric("Tatuadores Registrados", "156", "+12", delta_color="normal")
    
    with col3:
        st.metric("Ingresos Mensuales", "$2,850", "+$320", delta_color="normal")
    
    with col4:
        st.metric("Tasa de Crecimiento", "18%", "+3%", delta_color="normal")
    
    # Segunda fila de métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Plan Básico", "15")
    
    with col2:
        st.metric("Plan Premium", "7")
    
    with col3:
        st.metric("Plan Enterprise", "2")
    
    with col4:
        st.metric("Satisfacción General", "92%", "+2%", delta_color="normal")
    
    # Gráficos del sistema
    st.subheader("📈 Panorama del Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Distribución de Planes**")
        plans_data = pd.DataFrame({
            'Plan': ['Básico', 'Premium', 'Enterprise'],
            'Usuarios': [15, 7, 2]
        })
        fig = px.pie(plans_data, values='Usuarios', names='Plan', 
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.info("**Crecimiento Mensual**")
        growth_data = pd.DataFrame({
            'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
            'CRMs': [12, 15, 18, 22, 24, 28]
        })
        fig = px.line(growth_data, x='Mes', y='CRMs', markers=True,
                     title="Nuevos CRMs por Mes")
        st.plotly_chart(fig, use_container_width=True)
    
    # CRMs más activos
    st.subheader("🏆 CRMs Más Activos")
    
    active_crms = [
        {"nombre": "Studio InkMaster", "plan": "Enterprise", "citas_mes": 45, "ingresos": "$1,200", "satisfaccion": 95},
        {"nombre": "Tattoo Artisans", "plan": "Premium", "citas_mes": 32, "ingresos": "$850", "satisfaccion": 92},
        {"nombre": "Urban Ink", "plan": "Premium", "citas_mes": 28, "ingresos": "$740", "satisfaccion": 88},
        {"nombre": "Skin Canvas", "plan": "Básico", "citas_mes": 18, "ingresos": "$480", "satisfaccion": 85},
    ]
    
    for crm in active_crms:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
            with col1:
                st.write(f"**{crm['nombre']}**")
                st.write(f"_{crm['plan']}_")
            with col2:
                st.write(f"📅 {crm['citas_mes']} citas")
            with col3:
                st.write(f"💰 {crm['ingresos']}")
            with col4:
                st.write(f"⭐ {crm['satisfaccion']}%")
            with col5:
                progress = crm['satisfaccion'] / 100
                st.progress(progress)
            st.markdown("---")
    
    # Actividad reciente del sistema
    st.subheader("🔔 Actividad Reciente del Sistema")
    
    activities = [
        {"tipo": "🎯 Nuevo Registro", "detalle": "Studio Dragon Ink se registró en Plan Premium", "tiempo": "Hace 2 horas"},
        {"tipo": "💳 Pago Confirmado", "detalle": "Tattoo Legends - Pago mensual $79", "tiempo": "Hace 4 horas"},
        {"tipo": "⬆️ Upgrade", "detalle": "Skin Artists actualizó a Plan Enterprise", "tiempo": "Hace 6 horas"},
        {"tipo": "🔧 Soporte", "detalle": "Ink Revolution solicitó configuración avanzada", "tiempo": "Hace 1 día"},
    ]
    
    for activity in activities:
        with st.container():
            col1, col2, col3 = st.columns([2, 3, 1])
            with col1:
                st.write(f"**{activity['tipo']}**")
            with col2:
                st.write(activity['detalle'])
            with col3:
                st.write(f"_{activity['tiempo']}_")
            st.markdown("---")

def show_active_crms():
    st.title("👥 CRMs Activos - Findink")
    st.info("Gestión de todos los CRMs individuales de tatuadores")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        plan_filter = st.selectbox("Filtrar por Plan", ["Todos", "Básico", "Premium", "Enterprise"])
    
    with col2:
        status_filter = st.selectbox("Filtrar por Estado", ["Todos", "Activo", "Inactivo", "Prueba"])
    
    with col3:
        st.write("")
        export_btn = st.button("📊 Exportar Reporte", use_container_width=True)
        if export_btn:
            st.success("Reporte exportado exitosamente!")
    
    # Lista de CRMs activos
    st.subheader("📋 Lista de CRMs Activos")
    
    crms_data = [
        {"id": 1, "nombre": "Studio InkMaster", "email": "inkmaster@studio.com", "plan": "Enterprise", 
         "estado": "Activo", "registro": "2024-01-15", "citas_mes": 45, "ingresos": "$1,200"},
        {"id": 2, "nombre": "Tattoo Artisans", "email": "artisans@tattoo.com", "plan": "Premium", 
         "estado": "Activo", "registro": "2024-02-10", "citas_mes": 32, "ingresos": "$850"},
        {"id": 3, "nombre": "Urban Ink", "email": "urban@ink.com", "plan": "Premium", 
         "estado": "Activo", "registro": "2024-02-28", "citas_mes": 28, "ingresos": "$740"},
        {"id": 4, "nombre": "Skin Canvas", "email": "skin@canvas.com", "plan": "Básico", 
         "estado": "Activo", "registro": "2024-03-05", "citas_mes": 18, "ingresos": "$480"},
        {"id": 5, "nombre": "Dragon Ink", "email": "dragon@ink.com", "plan": "Premium", 
         "estado": "Prueba", "registro": "2024-03-12", "citas_mes": 8, "ingresos": "$0"},
    ]
    
    # Aplicar filtros
    filtered_crms = crms_data
    if plan_filter != "Todos":
        filtered_crms = [crm for crm in filtered_crms if crm['plan'] == plan_filter]
    if status_filter != "Todos":
        filtered_crms = [crm for crm in filtered_crms if crm['estado'] == status_filter]
    
    # Mostrar CRMs
    for crm in filtered_crms:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
            with col1:
                st.write(f"**{crm['nombre']}**")
                st.write(f"📧 {crm['email']}")
            with col2:
                st.write(f"🎯 {crm['plan']}")
                st.write(f"📅 {crm['citas_mes']} citas")
            with col3:
                st.write(f"💰 {crm['ingresos']}")
                st.write(f"📆 {crm['registro']}")
            with col4:
                status_color = "🟢" if crm['estado'] == "Activo" else "🟡" if crm['estado'] == "Prueba" else "🔴"
                st.write(f"{status_color} {crm['estado']}")
            with col5:
                if st.button("👁️", key=f"view_{crm['id']}"):
                    st.write(f"**Detalles de {crm['nombre']}**")
                    st.write(f"Plan: {crm['plan']}")
                    st.write(f"Estado: {crm['estado']}")
                    st.write(f"Registro: {crm['registro']}")
                    st.write(f"Citas este mes: {crm['citas_mes']}")
                    st.write(f"Ingresos: {crm['ingresos']}")
            st.markdown("---")
    
    # Métricas resumen
    st.subheader("📊 Resumen de CRMs")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_crms = len(crms_data)
        active_crms = len([c for c in crms_data if c['estado'] == 'Activo'])
        st.metric("CRMs Totales", total_crms, f"{active_crms} activos")
    
    with col2:
        basic_plan = len([c for c in crms_data if c['plan'] == 'Básico'])
        st.metric("Plan Básico", basic_plan)
    
    with col3:
        premium_plan = len([c for c in crms_data if c['plan'] == 'Premium'])
        st.metric("Plan Premium", premium_plan)
    
    with col4:
        enterprise_plan = len([c for c in crms_data if c['plan'] == 'Enterprise'])
        st.metric("Plan Enterprise", enterprise_plan)

def show_market_analytics():
    st.title("📈 Analytics de Mercado - Findink")
    st.info("Análisis completo del mercado de tatuajes y competencia")
    
    # Métricas de mercado
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tatuadores en Plataforma", "245", "+15")
    
    with col2:
        st.metric("Crecimiento Mercado", "+15%", "+3%")
    
    with col3:
        st.metric("Estudios Activos", "89", "+5")
    
    with col4:
        st.metric("Ingresos Totales", "$28,500", "+$2,100")
    
    # Gráficos de analytics avanzados
    st.subheader("🌍 Distribución Geográfica")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Usuarios por Ciudad**")
        city_data = pd.DataFrame({
            'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao'],
            'Usuarios': [45, 38, 22, 15, 12]
        })
        fig = px.bar(city_data, x='Ciudad', y='Usuarios', 
                    color='Usuarios', color_continuous_scale='viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.info("**Crecimiento por Región**")
        region_data = pd.DataFrame({
            'Región': ['Norte', 'Centro', 'Este', 'Sur', 'Islas'],
            'Crecimiento': [18, 25, 22, 15, 8]
        })
        fig = px.line(region_data, x='Región', y='Crecimiento', 
                     markers=True, title="Crecimiento (%) por Región")
        st.plotly_chart(fig, use_container_width=True)
    
    # Tendencias del mercado
    st.subheader("📊 Tendencias del Mercado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Estilos Más Populares**")
        styles_data = pd.DataFrame({
            'Estilo': ['Minimalista', 'Realismo', 'Japonés', 'Acuarela', 'Geométrico'],
            'Popularidad': [35, 28, 20, 12, 5]
        })
        fig = px.pie(styles_data, values='Popularidad', names='Estilo',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.info("**Retención de Clientes**")
        retention_data = pd.DataFrame({
            'Mes': ['Mes 1', 'Mes 2', 'Mes 3', 'Mes 6', 'Mes 12'],
            'Retención': [85, 78, 72, 65, 58]
        })
        fig = px.area(retention_data, x='Mes', y='Retención',
                     title="Tasa de Retención (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Análisis de competencia
    st.subheader("🔍 Análisis Competitivo")
    
    competition_data = pd.DataFrame({
        "Plataforma": ["Findink", "TattooCRM", "InkManager", "ArtistSuite"],
        "Usuarios": [245, 180, 120, 95],
        "Crecimiento (%)": [18, 12, 8, 6],
        "Satisfacción": [92, 85, 78, 82],
        "Precio Promedio": ["$79", "$65", "$89", "$72"]
    })
    
    st.dataframe(competition_data, use_container_width=True)
    
    # Gráfico comparativo
    fig = px.bar(competition_data, x='Plataforma', y='Usuarios',
                color='Crecimiento (%)', title="Comparativa de Plataformas")
    st.plotly_chart(fig, use_container_width=True)

def show_billing():
    st.title("💰 Facturación - Findink")
    st.info("Sistema de facturación y gestión de ingresos")
    
    # Resumen financiero
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Ingresos Mensuales", "$2,850")
    
    with col2:
        st.metric("Ingresos Anuales", "$34,200")
    
    with col3:
        st.metric("Clientes Activos", "24")
    
    with col4:
        st.metric("Tasa de Renovación", "92%")
    
    # Facturación detallada
    st.subheader("📋 Facturación Reciente")
    
    invoices = [
        {"cliente": "Studio InkMaster", "plan": "Enterprise", "monto": "$199", "fecha": "2024-03-01", "estado": "Pagado"},
        {"cliente": "Tattoo Artisans", "plan": "Premium", "monto": "$79", "fecha": "2024-03-01", "estado": "Pagado"},
        {"cliente": "Urban Ink", "plan": "Premium", "monto": "$79", "fecha": "2024-03-01", "estado": "Pagado"},
        {"cliente": "Skin Canvas", "plan": "Básico", "monto": "$29", "fecha": "2024-02-28", "estado": "Pagado"},
        {"cliente": "Dragon Ink", "plan": "Premium", "monto": "$79", "fecha": "2024-02-28", "estado": "Pendiente"},
    ]
    
    for invoice in invoices:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
            with col1:
                st.write(f"**{invoice['cliente']}**")
                st.write(f"_{invoice['plan']}_")
            with col2:
                st.write(f"💰 {invoice['monto']}")
            with col3:
                st.write(f"📅 {invoice['fecha']}")
            with col4:
                status_color = "🟢" if invoice['estado'] == "Pagado" else "🟡"
                st.write(f"{status_color} {invoice['estado']}")
            with col5:
                if st.button("📧", key=f"invoice_{invoice['cliente']}"):
                    st.info(f"Reenviar factura a {invoice['cliente']}")
            st.markdown("---")
    
    # Proyecciones de ingresos
    st.subheader("📈 Proyecciones de Ingresos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Ingresos por Plan**")
        revenue_data = pd.DataFrame({
            'Plan': ['Básico ($29)', 'Premium ($79)', 'Enterprise ($199)'],
            'Ingresos': [15 * 29, 7 * 79, 2 * 199]
        })
        fig = px.bar(revenue_data, x='Plan', y='Ingresos', 
                    color='Ingresos', title="Ingresos Mensuales por Plan")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.info("**Crecimiento Proyectado**")
        growth_data = pd.DataFrame({
            'Trimestre': ['Q1', 'Q2', 'Q3', 'Q4'],
            'Ingresos': [2850, 3200, 3800, 4500]
        })
        fig = px.line(growth_data, x='Trimestre', y='Ingresos', 
                     markers=True, title="Proyección de Ingresos")
        st.plotly_chart(fig, use_container_width=True)

def show_system_config():
    st.title("⚙️ Configuración del Sistema")
    st.info("Panel de configuración global de Findink CRM")
    
    # Configuración general
    with st.expander("🔧 Configuración General", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            platform_name = st.text_input("Nombre de la Plataforma", value="Findink CRM")
            support_email = st.text_input("Email de Soporte", value="soporte@findink.com")
            trial_days = st.number_input("Días de Prueba Gratuita", min_value=7, max_value=30, value=14)
        
        with col2:
            basic_limit = st.number_input("Límite Citas Plan Básico", min_value=10, max_value=100, value=50)
            premium_limit = st.number_input("Límite Citas Plan Premium", min_value=100, max_value=500, value=200)
            open_registration = st.checkbox("Registro Abierto", value=True)
            auto_approval = st.checkbox("Aprobación Automática", value=True)
        
        if st.button("💾 Guardar Configuración General", use_container_width=True):
            st.success("Configuración general guardada exitosamente")
    
    # Gestión de planes
    with st.expander("💰 Gestión de Planes"):
        st.subheader("Configuración de Planes")
        
        plans_config = [
            {"plan": "Básico", "precio": 29, "caracteristicas": "Agenda, Portfolio, 50 citas/mes, Soporte básico"},
            {"plan": "Premium", "precio": 79, "caracteristicas": "Todo Básico + Analytics, IA, 200 citas, Soporte prioritario"},
            {"plan": "Enterprise", "precio": 199, "caracteristicas": "Todo Premium + Ilimitado, API acceso, Soporte 24/7"},
        ]
        
        for plan in plans_config:
            st.markdown(f"### {plan['plan']}")
            col1, col2, col3 = st.columns([2, 2, 4])
            with col1:
                plan_name = st.text_input("Nombre Plan", value=plan["plan"], key=f"name_{plan['plan']}")
            with col2:
                plan_price = st.number_input("Precio ($)", value=plan["precio"], key=f"price_{plan['plan']}")
            with col3:
                plan_features = st.text_input("Características", value=plan["caracteristicas"], key=f"features_{plan['plan']}")
            
            st.markdown("---")
        
        if st.button("💾 Actualizar Planes", use_container_width=True):
            st.success("Planes actualizados exitosamente")
    
    # Configuración de API
    with st.expander("🔑 Configuración API y Seguridad"):
        st.subheader("Configuración de Integraciones")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gemini_key = st.text_input("Gemini API Key", type="password", placeholder="Ingresa tu API key de Google Gemini")
            stripe_key = st.text_input("Stripe Secret Key", type="password", placeholder="Ingresa tu clave secreta de Stripe")
        
        with col2:
            smtp_password = st.text_input("Email SMTP Password", type="password", placeholder="Contraseña SMTP para emails")
            encryption_key = st.text_input("Clave de Encriptación", type="password", placeholder="Clave para encriptación de datos")
        
        if st.button("💾 Guardar Configuración API", use_container_width=True):
            st.success("Configuración API guardada exitosamente")
    
    # Configuración de notificaciones
    with st.expander("🔔 Configuración de Notificaciones"):
        st.subheader("Preferencias de Notificaciones")
        
        col1, col2 = st.columns(2)
        
        with col1:
            email_notifications = st.checkbox("Notificaciones por Email", value=True)
            new_user_alerts = st.checkbox("Alertas de Nuevos Usuarios", value=True)
            payment_alerts = st.checkbox("Alertas de Pagos", value=True)
        
        with col2:
            system_alerts = st.checkbox("Alertas del Sistema", value=True)
            weekly_reports = st.checkbox("Reportes Semanales", value=True)
            monthly_reports = st.checkbox("Reportes Mensuales", value=True)
        
        if st.button("💾 Guardar Preferencias", use_container_width=True):
            st.success("Preferencias de notificaciones guardadas")

if __name__ == "__main__":
    main()
