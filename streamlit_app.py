import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuración inicial
st.set_page_config(page_title="Gestión de Pedidos TI", layout="wide")

# Persistencia de datos
def cargar_datos():
    if "pedidos" not in st.session_state:
        if os.path.exists("pedidos_cache.pkl"):
            st.session_state.pedidos = pd.read_pickle("pedidos_cache.pkl")
        else:
            st.session_state.pedidos = pd.DataFrame(columns=[
                "ID", "CONCEPTO", "Proveedor", "Número de proveedor", "Importe",
                "CCAR Request Number", "Solicitud", "Fecha Pedido", "Fecha Entrada",
                "Comentarios", "Inversión SAP"
            ])

def guardar_persistencia():
    st.session_state.pedidos.to_pickle("pedidos_cache.pkl")

cargar_datos()

# Menú principal
menu = st.sidebar.radio("Menú", ["📋 Pedidos", "🔄 Importar/Exportar"])

if menu == "📋 Pedidos":
    st.title("📋 Listado de Pedidos")
    
    # Editor de datos
    edited_df = st.data_editor(
        st.session_state.pedidos,
        num_rows="dynamic",
        use_container_width=True,
        key="pedidos_editor"
    )
    
    if st.button("💾 Guardar Cambios"):
        st.session_state.pedidos = edited_df
        guardar_persistencia()
        st.success("Datos actualizados!")
        st.rerun()

elif menu == "🔄 Importar/Exportar":
    st.title("🔄 Importar/Exportar Datos")
    
    # Exportación
    st.header("📤 Exportar a Excel")
    if not st.session_state.pedidos.empty:
        nombre = guardar_excel(st.session_state.pedidos, "pedidos")
        with open(nombre, "rb") as f:
            st.download_button(
                "Descargar Excel",
                data=f,
                file_name=nombre
            )
    
    # Importación
    st.header("📥 Importar desde Excel")
    archivo = st.file_uploader("Subir archivo", type="xlsx")
    
    if archivo:
        try:
            df = pd.read_excel(archivo)
            required = ["CONCEPTO", "Proveedor", "Importe"]
            
            if all(col in df.columns for col in required):
                if "ID" not in df.columns:
                    df["ID"] = range(len(st.session_state.pedidos)+1, len(st.session_state.pedidos)+len(df)+1)
                
                st.session_state.pedidos = pd.concat([st.session_state.pedidos, df]).drop_duplicates("ID")
                st.session_state.pedidos = st.session_state.pedidos.copy()  # Forzar actualización
                guardar_persistencia()
                st.success(f"✅ {len(df)} pedidos importados!")
                st.rerun()
            else:
                st.error(f"Faltan columnas: {', '.join(required)}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

guardar_persistencia()
