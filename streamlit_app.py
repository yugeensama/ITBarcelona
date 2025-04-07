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

# --- Datos iniciales (modelos de switches y bocas) ---
if "modelos_switches" not in st.session_state:
    st.session_state.modelos_switches = {
        "Cisco Catalyst 2960": 24,
        "Cisco Catalyst 3560": 48,
        "HP ProCurve 2520": 24,
        "TP-Link TL-SG1024": 24,
        "Ubiquiti USW-24": 24
    }

if "config_bocas" not in st.session_state:
    st.session_state.config_bocas = pd.DataFrame(columns=[
        "Modelo", "Total_Bocas", "Bocas_Disponibles", "Bocas_Ocupadas", "Notas"
    ])

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
    ["🏠 Inicio", "📦 Inventario", "🔌 Configurar Bocas", "📊 Reportes"]
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
        st.metric("Switches Registrados", len(st.session_state.config_bocas))

# 2. Inventario
elif menu_principal == "📦 Inventario":
    # (Mismo código de filtrado y tabla que antes)
    ...

# 3. Configuración de Bocas (¡Nueva sección interactiva!)
elif menu_principal == "🔌 Configurar Bocas":
    st.header("🔌 Configuración de Bocas de Switch")
    
    # Pestañas para gestión
    tab1, tab2 = st.tabs(["📋 Registrar Switch", "📊 Estado de Bocas"])
    
    with tab1:
        st.markdown("### 📋 Registrar Nuevo Switch")
        with st.form("form_switch"):
            col1, col2 = st.columns(2)
            with col1:
                modelo = st.selectbox(
                    "Modelo de Switch",
                    options=list(st.session_state.modelos_switches.keys()),
                    help="Selecciona un modelo predefinido o añade uno nuevo."
                )
                total_bocas = st.number_input(
                    "Total de Bocas",
                    min_value=1,
                    value=st.session_state.modelos_switches.get(modelo, 24),
                    key="total_bocas"
                )
            with col2:
                bocas_ocupadas = st.number_input(
                    "Bocas Ocupadas",
                    min_value=0,
                    max_value=total_bocas,
                    value=0,
                    help="Número de bocas en uso."
                )
                notas = st.text_area("Notas (Opcional)")
            
            if st.form_submit_button("💾 Guardar Configuración"):
                nuevo_switch = {
                    "Modelo": modelo,
                    "Total_Bocas": total_bocas,
                    "Bocas_Disponibles": total_bocas - bocas_ocupadas,
                    "Bocas_Ocupadas": bocas_ocupadas,
                    "Notas": notas
                }
                st.session_state.config_bocas = pd.concat([
                    st.session_state.config_bocas,
                    pd.DataFrame([nuevo_switch])
                ], ignore_index=True)
                st.success("✅ Switch registrado correctamente!")
    
    with tab2:
        st.markdown("### 📊 Estado Actual de Bocas")
        if not st.session_state.config_bocas.empty:
            st.dataframe(st.session_state.config_bocas, use_container_width=True)
            
            # Gráfico de ocupación (nativo de Streamlit)
            st.markdown("### 📈 Ocupación de Bocas")
            st.bar_chart(st.session_state.config_bocas.set_index("Modelo")[["Bocas_Disponibles", "Bocas_Ocupadas"]])
        else:
            st.warning("No hay switches registrados.")

# 4. Reportes
elif menu_principal == "📊 Reportes":
    # (Código de reportes existente)
    ...
