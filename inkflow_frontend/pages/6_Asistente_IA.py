import streamlit as st
from services.api_client import api_client
from services.session_state import is_authenticated

st.set_page_config(page_title="Asistente IA - InkFlow CRM", page_icon="🤖")

if not is_authenticated():
    st.warning("🔐 Por favor inicia sesión para acceder a esta página")
    st.stop()

def show_ai_assistant():
    st.title("🤖 Asistente de IA para Diseños")
    st.markdown("---")
    
    st.info("""
    🎯 **Genera ideas de diseño personalizadas** usando inteligencia artificial.
    Describe lo que tienes en mente y nuestro asistente te ayudará a conceptualizarlo.
    """)
    
    # Generación de diseño
    with st.form("ai_design_form"):
        st.subheader("💡 Describe tu idea de tatuaje")
        
        prompt = st.text_area(
            "¿Qué te gustaría tatuarte?",
            placeholder="Ej: Un dragón minimalista en el brazo, con tonos negros y grises, que represente fuerza y protección...",
            height=100
        )
        
        col1, col2 = st.columns(2)
        with col1:
            style_preference = st.selectbox(
                "Estilo preferido (opcional)",
                ["Cualquiera", "Minimalista", "Realismo", "Acuarela", "Japonés", "Tradicional", "Geométrico"]
            )
        with col2:
            color_preference = st.selectbox(
                "Esquema de color (opcional)",
                ["Cualquiera", "Negro y Gris", "Color", "Blanco y Negro", "Acuarela"]
            )
        
        submitted = st.form_submit_button("🚀 Generar Idea con IA", use_container_width=True)
        
        if submitted:
            if not prompt:
                st.error("❌ Por favor describe tu idea")
            else:
                with st.spinner("🤖 Generando idea de diseño..."):
                    # Mejorar el prompt con las preferencias
                    enhanced_prompt = prompt
                    if style_preference != "Cualquiera":
                        enhanced_prompt += f", estilo {style_preference.lower()}"
                    if color_preference != "Cualquiera":
                        enhanced_prompt += f", esquema de color {color_preference.lower()}"
                    
                    result = api_client.generate_design(enhanced_prompt)
                    
                    if result:
                        st.success("✅ ¡Idea generada exitosamente!")
                        
                        design_data = result.get("generated_design", {})
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🎨 Concepto Generado")
                            st.write(f"**Nombre:** {design_data.get('design_name', 'Diseño Personalizado')}")
                            st.write(f"**Descripción:** {design_data.get('description', 'Concepto único basado en tu descripción')}")
                            
                            st.subheader("🎯 Recomendaciones")
                            styles = design_data.get('style_suggestions', [])
                            if styles:
                                st.write("**Estilos sugeridos:** " + ", ".join(styles))
                            
                            elements = design_data.get('elements', [])
                            if elements:
                                st.write("**Elementos:** " + ", ".join(elements))
                        
                        with col2:
                            st.subheader("🎨 Paleta de Colores")
                            colors = design_data.get('color_palette', [])
                            for color in colors:
                                st.write(f"▪️ {color}")
                            
                            st.subheader("⏱️ Estimaciones")
                            st.write(f"**Tiempo estimado:** {design_data.get('estimated_time', '2-3 horas')}")
                            st.write(f"**Nivel de complejidad:** {design_data.get('complexity_level', 'medio')}")
                        
                        # Acciones
                        st.markdown("---")
                        st.subheader("📝 ¿Te gusta esta idea?")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("💾 Guardar Concepto", use_container_width=True):
                                st.success("Concepto guardado en tu portafolio!")
                        with col2:
                            if st.button("🔄 Generar Variación", use_container_width=True):
                                st.info("Generando nueva variación...")
                                st.rerun()
                        with col3:
                            if st.button("📅 Buscar Tatuador", use_container_width=True):
                                st.switch_page("pages/3_Agenda.py")
                    
                    else:
                        st.error("❌ Error al generar el diseño. Intenta nuevamente.")
    
    # Ejemplos de prompts
    with st.expander("💡 Ejemplos de prompts efectivos"):
        st.markdown("""
        **Ejemplos para mejores resultados:**
        
        - *"Un zorro geométrico en la espalda, con líneas limpias y simétricas"*
        - *"Flor de loto acuarela en el muslo, con tonos rosados y verdes difuminados"*
        - *"Frase 'carpe diem' en tipografía gótica, en el antebrazo"*
        - *"Ojo realista con detalles de cristal, en la pantorrilla"*
        - *"Serpiente estilo japonés rodeando el brazo, con escamas detalladas"*
        
        **Incluye en tu descripción:**
        - 📍 **Ubicación** en el cuerpo
        - 🎨 **Estilo** preferido  
        - 🌈 **Colores** deseados
        - 📏 **Tamaño** aproximado
        - 💭 **Significado** o simbolismo
        """)

if __name__ == "__main__":
    show_ai_assistant()
