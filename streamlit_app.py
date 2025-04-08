import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- Configuración de la página ---
st.set_page_config(
    page_title="Gestión de Pedidos TI",
    page_icon="📋",
    layout="wide"
)

# --- Persistencia de datos ---
def cargar_datos():
    if "pedidos" not in st.session_state:
        if os.path.exists("pedidos_cache.pkl"):
            st.session_state.pedidos = pd.read_pickle("pedidos_cache.pkl").sort_values("ID")
        else:
            st.session_state.pedidos = pd.DataFrame(columns=[
                "ID", "CONCEPTO", "Proveedor", "Número de proveedor", "Importe",
                "CCAR Request Number", "Solicitud", "Fecha Pedido", "Fecha Entrada",
                "Comentarios", "Inversión SAP"
            ])

def guardar_persistencia():
    st.session_state.pedidos.to_pickle("pedidos_cache.pkl")

cargar_datos()

# --- Funciones auxiliares ---
def generar_nuevo_id():
    if st.session_state.pedidos.empty:
        return 1
    return st.session_state.pedidos["ID"].max() + 1

def guardar_excel(df, nombre_base):
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"{nombre_base}_{fecha_actual}.xlsx"
    df.to_excel(nombre_archivo, index=False)
    return nombre_archivo

# --- Sidebar ---
st.sidebar.title("⚙️ Menú")
menu = st.sidebar.radio("Opciones", ["📝 Listado de Pedidos", "➕ Nuevo Pedido", "🔄 Importar/Exportar"])

# --- Contenido Principal ---
st.title("📋 Gestión de Pedidos TI")

# 1. Listado de Pedidos (Editable)
if menu == "📝 Listado de Pedidos":
    st.header("📝 Listado Completo de Pedidos")
    
    # Ordenar por ID (ascendente)
    df_ordenado = st.session_state.pedidos.sort_values("ID")
    
    # Editor de datos
    edited_df = st.data_editor(
        df_ordenado,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID", disabled=True),
            "Fecha Pedido": st.column_config.DateColumn("Fecha Pedido"),
            "Fecha Entrada": st.column_config.DateColumn("Fecha Entrada"),
            "Importe": st.column_config.NumberColumn("Importe (€)", format="%.2f")
        },
        key="pedidos_editor"
    )
    
    if st.button("💾 Guardar Cambios"):
        st.session_state.pedidos = edited_df.sort_values("ID")
        guardar_persistencia()
        st.success("¡Cambios guardados correctamente!")
        st.rerun()

# 2. Nuevo Pedido
elif menu == "➕ Nuevo Pedido":
    st.header("➕ Registrar Nuevo Pedido")
    
    with st.form("nuevo_pedido", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            concepto = st.text_input("CONCEPTO*")
            proveedor = st.text_input("Proveedor*")
            num_proveedor = st.text_input("Número de proveedor")
            importe = st.number_input("Importe (€)*", min_value=0.0, format="%.2f")
        
        with col2:
            ccar = st.text_input("CCAR Request Number")
            solicitud = st.text_input("Solicitud")
            fecha_pedido = st.date_input("Fecha Pedido*")
            fecha_entrada = st.date_input("Fecha Entrada (Opcional)", value=None)
        
        comentarios = st.text_area("Comentarios")
        inversion_sap = st.text_input("Inversión SAP")
        
        if st.form_submit_button("✅ Guardar Pedido"):
            nuevo_pedido = pd.DataFrame([{
                "ID": generar_nuevo_id(),
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
            }])
            
            st.session_state.pedidos = pd.concat(
                [st.session_state.pedidos, nuevo_pedido],
                ignore_index=True
            ).sort_values("ID")
            
            guardar_persistencia()
            st.success("¡Pedido registrado correctamente!")
            st.rerun()

# 3. Importar/Exportar
elif menu == "🔄 Importar/Exportar":
    st.header("🔄 Importar/Exportar Datos")
    
    tab1, tab2 = st.tabs(["📤 Exportar", "📥 Importar"])
    
    with tab1:
        st.subheader("Exportar a Excel")
        if not st.session_state.pedidos.empty:
            nombre_archivo = guardar_excel(st.session_state.pedidos, "pedidos_TI")
            with open(nombre_archivo, "rb") as f:
                st.download_button(
                    "⬇️ Descargar Excel",
                    data=f,
                    file_name=nombre_archivo,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.warning("No hay datos para exportar")
    
    with tab2:
        st.subheader("Importar desde Excel")
        archivo = st.file_uploader("Selecciona archivo Excel", type="xlsx")
        
        if archivo:
            try:
                df_nuevo = pd.read_excel(archivo)
                
                # Validar columnas obligatorias
                columnas_requeridas = ["CONCEPTO", "Proveedor", "Importe"]
                if not all(col in df_nuevo.columns for col in columnas_requeridas):
                    st.error(f"Faltan columnas requeridas: {', '.join(columnas_requeridas)}")
                else:
                    # Generar IDs si no existen
                    if "ID" not in df_nuevo.columns:
                        df_nuevo["ID"] = range(
                            generar_nuevo_id(),
                            generar_nuevo_id() + len(df_nuevo)
                        )
                    
                    # Combinar con datos existentes
                    st.session_state.pedidos = pd.concat(
                        [st.session_state.pedidos, df_nuevo],
                        ignore_index=True
                    ).sort_values("ID").drop_duplicates("ID", keep="last")
                    
                    guardar_persistencia()
                    st.success(f"¡{len(df_nuevo)} pedidos importados correctamente!")
                    st.rerun()
            
            except Exception as e:
                st.error(f"Error al importar: {str(e)}")

# --- Persistencia automática ---
guardar_persistencia()
