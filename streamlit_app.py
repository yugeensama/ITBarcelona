import streamlit as st

st.set_page_config(page_title="Gestión de Activos TI", layout="wide")

st.title("📦 Gestión de Activos TI")

# Estado de empleados y activos
if "employees" not in st.session_state:
    st.session_state.employees = []

if "assets" not in st.session_state:
    st.session_state.assets = []

# Sección: Añadir empleados
st.header("👤 Añadir Empleado")
col1, col2 = st.columns([3, 1])
with col1:
    employee_name = st.text_input("Nombre del empleado")
with col2:
    if st.button("Agregar Empleado") and employee_name.strip():
        st.session_state.employees.append(employee_name.strip())
        st.success(f"Empleado '{employee_name}' añadido correctamente")

st.divider()

# Sección: Asignar activos
st.header("💻 Asignar Activo")
asset_name = st.text_input("Nombre del activo")
assigned_to = st.selectbox("Asignar a...", st.session_state.employees)
if st.button("Asignar Activo"):
    if asset_name.strip() and assigned_to:
        st.session_state.assets.append({"name": asset_name.strip(), "assignedTo": assigned_to})
        st.success(f"Activo '{asset_name}' asignado a {assigned_to}")

st.divider()

# Tabla de activos
st.header("📊 Activos Asignados")
if st.session_state.assets:
    st.table(st.session_state.assets)
else:
    st.info("Aún no hay activos asignados.")
