import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- Configuración de la página ---
st.set_page_config(
    page_title="Gestión de Activos y Pedidos TI",
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

# --- Datos iniciales con persistencia ---
def cargar_datos():
    # Datos de pedidos
    if "pedidos" not in st.session_state:
        if os.path.exists("pedidos_cache.pkl"):
            st.session_state.pedidos = pd.read_pickle("pedidos_cache.pkl")
        else:
            st.session_state.pedidos = pd.DataFrame(columns=[
                "ID", "CONCEPTO", "Proveedor", "Número de proveedor", "Importe", 
                "CCAR Request Number", "Solicitud", "Fecha Pedido", "Fecha Entrada", 
                "Comentarios", "Inversión SAP"
            ])
    
    # Datos de proveedores
    if "proveedores" not in st.session_state:
        st.session_state.proveedores = {
            "Dell Technologies": "12345678",
            "Cisco Systems": "87654321",
            "HP Inc.": "55555555",
            "Amazon Web Services": "99999999"
        }
    
    # Datos de activos (si los necesitas)
    if "inventario" not in st.session_state:
        st.session_state.inventario = pd.DataFrame(columns=[
            "ID", "Categoría", "Tipo", "Marca", "Modelo", "Serial", 
            "Usuario", "Departamento", "Fecha_Adquisicion", "Estado", "Notas"
        ])

def guardar_persistencia():
    if "pedidos" in st.session_state:
        st.session_state.pedidos.to_pickle("pedidos_cache.pkl")

# --- Funciones auxiliares ---
def guardar_excel(df, nombre_base):
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"{nombre_base}_{fecha_actual}.xlsx"
    df.to_excel(nombre_archivo, index=False)
    return nombre_archivo

# --- Carga inicial ---
cargar_datos()

# --- Sidebar (Menú) ---
st.sidebar.title("⚙️ Menú de Gestión")
menu_principal = st.sidebar.radio(
    "**Opciones Principales**",
    ["🏠 Inicio", "📦 Activos", "📝 Pedidos", "🔌 Configuración"]
)

# --- Contenido Principal ---
st.title("💻 Gestión de Pedidos y Activos TI")

# 1. Página de Inicio
if menu_principal == "🏠 Inicio":
    st.markdown("""
        <div class="card">
            <h2 class="titulo-seccion">Bienvenido al Sistema de Gestión</h2>
            <p>Utiliza el menú lateral para navegar.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Pedidos", len(st.session_state.pedidos))
    with col2:
        st.metric("Proveedores Registrados", len(st.session_state.proveedores))
    with col3:
        st.metric("Activos TI", len(st.session_state.inventario))

# 2. Sección de Pedidos (Completamente funcional)
elif menu_principal == "📝 Pedidos":
    tab1, tab2, tab3 = st.tabs(["➕ Nuevo Pedido", "📋 Todos los Pedidos", "🔄 Importar/Exportar"])
    
    # Pestaña 1: Nuevo Pedido
    with tab1:
        st.header("📝 Registrar Nuevo Pedido")
        with st.form("form_pedido", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                concepto = st.text_input("CONCEPTO*")
                proveedor = st.selectbox(
                    "Proveedor*",
                    options=list(st.session_state.proveedores.keys())
                )
                num_proveedor = st.text_input(
                    "Número de Proveedor*",
                    value=st.session_state.proveedores.get(proveedor, "")
                )
                importe = st.number_input("Importe (€)*", min_value=0.0, format="%.2f")
                ccar = st.text_input("CCAR Request Number")
            with col2:
                solicitud = st.text_input("Solicitud")
                fecha_pedido = st.date_input("Fecha Pedido*")
                fecha_entrada = st.date_input("Fecha Entrada")
                inversion_sap = st.text_input("Inversión SAP")
                comentarios = st.text_area("Comentarios")
            
            if st.form_submit_button("💾 Guardar Pedido"):
                nuevo_pedido = {
                    "ID": len(st.session_state.pedidos) + 1,
                    "CONCEPTO": concepto,
                    "Proveedor": proveedor,
                    "Número de proveedor": num_proveedor,
                    "Importe": importe,
                    "CCAR Request Number": ccar,
                    "Solicitud": solicitud,
                    "Fecha Pedido": fecha_pedido,
                    "Fecha Entrada": fecha_entrada,
                    "Comentarios": comentarios,
                    "Inversión SAP": inversion_sap
                }
                st.session_state.pedidos = pd.concat([
                    st.session_state.pedidos,
                    pd.DataFrame([nuevo_pedido])
                ], ignore_index=True)
                guardar_persistencia()
                st.success("✅ Pedido registrado correctamente!")
                st.rerun()
    
    # Pestaña 2: Ver/Editar Pedidos
    with tab2:
        st.header("📋 Listado de Pedidos")
        if not st.session_state.pedidos.empty:
            edited_df = st.data_editor(
                st.session_state.pedidos,
                num_rows="dynamic",
                use_container_width=True,
                key="editor_pedidos"
            )
            
            if st.button("💾 Guardar Cambios", key="guardar_edicion"):
                st.session_state.pedidos = edited_df
                guardar_persistencia()
                st.success("Datos actualizados!")
                st.rerun()
        else:
            st.warning("No hay pedidos registrados.")
    
    # Pestaña 3: Importar/Exportar (Corregido)
    with tab3:
        st.header("🔄 Importar/Exportar Datos")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📤 Exportar a Excel")
            if not st.session_state.pedidos.empty:
                nombre_archivo = guardar_excel(st.session_state.pedidos, "pedidos_ti")
                with open(nombre_archivo, "rb") as f:
                    st.download_button(
                        label="⬇️ Descargar",
                        data=f,
                        file_name=nombre_archivo,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="descargar_excel"
                    )
            else:
                st.warning("No hay datos para exportar.")
        
        with col2:
            st.markdown("### 📥 Importar desde Excel")
            archivo = st.file_uploader(
                "Sube archivo Excel (.xlsx)", 
                type="xlsx", 
                key="uploader_pedidos"
            )
            
            if archivo is not None:
                try:
                    df_nuevo = pd.read_excel(archivo)
                    columnas_requeridas = ["CONCEPTO", "Proveedor", "Importe"]
                    
                    if all(col in df_nuevo.columns for col in columnas_requeridas):
                        # Generar IDs si no existen
                        if "ID" not in df_nuevo.columns:
                            df_nuevo["ID"] = range(
                                len(st.session_state.pedidos) + 1, 
                                len(st.session_state.pedidos) + len(df_nuevo) + 1
                            )
                        
                        # Combinar datos
                        st.session_state.pedidos = pd.concat(
                            [st.session_state.pedidos, df_nuevo],
                            ignore_index=True
                        ).drop_duplicates(subset=["ID"], keep="last")
                        
                        guardar_persistencia()
                        st.success(f"✅ {len(df_nuevo)} pedidos importados!")
                        st.rerun()
                    else:
                        st.error(f"❌ Faltan columnas requeridas: {', '.join(columnas_requeridas)}")
                except Exception as e:
                    st.error(f"❌ Error al importar: {str(e)}")

# (Las otras secciones como Activos y Configuración pueden añadirse aquí)

# --- Ejecutar al final ---
guardar_persistencia()
