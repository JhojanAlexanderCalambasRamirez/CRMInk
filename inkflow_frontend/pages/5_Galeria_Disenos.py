import streamlit as st
from services.api_client import api_client
from services.session_state import is_authenticated

st.set_page_config(page_title="Galería - InkFlow CRM", page_icon="🎨")

if not is_authenticated():
    st.warning("🔐 Por favor inicia sesión para acceder a esta página")
    st.stop()

def show_design_gallery():
    st.title("🎨 Galería de Diseños")
    st.markdown("---")
    
    # Obtener categorías
    categories_data = api_client.get_design_categories()
    categories = categories_data if categories_data else []
    
    if not categories:
        st.info("📡 Conectando con el servidor...")
        # Datos de ejemplo para demo
        categories = [
            {"id": 1, "style_name": "Minimalista", "characteristics": "Líneas simples y diseños limpios"},
            {"id": 2, "style_name": "Realismo", "characteristics": "Detalle fotográfico y sombras"},
            {"id": 3, "style_name": "Acuarela", "characteristics": "Efectos de pintura y difuminados"},
            {"id": 4, "style_name": "Japonés", "characteristics": "Tradicional con líneas gruesas"},
        ]
    
    # Selector de categoría
    category_names = [cat['style_name'] for cat in categories]
    selected_category = st.selectbox("Selecciona una categoría:", category_names)
    
    if selected_category:
        # Encontrar categoría seleccionada
        selected_cat = next((cat for cat in categories if cat['style_name'] == selected_category), None)
        
        if selected_cat:
            st.info(f"🔍 Mostrando diseños de: **{selected_category}**")
            st.caption(selected_cat.get('characteristics', ''))
            
            # Placeholder para diseños (en una app real, estos vendrían de la API)
            st.markdown("### 🖼️ Diseños de Ejemplo")
            
            cols = st.columns(3)
            design_examples = [
                {"name": "Líneas Geométricas", "desc": "Diseño con patrones simétricos", "time": "60 min", "price": "$80-150"},
                {"name": "Puntos y Círculos", "desc": "Composición orgánica minimalista", "time": "45 min", "price": "$60-120"},
                {"name": "Texto Delicado", "desc": "Frases en tipografía fina", "time": "90 min", "price": "$100-200"},
            ]
            
            for idx, design in enumerate(design_examples):
                with cols[idx % 3]:
                    st.image(
                        "https://via.placeholder.com/200x200/4CAF50/white?text=🎨", 
                        use_column_width=True,
                        caption=design["name"]
                    )
                    st.write(f"**{design['name']}**")
                    st.caption(design["desc"])
                    st.metric("Tiempo", design["time"])
                    st.metric("Precio", design["price"])
                    
                    if st.button("Seleccionar", key=f"select_{idx}"):
                        st.success(f"✅ Diseño '{design['name']}' seleccionado!")
    
    # Búsqueda por preferencias
    st.markdown("---")
    st.header("🔍 Encuentra diseños por tus preferencias")
    
    with st.form("design_preferences"):
        col1, col2 = st.columns(2)
        
        with col1:
            preferred_styles = st.multiselect(
                "Estilos que te gustan:",
                options=[cat['style_name'] for cat in categories],
                default=["Minimalista"]
            )
            max_budget = st.slider("Presupuesto máximo (USD):", 50, 2000, 500)
        
        with col2:
            body_area = st.selectbox("Área del cuerpo:", 
                                   ["Cualquiera", "brazo", "espalda", "pecho", "pierna", "muñeca", "cuello"])
            max_time = st.number_input("Tiempo disponible (minutos):", min_value=30, max_value=480, value=180)
        
        submitted = st.form_submit_button("🎯 Buscar Diseños Recomendados", use_container_width=True)
        
        if submitted and preferred_styles:
            preferences = {
                "styles": preferred_styles,
                "max_budget": max_budget,
                "min_budget": 0,
                "body_area": body_area if body_area != "Cualquiera" else None,
                "max_time": max_time
            }
            
            matched_designs = api_client.match_designs(preferences)
            
            if matched_designs:
                st.success(f"🎯 Encontramos {len(matched_designs)} diseños que coinciden con tus preferencias!")
                
                for design in matched_designs:
                    with st.expander(f"🎨 {design.get('design_name', 'Diseño')} - {design.get('match_percentage', 0)}% match"):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.image(
                                "https://via.placeholder.com/150x150/2196F3/white?text=🎨",
                                width=150
                            )
                        with col2:
                            st.write(f"**Descripción:** {design.get('description', 'Sin descripción')}")
                            st.write(f"**Tiempo estimado:** {design.get('estimated_time_min', 'N/A')} minutos")
                            st.write(f"**Precio estimado:** ${design.get('estimated_price_range', {}).get('min', 'N/A')} - ${design.get('estimated_price_range', {}).get('max', 'N/A')}")
                            st.write(f"**Nivel de complejidad:** {design.get('complexity_level', 'N/A')}/5")
                            
                            if st.button("💝 Seleccionar este diseño", key=f"select_match_{design.get('id', '0')}"):
                                st.session_state.selected_design_for_booking = design
                                st.success("Diseño seleccionado! Ahora puedes buscar un tatuador.")
            else:
                st.warning("No encontramos diseños que coincidan exactamente. Intenta ampliar tus criterios.")

if __name__ == "__main__":
    show_design_gallery()
