import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Gestión de Activos de TI",
    page_icon="💻",
    layout="wide"
)

# Función para cargar/guardar datos en Excel
def cargar_datos():
    if "inventario" not in st.session_state:
        st.session_state.inventario = pd.DataFrame(columns=[
            "ID", "Tipo", "Marca", "Modelo", "Serial", "Usuario", "Departamento", "Fecha_Adquisicion", "Estado", "Notas"
        ])

def guardar_excel(df):
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"inventario_activos_{fecha_actual}.xlsx"
    df.to_excel(nombre_archivo, index=False)
    return nombre_archivo

# Cargar datos iniciales
cargar_datos()

# Sidebar (Menú de opciones)
st.sidebar.title("⚙️ Menú de Gestión")
opcion = st.sidebar.radio(
    "Seleccione una opción:",
    ("📋 Ver Inventario", "➕ Agregar Activo", "📤 Importar desde Excel", "📥 Exportar a Excel", "🔍 Buscar Activo")
)

# Opción 1: Ver Inventario
if opcion == "📋 Ver Inventario":
    st.title("📋 Inventario de Activos de TI")
    st.dataframe(st.session_state.inventario, use_container_width=True)

# Opción 2: Agregar un nuevo activo
elif opcion == "➕ Agregar Activo":
    st.title("➕ Agregar Nuevo Activo")
    with st.form("form_agregar"):
        col1, col2 = st.columns(2)
        with col1:
            tipo = st.selectbox("Tipo de Activo", ["Laptop", "Desktop", "Monitor", "Impresora", "Servidor", "Router"])
            marca = st.text_input("Marca")
            modelo = st.text_input("Modelo")
            serial = st.text_input("Número de Serie")
        with col2:
            usuario = st.text_input("Usuario Asignado")
            departamento = st.selectbox("Departamento", ["IT", "Finanzas", "RH", "Ventas", "Operaciones"])
            fecha_adq = st.date_input("Fecha de Adquisición")
            estado = st.selectbox("Estado", ["Activo", "En Mantenimiento", "Obsoleto", "Dado de Baja"])
        
        notas = st.text_area("Notas Adicionales")
        
        if st.form_submit_button("💾 Guardar Activo"):
            nuevo_activo = {
                "ID": len(st.session_state.inventario) + 1,
                "Tipo": tipo,
                "Marca": marca,
                "Modelo": modelo,
                "Serial": serial,
                "Usuario": usuario,
                "Departamento": departamento,
                "Fecha_Adquisicion": fecha_adq,
                "Estado": estado,
                "Notas": notas
            }
            st.session_state.inventario = pd.concat([
                st.session_state.inventario,
                pd.DataFrame([nuevo_activo])
            ], ignore_index=True)
            st.success("✅ Activo agregado correctamente!")

# Opción 3: Importar desde Excel
elif opcion == "📤 Importar desde Excel":
    st.title("📤 Importar desde Excel")
    archivo = st.file_uploader("Sube tu archivo Excel (.xlsx)", type="xlsx")
    if archivo:
        try:
            df_nuevo = pd.read_excel(archivo)
            st.session_state.inventario = pd.concat([st.session_state.inventario, df_nuevo], ignore_index=True)
            st.success("✅ Datos importados correctamente!")
        except Exception as e:
            st.error(f"❌ Error al importar: {e}")

# Opción 4: Exportar a Excel
elif opcion == "📥 Exportar a Excel":
    st.title("📥 Exportar a Excel")
    if not st.session_state.inventario.empty:
        nombre_archivo = guardar_excel(st.session_state.inventario)
        with open(nombre_archivo, "rb") as f:
            st.download_button(
                label="⬇️ Descargar Inventario en Excel",
                data=f,
                file_name=nombre_archivo,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("⚠️ No hay datos para exportar.")

# Opción 5: Buscar Activo
elif opcion == "🔍 Buscar Activo":
    st.title("🔍 Buscar Activo")
    busqueda = st.text_input("Buscar por Serial, Usuario o Departamento")
    if busqueda:
        resultados = st.session_state.inventario[
            (st.session_state.inventario["Serial"].str.contains(busqueda, case=False)) |
            (st.session_state.inventario["Usuario"].str.contains(busqueda, case=False)) |
            (st.session_state.inventario["Departamento"].str.contains(busqueda, case=False))
        ]
        st.dataframe(resultados, use_container_width=True)
    else:
        st.info("🔎 Ingresa un término de búsqueda.")
