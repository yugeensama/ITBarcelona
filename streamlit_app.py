import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuración de la página ---
st.set_page_config(
    page_title="Gestión de Activos de TI",
    page_icon="💻",
    layout="wide"
)

# --- Estilos CSS ---
st.markdown("""
    <style>
    .card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        background-color: #f9f9f9;
    }
    .titulo-seccion {
        font-size: 1.5em;
        color: #2e86c1;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Funciones clave ---
def cargar_datos():
    if "inventario" not in st.session_state:
        st.session_state.inventario = pd.DataFrame(columns=[
            "ID", "Categoría", "Tipo", "Marca", "Modelo", "Serial", 
            "Usuario", "Departamento", "Fecha_Adquisicion", "Estado", "Notas"
        ])

def guardar_excel(df):
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"inventario_activos_{fecha_actual}.xlsx"
    df.to_excel(nombre_archivo, index=False)
    return nombre_archivo

# --- Carga inicial ---
cargar_datos()

# --- Sidebar (Menú) ---
st.sidebar.title("⚙️ Menú de Gestión")
menu_principal = st.sidebar.radio(
    "**Opciones Principales**",
    ["🏠 Inicio", "📦 Inventario", "📊 Reportes", "⚙️ Configuración"]
)

if menu_principal == "📦 Inventario":
    st.sidebar.markdown("### 📦 Categorías")
    submenu = st.sidebar.selectbox(
        "Seleccione:",
        ["💻 Ordenadores", "🔌 Switch", "🌐 Routers", "Todos los Activos"]
    )

# --- Contenido Principal ---
st.title("💻 Gestión de Activos de TI")

# 1. Página de Inicio
if menu_principal == "🏠 Inicio":
    st.markdown("""
        <div class="card">
            <h2 class="titulo-seccion">Bienvenido al Sistema de Gestión de Activos</h2>
            <p>Utiliza el menú lateral para navegar.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Activos", len(st.session_state.inventario))
    with col2:
        activos_operativos = len(st.session_state.inventario[st.session_state.inventario["Estado"] == "Activo"])
        st.metric("Activos Operativos", activos_operativos)
    with col3:
        st.metric("En Mantenimiento", 
                 len(st.session_state.inventario[st.session_state.inventario["Estado"] == "En Mantenimiento"]))
    
    # Gráfico alternativo (sin Plotly)
    if not st.session_state.inventario.empty:
        st.markdown("### 📊 Distribución por Categoría")
        st.bar_chart(st.session_state.inventario["Categoría"].value_counts())

# 2. Inventario (con submenú)
elif menu_principal == "📦 Inventario":
    # Filtrado por categoría
    if submenu == "💻 Ordenadores":
        st.header("💻 Ordenadores")
        df_filtrado = st.session_state.inventario[st.session_state.inventario["Categoría"] == "Ordenadores"]
    elif submenu == "🔌 Switch":
        st.header("🔌 Switch")
        df_filtrado = st.session_state.inventario[st.session_state.inventario["Categoría"] == "Switch"]
    elif submenu == "🌐 Routers":
        st.header("🌐 Routers")
        df_filtrado = st.session_state.inventario[st.session_state.inventario["Categoría"] == "Routers"]
    else:
        st.header("Todos los Activos")
        df_filtrado = st.session_state.inventario
    
    # Tabla y acciones
    st.dataframe(df_filtrado, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Agregar Activo"):
            st.session_state["mostrar_formulario"] = True
    with col2:
        if st.button("📥 Exportar a Excel") and not df_filtrado.empty:
            nombre_archivo = guardar_excel(df_filtrado)
            st.success(f"✅ Exportado: {nombre_archivo}")
    
    # Formulario dinámico
    if st.session_state.get("mostrar_formulario"):
        with st.form("form_activo"):
            st.markdown("### 📝 Nuevo Activo")
            categoria = st.selectbox("Categoría", ["Ordenadores", "Switch", "Routers", "Otros"])
            tipo = st.text_input("Tipo (ej: Laptop, Cisco 2960)")
            if st.form_submit_button("💾 Guardar"):
                nuevo_activo = {
                    "ID": len(st.session_state.inventario) + 1,
                    "Categoría": categoria,
                    "Tipo": tipo,
                    # ... (resto de campos)
                }
                st.session_state.inventario = pd.concat([
                    st.session_state.inventario,
                    pd.DataFrame([nuevo_activo])
                ], ignore_index=True)
                st.success("✅ ¡Activo agregado!")
                st.session_state["mostrar_formulario"] = False

# 3. Reportes (alternativo sin Plotly)
elif menu_principal == "📊 Reportes":
    st.header("📊 Reportes")
    if not st.session_state.inventario.empty:
        st.markdown("### 📈 Activos por Estado")
        st.bar_chart(st.session_state.inventario["Estado"].value_counts())
        
        st.markdown("### 📅 Adquisiciones por Año")
        if "Fecha_Adquisicion" in st.session_state.inventario.columns:
            st.session_state.inventario["Año"] = pd.to_datetime(st.session_state.inventario["Fecha_Adquisicion"]).dt.year
            st.line_chart(st.session_state.inventario["Año"].value_counts())
    else:
        st.warning("No hay datos para reportes.")

# 4. Configuración
elif menu_principal == "⚙️ Configuración":
    st.header("Configuración")
    st.write("Opciones avanzadas aquí.")
