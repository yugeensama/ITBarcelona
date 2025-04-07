import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px  # Para gráficos bonitos

# Configuración de la página
st.set_page_config(
    page_title="Gestión de Activos de TI",
    page_icon="💻",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .st-emotion-cache-1v0mbdj {
        border-radius: 10px;
    }
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

# Función para cargar/guardar datos
def cargar_datos():
    if "inventario" not in st.session_state:
        st.session_state.inventario = pd.DataFrame(columns=[
            "ID", "Categoría", "Tipo", "Marca", "Modelo", "Serial", "Usuario", 
            "Departamento", "Fecha_Adquisicion", "Estado", "Notas"
        ])

def guardar_excel(df):
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"inventario_activos_{fecha_actual}.xlsx"
    df.to_excel(nombre_archivo, index=False)
    return nombre_archivo

# Cargar datos iniciales
cargar_datos()

# --- SIDEBAR (Menú principal) ---
st.sidebar.title("⚙️ Menú de Gestión")
menu_principal = st.sidebar.radio(
    "**Opciones Principales**",
    ["🏠 Inicio", "📦 Inventario", "📊 Reportes", "⚙️ Configuración"]
)

# --- SUBMENÚ: INVENTARIO ---
if menu_principal == "📦 Inventario":
    st.sidebar.markdown("### 📦 Categorías de Activos")
    submenu = st.sidebar.selectbox(
        "Seleccione una categoría:",
        ["💻 Ordenadores", "🔌 Switch", "🌐 Routers", "Todos los Activos"]
    )

# --- CONTENIDO PRINCIPAL ---
st.title("💻 Gestión de Activos de TI")

# Opción 1: Página de Inicio
if menu_principal == "🏠 Inicio":
    st.markdown("""
        <div class="card">
            <h2 class="titulo-seccion">Bienvenido al Sistema de Gestión de Activos de TI</h2>
            <p>Utiliza el menú lateral para navegar entre las diferentes opciones.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Estadísticas rápidas (ejemplo)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Activos", len(st.session_state.inventario))
    with col2:
        st.metric("Activos Operativos", len(st.session_state.inventario[st.session_state.inventario["Estado"] == "Activo"]))
    with col3:
        st.metric("En Mantenimiento", len(st.session_state.inventario[st.session_state.inventario["Estado"] == "En Mantenimiento"]))
    
    # Gráfico de distribución por categoría (usando Plotly)
    if not st.session_state.inventario.empty:
        fig = px.pie(
            st.session_state.inventario, 
            names="Categoría", 
            title="Distribución de Activos por Categoría"
        )
        st.plotly_chart(fig, use_container_width=True)

# Opción 2: Inventario (con submenú)
elif menu_principal == "📦 Inventario":
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
    
    # Mostrar tabla filtrada
    st.dataframe(df_filtrado, use_container_width=True)
    
    # Botones de acción
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Agregar Nuevo Activo"):
            st.session_state["formulario_activo"] = True
    with col2:
        if st.button("📥 Exportar a Excel"):
            if not df_filtrado.empty:
                nombre_archivo = guardar_excel(df_filtrado)
                st.success(f"✅ Exportado como: {nombre_archivo}")
            else:
                st.warning("⚠️ No hay datos para exportar.")
    
    # Formulario para agregar activo (aparece al hacer clic en el botón)
    if st.session_state.get("formulario_activo"):
        with st.form("form_agregar"):
            st.markdown("### 📝 Nuevo Activo")
            categoria = st.selectbox("Categoría", ["Ordenadores", "Switch", "Routers", "Otros"])
            tipo = st.text_input("Tipo (Ej: Laptop, Desktop, Cisco 2960)")
            marca = st.text_input("Marca")
            modelo = st.text_input("Modelo")
            serial = st.text_input("Serial")
            
            if st.form_submit_button("💾 Guardar"):
                nuevo_activo = {
                    "ID": len(st.session_state.inventario) + 1,
                    "Categoría": categoria,
                    "Tipo": tipo,
                    "Marca": marca,
                    "Modelo": modelo,
                    "Serial": serial,
                    "Usuario": "",
                    "Departamento": "",
                    "Fecha_Adquisicion": "",
                    "Estado": "Activo",
                    "Notas": ""
                }
                st.session_state.inventario = pd.concat([
                    st.session_state.inventario,
                    pd.DataFrame([nuevo_activo])
                ], ignore_index=True)
                st.success("✅ Activo agregado!")
                st.session_state["formulario_activo"] = False

# Opción 3: Reportes
elif menu_principal == "📊 Reportes":
    st.header("📊 Reportes")
    if not st.session_state.inventario.empty:
        # Gráfico de estado de activos
        fig_estado = px.bar(
            st.session_state.inventario,
            x="Estado",
            title="Activos por Estado"
        )
        st.plotly_chart(fig_estado, use_container_width=True)
    else:
        st.warning("No hay datos para generar reportes.")

# Opción 4: Configuración
elif menu_principal == "⚙️ Configuración":
    st.header("⚙️ Configuración")
    st.markdown("Opciones avanzadas de configuración.")
